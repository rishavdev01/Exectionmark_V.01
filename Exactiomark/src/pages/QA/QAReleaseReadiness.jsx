import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { Shield, Bug, AlertTriangle, CheckCircle, Cpu, Rocket, XCircle } from 'lucide-react';
import { qaAPI } from '../../services/api';

const releaseChecks = [
    { label: 'Critical Bugs Open', value: 2, threshold: 0, status: 'fail' },
    { label: 'High Bugs Open', value: 3, threshold: 2, status: 'fail' },
    { label: 'Regression Pass %', value: 86, threshold: 90, status: 'fail' },
    { label: 'CI Stability', value: 95, threshold: 90, status: 'pass' },
    { label: 'Test Coverage', value: 82, threshold: 80, status: 'pass' },
    { label: 'Deployment Risk', value: 'Medium', threshold: 'Low', status: 'warning' },
];

const blockingBugs = [
    { id: 'BUG-001', summary: 'Stripe webhook fails for recurring payments', severity: 'Critical', service: 'Payment Gateway' },
    { id: 'BUG-005', summary: 'Transaction rollback not triggered on timeout', severity: 'Critical', service: 'Payment Gateway' },
    { id: 'BUG-002', summary: 'Memory leak on chart re-render after 10+ refreshes', severity: 'High', service: 'Dashboard' },
    { id: 'BUG-006', summary: 'WebSocket disconnects after 5 min idle', severity: 'High', service: 'Chat' },
    { id: 'BUG-007', summary: 'Lazy-loaded charts flash white before render', severity: 'High', service: 'Dashboard' },
];

const riskLevel = 'Medium';
const riskColor = riskLevel === 'Low' ? '#10b981' : riskLevel === 'Medium' ? '#f59e0b' : '#ef4444';

