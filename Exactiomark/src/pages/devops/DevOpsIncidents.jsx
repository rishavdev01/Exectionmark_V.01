import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { AlertOctagon, Clock, CheckCircle, XCircle, Cpu, Search, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { devopsAPI } from '../../services/api';

const incidents = [
    {
        id: 'INC-001', incident: 'Production database connection pool exhaustion', severity: 'Critical',
        service: 'DB Primary', openedAt: 'Feb 20, 06:20 AM', resolvedAt: 'Feb 20, 08:05 AM',
        rootCause: 'Leaked connections from beta-service due to missing connection.release() calls',
        mttd: '8m', mttr: '1h 45m', repeat: false,
        aiSummary: 'Incident caused by connection leak in beta-service. Missing connection.release() in 3 API handlers. Recommend adding connection pool monitoring.'
    },
    {
        id: 'INC-002', incident: 'Auth service 503 errors during login', severity: 'High',
        service: 'auth-service', openedAt: 'Feb 19, 08:30 AM', resolvedAt: 'Feb 19, 09:15 AM',
        rootCause: 'JWT signing key rotation triggered during peak hours',
        mttd: '3m', mttr: '45m', repeat: false,
        aiSummary: 'Key rotation executed during peak login window (8-9 AM). Recommend scheduling rotations during off-peak hours (2-4 AM).'
    },
    {
        id: 'INC-003', incident: 'Staging deployment failure for beta-service', severity: 'Medium',
        service: 'beta-service', openedAt: 'Feb 18, 02:00 PM', resolvedAt: 'Feb 18, 03:30 PM',
        rootCause: 'Docker image tag mismatch between CI and deployment manifest',
        mttd: '15m', mttr: '1h 30m', repeat: true,
        aiSummary: 'Repeat incident: Docker image tag inconsistency. Same root cause as INC-007 from Sprint 10. Automate image tag pinning in CI pipeline.'
    },
    {
        id: 'INC-004', incident: 'SSL certificate expired for staging API', severity: 'High',
        service: 'API Gateway', openedAt: 'Feb 17, 11:00 PM', resolvedAt: 'Feb 18, 01:00 AM',
        rootCause: 'Auto-renewal cron job disabled after infrastructure migration',
        mttd: '2h', mttr: '2h', repeat: false,
        aiSummary: 'SSL auto-renewal was disabled after Terraform migration. Add Certbot renewal to IaC and set up certificate expiry alerts at 30/14/7 day thresholds.'
    },
    {
        id: 'INC-005', incident: 'Memory spike causing API Gateway restarts', severity: 'Critical',
        service: 'API Gateway', openedAt: 'Feb 16, 10:00 AM', resolvedAt: 'Feb 16, 12:30 PM',
        rootCause: 'Unbounded in-memory cache for session data',
        mttd: '5m', mttr: '2h 30m', repeat: true,
        aiSummary: 'Repeat incident: Memory leak from session cache. Previously mitigated by increasing RAM, but root fix requires implementing LRU eviction policy.'
    },
];

const severityConfig = {
    Critical: { bg: '#fef2f2', color: '#dc2626', icon: '🔴' },
    High: { bg: '#fff7ed', color: '#ea580c', icon: '🟠' },
    Medium: { bg: '#fffbeb', color: '#d97706', icon: '🟡' },
    Low: { bg: '#f0fdf4', color: '#16a34a', icon: '🟢' },
};

const mttrData = [
    { id: 'INC-001', mttr: 105 }, { id: 'INC-002', mttr: 45 }, { id: 'INC-003', mttr: 90 },
    { id: 'INC-004', mttr: 120 }, { id: 'INC-005', mttr: 150 },
];

export default function DevOpsIncidents() {
    const [incidents, setIncidents] = useState([]);
    const [expanded, setExpanded] = useState(null);

    useEffect(() => {
        devopsAPI.incidents().then(data => { if (data?.length) setIncidents(data); }).catch(() => { });
    }, []);

    const criticalCount = incidents.filter(i => i.severity === 'Critical').length;
    const repeatCount = incidents.filter(i => i.repeat).length;
    const avgMttr = Math.round(mttrData.reduce((a, m) => a + m.mttr, 0) / mttrData.length);
    const avgMttd = '7m';

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<AlertOctagon size={24} />} value={incidents.length} label="Total Incidents" color="blue" delay={0} />
                <StatsCard icon={<XCircle size={24} />} value={criticalCount} label="Critical" color="red" delay={0.08} />
                <StatsCard icon={<Clock size={24} />} value={`${avgMttr}m`} label="Avg MTTR" color="orange" delay={0.16} />
                <StatsCard icon={<Search size={24} />} value={avgMttd} label="Avg MTTD" color="green" delay={0.24} />
            </div>

            {repeatCount > 0 && (
                <AnimatedCard delay={0.28} style={{ marginBottom: 12 }}>
                    <div style={{
                        padding: '14px 20px', background: '#fffbeb', borderRadius: 'var(--radius-md)', borderLeft: '4px solid #f59e0b',
                        display: 'flex', alignItems: 'center', gap: 12
                    }}>
                        <Activity size={20} style={{ color: '#f59e0b', flexShrink: 0 }} />
                        <div>
                            <span style={{ fontWeight: 700, fontSize: '0.88rem', color: '#92400e' }}>Repeat Incident Alert:</span>
                            <span style={{ fontSize: '0.85rem', color: '#78350f', marginLeft: 6 }}>{repeatCount} incident(s) are recurring. Root cause analysis recommended.</span>
                        </div>
                    </div>
                </AnimatedCard>
            )}

            <AnimatedCard delay={0.35}>
                <div className="card-header">
                    <span className="card-title">Incidents</span>
                    <span className="badge badge-danger">{incidents.length} total</span>
                </div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>ID</th><th>Incident</th><th>Severity</th><th>Service</th>
                                    <th>Opened At</th><th>Resolved At</th><th>MTTD</th><th>MTTR</th><th>Repeat</th><th></th>
                                </tr>
                            </thead>
                            <tbody>
                                {incidents.map(inc => {
                                    const sev = severityConfig[inc.severity];
                                    return (
                                        <>
                                            <tr key={inc.id} onClick={() => setExpanded(expanded === inc.id ? null : inc.id)}
                                                style={{ cursor: 'pointer' }}>
                                                <td style={{ fontWeight: 700, fontSize: '0.82rem', fontFamily: "'Courier New', monospace" }}>{inc.id}</td>
                                                <td style={{ fontWeight: 600, fontSize: '0.82rem', maxWidth: 260 }}>{inc.incident}</td>
                                                <td>
                                                    <span className="badge" style={{ background: sev.bg, color: sev.color }}>
                                                        {sev.icon} {inc.severity}
                                                    </span>
                                                </td>
                                                <td style={{ fontWeight: 600, fontSize: '0.82rem' }}>{inc.service}</td>
                                                <td style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', whiteSpace: 'nowrap' }}>{inc.openedAt}</td>
                                                <td style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', whiteSpace: 'nowrap' }}>{inc.resolvedAt}</td>
                                                <td style={{ fontWeight: 700, fontSize: '0.82rem', color: '#10b981' }}>{inc.mttd}</td>
                                                <td style={{ fontWeight: 700, fontSize: '0.82rem', color: '#f59e0b' }}>{inc.mttr}</td>
                                                <td>
                                                    {inc.repeat ? (
                                                        <span style={{ color: '#ef4444', fontWeight: 700, fontSize: '0.78rem' }}>⚠️ Yes</span>
                                                    ) : (
                                                        <span style={{ color: '#10b981', fontWeight: 600, fontSize: '0.78rem' }}>No</span>
                                                    )}
                                                </td>
                                                <td style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)' }}>{expanded === inc.id ? '▲' : '▼'}</td>
                                            </tr>
                                            {expanded === inc.id && (
                                                <tr key={`${inc.id}-detail`}>
                                                    <td colSpan={10} style={{ padding: 0 }}>
                                                        <div style={{ padding: '16px 20px', background: 'var(--bg-page)', borderTop: '1px solid var(--border-light)' }}>
                                                            <div style={{ marginBottom: 10 }}>
                                                                <span style={{ fontWeight: 700, fontSize: '0.82rem' }}>Root Cause: </span>
                                                                <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{inc.rootCause}</span>
                                                            </div>
                                                            <div style={{
                                                                padding: '10px 14px', borderRadius: 'var(--radius-sm)',
                                                                background: 'var(--warning-bg)', borderLeft: '3px solid var(--warning)',
                                                                fontSize: '0.82rem', display: 'flex', alignItems: 'flex-start', gap: 6
                                                            }}>
                                                                <Cpu size={14} style={{ flexShrink: 0, marginTop: 2 }} />
                                                                <div><strong>AI Root Cause Summary:</strong> {inc.aiSummary}</div>
                                                            </div>
                                                        </div>
                                                    </td>
                                                </tr>
                                            )}
                                        </>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>
            </AnimatedCard>

            <AnimatedCard delay={0.45} style={{ marginTop: 16 }}>
                <div className="card-header"><span className="card-title">Mean Time To Resolve (MTTR)</span></div>
                <div className="card-body">
                    <div className="chart-container">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={mttrData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                <XAxis dataKey="id" tick={{ fontSize: 11 }} />
                                <YAxis tick={{ fontSize: 12 }} label={{ value: 'Minutes', angle: -90, position: 'insideLeft', style: { fontSize: 11 } }} />
                                <Tooltip formatter={(v) => [`${v} min`, 'MTTR']} />
                                <Bar dataKey="mttr" radius={[4, 4, 0, 0]} name="MTTR (min)">
                                    {mttrData.map((d, i) => (
                                        <Cell key={i} fill={d.mttr > 120 ? '#ef4444' : d.mttr > 60 ? '#f59e0b' : '#10b981'} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </AnimatedCard>
        </div>
    );
}
