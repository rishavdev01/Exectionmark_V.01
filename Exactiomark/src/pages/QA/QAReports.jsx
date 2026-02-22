import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { FileText, Download, BarChart2, Bug, FlaskConical, Shield } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, LineChart, Line, Legend } from 'recharts';
import { qaAPI } from '../../services/api';

const ICON_MAP = {
    Sprint: <BarChart2 size={16} />,
    Bugs: <Bug size={16} />,
    Release: <Shield size={16} />,
    Regression: <FlaskConical size={16} />,
};

const FALLBACK_REPORTS = [
    {
        id: 1, name: 'Sprint QA Report', icon: <BarChart2 size={16} />, color: '#3b82f6', category: 'Sprint',
        description: 'Comprehensive QA summary for the current sprint including test results, bug counts, and quality scores.',
        lastGenerated: 'Feb 20, 2026', data: [
            { label: 'Tests Run', value: '271' }, { label: 'Pass Rate', value: '91%' },
            { label: 'Bugs Found', value: '8' }, { label: 'Quality Score', value: '85%' },
        ]
    },
    {
        id: 2, name: 'Bug Trend Report', icon: <Bug size={16} />, color: '#ef4444', category: 'Bugs',
        description: 'Analysis of bug discovery and resolution trends across recent sprints. Highlights repeat defects.',
        lastGenerated: 'Feb 20, 2026', data: [
            { label: 'New Bugs', value: '8' }, { label: 'Resolved', value: '14' },
            { label: 'Reopened', value: '3' }, { label: 'Net Change', value: '-6' },
        ]
    },
    {
        id: 3, name: 'Release Quality Report', icon: <Shield size={16} />, color: '#10b981', category: 'Release',
        description: 'Pre-release quality assessment including blocking bugs, regression results, and AI risk verdict.',
        lastGenerated: 'Feb 19, 2026', data: [
            { label: 'Risk Level', value: 'Medium' }, { label: 'Blockers', value: '5' },
            { label: 'Regression Pass', value: '86%' }, { label: 'Coverage', value: '82%' },
        ]
    },
    {
        id: 4, name: 'Regression Stability Report', icon: <FlaskConical size={16} />, color: '#8b5cf6', category: 'Regression',
        description: 'Stability analysis of regression suite across sprints with flaky test detection and module-level breakdown.',
        lastGenerated: 'Feb 20, 2026', data: [
            { label: 'Total Cases', value: '86' }, { label: 'Pass Rate', value: '86%' },
            { label: 'Flaky Tests', value: '2' }, { label: 'Stable Modules', value: '4/6' },
        ]
    },
];

const bugTrend = [
    { sprint: 'S8', found: 12, resolved: 10 }, { sprint: 'S9', found: 8, resolved: 12 },
    { sprint: 'S10', found: 14, resolved: 11 }, { sprint: 'S11', found: 6, resolved: 9 },
    { sprint: 'S12', found: 8, resolved: 14 },
];

const qualityTrend = [
    { sprint: 'S8', score: 78 }, { sprint: 'S9', score: 82 },
    { sprint: 'S10', score: 75 }, { sprint: 'S11', score: 80 }, { sprint: 'S12', score: 85 },
];

export default function QAReports() {
    const [reports, setReports] = useState(FALLBACK_REPORTS);
    const [exporting, setExporting] = useState(null);

    useEffect(() => {
        qaAPI.reports().then(data => {
            if (data?.length) {
                setReports(data.map(r => ({ ...r, icon: ICON_MAP[r.category] || <FileText size={16} /> })));
            }
        }).catch(() => { });
    }, []);

    const handleExport = (id) => {
        setExporting(id);
        setTimeout(() => setExporting(null), 1500);
    };

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<FileText size={24} />} value={reports.length} label="Available Reports" color="blue" delay={0} />
                <StatsCard icon={<Download size={24} />} value="PDF/CSV" label="Export Formats" color="green" delay={0.08} />
                <StatsCard icon={<BarChart2 size={24} />} value="Sprint 12" label="Current Period" color="orange" delay={0.16} />
                <StatsCard icon={<Shield size={24} />} value="85%" label="Quality Score" color="green" delay={0.24} />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(380px, 1fr))', gap: 16, marginBottom: 16 }}>
                {reports.map((r, idx) => (
                    <AnimatedCard key={r.id} delay={0.3 + idx * 0.08}>
                        <div className="card-header" style={{ borderBottom: `2px solid ${r.color}20` }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <div style={{
                                    width: 32, height: 32, borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    background: `${r.color}15`, color: r.color
                                }}>{r.icon}</div>
                                <div>
                                    <span className="card-title" style={{ fontSize: '0.9rem' }}>{r.name}</span>
                                    <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)' }}>{r.category}</div>
                                </div>
                            </div>
                            <span className="badge badge-neutral" style={{ fontSize: '0.68rem' }}>{r.lastGenerated}</span>
                        </div>
                        <div className="card-body">
                            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: 12, lineHeight: 1.5 }}>{r.description}</p>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 14 }}>
                                {r.data.map((d, i) => (
                                    <div key={i} style={{
                                        padding: '8px 10px', borderRadius: 'var(--radius-sm)', background: 'var(--bg-page)',
                                        display: 'flex', justifyContent: 'space-between', alignItems: 'center'
                                    }}>
                                        <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>{d.label}</span>
                                        <span style={{ fontSize: '0.82rem', fontWeight: 700, color: r.color }}>{d.value}</span>
                                    </div>
                                ))}
                            </div>
                            <button onClick={() => handleExport(r.id)} style={{
                                width: '100%', padding: '8px 16px', borderRadius: 'var(--radius-sm)', background: r.color,
                                color: '#fff', border: 'none', fontWeight: 600, fontSize: '0.82rem', cursor: 'pointer',
                                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
                                opacity: exporting === r.id ? 0.6 : 1, transition: 'all 0.15s ease'
                            }}>
                                <Download size={14} /> {exporting === r.id ? 'Exporting...' : 'Export Report'}
                            </button>
                        </div>
                    </AnimatedCard>
                ))}
            </div>

            <div className="grid-2">
                <AnimatedCard delay={0.65}>
                    <div className="card-header"><span className="card-title">Bug Trend</span></div>
                    <div className="card-body">
                        <div className="chart-container">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={bugTrend}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                    <XAxis dataKey="sprint" tick={{ fontSize: 12 }} />
                                    <YAxis tick={{ fontSize: 12 }} />
                                    <Tooltip /><Legend />
                                    <Bar dataKey="found" fill="#ef4444" radius={[4, 4, 0, 0]} name="Found" />
                                    <Bar dataKey="resolved" fill="#10b981" radius={[4, 4, 0, 0]} name="Resolved" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </AnimatedCard>

                <AnimatedCard delay={0.73}>
                    <div className="card-header"><span className="card-title">Quality Trend</span></div>
                    <div className="card-body">
                        <div className="chart-container">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={qualityTrend}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                    <XAxis dataKey="sprint" tick={{ fontSize: 12 }} />
                                    <YAxis domain={[60, 100]} tick={{ fontSize: 12 }} />
                                    <Tooltip formatter={(v) => `${v}%`} />
                                    <Line type="monotone" dataKey="score" stroke="#3b82f6" strokeWidth={2.5} dot={{ r: 5, fill: '#3b82f6' }} name="Quality %" />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </AnimatedCard>
            </div>
        </div>
    );
}