export default function QAReleaseReadiness() {
    const [releaseChecks, setReleaseChecks] = useState([
        { label: 'Critical Bugs Open', value: 2, threshold: 0, status: 'fail' },
        { label: 'High Bugs Open', value: 3, threshold: 2, status: 'fail' },
        { label: 'Regression Pass %', value: 86, threshold: 90, status: 'fail' },
        { label: 'CI Stability', value: 95, threshold: 90, status: 'pass' },
        { label: 'Test Coverage', value: 82, threshold: 80, status: 'pass' },
        { label: 'Deployment Risk', value: 'Medium', threshold: 'Low', status: 'warning' },
    ]);
    const [blockingBugs, setBlockingBugs] = useState([]);
    const [riskLevel, setRiskLevel] = useState('Medium');

    useEffect(() => {
        qaAPI.releaseReadiness().then(data => {
            if (!data) return;
            if (data.release_checks?.length) setReleaseChecks(data.release_checks);
            if (data.blocking_bugs?.length) setBlockingBugs(data.blocking_bugs);
            if (data.risk_level) setRiskLevel(data.risk_level);
        }).catch(() => { });
    }, []);

    const riskColor = riskLevel === 'Low' ? '#10b981' : riskLevel === 'Medium' ? '#f59e0b' : '#ef4444';
    const passCount = releaseChecks.filter(c => c.status === 'pass').length;
    const failCount = releaseChecks.filter(c => c.status === 'fail').length;

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<Rocket size={24} />} value={riskLevel} label="Release Risk" color={riskLevel === 'Low' ? 'green' : riskLevel === 'Medium' ? 'orange' : 'red'} delay={0} />
                <StatsCard icon={<CheckCircle size={24} />} value={passCount} label="Checks Passed" color="green" delay={0.08} />
                <StatsCard icon={<XCircle size={24} />} value={failCount} label="Checks Failed" color="red" delay={0.16} />
                <StatsCard icon={<Bug size={24} />} value={blockingBugs.length} label="Blocking Bugs" color="red" delay={0.24} />
            </div>

            {/* AI Verdict Banner */}
            <AnimatedCard delay={0.28} style={{ marginBottom: 16 }}>
                <div style={{
                    padding: '20px 24px', borderRadius: 'var(--radius-md)',
                    background: `linear-gradient(135deg, ${riskColor}10, ${riskColor}05)`,
                    border: `2px solid ${riskColor}40`,
                    display: 'flex', alignItems: 'center', gap: 16
                }}>
                    <div style={{
                        width: 56, height: 56, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                        background: `${riskColor}15`, border: `2px solid ${riskColor}`
                    }}>
                        <Cpu size={28} style={{ color: riskColor }} />
                    </div>
                    <div>
                        <div style={{ fontWeight: 800, fontSize: '1.1rem', color: 'var(--text-primary)' }}>
                            AI Verdict: Release Risk — <span style={{ color: riskColor }}>{riskLevel}</span>
                        </div>
                        <div style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', marginTop: 4 }}>
                            Reason: 2 critical bugs unresolved in Payment Gateway. Regression pass rate below 90% threshold. Recommend fixing blockers before release.
                        </div>
                    </div>
                </div>
            </AnimatedCard>

            <div className="grid-2 mb-lg">
                <AnimatedCard delay={0.35}>
                    <div className="card-header"><span className="card-title">Release Checklist</span></div>
                    <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                        {releaseChecks.map((c, i) => (
                            <div key={i} style={{
                                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                                padding: '10px 14px', borderRadius: 'var(--radius-sm)',
                                background: c.status === 'pass' ? '#ecfdf5' : c.status === 'fail' ? '#fef2f2' : '#fffbeb',
                                borderLeft: `3px solid ${c.status === 'pass' ? '#10b981' : c.status === 'fail' ? '#ef4444' : '#f59e0b'}`
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                    {c.status === 'pass' ? <CheckCircle size={16} color="#10b981" /> :
                                        c.status === 'fail' ? <XCircle size={16} color="#ef4444" /> :
                                            <AlertTriangle size={16} color="#f59e0b" />}
                                    <span style={{ fontWeight: 600, fontSize: '0.85rem' }}>{c.label}</span>
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                    <span style={{ fontWeight: 700, fontSize: '0.85rem', color: c.status === 'pass' ? '#10b981' : c.status === 'fail' ? '#ef4444' : '#f59e0b' }}>
                                        {typeof c.value === 'number' && c.label.includes('%') ? `${c.value}%` : c.value}
                                    </span>
                                    <span style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)' }}>
                                        (threshold: {typeof c.threshold === 'number' && c.label.includes('%') ? `${c.threshold}%` : c.threshold})
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </AnimatedCard>

                <AnimatedCard delay={0.42}>
                    <div className="card-header">
                        <span className="card-title">Blocking Bugs</span>
                        <span className="badge badge-danger">{blockingBugs.length}</span>
                    </div>
                    <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                        {blockingBugs.map((b, i) => (
                            <div key={i} style={{
                                padding: '10px 14px', borderRadius: 'var(--radius-sm)',
                                background: b.severity === 'Critical' ? '#fef2f2' : '#fff7ed',
                                borderLeft: `3px solid ${b.severity === 'Critical' ? '#ef4444' : '#f97316'}`,
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                    <div>
                                        <span style={{ fontWeight: 700, fontFamily: "'Courier New', monospace", fontSize: '0.78rem', marginRight: 8 }}>{b.id}</span>
                                        <span style={{ fontWeight: 600, fontSize: '0.82rem' }}>{b.summary}</span>
                                    </div>
                                    <span className="badge" style={{
                                        background: b.severity === 'Critical' ? '#fef2f2' : '#fff7ed',
                                        color: b.severity === 'Critical' ? '#dc2626' : '#ea580c',
                                        fontSize: '0.68rem', flexShrink: 0
                                    }}>{b.severity}</span>
                                </div>
                                <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginTop: 4 }}>{b.service}</div>
                            </div>
                        ))}
                    </div>
                </AnimatedCard>
            </div>
        </div>
    );
}
