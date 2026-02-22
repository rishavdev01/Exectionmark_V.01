"""
LLM Provider — Gemini (primary) with HuggingFace (fallback).

Tries ChatGoogleGenerativeAI first. If the API key is missing or the
call fails at runtime, it falls back to HuggingFaceEndpoint.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings


def _gemini_llm() -> BaseChatModel | None:
    api_key = settings.GOOGLE_API_KEY
    if not api_key or api_key.startswith("your-"):
        return None
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.3,
        convert_system_message_to_human=True,
    )


def _huggingface_llm() -> BaseChatModel | None:
    hf_token = settings.HF_TOKEN
    if not hf_token or hf_token.startswith("your-"):
        return None
    try:
        from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
        endpoint = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            huggingfacehub_api_token=hf_token,
            temperature=0.3,
            max_new_tokens=2048,
        )
        return ChatHuggingFace(llm=endpoint)
    except Exception:
        return None


def get_llm() -> BaseChatModel:
    """Return best available LLM: Gemini first, then HuggingFace."""
    llm = _gemini_llm()
    if llm is not None:
        return llm
    llm = _huggingface_llm()
    if llm is not None:
        return llm
    raise RuntimeError(
        "No LLM available. Set GOOGLE_API_KEY or HF_TOKEN in .env"
    )
