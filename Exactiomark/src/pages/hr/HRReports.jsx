import AnimatedCard from '../../components/AnimatedCard';
import { FileText, Download, BarChart3, Award, Star, AlertTriangle, UserPlus } from 'lucide-react';

const reports = [
    { title: 'Quarterly Performance Report', desc: 'Company-wide performance metrics, KPIs, and trends for the quarter.', icon: <BarChart3 size={24} />, color: '#3b82f6', lastGenerated: 'Feb 18, 2026' },
    { title: 'Promotion Readiness Report', desc: 'Eligible candidates, AI recommendations, and manager review status.', icon: <Award size={24} />, color: '#10b981', lastGenerated: 'Feb 17, 2026' },
    { title: 'Behaviour Evaluation Report', desc: 'Monthly behaviour scores, trends, and comparison across departments.', icon: <Star size={24} />, color: '#8b5cf6', lastGenerated: 'Feb 15, 2026' },
    { title: 'Attrition Risk Report', desc: 'Members at risk of leaving based on performance drop, overload, and engagement.', icon: <AlertTriangle size={24} />, color: '#ef4444', lastGenerated: 'Feb 14, 2026' },
    { title: 'Onboarding Completion Report', desc: 'New hire onboarding progress, invitation acceptance rates, and training status.', icon: <UserPlus size={24} />, color: '#f59e0b', lastGenerated: 'Feb 12, 2026' },
];

export default function HRReports() {
    return (
        <div>
            <AnimatedCard delay={0.1}>
                <div className="card-header">
                    <span className="card-title">HR Reports</span>
                    <span className="badge badge-info">{reports.length} Reports</span>
                </div>
                <div className="card-body">
                    <div style={{ display: 'grid', gap: 16 }}>
                        {reports.map((r, i) => (
                            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 20, padding: '20px 24px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
                                <div style={{ width: 52, height: 52, borderRadius: 'var(--radius-md)', background: `${r.color}15`, color: r.color, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                                    {r.icon}
                                </div>
                                <div style={{ flex: 1 }}>
                                    <div style={{ fontWeight: 700, fontSize: '0.95rem', marginBottom: 4 }}>{r.title}</div>
                                    <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{r.desc}</div>
                                    <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginTop: 6 }}>Last generated: {r.lastGenerated}</div>
                                </div>
                                <div style={{ display: 'flex', gap: 8, flexShrink: 0 }}>
                                    <button className="btn btn-sm btn-primary" style={{ display: 'flex', alignItems: 'center', gap: 6 }} onClick={() => alert(`Exporting ${r.title} as PDF...`)}>
                                        <Download size={14} /> PDF
                                    </button>
                                    <button className="btn btn-sm btn-secondary" style={{ display: 'flex', alignItems: 'center', gap: 6 }} onClick={() => alert(`Exporting ${r.title} as CSV...`)}>
                                        <Download size={14} /> CSV
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </AnimatedCard>
        </div>
    );
}
