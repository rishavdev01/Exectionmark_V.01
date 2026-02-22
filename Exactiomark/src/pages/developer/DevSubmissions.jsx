import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { Upload, Clock, CheckCircle, XCircle, RotateCcw } from 'lucide-react';
import { devAPI } from '../../services/api';

const submissions = [
    {
        id: 'SUB-101', story: 'ST-201 – Implement OAuth2 Login Flow', status: 'Approved',
        submittedAt: 'Feb 18, 10:30 AM', approvedAt: 'Feb 18, 02:15 PM', approvalTime: '3h 45m',
        rejectionReason: null,
        revisions: [
            { version: 'v1', date: 'Feb 17', action: 'Submitted', note: 'Initial implementation' },
            { version: 'v2', date: 'Feb 18', action: 'Revised', note: 'Added error handling for token refresh' },
            { version: 'v3', date: 'Feb 18', action: 'Approved', note: 'Final approval by Sneha Iyer' },
        ]
    },
    {
        id: 'SUB-102', story: 'ST-204 – Fix Pagination on Dashboard', status: 'Approved',
        submittedAt: 'Feb 15, 09:00 AM', approvedAt: 'Feb 15, 10:20 AM', approvalTime: '1h 20m',
        rejectionReason: null,
        revisions: [
            { version: 'v1', date: 'Feb 15', action: 'Submitted', note: 'Quick pagination fix' },
            { version: 'v2', date: 'Feb 15', action: 'Approved', note: 'Approved immediately' },
        ]
    },
    {
        id: 'SUB-103', story: 'ST-203 – Refactor Notification Service', status: 'Pending',
        submittedAt: 'Feb 19, 04:00 PM', approvedAt: null, approvalTime: 'Awaiting...',
        rejectionReason: null,
        revisions: [
            { version: 'v1', date: 'Feb 18', action: 'Submitted', note: 'Initial refactor' },
            { version: 'v2', date: 'Feb 19', action: 'Revised', note: 'Added retry mechanism' },
        ]
    },
    {
        id: 'SUB-104', story: 'ST-206 – Database Migration Script', status: 'Rejected',
        submittedAt: 'Feb 17, 11:00 AM', approvedAt: null, approvalTime: '—',
        rejectionReason: 'Missing rollback script. Migration touches 4 unrelated tables which violates scope.',
        revisions: [
            { version: 'v1', date: 'Feb 16', action: 'Submitted', note: 'Initial migration scripts' },
            { version: 'v2', date: 'Feb 17', action: 'Rejected', note: 'Scope issues — missing rollback' },
        ]
    },
    {
        id: 'SUB-105', story: 'ST-205 – API Rate Limiting Middleware', status: 'Pending',
        submittedAt: 'Feb 20, 08:00 AM', approvedAt: null, approvalTime: 'Awaiting...',
        rejectionReason: null,
        revisions: [
            { version: 'v1', date: 'Feb 19', action: 'Submitted', note: 'Rate limiter with Redis backend' },
            { version: 'v2', date: 'Feb 20', action: 'Revised', note: 'Fixed scope drift, removed unrelated files' },
        ]
    },
    {
        id: 'SUB-106', story: 'ST-202 – Write Unit Tests for Payments', status: 'Rejected',
        submittedAt: 'Feb 19, 02:30 PM', approvedAt: null, approvalTime: '—',
        rejectionReason: 'Test coverage at 72%, below the minimum 85% threshold. Missing webhook handler tests.',
        revisions: [
            { version: 'v1', date: 'Feb 19', action: 'Submitted', note: 'Payment unit tests' },
            { version: 'v2', date: 'Feb 19', action: 'Rejected', note: 'Insufficient coverage' },
        ]
    },
];

const tabs = ['All', 'Approved', 'Pending', 'Rejected'];
const statusConfig = {
    Approved: { bg: '#ecfdf5', color: '#10b981', icon: <CheckCircle size={14} /> },
    Pending: { bg: '#fffbeb', color: '#f59e0b', icon: <Clock size={14} /> },
    Rejected: { bg: '#fef2f2', color: '#ef4444', icon: <XCircle size={14} /> },
};

const actionColor = {
    Submitted: '#3b82f6',
    Revised: '#f59e0b',
    Approved: '#10b981',
    Rejected: '#ef4444',
};

