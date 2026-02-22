import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { FlaskConical, CheckCircle, XCircle, AlertTriangle, Clock, Cpu } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, PieChart, Pie, Legend } from 'recharts';
import { qaAPI } from '../../services/api';

const regressionCases = [
    { id: 'REG-001', module: 'Authentication', cases: 18, passed: 17, failed: 1, flaky: false, lastRun: '2h ago' },
    { id: 'REG-002', module: 'Payment', cases: 24, passed: 16, failed: 8, flaky: true, lastRun: '2h ago' },
    { id: 'REG-003', module: 'Dashboard', cases: 12, passed: 10, failed: 2, flaky: true, lastRun: '4h ago' },
    { id: 'REG-004', module: 'User Management', cases: 15, passed: 15, failed: 0, flaky: false, lastRun: '6h ago' },
    { id: 'REG-005', module: 'Notifications', cases: 9, passed: 8, failed: 1, flaky: false, lastRun: '6h ago' },
    { id: 'REG-006', module: 'Reporting', cases: 8, passed: 8, failed: 0, flaky: false, lastRun: '1d ago' },
];

const sprintRegression = [
    { sprint: 'S8', passRate: 88 }, { sprint: 'S9', passRate: 82 }, { sprint: 'S10', passRate: 90 },
    { sprint: 'S11', passRate: 78 }, { sprint: 'S12', passRate: 86 },
];

const overallPie = [
    { name: 'Passed', value: 74, color: '#10b981' },
    { name: 'Failed', value: 12, color: '#ef4444' },
];

const aiInsights = [
    { text: 'Payment regression failing 3 sprints consecutively. Possible unstable backend logic in PaymentProcessor.', type: 'danger' },
    { text: 'Dashboard module has 2 flaky tests. Investigate CSS animation timing in chart re-renders.', type: 'warning' },
    { text: 'Authentication and User Management modules are stable with 94%+ pass rate.', type: 'success' },
];

