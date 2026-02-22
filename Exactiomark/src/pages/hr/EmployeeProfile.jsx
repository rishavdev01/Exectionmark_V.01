import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import { employeesAPI } from '../../services/api';
import { getEmployee } from '../../data/employeeData';
import {
    Mail, Building, Shield, Phone, BarChart3, TrendingUp, AlertTriangle,
    Award, User, MessageSquare, Zap, Clock, ArrowLeft, CheckCircle, PauseCircle, Send
} from 'lucide-react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

const getColor = (s) => s >= 80 ? '#10b981' : s >= 60 ? '#f59e0b' : '#ef4444';
const riskColors = { Low: '#10b981', Medium: '#f59e0b', High: '#ef4444' };
const statusColors = { Active: '#10b981', 'On Leave': '#3b82f6', Probation: '#f59e0b' };
const verdictColors = { 'Strongly Recommend': '#10b981', 'Recommend': '#3b82f6', 'Not Recommended': '#ef4444' };
const decisionColors = { Promoted: '#10b981', Pending: '#f59e0b', Hold: '#ef4444', '—': '#94a3b8' };

function StatRow({ icon, label, value, color }) {
    return (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderBottom: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                {icon}
                <span style={{ fontSize: '0.85rem' }}>{label}</span>
            </div>
            <span style={{ fontWeight: 700, fontSize: '0.95rem', color: color || 'var(--text-primary)' }}>{value}</span>
        </div>
    );
}