export default function DevSubmissions() {
    const [submissions, setSubmissions] = useState([]);
    const [tab, setTab] = useState('All');
    const [expanded, setExpanded] = useState(null);

    useEffect(() => {
        devAPI.submissions().then(data => { if (data?.length) setSubmissions(data); }).catch(() => { });
    }, []);

    const filtered = tab === 'All' ? submissions : submissions.filter(s => s.status === tab);
    const approvedCount = submissions.filter(s => s.status === 'Approved').length;
    const pendingCount = submissions.filter(s => s.status === 'Pending').length;
    const rejectedCount = submissions.filter(s => s.status === 'Rejected').length;

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<Upload size={24} />} value={submissions.length} label="Total Submissions" color="blue" delay={0} />
                <StatsCard icon={<CheckCircle size={24} />} value={approvedCount} label="Approved" color="green" delay={0.08} />
                <StatsCard icon={<Clock size={24} />} value={pendingCount} label="Pending" color="orange" delay={0.16} />
                <StatsCard icon={<XCircle size={24} />} value={rejectedCount} label="Rejected" color="red" delay={0.24} />
            </div>

            <AnimatedCard delay={0.3}>
                <div className="card-header">
                    <span className="card-title">Submissions</span>
                    <div style={{ display: 'flex', gap: 6 }}>
                        {tabs.map(t => (
                            <button key={t} onClick={() => setTab(t)}
                                style={{
                                    padding: '4px 12px', borderRadius: 20, fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer',
                                    background: tab === t ? 'var(--brand-primary)' : 'var(--bg-page)',
                                    color: tab === t ? '#fff' : 'var(--text-secondary)',
                                    border: tab === t ? 'none' : '1px solid var(--border-light)',
                                    transition: 'all 0.15s ease'
                                }}>{t}{t !== 'All' ? ` (${submissions.filter(s => t === 'Approved' ? s.status === 'Approved' : t === 'Pending' ? s.status === 'Pending' : s.status === 'Rejected').length})` : ''}</button>
                        ))}
                    </div>
                </div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Submission</th><th>Story</th><th>Status</th>
                                    <th>Submitted</th><th>Approval Time</th><th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filtered.map(s => (
                                    <>
                                        <tr key={s.id} onClick={() => setExpanded(expanded === s.id ? null : s.id)} style={{ cursor: 'pointer' }}>
                                            <td><span style={{ fontWeight: 700, fontSize: '0.85rem' }}>{s.id}</span></td>
                                            <td>
                                                <div style={{ fontWeight: 600, fontSize: '0.82rem' }}>{(s.story || s.title || '').split(' – ')[1] || s.story || s.title}</div>
                                                <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)' }}>{(s.story || s.title || '').split(' – ')[0]}</div>
                                            </td>
                                            <td>
                                                <span className="badge" style={{
                                                    background: (statusConfig[s.status] || statusConfig.Pending).bg,
                                                    color: (statusConfig[s.status] || statusConfig.Pending).color,
                                                    display: 'inline-flex', alignItems: 'center', gap: 4
                                                }}>
                                                    {(statusConfig[s.status] || statusConfig.Pending).icon} {s.status}
                                                </span>
                                            </td>
                                            <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{s.submittedAt}</td>
                                            <td>
                                                <span style={{
                                                    fontWeight: 600, fontSize: '0.82rem',
                                                    color: s.approvalTime === 'Awaiting...' ? '#f59e0b' : s.approvalTime === '—' ? '#ef4444' : '#10b981'
                                                }}>{s.approvalTime}</span>
                                            </td>
                                            <td>
                                                <button style={{
                                                    padding: '4px 10px', borderRadius: 'var(--radius-sm)', fontSize: '0.75rem',
                                                    fontWeight: 600, cursor: 'pointer',
                                                    background: 'var(--bg-page)', color: 'var(--text-secondary)',
                                                    border: '1px solid var(--border-light)', transition: 'all 0.15s ease'
                                                }}>{expanded === s.id ? 'Collapse' : 'Expand'}</button>
                                            </td>
                                        </tr>
                                        {expanded === s.id && (
                                            <tr key={`${s.id}-detail`}>
                                                <td colSpan={6} style={{ background: '#f9fafb', padding: '16px 24px' }}>
                                                    <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
                                                        {/* Rejection Reason */}
                                                        {s.rejectionReason && (
                                                            <div style={{ flex: '1 1 300px' }}>
                                                                <div style={{ fontWeight: 700, fontSize: '0.82rem', color: '#ef4444', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 4 }}>
                                                                    <XCircle size={14} /> Rejection Reason
                                                                </div>
                                                                <div style={{
                                                                    padding: '10px 14px', background: '#fef2f2',
                                                                    borderRadius: 'var(--radius-sm)', border: '1px solid #fecaca',
                                                                    fontSize: '0.82rem', color: '#991b1b', lineHeight: 1.6
                                                                }}>{s.rejectionReason}</div>
                                                            </div>
                                                        )}
                                                        {/* Revision History */}
                                                        <div style={{ flex: '1 1 300px' }}>
                                                            <div style={{ fontWeight: 700, fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 4 }}>
                                                                <RotateCcw size={14} /> Revision History
                                                            </div>
                                                            <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
                                                                {s.revisions.map((r, i) => (
                                                                    <div key={i} style={{ display: 'flex', gap: 12, position: 'relative', paddingBottom: i < s.revisions.length - 1 ? 16 : 0 }}>
                                                                        {/* Timeline line */}
                                                                        {i < s.revisions.length - 1 && (
                                                                            <div style={{
                                                                                position: 'absolute', left: 7, top: 16, bottom: 0,
                                                                                width: 2, background: 'var(--border-light)'
                                                                            }} />
                                                                        )}
                                                                        {/* Timeline dot */}
                                                                        <div style={{
                                                                            width: 16, height: 16, borderRadius: '50%',
                                                                            background: actionColor[r.action] || '#6b7280',
                                                                            flexShrink: 0, marginTop: 2,
                                                                            display: 'flex', alignItems: 'center', justifyContent: 'center'
                                                                        }}>
                                                                            <div style={{ width: 6, height: 6, borderRadius: '50%', background: '#fff' }} />
                                                                        </div>
                                                                        <div>
                                                                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                                                                <span style={{ fontWeight: 700, fontSize: '0.78rem', color: actionColor[r.action] }}>{r.action}</span>
                                                                                <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>{r.version} · {r.date}</span>
                                                                            </div>
                                                                            <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: 2 }}>{r.note}</div>
                                                                        </div>
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    </div>
                                                </td>
                                            </tr>
                                        )}
                                    </>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </AnimatedCard>
        </div>
    );
}
