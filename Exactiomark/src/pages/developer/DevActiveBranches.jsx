import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { GitBranch, GitMerge, AlertTriangle, Cpu, CheckCircle, XCircle, AlertOctagon } from 'lucide-react';
import { devAPI } from '../../services/api';

const branches = [
    {
        id: 1, name: 'feature/oauth2-flow', story: 'ST-201 – Implement OAuth2 Login Flow',
        lastCommit: '30m ago', commits: 12, status: 'Ahead',
        mergeReady: true, aiRelevance: 94, conflicts: false,
        aiNote: 'All files aligned with Auth Service scope.'
    },
    {
        id: 2, name: 'test/payment-unit-tests', story: 'ST-202 – Write Unit Tests for Payments',
        lastCommit: '2h ago', commits: 5, status: 'Up to date',
        mergeReady: false, aiRelevance: 78, conflicts: false,
        aiNote: 'Test coverage at 72%. Needs additional edge cases.'
    },
    {
        id: 3, name: 'refactor/notifications-v2', story: 'ST-203 – Refactor Notification Service',
        lastCommit: '1d ago', commits: 8, status: 'Behind',
        mergeReady: false, aiRelevance: 85, conflicts: true,
        aiNote: 'Conflict detected in notification_handler.py with main.'
    },
    {
        id: 4, name: 'fix/pagination-bug', story: 'ST-204 – Fix Pagination on Dashboard',
        lastCommit: '3d ago', commits: 3, status: 'Up to date',
        mergeReady: true, aiRelevance: 96, conflicts: false,
        aiNote: 'Clean branch. Ready to merge.'
    },
    {
        id: 5, name: 'feature/rate-limiting', story: 'ST-205 – API Rate Limiting Middleware',
        lastCommit: '45m ago', commits: 15, status: 'Ahead',
        mergeReady: false, aiRelevance: 68, conflicts: true,
        aiNote: '⚠️ Scope drift: 3 files outside API Gateway modified.'
    },
    {
        id: 6, name: 'migration/user-prefs-v2', story: 'ST-206 – Database Migration Script',
        lastCommit: '6h ago', commits: 7, status: 'Behind',
        mergeReady: false, aiRelevance: 62, conflicts: false,
        aiNote: 'Missing rollback script. 4 unrelated tables touched.'
    },
];

const statusBadge = {
    Ahead: { bg: '#ecfdf5', color: '#10b981' },
    'Up to date': { bg: '#eff6ff', color: '#3b82f6' },
    Behind: { bg: '#fef2f2', color: '#ef4444' },
};
const getColor = (v) => v >= 80 ? '#10b981' : v >= 60 ? '#f59e0b' : '#ef4444';

