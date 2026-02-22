import AnimatedCard from '../../components/AnimatedCard';
import { FileText, Download, BarChart3, Shield, Activity, Users, MessageSquare } from 'lucide-react';

const reports = [
    { title: 'Sprint Report', desc: 'Complete sprint summary including velocity, story completion, and burndown analysis.', icon: <BarChart3 size={24} />, color: '#3b82f6', lastGenerated: 'Feb 18, 2026' },
    { title: 'Member Performance Report', desc: 'Individual performance metrics, alignment scores, and promotion recommendations.', icon: <Users size={24} />, color: '#10b981', lastGenerated: 'Feb 17, 2026' },
    { title: 'Risk Analysis Report', desc: 'Active risks, escalation history, and AI-detected risk patterns across sprints.', icon: <Shield size={24} />, color: '#ef4444', lastGenerated: 'Feb 18, 2026' },
    { title: 'Health Trend Report', desc: 'Execution health trends over time with factor-wise breakdown and predictions.', icon: <Activity size={24} />, color: '#8b5cf6', lastGenerated: 'Feb 16, 2026' },
    { title: 'Retrospective Summary', desc: 'AI-generated retrospective insights, improvement actions, and behaviour feedback.', icon: <MessageSquare size={24} />, color: '#f59e0b', lastGenerated: 'Feb 15, 2026' },
];

export default function CEOReports() {
    return (
        <div>
            <AnimatedCard delay={0.1}>
                <div className="card-header">
                    <span className="card-title">Available Reports</span>
                    <span className="badge badge-info">{reports.length} Reports</span>
                </div>
                <div className="card-body">
                    <div style={{ display: 'grid', gap: 16 }}>
                        {reports.map((r, i) => (
                            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 20, padding: '20px 24px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', transition: 'all 0.2s ease' }}>
                                <div style={{ width: 52, height: 52, borderRadius: 'var(--radius-md)', background: `${r.color}15`, color: r.color, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                                    {r.icon}
                                </div>
                                <div style={{ flex: 1 }}>
                                    <div style={{ fontWeight: 700, fontSize: '0.95rem', marginBottom: 4 }}>{r.title}</div>
                                    <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{r.desc}</div>
                                    <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginTop: 6 }}>Last generated: {r.lastGenerated}</div>
                                </div>
                                <button
                                    className="btn btn-sm btn-primary"
                                    style={{ display: 'flex', alignItems: 'center', gap: 6, flexShrink: 0 }}
                                    onClick={() => alert(`Exporting ${r.title} as PDF...`)}
                                >
                                    <Download size={14} /> Export PDF
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </AnimatedCard>
        </div>
    );
}
