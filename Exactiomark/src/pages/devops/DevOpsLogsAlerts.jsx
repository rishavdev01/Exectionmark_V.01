import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { FileText, AlertTriangle, Shield, AlertOctagon, Cpu, Bell, Clock } from 'lucide-react';
import { devopsAPI } from '../../services/api';

const logs = [
    { id: 1, category: 'Error', severity: 'Critical', service: 'beta-service', message: 'NullPointerException in PaymentProcessor.java:142', timestamp: 'Feb 20, 08:12 AM', count: 48 },
    { id: 2, category: 'Error', severity: 'High', service: 'alpha-backend', message: 'Connection refused: Redis cluster unreachable on port 6379', timestamp: 'Feb 20, 07:55 AM', count: 12 },
    { id: 3, category: 'Warning', severity: 'Medium', service: 'API Gateway', message: 'Rate limit threshold reached for /api/v2/users endpoint', timestamp: 'Feb 20, 07:30 AM', count: 156 },
    { id: 4, category: 'Security', severity: 'Critical', service: 'auth-service', message: 'Suspicious login attempt: 15 failed logins from IP 192.168.1.45', timestamp: 'Feb 20, 06:45 AM', count: 15 },
    { id: 5, category: 'Memory', severity: 'High', service: 'DB Primary', message: 'Memory usage at 92% — approaching OOM threshold', timestamp: 'Feb 20, 06:20 AM', count: 1 },
    { id: 6, category: 'Warning', severity: 'Low', service: 'notification-svc', message: 'Deprecated API call to /v1/push — migration to v2 recommended', timestamp: 'Feb 19, 11:30 PM', count: 89 },
    { id: 7, category: 'Security', severity: 'Medium', service: 'Infrastructure', message: 'SSL certificate for api.example.com expires in 7 days', timestamp: 'Feb 19, 10:00 PM', count: 1 },
    { id: 8, category: 'Error', severity: 'High', service: 'gamma-frontend', message: 'Webpack build failed: Module not found @components/Chart', timestamp: 'Feb 19, 08:15 PM', count: 3 },
    { id: 9, category: 'Memory', severity: 'Medium', service: 'Cache Redis', message: 'Eviction rate spiked to 450 keys/sec — consider increasing maxmemory', timestamp: 'Feb 19, 06:00 PM', count: 1 },
    { id: 10, category: 'Warning', severity: 'Low', service: 'alpha-backend', message: 'Slow query detected: SELECT * FROM analytics_events took 4.2s', timestamp: 'Feb 19, 04:30 PM', count: 7 },
];

const categories = ['All', 'Error', 'Warning', 'Security', 'Memory'];
const severityConfig = {
    Critical: { bg: '#fef2f2', color: '#dc2626', border: '#ef4444' },
    High: { bg: '#fff7ed', color: '#ea580c', border: '#f97316' },
    Medium: { bg: '#fffbeb', color: '#d97706', border: '#f59e0b' },
    Low: { bg: '#f0fdf4', color: '#16a34a', border: '#22c55e' },
};

const categoryIcon = {
    Error: <AlertOctagon size={14} />,
    Warning: <AlertTriangle size={14} />,
    Security: <Shield size={14} />,
    Memory: <Bell size={14} />,
};

const aiAnalysis = [
    { text: 'Memory spike pattern detected before backend crash. Recommend increasing RAM allocation for DB Primary to 16GB.', type: 'danger' },
    { text: 'Redis connection failures correlate with high traffic periods (8-9 AM). Implement connection pooling.', type: 'warning' },
    { text: 'SSL certificate expiry alert — auto-renewal should be configured via Certbot or AWS ACM.', type: 'warning' },
    { text: 'Suspicious login pattern from IP 192.168.1.45 matches known brute-force signature. Consider IP blocking.', type: 'danger' },
];