export default function DevActiveBranches() {
    const [branches, setBranches] = useState([]);

    useEffect(() => {
        devAPI.activeBranches().then(data => { if (data?.length) setBranches(data); }).catch(() => { });
    }, []);

    const mergeReadyCount = branches.filter(b => b.mergeReady).length;
    const conflictCount = branches.filter(b => b.conflicts).length;
    const avgRelevance = branches.length ? Math.round(branches.reduce((a, b) => a + b.aiRelevance, 0) / branches.length) : 0;

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<GitBranch size={24} />} value={branches.length} label="Active Branches" color="blue" delay={0} />
                <StatsCard icon={<GitMerge size={24} />} value={mergeReadyCount} label="Merge Ready" color="green" delay={0.08} />
                <StatsCard icon={<AlertTriangle size={24} />} value={conflictCount} label="Conflicts" color="red" delay={0.16} />
                <StatsCard icon={<Cpu size={24} />} value={`${avgRelevance}%`} label="Avg AI Relevance" color="orange" delay={0.24} />
            </div>

            <AnimatedCard delay={0.3}>
                <div className="card-header">
                    <span className="card-title">Active Branches</span>
                    <span className="badge badge-info">{branches.length} branches</span>
                </div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Branch Name</th><th>Linked Story</th><th>Last Commit</th>
                                    <th>Commits</th><th>Status</th><th>Merge Ready</th>
                                    <th>AI Relevance</th><th>Conflicts</th>
                                </tr>
                            </thead>
                            <tbody>
                                {branches.map(b => (
                                    <tr key={b.id}>
                                        <td>
                                            <div style={{ fontFamily: "'Courier New', monospace", fontWeight: 600, fontSize: '0.84rem', display: 'flex', alignItems: 'center', gap: 6 }}>
                                                <GitBranch size={14} style={{ color: 'var(--info)', flexShrink: 0 }} />
                                                {b.name}
                                            </div>
                                        </td>
                                        <td>
                                            <div style={{ fontWeight: 600, fontSize: '0.82rem' }}>{(b.story || b.name || '').split(' – ')[1] || b.story || b.name}</div>
                                            <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>{(b.story || b.name || '').split(' – ')[0]}</div>
                                        </td>
                                        <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{b.lastCommit}</td>
                                        <td>
                                            <span style={{
                                                display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                                                minWidth: 28, height: 24, borderRadius: 12,
                                                background: 'var(--info-bg)', color: 'var(--info)',
                                                fontWeight: 700, fontSize: '0.78rem', padding: '0 8px'
                                            }}>{b.commits}</span>
                                        </td>
                                        <td>
                                            <span className="badge" style={{
                                                background: (statusBadge[b.status] || statusBadge.Ahead).bg,
                                                color: (statusBadge[b.status] || statusBadge.Ahead).color
                                            }}>{b.status}</span>
                                        </td>
                                        <td>
                                            {b.mergeReady ? (
                                                <span style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#10b981', fontWeight: 600, fontSize: '0.82rem' }}>
                                                    <CheckCircle size={15} /> Ready
                                                </span>
                                            ) : (
                                                <span style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#f59e0b', fontWeight: 600, fontSize: '0.82rem' }}>
                                                    <XCircle size={15} /> Not Ready
                                                </span>
                                            )}
                                        </td>
                                        <td>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                                <div style={{ width: 50, height: 5, borderRadius: 3, background: '#e5e7eb' }}>
                                                    <div style={{
                                                        height: '100%', borderRadius: 3,
                                                        width: `${b.aiRelevance}%`,
                                                        background: getColor(b.aiRelevance),
                                                        transition: 'width 0.5s ease'
                                                    }} />
                                                </div>
                                                <span style={{ fontWeight: 700, fontSize: '0.78rem', color: getColor(b.aiRelevance) }}>
                                                    {b.aiRelevance}%
                                                </span>
                                            </div>
                                        </td>
                                        <td>
                                            {b.conflicts ? (
                                                <span style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#ef4444', fontWeight: 600, fontSize: '0.82rem' }}>
                                                    <AlertOctagon size={15} /> Conflict
                                                </span>
                                            ) : (
                                                <span style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#10b981', fontWeight: 600, fontSize: '0.82rem' }}>
                                                    <CheckCircle size={15} /> Clean
                                                </span>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </AnimatedCard>

            {/* AI Notes */}
            <AnimatedCard delay={0.4}>
                <div className="card-header">
                    <span className="card-title">AI Code Relevance Notes</span>
                    <span className="badge badge-info">AI</span>
                </div>
                <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                    {branches.filter(b => b.aiRelevance < 80 || b.conflicts).map(b => (
                        <div key={b.id} style={{
                            padding: '12px 16px', borderRadius: 'var(--radius-sm)',
                            background: b.aiRelevance < 70 ? 'var(--danger-bg)' : 'var(--warning-bg)',
                            borderLeft: `3px solid ${b.aiRelevance < 70 ? 'var(--danger)' : 'var(--warning)'}`,
                        }}>
                            <div style={{ fontWeight: 700, fontSize: '0.82rem', marginBottom: 4, fontFamily: "'Courier New', monospace" }}>
                                {b.name}
                            </div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: 4 }}>
                                <Cpu size={12} /> {b.aiNote}
                            </div>
                        </div>
                    ))}
                </div>
            </AnimatedCard>
        </div>
    );
}