export default function QARegressionSuite() {
    const [regressionCases, setRegressionCases] = useState([
        { id: 'REG-001', module: 'Authentication', cases: 18, passed: 17, failed: 1, flaky: false, lastRun: '2h ago' },
        { id: 'REG-002', module: 'Payment', cases: 24, passed: 16, failed: 8, flaky: true, lastRun: '2h ago' },
        { id: 'REG-003', module: 'Dashboard', cases: 12, passed: 10, failed: 2, flaky: true, lastRun: '4h ago' },
    ]);

    useEffect(() => {
        qaAPI.regressionSuite().then(data => { if (data?.length) setRegressionCases(data); }).catch(() => { });
    }, []);

    const totalCases = regressionCases.reduce((a, r) => a + r.cases, 0);
    const totalPassed = regressionCases.reduce((a, r) => a + r.passed, 0);
    const totalFailed = regressionCases.reduce((a, r) => a + r.failed, 0);
    const flakyCount = regressionCases.filter(r => r.flaky).length;
    const passRate = Math.round((totalPassed / totalCases) * 100);

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<FlaskConical size={24} />} value={totalCases} label="Total Regression Cases" color="blue" delay={0} />
                <StatsCard icon={<CheckCircle size={24} />} value={`${passRate}%`} label="Pass Rate" color="green" delay={0.08} />
                <StatsCard icon={<XCircle size={24} />} value={totalFailed} label="Failures" color="red" delay={0.16} />
                <StatsCard icon={<AlertTriangle size={24} />} value={flakyCount} label="Flaky Tests" color="orange" delay={0.24} />
            </div>

            <AnimatedCard delay={0.3}>
                <div className="card-header"><span className="card-title">Regression Suite by Module</span><span className="badge badge-neutral">Last run: 2h ago</span></div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr><th>ID</th><th>Module</th><th>Total</th><th>Passed</th><th>Failed</th><th>Pass %</th><th>Flaky</th><th>Last Run</th></tr>
                            </thead>
                            <tbody>
                                {regressionCases.map(r => {
                                    const pct = Math.round((r.passed / r.cases) * 100);
                                    const clr = pct >= 90 ? '#10b981' : pct >= 75 ? '#f59e0b' : '#ef4444';
                                    return (
                                        <tr key={r.id}>
                                            <td style={{ fontWeight: 700, fontFamily: "'Courier New', monospace", fontSize: '0.82rem' }}>{r.id}</td>
                                            <td style={{ fontWeight: 700, fontSize: '0.85rem' }}>{r.module}</td>
                                            <td style={{ fontWeight: 600 }}>{r.cases}</td>
                                            <td style={{ fontWeight: 600, color: '#10b981' }}>{r.passed}</td>
                                            <td style={{ fontWeight: 600, color: r.failed > 0 ? '#ef4444' : 'var(--text-tertiary)' }}>{r.failed}</td>
                                            <td>
                                                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                                    <div style={{ width: 50, height: 5, borderRadius: 3, background: '#e5e7eb' }}>
                                                        <div style={{ height: '100%', borderRadius: 3, width: `${pct}%`, background: clr }} />
                                                    </div>
                                                    <span style={{ fontWeight: 700, fontSize: '0.78rem', color: clr }}>{pct}%</span>
                                                </div>
                                            </td>
                                            <td>
                                                {r.flaky ? (
                                                    <span style={{ color: '#ef4444', fontWeight: 600, fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: 4 }}>
                                                        <AlertTriangle size={13} /> Flaky
                                                    </span>
                                                ) : <span style={{ color: '#10b981', fontWeight: 600, fontSize: '0.78rem' }}>Stable</span>}
                                            </td>
                                            <td style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{r.lastRun}</td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>
            </AnimatedCard>

            <div className="grid-2 mb-lg" style={{ marginTop: 16 }}>
                <AnimatedCard delay={0.4}>
                    <div className="card-header"><span className="card-title">Pass Rate Trend</span></div>
                    <div className="card-body">
                        <div className="chart-container">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={sprintRegression}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                    <XAxis dataKey="sprint" tick={{ fontSize: 12 }} />
                                    <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
                                    <Tooltip formatter={(v) => `${v}%`} />
                                    <Bar dataKey="passRate" radius={[4, 4, 0, 0]} name="Pass Rate">
                                        {sprintRegression.map((d, i) => <Cell key={i} fill={d.passRate >= 85 ? '#10b981' : d.passRate >= 75 ? '#f59e0b' : '#ef4444'} />)}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </AnimatedCard>

                <AnimatedCard delay={0.48}>
                    <div className="card-header"><span className="card-title">Overall Results</span></div>
                    <div className="card-body">
                        <div className="chart-container">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie data={overallPie} cx="50%" cy="50%" outerRadius={75} innerRadius={40}
                                        dataKey="value" nameKey="name" label={({ name, value }) => `${name}: ${value}`}>
                                        {overallPie.map((d, i) => <Cell key={i} fill={d.color} />)}
                                    </Pie>
                                    <Tooltip /><Legend />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </AnimatedCard>
            </div>

            <AnimatedCard delay={0.56}>
                <div className="card-header">
                    <span className="card-title">AI Insights</span>
                    <span className="badge badge-info"><Cpu size={10} style={{ display: 'inline', marginRight: 4 }} />AI</span>
                </div>
                <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                    {aiInsights.map((ai, i) => (
                        <div key={i} style={{
                            padding: '12px 16px', borderRadius: 'var(--radius-sm)',
                            background: ai.type === 'success' ? 'var(--success-bg)' : ai.type === 'danger' ? 'var(--danger-bg)' : 'var(--warning-bg)',
                            borderLeft: `3px solid ${ai.type === 'success' ? 'var(--success)' : ai.type === 'danger' ? 'var(--danger)' : 'var(--warning)'}`,
                            fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: 6
                        }}>
                            <Cpu size={13} style={{ flexShrink: 0 }} /> {ai.text}
                        </div>
                    ))}
                </div>
            </AnimatedCard>
        </div>
    );
}
