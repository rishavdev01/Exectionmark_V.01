import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { AlertTriangle, Shield, Clock, TrendingUp, AlertCircle, CheckCircle, XCircle, ArrowRight } from 'lucide-react';
import { ceoAPI } from '../../services/api';

const riskLevelColors = { Critical: '#ef4444', High: '#f59e0b', Medium: '#3b82f6', Low: '#10b981' };

export default function RiskEscalations() {
    const [activeRisks, setActiveRisks] = useState([]);
    const [timeline, setTimeline] = useState([]);
    const [patterns, setPatterns] = useState([]);

    useEffect(() => {
        ceoAPI.activeRisks().then(setActiveRisks).catch(() => { });
        ceoAPI.escalationEvents().then(setTimeline).catch(() => { });
        ceoAPI.riskPatterns().then(setPatterns).catch(() => { });
    }, []);

    return (
        <div>
            {/* KPI Row */}
            <div className="stats-grid mb-lg">
                <StatsCard icon={<AlertTriangle size={24} />} value="4" label="Active Risks" trend="2 critical" trendDir="up" color="red" delay={0} />
                <StatsCard icon={<Shield size={24} />} value="3" label="Open Escalations" trend="1 pending" trendDir="up" color="orange" delay={0.08} />
                <StatsCard icon={<Clock size={24} />} value="4.0 hrs" label="Avg Resolution Time" trend="-1.2 hrs" trendDir="down" color="blue" delay={0.16} />
                <StatsCard icon={<TrendingUp size={24} />} value="3" label="Patterns Detected" trend="AI analyzed" trendDir="up" color="purple" delay={0.24} />
            </div>

            {/* Active Risks Table */}
            <AnimatedCard delay={0.3}>
                <div className="card-header">
                    <span className="card-title">Active Risks</span>
                </div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Story ID</th>
                                    <th>Risk Type</th>
                                    <th>Risk Level</th>
                                    <th>Responsible</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                {activeRisks.map(r => (
                                    <tr key={r.storyId}>
                                        <td style={{ fontWeight: 700, color: '#3b82f6' }}>{r.storyId}</td>
                                        <td><span className="badge badge-info">{r.riskType}</span></td>
                                        <td><span className="badge" style={{ background: riskLevelColors[r.riskLevel], color: '#fff' }}>{r.riskLevel}</span></td>
                                        <td style={{ fontWeight: 500 }}>{r.responsible}</td>
                                        <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{r.desc}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </AnimatedCard>

            {/* Escalation Timeline */}
            <AnimatedCard delay={0.38} style={{ marginTop: 20 }}>
                <div className="card-header">
                    <span className="card-title">Escalation Timeline</span>
                </div>
                <div className="card-body">
                    <div style={{ position: 'relative', paddingLeft: 32 }}>
                        <div style={{ position: 'absolute', left: 11, top: 0, bottom: 0, width: 2, background: 'var(--border-color)' }} />
                        {timeline.map((t, i) => (
                            <div key={t.id} style={{ position: 'relative', paddingBottom: i < timeline.length - 1 ? 28 : 0 }}>
                                <div style={{ position: 'absolute', left: -27, top: 4, width: 14, height: 14, borderRadius: '50%', background: t.resolution === 'Pending' ? '#ef4444' : '#10b981', border: '3px solid #fff', boxShadow: '0 0 0 2px var(--border-color)' }} />
                                <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginBottom: 4 }}>{t.time}</div>
                                <div style={{ fontWeight: 700, fontSize: '0.88rem', marginBottom: 4, display: 'flex', alignItems: 'center', gap: 8 }}>
                                    {t.event}
                                    <span className="badge" style={{ background: riskLevelColors[t.severity], color: '#fff', fontSize: '0.65rem' }}>{t.severity}</span>
                                </div>
                                <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: 6 }}>{t.detail}</div>
                                <div style={{ display: 'flex', gap: 16, fontSize: '0.78rem', color: 'var(--text-tertiary)' }}>
                                    <span>Notified: <strong style={{ color: 'var(--text-primary)' }}>{t.notified}</strong></span>
                                    <span>Resolution: <strong style={{ color: t.resolution === 'Pending' ? '#ef4444' : '#10b981' }}>{t.resolution}</strong></span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </AnimatedCard>

            {/* Risk Pattern Analysis */}
            <AnimatedCard delay={0.46} style={{ marginTop: 20 }}>
                <div className="card-header">
                    <span className="card-title">Risk Pattern Analysis</span>
                    <span className="badge badge-info">AI Detected</span>
                </div>
                <div className="card-body">
                    <div style={{ display: 'grid', gap: 16 }}>
                        {patterns.map((p, i) => (
                            <div key={i} style={{ padding: '18px 22px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)', borderLeft: `4px solid ${p.color}` }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                                    <span style={{ fontWeight: 700, fontSize: '0.92rem' }}>{p.title}</span>
                                    <span className="badge" style={{ background: `${p.color}20`, color: p.color, fontWeight: 600 }}>{p.occurrences} occurrences</span>
                                </div>
                                <div style={{ display: 'flex', gap: 24, fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: 10 }}>
                                    <span>Across: <strong>{p.sprints}</strong></span>
                                    <span>Impact: <strong>{p.impact}</strong></span>
                                </div>
                                <div style={{ fontSize: '0.82rem', color: 'var(--text-primary)', padding: '10px 14px', background: '#fff', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                                    <strong>💡 Recommendation:</strong> {p.recommendation}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </AnimatedCard>
        </div>
    );
}
