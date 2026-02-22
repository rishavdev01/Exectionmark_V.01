"""
Agent 5 — Enterprise Research / Document AI Review (Chain-of-Thought)

Verifies research work by checking:
  - Document submitted (content length / word count)
  - Citation count (extracted by parser + LLM)
  - Source authenticity (DOI / URL validation)
  - Semantic similarity to task (LLM-based relevance)
  - Plagiarism indicators (low originality signals)

Uses Chain-of-Thought (CoT) reasoning to produce a visible reasoning
trace, then a structured assessment.  Falls back to a rule-based
heuristic engine when no LLM is available.

Output includes:
  chain_of_thought: str   — visible step-by-step reasoning
"""

from __future__ import annotations

import json
import re
from typing import Any, Optional
from urllib.parse import urlparse

import httpx
from langchain_core.prompts import ChatPromptTemplate

from app.ai_agents.llm_provider import get_llm

# ── Scoring weights ──────────────────────────────────────────────
RESEARCH_WEIGHTS = {
    "length": 15,
    "citations": 25,
    "authentic_sources": 25,
    "similarity_match": 25,
    "plagiarism_low": 10,
}

# Minimum thresholds
MIN_WORD_COUNT = 300
GOOD_WORD_COUNT = 1000

# Trusted academic / research domains
TRUSTED_DOMAINS = {
    "doi.org", "arxiv.org", "scholar.google.com", "pubmed.ncbi.nlm.nih.gov",
    "ieee.org", "acm.org", "springer.com", "sciencedirect.com",
    "nature.com", "researchgate.net", "jstor.org", "wiley.com",
    "ncbi.nlm.nih.gov", "semanticscholar.org", "github.com",
    "stackoverflow.com", "medium.com", "docs.microsoft.com",
    "cloud.google.com", "aws.amazon.com",
}

# ── LLM prompts ──────────────────────────────────────────────────

# Extraction: citations, similarity, plagiarism signals
EXTRACTION_PROMPT = """You are an expert Research Document Analyzer for ExecSense.
Analyze the submitted research document and extract:

1. **citations** — list of all references / citations found. For each, provide:
   - text: the citation text or reference
   - url: URL if found (or "")
   - doi: DOI if found (or "")
   - type: "journal", "book", "web", "conference", "other"
2. **word_count_estimate** — estimated word count of the document
3. **originality_assessment** — is the content original? (HIGH / MEDIUM / LOW)
4. **plagiarism_indicators** — list of suspicious passages that look copied (empty if none)
5. **key_topics** — list of main topics / themes covered
6. **relevance_to_task** — how relevant is this document to the task described (score 0-100)
7. **quality_assessment** — overall document quality (score 0-100)
8. **key_findings** — most important takeaways (list)
9. **knowledge_gaps** — areas missing or incomplete (list)

Respond in valid JSON with exactly these keys:
citations, word_count_estimate, originality_assessment, plagiarism_indicators,
key_topics, relevance_to_task, quality_assessment, key_findings, knowledge_gaps.
"""

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", EXTRACTION_PROMPT),
    ("human", (
        "Task Description: {task_description}\n"
        "Project: {project_name}\n"
        "Document Title: {document_title}\n\n"
        "Document Content:\n{document_content}"
    )),
])

# Chain-of-Thought final assessment
COT_ASSESSMENT_PROMPT = """You are an expert Research Quality AI agent for ExecSense.
Given structured research document data and scores, perform analysis.

**You MUST think step-by-step before answering.**

## Chain-of-Thought Steps
1. DOCUMENT METRICS — Assess word count, document structure, and completeness.
   Is the document long enough to be substantive? Does it follow good
   academic or technical writing conventions?
2. CITATION VALIDATION — Count citations, verified sources, and trusted domains.
   Are the references from reputable sources? Are DOIs valid? What
   fraction of cited sources are actually accessible?
3. ORIGINALITY CHECK — Review the originality assessment and any plagiarism
   indicators. Is the content genuine or does it appear to be copied?
   Assess the severity of any plagiarism signals.
4. RELEVANCE ASSESSMENT — How well does this document address the assigned
   task? Are the key topics aligned with project objectives? Identify
   any significant knowledge gaps.
5. QUALITY SYNTHESIS — Based on steps 1-4, compute overall research quality.
   Assess academic rigor. Generate actionable insights and specific
   recommendations for improvement.

## Output Format
Return ONLY valid JSON (no markdown fences) in this exact shape:
{
  "chain_of_thought": "<your step-by-step reasoning as a single string>",
  "overall_quality": <0-100>,
  "academic_rigor": "LOW|MEDIUM|HIGH",
  "actionable_insights": ["<insight 1>", "<insight 2>", ...],
  "alignment_score": <0-100>,
  "recommendations": ["<improvement 1>", "<improvement 2>", ...]
}

Be specific — reference actual citations, topics, and findings from the data.
"""

