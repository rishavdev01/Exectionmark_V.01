import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import { FileText, Download, BarChart3, Award, Star, AlertTriangle, UserPlus, Loader2 } from 'lucide-react';
import { hrAPI } from '../../services/api';

const ICON_MAP = {
    'BarChart3': <BarChart3 size={24} />,
    'Award': <Award size={24} />,
    'Star': <Star size={24} />,
    'AlertTriangle': <AlertTriangle size={24} />,
    'UserPlus': <UserPlus size={24} />
};

export default function HRReports() {
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        hrAPI.hrReports()
            .then(data => {
                if (Array.isArray(data)) setReports(data);
            })
            .catch(err => console.error('Failed to fetch reports:', err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return <div style={{ textAlign: 'center', padding: 100, color: 'var(--text-tertiary)' }}>Loading reports...</div>;
    }

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
                                    {ICON_MAP[r.icon] || <FileText size={24} />}
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
