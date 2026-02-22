import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { TrendingUp, Users, AlertTriangle, Activity, Award, Cpu } from 'lucide-react';
import { pmAPI } from '../../services/api';

export default function PMTeamPerformance() {
    const [healthFactors, setHealthFactors] = useState([
        { label: 'Sprint Completion Rate', value: 82, weight: 25 },
        { label: 'Alignment Avg', value: 84, weight: 25 },
        { label: 'Approval Speed', value: 78, weight: 15 },
        { label: 'DevOps Stability', value: 91, weight: 20 },
        { label: 'Escalations (inverse)', value: 88, weight: 15 },
    ]);
    const [topContributors, setTopContributors] = useState([
        { name: 'Vikram Singh', score: 89.2, contributions: '26 SP, 94% on-time' },
        { name: 'Sneha Iyer', score: 86.8, contributions: '18 SP, 88% on-time' },
        { name: 'Meera Nair', score: 81.4, contributions: '16 SP, 85% on-time' },
    ]);
    const [riskContributors, setRiskContributors] = useState([
        { name: 'Karan Joshi', score: 68.5, issue: 'Low velocity, 3 overdue tasks' },
        { name: 'Rahul Verma', score: 72.1, issue: 'High rejection rate, 18% deviation' },
        { name: 'Ananya Reddy', score: 74.3, issue: 'Overloaded at 92% capacity' },
    ]);
    const [sprintTrend, setSprintTrend] = useState([]);

    useEffect(() => {
        pmAPI.teamPerformance().then(data => {
            if (!data) return;
            if (data.health_factors?.length) setHealthFactors(data.health_factors);
            if (data.top_contributors?.length) setTopContributors(data.top_contributors);
            if (data.risk_contributors?.length) setRiskContributors(data.risk_contributors);
            if (data.sprint_trend?.length) setSprintTrend(data.sprint_trend);
        }).catch(() => { });
    }, []);

    const overallHealth = Math.round(healthFactors.reduce((a, f) => a + (f.value * f.weight / 100), 0));
    const getColor = (v) => v >= 80 ? '#10b981' : v >= 60 ? '#f59e0b' : '#ef4444';



    const perfAlerts = [
        { member: 'Karan Joshi', alert: 'Performance dropped 9.1% since last sprint', severity: 'High' },
        { member: 'Rahul Verma', alert: 'Rejection rate increased to 18%', severity: 'Medium' },
        { member: 'Ananya Reddy', alert: 'Workload at 92% — risk of burnout', severity: 'High' },
    ];

    const sevColors = { High: '#ef4444', Medium: '#f59e0b', Low: '#10b981' };

    return (
        <div>
            <div className="stats-grid mb-lg">

                <StatsCard icon={<Activity size={24} />} value={`${overallHealth}%`} label="Team Health Score" trend="+2.3%" trendDir="up" color="green" delay={0} />
                <StatsCard icon={<TrendingUp size={24} />} value="84%" label="Alignment Avg" color="blue" delay={0.08} />
                <StatsCard icon={<Award size={24} />} value={topContributors.length} label="Top Contributors" color="purple" delay={0.16} />
                <StatsCard icon={<AlertTriangle size={24} />} value={perfAlerts.length} label="Active Alerts" color="red" delay={0.24} />
            </div>

            {/* Health Score Breakdown */}
            <AnimatedCard delay={0.3}>
                <div className="card-header">
                    <span className="card-title">Team Health Score Breakdown</span>
                    <span className="badge" style={{ background: getColor(overallHealth) + '20', color: getColor(overallHealth), fontWeight: 700, fontSize: '0.9rem' }}>{overallHealth}%</span>
                </div>
                <div className="card-body">
                    <div style={{ display: 'grid', gap: 14 }}>
                        {healthFactors.map(f => (
                            <div key={f.label}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                                    <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{f.label}</span>
                                    <span style={{ fontSize: '0.82rem', fontWeight: 700, color: getColor(f.value) }}>{f.value}% <span style={{ color: 'var(--text-tertiary)', fontWeight: 400 }}>({f.weight}% weight)</span></span>
                                </div>
                                <div style={{ height: 8, background: '#e5e7eb', borderRadius: 4, overflow: 'hidden' }}>
                                    <div style={{ width: `${f.value}%`, height: '100%', background: getColor(f.value), borderRadius: 4, transition: 'width 0.5s ease' }} />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </AnimatedCard>

            <div className="grid-2" style={{ marginTop: 20 }}>
                {/* Top Contributors */}
                <AnimatedCard delay={0.38}>
                    <div className="card-header"><span className="card-title">🏆 Top Contributors</span></div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <div className="table-wrapper">
                            <table className="table">
                                <thead><tr><th>#</th><th>Member</th><th>Score</th><th>Contributions</th></tr></thead>
                                <tbody>
                                    {topContributors.map((c, i) => (
                                        <tr key={c.name}>
                                            <td style={{ fontWeight: 700, color: '#f59e0b' }}>{i + 1}</td>
                                            <td style={{ fontWeight: 600 }}>{c.name}</td>
                                            <td><span style={{ fontWeight: 700, color: '#10b981' }}>{c.score}%</span></td>
                                            <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{c.contributions}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </AnimatedCard>

                {/* Risk Contributors */}
                <AnimatedCard delay={0.46}>
                    <div className="card-header"><span className="card-title">⚠ Risk Contributors</span></div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <div className="table-wrapper">
                            <table className="table">
                                <thead><tr><th>Member</th><th>Score</th><th>Issue</th></tr></thead>
                                <tbody>
                                    {riskContributors.map(c => (
                                        <tr key={c.name}>
                                            <td style={{ fontWeight: 600 }}>{c.name}</td>
                                            <td><span style={{ fontWeight: 700, color: getColor(c.score) }}>{c.score}%</span></td>
                                            <td style={{ fontSize: '0.82rem', color: '#ef4444' }}>{c.issue}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </AnimatedCard>
            </div>

            {/* Performance Drop Alerts */}
            <AnimatedCard delay={0.54} style={{ marginTop: 20 }}>
                <div className="card-header"><span className="card-title">🚨 Performance Drop Alerts</span></div>
                <div className="card-body">
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                        {perfAlerts.map((a, i) => (
                            <div key={i} style={{
                                padding: '12px 16px', borderRadius: 'var(--radius-sm)', display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                                background: a.severity === 'High' ? '#fef2f2' : '#fffbeb',
                                border: `1px solid ${a.severity === 'High' ? '#fecaca' : '#fde68a'}`
                            }}>
                                <div>
                                    <span style={{ fontWeight: 700, color: sevColors[a.severity] }}>{a.member}</span>
                                    <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginLeft: 8 }}>— {a.alert}</span>
                                </div>
                                <span className="badge" style={{ background: sevColors[a.severity], color: '#fff' }}>{a.severity}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </AnimatedCard>
        </div>
    );
}