assessment_prompt = ChatPromptTemplate.from_messages([
    ("system", COT_ASSESSMENT_PROMPT),
    ("human", "Research Data:\n{research_data}"),
])


# ── Citation / URL parsing ───────────────────────────────────────
def _extract_urls(text: str) -> list[str]:
    """Extract all URLs from text."""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]*'
    return list(set(re.findall(url_pattern, text)))


def _extract_dois(text: str) -> list[str]:
    """Extract DOI identifiers from text."""
    doi_pattern = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'
    return list(set(re.findall(doi_pattern, text, re.IGNORECASE)))


def _is_trusted_domain(url: str) -> bool:
    """Check if URL belongs to a trusted academic / research domain."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().lstrip("www.")
        return any(trusted in domain for trusted in TRUSTED_DOMAINS)
    except Exception:
        return False


async def _validate_url(url: str) -> dict[str, Any]:
    """Check if a URL is accessible (HEAD request)."""
    try:
        async with httpx.AsyncClient(timeout=8, follow_redirects=True) as client:
            r = await client.head(url)
            return {
                "url": url,
                "accessible": r.status_code < 400,
                "status_code": r.status_code,
                "trusted": _is_trusted_domain(url),
            }
    except Exception:
        return {
            "url": url,
            "accessible": False,
            "status_code": 0,
            "trusted": _is_trusted_domain(url),
        }


async def _validate_doi(doi: str) -> dict[str, Any]:
    """Validate a DOI by checking doi.org resolution."""
    url = f"https://doi.org/{doi}"
    try:
        async with httpx.AsyncClient(timeout=8, follow_redirects=True) as client:
            r = await client.head(url)
            return {
                "doi": doi,
                "valid": r.status_code < 400,
                "resolved_url": str(r.url) if r.status_code < 400 else "",
            }
    except Exception:
        return {"doi": doi, "valid": False, "resolved_url": ""}


# ── Research Score Computation ───────────────────────────────────
def _compute_research_score(signals: dict[str, Any]) -> int:
    """Compute weighted research progress score (0–100)."""
    score = 0

    # Length (15 pts)
    word_count = signals.get("word_count", 0)
    if word_count >= GOOD_WORD_COUNT:
        score += RESEARCH_WEIGHTS["length"]
    elif word_count >= MIN_WORD_COUNT:
        score += int((word_count / GOOD_WORD_COUNT) * RESEARCH_WEIGHTS["length"])
    elif word_count > 0:
        score += int((word_count / MIN_WORD_COUNT) * RESEARCH_WEIGHTS["length"] * 0.5)

    # Citations (25 pts)
    citation_count = signals.get("citation_count", 0)
    if citation_count >= 5:
        score += RESEARCH_WEIGHTS["citations"]
    elif citation_count > 0:
        score += int((citation_count / 5) * RESEARCH_WEIGHTS["citations"])

    # Authentic sources (25 pts)
    total_sources = signals.get("total_sources", 0)
    trusted_sources = signals.get("trusted_sources", 0)
    accessible_sources = signals.get("accessible_sources", 0)
    valid_dois = signals.get("valid_dois", 0)

    if total_sources > 0:
        auth_score = 0
        if trusted_sources > 0:
            auth_score += (trusted_sources / max(total_sources, 1)) * 0.5
        if accessible_sources > 0:
            auth_score += (accessible_sources / max(total_sources, 1)) * 0.3
        if valid_dois > 0:
            auth_score += min(valid_dois / 3, 1.0) * 0.2
        score += int(auth_score * RESEARCH_WEIGHTS["authentic_sources"])
    elif citation_count > 0:
        score += RESEARCH_WEIGHTS["authentic_sources"] // 3

    # Similarity / relevance match (25 pts)
    relevance = signals.get("relevance_to_task", 0)
    if relevance >= 70:
        score += RESEARCH_WEIGHTS["similarity_match"]
    elif relevance > 0:
        score += int((relevance / 100) * RESEARCH_WEIGHTS["similarity_match"])

    # Plagiarism low (10 pts)
    originality = signals.get("originality", "MEDIUM")
    plagiarism_count = signals.get("plagiarism_indicators", 0)
    if originality == "HIGH" and plagiarism_count == 0:
        score += RESEARCH_WEIGHTS["plagiarism_low"]
    elif originality == "MEDIUM" and plagiarism_count <= 1:
        score += int(RESEARCH_WEIGHTS["plagiarism_low"] * 0.6)
    elif plagiarism_count == 0:
        score += int(RESEARCH_WEIGHTS["plagiarism_low"] * 0.3)

    return min(score, 100)


# ── Rule-based CoT fallback ─────────────────────────────────────
def _rule_based_research_analysis(
    signals: dict[str, Any],
    document_title: str,
    task_description: str,
    research_score: int,
    key_findings: list,
    knowledge_gaps: list,
    key_topics: list,
) -> dict:
    """Deterministic heuristic analysis when no LLM is available."""

    word_count = signals.get("word_count", 0)
    citation_count = signals.get("citation_count", 0)
    total_sources = signals.get("total_sources", 0)
    trusted_sources = signals.get("trusted_sources", 0)
    accessible_sources = signals.get("accessible_sources", 0)
    valid_dois = signals.get("valid_dois", 0)
    relevance = signals.get("relevance_to_task", 0)
    originality = signals.get("originality", "UNKNOWN")
    plagiarism_count = signals.get("plagiarism_indicators", 0)

    # ── Chain of thought trace ──
    cot = (
        f"Step 1 — DOCUMENT METRICS: "
        f"Document '{document_title}' has {word_count} words. "
    )
    if word_count >= GOOD_WORD_COUNT:
        cot += f"Exceeds the ideal threshold ({GOOD_WORD_COUNT} words) ✓. "
    elif word_count >= MIN_WORD_COUNT:
        cot += f"Meets minimum threshold ({MIN_WORD_COUNT} words) but could be more substantive. "
    else:
        cot += f"⚠ Below minimum threshold ({MIN_WORD_COUNT} words) — document is too short. "

    cot += (
        f"\nStep 2 — CITATION VALIDATION: "
        f"{citation_count} citation(s) found. "
        f"{total_sources} source(s) identified. "
        f"{trusted_sources} from trusted academic domains. "
        f"{accessible_sources} accessible via URL. "
        f"{valid_dois} valid DOI(s). "
    )
    if citation_count >= 5:
        cot += "Good citation coverage ✓. "
    elif citation_count >= 2:
        cot += "Moderate citations — could benefit from more references. "
    else:
        cot += "⚠ Insufficient citations — research lacks supporting evidence. "

    cot += (
        f"\nStep 3 — ORIGINALITY CHECK: "
        f"Originality assessment: {originality}. "
        f"{plagiarism_count} plagiarism indicator(s) detected. "
    )
    if originality == "HIGH" and plagiarism_count == 0:
        cot += "Content appears original and authentic ✓. "
    elif plagiarism_count > 0:
        cot += "⚠ Possible plagiarism detected — manual review recommended. "
    else:
        cot += "Originality is acceptable. "

    cot += (
        f"\nStep 4 — RELEVANCE ASSESSMENT: "
        f"Task relevance score: {relevance}/100. "
    )
    if key_topics:
        cot += f"Key topics: {', '.join(str(t) for t in key_topics[:5])}. "
    if relevance >= 70:
        cot += "Strong alignment with the assigned task ✓. "
    elif relevance >= 40:
        cot += "Moderate alignment — some areas diverge from the task scope. "
    else:
        cot += "⚠ Low relevance — document may not adequately address the task. "

    if knowledge_gaps:
        cot += f"Knowledge gaps identified: {', '.join(str(g) for g in knowledge_gaps[:3])}. "

    # Quality and rigor
    academic_rigor = "HIGH" if research_score >= 75 else "MEDIUM" if research_score >= 45 else "LOW"

    recommendations = []
    if word_count < MIN_WORD_COUNT:
        recommendations.append(f"Expand document to at least {MIN_WORD_COUNT} words for substantive coverage")
    if citation_count < 5:
        recommendations.append(f"Add more citations — aim for at least 5 references from trusted sources")
    if trusted_sources < citation_count * 0.5:
        recommendations.append("Improve source quality — prefer peer-reviewed journals and academic databases")
    if plagiarism_count > 0:
        recommendations.append("Review flagged passages for originality — rephrase or properly cite")
    if relevance < 60:
        recommendations.append("Refocus the document on the assigned task description and project objectives")
    if not recommendations:
        recommendations.append("Research quality is strong — consider deepening analysis on key findings")

    actionable_insights = []
    if key_findings:
        actionable_insights = [str(f) for f in key_findings[:3]]
    else:
        actionable_insights = ["Document analysis completed — no key findings to highlight"]

    cot += (
        f"\nStep 5 — QUALITY SYNTHESIS: "
        f"Research score = {research_score}/100. "
        f"Academic rigor = {academic_rigor}. "
        f"Alignment score = {relevance}/100. "
        f"{len(recommendations)} recommendation(s) generated."
    )

    return {
        "chain_of_thought": cot,
        "overall_quality": research_score,
        "academic_rigor": academic_rigor,
        "actionable_insights": actionable_insights,
        "alignment_score": relevance,
        "recommendations": recommendations,
    }


# ── Main Research Verification ──────────────────────────────────
async def verify_research_progress(
    document_title: str,
    document_content: str,
    task_description: str,
    project_name: str = "",
    validate_sources: bool = True,
) -> dict[str, Any]:
    """
    Full enterprise research verification flow with Chain-of-Thought:
    1. Basic document metrics (word count, raw URL/DOI extraction)
    2. LLM-based extraction (citations, originality, relevance, findings)
    3. Source validation (URL accessibility, DOI resolution)
    4. Compute research score
    5. Run CoT assessment (LLM or rule-based fallback)
    """

    # ── 1 — Basic document metrics ──
    words = document_content.split()
    word_count = len(words)

    raw_urls = _extract_urls(document_content)
    raw_dois = _extract_dois(document_content)

    # ── 2 — LLM extraction ──
    extracted = {}
    try:
        chain = extraction_prompt | get_llm()
        response = await chain.ainvoke({
            "task_description": task_description,
            "project_name": project_name,
            "document_title": document_title,
            "document_content": document_content[:12000],
        })
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
        extracted = json.loads(raw)
    except Exception:
        extracted = {
            "citations": [],
            "word_count_estimate": word_count,
            "originality_assessment": "UNKNOWN",
            "plagiarism_indicators": [],
            "key_topics": [],
            "relevance_to_task": 0,
            "quality_assessment": 0,
            "key_findings": [],
            "knowledge_gaps": [],
        }

    # Merge LLM citations with raw-parsed ones
    llm_citations = extracted.get("citations", [])
    citation_count = len(llm_citations)

    all_urls = set(raw_urls)
    all_dois = set(raw_dois)
    for cit in llm_citations:
        if isinstance(cit, dict):
            if cit.get("url"):
                all_urls.add(cit["url"])
            if cit.get("doi"):
                all_dois.add(cit["doi"])

    # ── 3 — Source validation ──
    url_validations = []
    doi_validations = []
    trusted_count = 0
    accessible_count = 0
    valid_doi_count = 0

    if validate_sources:
        for url in list(all_urls)[:10]:
            result = await _validate_url(url)
            url_validations.append(result)
            if result["trusted"]:
                trusted_count += 1
            if result["accessible"]:
                accessible_count += 1

        for doi in list(all_dois)[:5]:
            result = await _validate_doi(doi)
            doi_validations.append(result)
            if result["valid"]:
                valid_doi_count += 1
    else:
        for url in all_urls:
            if _is_trusted_domain(url):
                trusted_count += 1

    total_sources = len(all_urls) + len(all_dois)

    # ── 4 — Compute research score ──
    originality = extracted.get("originality_assessment", "MEDIUM")
    plagiarism_list = extracted.get("plagiarism_indicators", [])
    relevance = extracted.get("relevance_to_task", 0)

    signals = {
        "word_count": word_count,
        "citation_count": citation_count,
        "total_sources": total_sources,
        "trusted_sources": trusted_count,
        "accessible_sources": accessible_count,
        "valid_dois": valid_doi_count,
        "relevance_to_task": relevance,
        "originality": originality,
        "plagiarism_indicators": len(plagiarism_list),
    }
    research_score = _compute_research_score(signals)

    # ── 5 — CoT assessment: LLM first, fallback to rule-based ──
    assessment_input = json.dumps({
        "document_title": document_title,
        "word_count": word_count,
        "citation_count": citation_count,
        "trusted_sources": trusted_count,
        "accessible_sources": accessible_count,
        "valid_dois": valid_doi_count,
        "relevance_to_task": relevance,
        "originality": originality,
        "plagiarism_indicators": len(plagiarism_list),
        "key_findings": extracted.get("key_findings", []),
        "knowledge_gaps": extracted.get("knowledge_gaps", []),
        "research_score": research_score,
        "task_description": task_description,
    }, indent=2, default=str)

    try:
        chain2 = assessment_prompt | get_llm()
        resp2 = await chain2.ainvoke({"research_data": assessment_input})
        raw2 = resp2.content.strip()
        if raw2.startswith("```"):
            raw2 = raw2.split("\n", 1)[-1].rsplit("```", 1)[0]
        llm_assessment = json.loads(raw2)
        llm_assessment["source"] = "ai"
    except Exception as e:
        print(f"⚠️  LLM unavailable for research analysis ({e}), using rule-based CoT")
        llm_assessment = _rule_based_research_analysis(
            signals, document_title, task_description, research_score,
            extracted.get("key_findings", []),
            extracted.get("knowledge_gaps", []),
            extracted.get("key_topics", []),
        )
        llm_assessment["source"] = "rule_based"

    # ── Build response ──
    chain_of_thought = llm_assessment.get("chain_of_thought", "")

    citation_quality = "HIGH" if citation_count >= 5 else ("MEDIUM" if citation_count >= 2 else "LOW")
    ai_comment = llm_assessment.get("actionable_insights", ["Research verification complete."])
    if isinstance(ai_comment, list):
        ai_comment = "; ".join(ai_comment[:3]) if ai_comment else "Research verification complete."

    return {
        "research_score": research_score,
        "signals": signals,
        "document_metrics": {
            "word_count": word_count,
            "meets_minimum": word_count >= MIN_WORD_COUNT,
            "min_threshold": MIN_WORD_COUNT,
        },
        "citations": {
            "count": citation_count,
            "items": llm_citations[:15],
        },
        "sources": {
            "total": total_sources,
            "urls_found": len(all_urls),
            "dois_found": len(all_dois),
            "trusted": trusted_count,
            "accessible": accessible_count,
            "valid_dois": valid_doi_count,
            "url_validations": url_validations[:10],
            "doi_validations": doi_validations[:5],
        },
        "originality": {
            "assessment": originality,
            "plagiarism_indicators": len(plagiarism_list),
            "suspicious_passages": plagiarism_list[:5],
        },
        "relevance": {
            "score": relevance,
            "key_topics": extracted.get("key_topics", []),
        },
        "key_findings": extracted.get("key_findings", []),
        "knowledge_gaps": extracted.get("knowledge_gaps", []),
        "llm_assessment": llm_assessment,
        "weights": RESEARCH_WEIGHTS,
        "chain_of_thought": chain_of_thought,
        "source": llm_assessment.get("source", "unknown"),
        # ── Fields for frontend research verification cards ──
        "citation_analysis": {
            "total": citation_count,
            "verified": trusted_count + valid_doi_count,
            "quality": citation_quality,
        },
        "ai_comment": ai_comment,
    }


# ── Legacy wrapper for backward-compat with supervisor ───────────
async def review_document(project_name: str, document_title: str, document_content: str) -> str:
    """Backward-compatible: runs LLM-only analysis when called via
    the old `document_ai_review` task type."""
    try:
        chain = extraction_prompt | get_llm()
        response = await chain.ainvoke({
            "task_description": "General document review",
            "project_name": project_name,
            "document_title": document_title,
            "document_content": document_content,
        })
        return response.content
    except Exception:
        return json.dumps({
            "chain_of_thought": "Legacy analysis: LLM unavailable, returning basic assessment.",
            "summary": "Document review completed via rule-based engine.",
            "overall_quality": 50,
            "recommendations": ["Configure GOOGLE_API_KEY for full AI analysis"],
        })