export default function DevOpsLogsAlerts() {
    const [logs, setLogs] = useState([]);
    const [filter, setFilter] = useState('All');

    useEffect(() => {
        devopsAPI.logsAlerts().then(data => { if (data?.length) setLogs(data); }).catch(() => { });
    }, []);

    const filtered = filter === 'All' ? logs : logs.filter(l => l.category === filter);
    const criticalCount = logs.filter(l => l.severity === 'Critical').length;
    const highCount = logs.filter(l => l.severity === 'High').length;
    const securityCount = logs.filter(l => l.category === 'Security').length;

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<FileText size={24} />} value={logs.length} label="Total Logs" color="blue" delay={0} />
                <StatsCard icon={<AlertOctagon size={24} />} value={criticalCount} label="Critical" color="red" delay={0.08} />
                <StatsCard icon={<AlertTriangle size={24} />} value={highCount} label="High Severity" color="orange" delay={0.16} />
                <StatsCard icon={<Shield size={24} />} value={securityCount} label="Security Alerts" color="red" delay={0.24} />
            </div>

            <AnimatedCard delay={0.3}>
                <div className="card-header">
                    <span className="card-title">Logs & Alerts</span>
                    <div style={{ display: 'flex', gap: 6 }}>
                        {categories.map(c => (
                            <button key={c} onClick={() => setFilter(c)}
                                style={{
                                    padding: '4px 12px', borderRadius: 20, fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer',
                                    background: filter === c ? 'var(--brand-primary)' : 'var(--bg-page)',
                                    color: filter === c ? '#fff' : 'var(--text-secondary)',
                                    border: filter === c ? 'none' : '1px solid var(--border-light)', transition: 'all 0.15s ease'
                                }}>{c}</button>
                        ))}
                    </div>
                </div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Category</th><th>Severity</th><th>Service</th>
                                    <th>Message</th><th>Timestamp</th><th>Count</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filtered.map(l => {
                                    const sev = severityConfig[l.severity];
                                    return (
                                        <tr key={l.id} style={{ background: l.severity === 'Critical' ? '#fef2f210' : 'transparent' }}>
                                            <td>
                                                <span style={{
                                                    display: 'flex', alignItems: 'center', gap: 6, fontWeight: 600, fontSize: '0.82rem',
                                                    color: l.category === 'Error' ? '#ef4444' : l.category === 'Security' ? '#7c3aed' : l.category === 'Memory' ? '#f59e0b' : '#6b7280'
                                                }}>
                                                    {categoryIcon[l.category]} {l.category}
                                                </span>
                                            </td>
                                            <td>
                                                <span className="badge" style={{ background: sev.bg, color: sev.color, borderLeft: `2px solid ${sev.border}` }}>
                                                    {l.severity}
                                                </span>
                                            </td>
                                            <td style={{ fontWeight: 600, fontSize: '0.82rem' }}>{l.service}</td>
                                            <td style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', maxWidth: 320 }}>{l.message}</td>
                                            <td style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', whiteSpace: 'nowrap' }}>{l.timestamp}</td>
                                            <td>
                                                <span style={{
                                                    display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                                                    minWidth: 28, height: 24, borderRadius: 12,
                                                    background: l.count > 50 ? '#fef2f2' : l.count > 10 ? '#fffbeb' : '#f0fdf4',
                                                    color: l.count > 50 ? '#ef4444' : l.count > 10 ? '#f59e0b' : '#10b981',
                                                    fontWeight: 700, fontSize: '0.78rem', padding: '0 8px'
                                                }}>{l.count}</span>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>
            </AnimatedCard>

            <AnimatedCard delay={0.4} style={{ marginTop: 16 }}>
                <div className="card-header">
                    <span className="card-title">AI Log Analyzer</span>
                    <span className="badge badge-info"><Cpu size={10} style={{ display: 'inline', marginRight: 4 }} />AI</span>
                </div>
                <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                    {aiAnalysis.map((ai, i) => (
                        <div key={i} style={{
                            padding: '12px 16px', borderRadius: 'var(--radius-sm)',
                            background: ai.type === 'danger' ? 'var(--danger-bg)' : 'var(--warning-bg)',
                            borderLeft: `3px solid ${ai.type === 'danger' ? 'var(--danger)' : 'var(--warning)'}`,
                        }}>
                            <div style={{ fontSize: '0.85rem', color: 'var(--text-primary)', display: 'flex', alignItems: 'flex-start', gap: 6 }}>
                                <Cpu size={14} style={{ flexShrink: 0, marginTop: 2 }} /> {ai.text}
                            </div>
                        </div>
                    ))}
                </div>
            </AnimatedCard>
        </div>
    );
}
