import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { Server, AlertTriangle, Shield, Clock, Cpu, AlertOctagon } from 'lucide-react';
import { devopsAPI } from '../../services/api';

const changes = [
    { id: 1, type: 'Docker Config Update', service: 'alpha-backend', changedBy: 'Vikram Singh', timestamp: 'Feb 20, 07:30 AM', risk: 'Low', approved: true, details: 'Updated base image from node:18 to node:20-alpine' },
    { id: 2, type: 'Kubernetes Scaling', service: 'API Gateway', changedBy: 'Ananya Reddy', timestamp: 'Feb 19, 06:15 PM', risk: 'Medium', approved: true, details: 'Scaled replicas from 3 to 5 for peak traffic' },
    { id: 3, type: 'Environment Variable', service: 'beta-service', changedBy: 'Karan Joshi', timestamp: 'Feb 19, 03:45 PM', risk: 'High', approved: false, details: 'Changed DB_HOST without approval — possible unauthorized change' },
    { id: 4, type: 'Terraform Modification', service: 'Infrastructure', changedBy: 'Meera Nair', timestamp: 'Feb 18, 11:20 AM', risk: 'High', approved: true, details: 'Modified VPC subnet allocation for staging environment' },
    { id: 5, type: 'Docker Config Update', service: 'notification-svc', changedBy: 'Rahul Verma', timestamp: 'Feb 18, 09:00 AM', risk: 'Low', approved: true, details: 'Added health check endpoint to Dockerfile' },
    { id: 6, type: 'Kubernetes Scaling', service: 'Cache Redis', changedBy: 'System (Auto)', timestamp: 'Feb 17, 11:55 PM', risk: 'Low', approved: true, details: 'Auto-scale triggered: memory usage exceeded 85%' },
    { id: 7, type: 'Environment Variable', service: 'auth-service', changedBy: 'Vikram Singh', timestamp: 'Feb 17, 04:30 PM', risk: 'Medium', approved: true, details: 'Rotated JWT_SECRET key across all environments' },
    { id: 8, type: 'Terraform Modification', service: 'Infrastructure', changedBy: 'Unknown', timestamp: 'Feb 16, 02:00 AM', risk: 'High', approved: false, details: 'Security group rules modified — drift detected from IaC state' },
];

const riskConfig = {
    Low: { bg: '#ecfdf5', color: '#10b981', label: '🟢 Low' },
    Medium: { bg: '#fffbeb', color: '#f59e0b', label: '🟡 Medium' },
    High: { bg: '#fef2f2', color: '#ef4444', label: '🔴 High' },
};

const typeIcons = {
    'Docker Config Update': '🐳',
    'Kubernetes Scaling': '☸️',
    'Environment Variable': '🔑',
    'Terraform Modification': '🏗️',
};

export default function DevOpsInfrastructure() {
    const [changes, setChanges] = useState([]);

    useEffect(() => {
        devopsAPI.infrastructure().then(data => { if (data?.length) setChanges(data); }).catch(() => { });
    }, []);

    const highRisk = changes.filter(c => c.risk === 'High').length;
    const unauthorized = changes.filter(c => !c.approved).length;
    const driftDetected = changes.filter(c => c.details.includes('drift')).length;

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<Server size={24} />} value={changes.length} label="Total Changes" color="blue" delay={0} />
                <StatsCard icon={<AlertTriangle size={24} />} value={highRisk} label="High Risk" color="red" delay={0.08} />
                <StatsCard icon={<AlertOctagon size={24} />} value={unauthorized} label="Unauthorized" color="red" delay={0.16} />
                <StatsCard icon={<Shield size={24} />} value={driftDetected} label="Drift Detected" color="orange" delay={0.24} />
            </div>

            {/* Alert Banners */}
            {changes.filter(c => !c.approved).map(c => (
                <AnimatedCard key={c.id} delay={0.28} style={{ marginBottom: 12, border: '1px solid #fecaca' }}>
                    <div style={{
                        padding: '14px 20px', background: '#fef2f2', borderRadius: 'var(--radius-md)',
                        display: 'flex', alignItems: 'center', gap: 12
                    }}>
                        <AlertOctagon size={20} style={{ color: '#ef4444', flexShrink: 0 }} />
                        <div style={{ flex: 1 }}>
                            <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#991b1b' }}>
                                ⚠️ {c.approved === false ? 'Unauthorized Change Alert' : 'Drift Detection'}
                            </div>
                            <div style={{ fontSize: '0.82rem', color: '#b91c1c', marginTop: 2 }}>
                                {c.type} on <strong>{c.service}</strong> by {c.changedBy} — {c.details}
                            </div>
                        </div>
                        <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', flexShrink: 0 }}>{c.timestamp}</span>
                    </div>
                </AnimatedCard>
            ))}

            <AnimatedCard delay={0.35}>
                <div className="card-header">
                    <span className="card-title">Infrastructure Changes</span>
                    <span className="badge badge-info">{changes.length} changes</span>
                </div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Change Type</th><th>Service</th><th>Changed By</th>
                                    <th>Timestamp</th><th>Risk Level</th><th>Approved</th><th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                {changes.map(c => {
                                    const risk = riskConfig[c.risk];
                                    return (
                                        <tr key={c.id} style={{ background: !c.approved ? '#fef2f220' : 'transparent' }}>
                                            <td>
                                                <span style={{ fontWeight: 600, fontSize: '0.85rem' }}>
                                                    {typeIcons[c.type] || '📦'} {c.type}
                                                </span>
                                            </td>
                                            <td style={{ fontWeight: 600, fontSize: '0.82rem' }}>{c.service}</td>
                                            <td style={{ fontSize: '0.82rem', color: c.changedBy === 'Unknown' ? '#ef4444' : 'var(--text-primary)' }}>
                                                {c.changedBy}
                                            </td>
                                            <td style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{c.timestamp}</td>
                                            <td>
                                                <span className="badge" style={{ background: risk.bg, color: risk.color }}>{risk.label}</span>
                                            </td>
                                            <td>
                                                {c.approved ? (
                                                    <span style={{ color: '#10b981', fontWeight: 600, fontSize: '0.82rem', display: 'flex', alignItems: 'center', gap: 4 }}>
                                                        <Shield size={13} /> Yes
                                                    </span>
                                                ) : (
                                                    <span style={{ color: '#ef4444', fontWeight: 600, fontSize: '0.82rem', display: 'flex', alignItems: 'center', gap: 4 }}>
                                                        <AlertOctagon size={13} /> No
                                                    </span>
                                                )}
                                            </td>
                                            <td style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', maxWidth: 250 }}>{c.details}</td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>
            </AnimatedCard>
        </div>
    );
}