export default function EmployeeProfile() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [emp, setEmp] = useState(() => getEmployee(id));

    useEffect(() => {
        employeesAPI.getById(id).then(setEmp).catch(() => setEmp(getEmployee(id)));
    }, [id]);

    if (!emp) {
        return (
            <div style={{ textAlign: 'center', padding: 60 }}>
                <h2>Employee Not Found</h2>
                <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => navigate('/employees')}>
                    ← Back to Employees
                </button>
            </div>
        );
    }

    const b = emp.behaviourScores;
    const avgBehaviour = ((b.communication + b.ownership + b.teamwork + b.leadership + b.discipline) / 5).toFixed(1);

    return (
        <div style={{ maxWidth: 1000, margin: '0 auto' }}>
            {/* Back Button */}
            <button onClick={() => navigate('/employees')}
                style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '8px 16px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', background: '#fff', cursor: 'pointer', fontWeight: 600, fontSize: '0.85rem', marginBottom: 16, transition: 'all 0.15s ease' }}>
                <ArrowLeft size={16} /> Back to Employees
            </button>

            {/* Header Card */}
            <AnimatedCard delay={0}>
                <div className="card-body" style={{ display: 'flex', alignItems: 'center', gap: 24, padding: 30 }}>
                    <div style={{
                        width: 80, height: 80, borderRadius: '50%', background: 'var(--brand-gradient)',
                        color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: '1.6rem', fontWeight: 800, flexShrink: 0
                    }}>{emp.avatar}</div>
                    <div style={{ flex: 1 }}>
                        <h2 style={{ fontSize: '1.4rem', fontWeight: 800, marginBottom: 4 }}>{emp.name}</h2>
                        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{emp.role} · {emp.dept}</p>
                        <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
                            <span className="badge" style={{ background: `${statusColors[emp.status]}20`, color: statusColors[emp.status], fontWeight: 600 }}>{emp.status}</span>
                            <span className="badge" style={{ background: `${riskColors[emp.risk]}20`, color: riskColors[emp.risk], fontWeight: 600 }}>{emp.risk} Risk</span>
                            <span className="badge badge-info">{emp.sprintContrib}</span>
                        </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '2rem', fontWeight: 800, color: getColor(emp.perfScore) }}>{emp.perfScore}%</div>
                        <div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)' }}>Overall Performance</div>
                    </div>
                </div>
            </AnimatedCard>

            {/* Contact Info */}
            <div className="grid-2 mt-lg">
                <AnimatedCard delay={0.08}>
                    <div className="card-header"><span className="card-title">Contact Info</span></div>
                    <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Mail size={18} color="var(--text-tertiary)" /><div><div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Email</div><div style={{ fontWeight: 600 }}>{emp.email}</div></div></div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Phone size={18} color="var(--text-tertiary)" /><div><div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Phone</div><div style={{ fontWeight: 600 }}>{emp.phone}</div></div></div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Building size={18} color="var(--text-tertiary)" /><div><div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Department</div><div style={{ fontWeight: 600 }}>{emp.dept}</div></div></div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Shield size={18} color="var(--text-tertiary)" /><div><div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Projects</div><div style={{ fontWeight: 600 }}>{emp.projects.join(', ')}</div></div></div>
                    </div>
                </AnimatedCard>

                {/* Quick Stats */}
                <AnimatedCard delay={0.14}>
                    <div className="card-header"><span className="card-title">Quick Stats</span></div>
                    <div className="card-body">
                        <StatRow icon={<TrendingUp size={16} color="#3b82f6" />} label="Alignment Score" value={`${emp.alignment}%`} color={getColor(emp.alignment)} />
                        <StatRow icon={<Clock size={16} color="#10b981" />} label="On-time Delivery" value={`${emp.onTime}%`} color={getColor(emp.onTime)} />
                        <StatRow icon={<AlertTriangle size={16} color="#ef4444" />} label="Rejection Rate" value={`${emp.rejection}%`} color={emp.rejection > 10 ? '#ef4444' : '#10b981'} />
                        <StatRow icon={<User size={16} color="#8b5cf6" />} label="Behaviour Score" value={`${emp.behaviour}/10`} color={getColor(emp.behaviour * 10)} />
                    </div>
                </AnimatedCard>
            </div>

            {/* 📊 Performance Section */}
            <AnimatedCard delay={0.2} style={{ marginTop: 20 }}>
                <div className="card-header">
                    <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <BarChart3 size={18} style={{ color: '#3b82f6' }} /> Performance Trends
                    </span>
                </div>
                <div className="card-body">
                    <div className="grid-2" style={{ gap: 20 }}>
                        <div>
                            <div style={{ fontWeight: 700, fontSize: '0.82rem', marginBottom: 8 }}>Alignment Score History</div>
                            <div style={{ height: 200 }}>
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={emp.alignmentHistory}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                        <XAxis dataKey="sprint" tick={{ fontSize: 11 }} />
                                        <YAxis domain={[50, 100]} tick={{ fontSize: 11 }} />
                                        <Tooltip formatter={(v) => `${v}%`} />
                                        <Line type="monotone" dataKey="score" stroke="#3b82f6" strokeWidth={2} dot={{ fill: '#3b82f6', r: 4 }} />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                        <div>
                            <div style={{ fontWeight: 700, fontSize: '0.82rem', marginBottom: 8 }}>Sprint Contribution Trend</div>
                            <div style={{ height: 200 }}>
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={emp.sprintTrend}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                        <XAxis dataKey="sprint" tick={{ fontSize: 11 }} />
                                        <YAxis tick={{ fontSize: 11 }} />
                                        <Tooltip formatter={(v) => `${v} SP`} />
                                        <Line type="monotone" dataKey="sp" stroke="#10b981" strokeWidth={2} dot={{ fill: '#10b981', r: 4 }} />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>
                </div>
            </AnimatedCard>

            {/* 👤 Behaviour Section */}
            <AnimatedCard delay={0.28} style={{ marginTop: 20 }}>
                <div className="card-header">
                    <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <User size={18} style={{ color: '#8b5cf6' }} /> Behaviour Assessment
                    </span>
                    <span className="badge" style={{ background: '#8b5cf620', color: '#8b5cf6' }}>Avg: {avgBehaviour}/10 · 10% Weight</span>
                </div>
                <div className="card-body">
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 12, marginBottom: 16 }}>
                        {Object.entries(emp.behaviourScores).map(([key, val]) => (
                            <div key={key} style={{ textAlign: 'center', padding: 16, background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
                                <div style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: 8 }}>{key}</div>
                                <div style={{ fontWeight: 800, fontSize: '1.4rem', color: getColor(val * 10) }}>{val}</div>
                                <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', marginTop: 2 }}>/ 10</div>
                            </div>
                        ))}
                    </div>
                    <div style={{ padding: '14px 18px', background: '#faf5ff', borderRadius: 'var(--radius-sm)', border: '1px solid #e9d5ff' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6, fontWeight: 600, fontSize: '0.82rem', color: '#7c3aed' }}>
                            <MessageSquare size={14} /> Manager Comments
                        </div>
                        <div style={{ fontSize: '0.85rem', lineHeight: 1.6, color: '#4c1d95' }}>{emp.managerComment}</div>
                    </div>
                </div>
            </AnimatedCard>

            {/* 🚨 Risk Section */}
            <AnimatedCard delay={0.36} style={{ marginTop: 20 }}>
                <div className="card-header">
                    <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <AlertTriangle size={18} style={{ color: '#ef4444' }} /> Risk Assessment
                    </span>
                    <span className="badge" style={{ background: `${riskColors[emp.risk]}20`, color: riskColors[emp.risk] }}>{emp.risk} Risk</span>
                </div>
                <div className="card-body">
                    <StatRow icon={<Zap size={16} color="#f59e0b" />} label="Overload Frequency (last 3 sprints)" value={`${emp.riskData.overloadFreq} time(s)`} color={emp.riskData.overloadFreq > 3 ? '#ef4444' : '#10b981'} />
                    <StatRow icon={<AlertTriangle size={16} color="#ef4444" />} label="Escalation Involvement" value={`${emp.riskData.escalationInvolvement} escalation(s)`} color={emp.riskData.escalationInvolvement > 2 ? '#ef4444' : '#10b981'} />
                    <StatRow icon={<TrendingUp size={16} color={emp.riskData.perfDrop < 0 ? '#ef4444' : '#10b981'} />} label="Performance Change %" value={`${emp.riskData.perfDrop > 0 ? '+' : ''}${emp.riskData.perfDrop}%`} color={emp.riskData.perfDrop < 0 ? '#ef4444' : '#10b981'} />
                </div>
            </AnimatedCard>

            {/* 🏆 Promotion Section — from Promotion Recommendations */}
            <AnimatedCard delay={0.44} style={{ marginTop: 20, marginBottom: 20 }}>
                <div className="card-header">
                    <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <Award size={18} style={{ color: '#f59e0b' }} /> Promotion Status
                    </span>
                    <span className="badge" style={{ background: emp.promotion.eligible ? '#10b98120' : '#ef444420', color: emp.promotion.eligible ? '#10b981' : '#ef4444' }}>
                        {emp.promotion.eligible ? '✓ Eligible' : '✗ Not Eligible'}
                    </span>
                </div>
                <div className="card-body">
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 20 }}>
                        <div style={{ padding: '16px 20px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)', textAlign: 'center' }}>
                            <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: 6 }}>AI Verdict</div>
                            <div style={{ fontWeight: 700, fontSize: '0.95rem', color: verdictColors[emp.promotion.aiVerdict] }}>{emp.promotion.aiVerdict}</div>
                        </div>
                        <div style={{ padding: '16px 20px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)', textAlign: 'center' }}>
                            <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: 6 }}>Manager Review</div>
                            <div style={{ fontWeight: 700, fontSize: '0.95rem', color: emp.promotion.managerReview === 'Approved' ? '#10b981' : emp.promotion.managerReview === 'Hold' ? '#ef4444' : '#f59e0b' }}>{emp.promotion.managerReview}</div>
                        </div>
                        <div style={{ padding: '16px 20px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)', textAlign: 'center' }}>
                            <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: 6 }}>Decision</div>
                            <span className="badge" style={{ background: decisionColors[emp.promotion.finalDecision], color: '#fff', fontSize: '0.85rem', padding: '4px 14px' }}>{emp.promotion.finalDecision}</span>
                        </div>
                    </div>

                    <StatRow icon={<Clock size={16} color="#6b7280" />} label="Last Review Date" value={emp.promotion.lastReview} />
                    <StatRow icon={<User size={16} color="#3b82f6" />} label="Reviewed By" value={emp.promotion.reviewedBy} />

                    {/* Action Buttons */}
                    {emp.promotion.finalDecision !== 'Promoted' && (
                        <div style={{ marginTop: 16, display: 'flex', gap: 10 }}>
                            <button className="btn btn-sm btn-primary" style={{ display: 'flex', alignItems: 'center', gap: 6 }}
                                onClick={() => alert(`Sending ${emp.name}'s promotion to review...`)}>
                                <Send size={14} /> Send to Review
                            </button>
                            <button className="btn btn-sm" style={{ display: 'flex', alignItems: 'center', gap: 6, background: '#10b981', color: '#fff', border: 'none', borderRadius: 'var(--radius-sm)', padding: '6px 14px', cursor: 'pointer', fontWeight: 600 }}
                                onClick={() => alert(`Approving promotion for ${emp.name}...`)}>
                                <CheckCircle size={14} /> Approve Promotion
                            </button>
                            <button className="btn btn-sm" style={{ display: 'flex', alignItems: 'center', gap: 6, background: '#ef4444', color: '#fff', border: 'none', borderRadius: 'var(--radius-sm)', padding: '6px 14px', cursor: 'pointer', fontWeight: 600 }}
                                onClick={() => alert(`Putting ${emp.name}'s promotion on hold...`)}>
                                <PauseCircle size={14} /> Hold
                            </button>
                        </div>
                    )}
                </div>
            </AnimatedCard>
        </div>
    );
}
