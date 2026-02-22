import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { Play, CheckCircle, XCircle, Clock, Cpu, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { qaAPI } from '../../services/api';

const testRuns = [
    { id: 1, build: 'v2.4.1-rc3', env: 'Staging', total: 86, passed: 78, failed: 8, duration: '12m 34s', ciStatus: 'Passed', coverage: 82 },
    { id: 2, build: 'v3.1.0-rc1', env: 'Staging', total: 42, passed: 36, failed: 6, duration: '8m 12s', ciStatus: 'Failed', coverage: 78 },
    { id: 3, build: 'v2.3.8-hotfix', env: 'Dev', total: 24, passed: 20, failed: 4, duration: '4m 48s', ciStatus: 'Passed', coverage: 65 },
    { id: 4, build: 'v1.5.0-beta', env: 'Dev', total: 18, passed: 16, failed: 2, duration: '3m 22s', ciStatus: 'Passed', coverage: 88 },
    { id: 5, build: 'v2.4.0-rc2', env: 'Staging', total: 86, passed: 82, failed: 4, duration: '11m 56s', ciStatus: 'Passed', coverage: 85 },
    { id: 6, build: 'v1.0.0-alpha', env: 'Dev', total: 15, passed: 12, failed: 3, duration: '2m 45s', ciStatus: 'Failed', coverage: 55 },
];

const performanceData = [
    { build: 'v2.4.1-rc3', p50: 120, p95: 350, p99: 580 },
    { build: 'v3.1.0-rc1', p50: 180, p95: 520, p99: 890 },
    { build: 'v2.3.8', p50: 95, p95: 280, p99: 420 },
    { build: 'v1.5.0', p50: 85, p95: 240, p99: 380 },
];

const getCoverageColor = (v) => v >= 80 ? '#10b981' : v >= 60 ? '#f59e0b' : '#ef4444';

export default function QATestRuns() {
    const [testRuns, setTestRuns] = useState([
        { id: 1, build: 'v2.4.1-rc3', env: 'Staging', total: 86, passed: 78, failed: 8, duration: '12m 34s', ciStatus: 'Passed', coverage: 82 },
        { id: 2, build: 'v3.1.0-rc1', env: 'Staging', total: 42, passed: 36, failed: 6, duration: '8m 12s', ciStatus: 'Failed', coverage: 78 },
        { id: 3, build: 'v2.3.8-hotfix', env: 'Dev', total: 24, passed: 20, failed: 4, duration: '4m 48s', ciStatus: 'Passed', coverage: 65 },
    ]);

    useEffect(() => {
        qaAPI.testRuns().then(data => { if (data?.length) setTestRuns(data); }).catch(() => { });
    }, []);

    const totalTests = testRuns.reduce((a, r) => a + r.total, 0);
    const totalPassed = testRuns.reduce((a, r) => a + r.passed, 0);
    const avgCoverage = testRuns.length ? Math.round(testRuns.reduce((a, r) => a + r.coverage, 0) / testRuns.length) : 0;

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<Play size={24} />} value={testRuns.length} label="Test Runs" color="blue" delay={0} />
                <StatsCard icon={<CheckCircle size={24} />} value={totalPassed} label="Total Passed" color="green" delay={0.08} />
                <StatsCard icon={<XCircle size={24} />} value={totalTests - totalPassed} label="Total Failed" color="red" delay={0.16} />
                <StatsCard icon={<Activity size={24} />} value={`${avgCoverage}%`} label="Avg Coverage" color="orange" delay={0.24} />
            </div>

            <AnimatedCard delay={0.3}>
                <div className="card-header"><span className="card-title">Test Runs</span></div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr><th>Build</th><th>Env</th><th>Total</th><th>Passed</th><th>Failed</th><th>Duration</th><th>CI</th><th>Coverage</th></tr>
                            </thead>
                            <tbody>
                                {testRuns.map(r => (
                                    <tr key={r.id}>
                                        <td><span style={{ fontWeight: 700, fontFamily: "'Courier New', monospace", fontSize: '0.85rem' }}>{r.build}</span></td>
                                        <td><span className="badge" style={{ background: r.env === 'Staging' ? '#dbeafe' : '#f3e8ff', color: r.env === 'Staging' ? '#1d4ed8' : '#7c3aed' }}>{r.env}</span></td>
                                        <td style={{ fontWeight: 600 }}>{r.total}</td>
                                        <td style={{ fontWeight: 700, color: '#10b981' }}>{r.passed}</td>
                                        <td style={{ fontWeight: 700, color: r.failed > 0 ? '#ef4444' : 'var(--text-tertiary)' }}>{r.failed}</td>
                                        <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}><Clock size={12} style={{ display: 'inline', marginRight: 4 }} />{r.duration}</td>
                                        <td>
                                            <span className="badge" style={{
                                                background: r.ciStatus === 'Passed' ? '#ecfdf5' : '#fef2f2',
                                                color: r.ciStatus === 'Passed' ? '#10b981' : '#ef4444',
                                                display: 'inline-flex', alignItems: 'center', gap: 4
                                            }}>
                                                {r.ciStatus === 'Passed' ? <CheckCircle size={12} /> : <XCircle size={12} />} {r.ciStatus}
                                            </span>
                                        </td>
                                        <td>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                                <div style={{ width: 50, height: 5, borderRadius: 3, background: '#e5e7eb' }}>
                                                    <div style={{ height: '100%', borderRadius: 3, width: `${r.coverage}%`, background: getCoverageColor(r.coverage) }} />
                                                </div>
                                                <span style={{ fontWeight: 700, fontSize: '0.78rem', color: getCoverageColor(r.coverage) }}>{r.coverage}%</span>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </AnimatedCard>

            <AnimatedCard delay={0.4} style={{ marginTop: 16 }}>
                <div className="card-header"><span className="card-title">Response Time Percentiles (ms)</span></div>
                <div className="card-body">
                    <div className="chart-container">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={performanceData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                <XAxis dataKey="build" tick={{ fontSize: 10 }} />
                                <YAxis tick={{ fontSize: 12 }} />
                                <Tooltip />
                                <Bar dataKey="p50" fill="#10b981" radius={[4, 4, 0, 0]} name="P50" />
                                <Bar dataKey="p95" fill="#f59e0b" radius={[4, 4, 0, 0]} name="P95" />
                                <Bar dataKey="p99" fill="#ef4444" radius={[4, 4, 0, 0]} name="P99" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </AnimatedCard>
        </div>
    );
}
