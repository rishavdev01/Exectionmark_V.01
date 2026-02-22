import { useState, useRef } from 'react';
import { useAuth } from '../../context/AuthContext';
import { ROLE_LABELS } from '../../data/navigation';
import AnimatedCard from '../../components/AnimatedCard';
import { Mail, Building, Shield, Phone, BarChart3, TrendingUp, AlertTriangle, Award, User, MessageSquare, Zap, Clock, Github, Eye, EyeOff, Copy, Check, Fingerprint, Camera } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

/* Mock data for employee detail view */
const alignmentHistory = [
    { sprint: 'S1', score: 78 }, { sprint: 'S2', score: 82 }, { sprint: 'S3', score: 85 },
    { sprint: 'S4', score: 80 }, { sprint: 'S5', score: 88 }, { sprint: 'S6', score: 91 },
];

const sprintContribution = [
    { sprint: 'S1', sp: 18 }, { sprint: 'S2', sp: 22 }, { sprint: 'S3', sp: 20 },
    { sprint: 'S4', sp: 24 }, { sprint: 'S5', sp: 21 }, { sprint: 'S6', sp: 26 },
];

const perfMetrics = { alignment: 91, onTime: 94, rejection: 5 };
const behaviourScores = { communication: 9, ownership: 9, teamwork: 8, managerComment: 'Consistently delivers high-quality code. Excellent problem solver and proactive communicator.' };
const riskData = { overloadFreq: 2, escalationInvolvement: 1, perfDrop: -3.2 };
const promoData = { eligible: true, aiRecommendation: 'Strongly Recommend', lastReview: 'Feb 15, 2026' };

const getColor = (s) => s >= 80 ? '#10b981' : s >= 60 ? '#f59e0b' : '#ef4444';

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

export default function ProfilePage() {
    const { user } = useAuth();
    const isCEO = user?.role === 'CEO';
    const showPAT = user?.role === 'DEVELOPER' || user?.role === 'DEVOPS';

    const [pat, setPat] = useState('ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890');
    const [patVisible, setPatVisible] = useState(false);
    const [patEditing, setPatEditing] = useState(false);
    const [copied, setCopied] = useState(false);
    const [profileImg, setProfileImg] = useState(null);
    const fileInputRef = useRef(null);

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (ev) => setProfileImg(ev.target.result);
        reader.readAsDataURL(file);
    };

    const handleCopy = () => {
        navigator.clipboard.writeText(pat);
        setCopied(true);
        setTimeout(() => setCopied(false), 1800);
    };

    return (
        <div style={{ maxWidth: 1000, margin: '0 auto' }}>
            {/* Header Card */}
            <AnimatedCard delay={0}>
                <div className="card-body" style={{ textAlign: 'center', padding: '48px 24px 24px' }}>
                    {/* Hidden file input */}
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/*"
                        style={{ display: 'none' }}
                        onChange={handleImageChange}
                    />

                    {/* Avatar / profile image with camera button overlay */}
                    <div style={{ position: 'relative', width: 96, height: 96, margin: '0 auto 16px' }}>
                        {profileImg ? (
                            <img
                                src={profileImg}
                                alt="Profile"
                                style={{ width: 96, height: 96, borderRadius: '50%', objectFit: 'cover', border: '3px solid var(--brand-primary)' }}
                            />
                        ) : (
                            <div style={{
                                width: 96, height: 96, borderRadius: '50%', background: 'var(--brand-gradient)',
                                color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center',
                                fontSize: '1.8rem', fontWeight: 800,
                            }}>{user?.avatar}</div>
                        )}
                        {/* Camera button */}
                        <button
                            onClick={() => fileInputRef.current?.click()}
                            title="Edit profile photo"
                            style={{
                                position: 'absolute', bottom: 2, right: 2,
                                width: 28, height: 28, borderRadius: '50%',
                                background: 'var(--brand-primary)', border: '2px solid #fff',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                cursor: 'pointer', boxShadow: '0 2px 6px rgba(0,0,0,0.25)',
                                transition: 'transform 0.15s ease',
                            }}
                            onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.12)'}
                            onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
                        >
                            <Camera size={13} color="#fff" />
                        </button>
                    </div>

                    <h2 style={{ fontSize: '1.5rem', fontWeight: 800 }}>{user?.name}</h2>
                    <p style={{ color: 'var(--text-secondary)', marginTop: 4 }}>{ROLE_LABELS[user?.role] || user?.role}</p>
                </div>
            </AnimatedCard>

            {/* Contact Info (always shown) + Activity (hidden for CEO) */}
            <div className={isCEO ? 'mt-lg' : 'grid-2 mt-lg'}>
                <AnimatedCard delay={0.1}>
                    <div className="card-header"><span className="card-title">Contact Info</span></div>
                    <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                        {/* Employee ID — all roles */}
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                            <Fingerprint size={18} color="var(--text-tertiary)" />
                            <div>
                                <div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)' }}>Employee ID</div>
                                <div style={{ fontWeight: 700, fontFamily: 'monospace', letterSpacing: '0.5px' }}>
                                    {user?.id}
                                </div>
                            </div>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Mail size={18} color="var(--text-tertiary)" /><div><div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)' }}>Email</div><div style={{ fontWeight: 600 }}>{user?.email}</div></div></div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Building size={18} color="var(--text-tertiary)" /><div><div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)' }}>Department</div><div style={{ fontWeight: 600 }}>{user?.department}</div></div></div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Shield size={18} color="var(--text-tertiary)" /><div><div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)' }}>Role</div><div style={{ fontWeight: 600 }}>{user?.role}</div></div></div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}><Phone size={18} color="var(--text-tertiary)" /><div><div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)' }}>Phone</div><div style={{ fontWeight: 600 }}>+91 98765 43210</div></div></div>

                        {/* GitHub PAT — DEVELOPER & DEVOPS only */}
                        {showPAT && (
                            <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                                <Github size={18} color="var(--text-tertiary)" style={{ marginTop: 3 }} />
                                <div style={{ flex: 1 }}>
                                    <div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)', marginBottom: 4 }}>GitHub PAT</div>
                                    {patEditing ? (
                                        <div style={{ display: 'flex', gap: 6 }}>
                                            <input
                                                autoFocus
                                                value={pat}
                                                onChange={e => setPat(e.target.value)}
                                                style={{ flex: 1, padding: '5px 10px', borderRadius: 6, border: '1px solid #3b82f6', fontFamily: 'monospace', fontSize: '0.78rem' }}
                                            />
                                            <button onClick={() => setPatEditing(false)}
                                                style={{ padding: '4px 10px', borderRadius: 6, border: 'none', background: '#3b82f6', color: '#fff', fontWeight: 700, fontSize: '0.75rem', cursor: 'pointer' }}>
                                                Save
                                            </button>
                                        </div>
                                    ) : (
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                            <span style={{ fontFamily: 'monospace', fontWeight: 600, fontSize: '0.82rem', letterSpacing: patVisible ? 0 : '2px', color: 'var(--text-primary)' }}>
                                                {patVisible ? pat : '•'.repeat(Math.min(pat.length, 32))}
                                            </span>
                                            <button onClick={() => setPatVisible(v => !v)} title={patVisible ? 'Hide' : 'Show'}
                                                style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 2 }}>
                                                {patVisible ? <EyeOff size={14} color="#6b7280" /> : <Eye size={14} color="#6b7280" />}
                                            </button>
                                            <button onClick={handleCopy} title="Copy" style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 2 }}>
                                                {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} color="#6b7280" />}
                                            </button>
                                            <button onClick={() => setPatEditing(true)}
                                                style={{ fontSize: '0.7rem', padding: '2px 8px', borderRadius: 5, border: '1px solid #e5e7eb', background: '#f9fafb', cursor: 'pointer', fontWeight: 600, color: '#374151' }}>
                                                Edit
                                            </button>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                </AnimatedCard>

                {!isCEO && (
                    <AnimatedCard delay={0.15}>
                        <div className="card-header"><span className="card-title">Activity</span></div>
                        <div className="card-body">
                            <div className="timeline">
                                <div className="timeline-item"><div className="timeline-item-title">Logged in</div><div className="timeline-item-time">Just now</div></div>
                                <div className="timeline-item"><div className="timeline-item-title">Updated profile settings</div><div className="timeline-item-time">2 days ago</div></div>
                                <div className="timeline-item"><div className="timeline-item-title">Completed security training</div><div className="timeline-item-time">1 week ago</div></div>
                                <div className="timeline-item"><div className="timeline-item-title">Joined Exactiomark</div><div className="timeline-item-time">3 months ago</div></div>
                            </div>
                        </div>
                    </AnimatedCard>
                )}
            </div>

            {/* Everything below is hidden for CEO – CEO only sees Contact Info */}
            {!isCEO && (
                <>
                    {/* 📊 Performance Section */}
                    <AnimatedCard delay={0.2} style={{ marginTop: 20 }}>
                        <div className="card-header">
                            <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <BarChart3 size={18} style={{ color: '#3b82f6' }} /> Performance
                            </span>
                        </div>
                        <div className="card-body">
                            <StatRow icon={<TrendingUp size={16} color="#3b82f6" />} label="Current Alignment Score" value={`${perfMetrics.alignment}%`} color={getColor(perfMetrics.alignment)} />
                            <StatRow icon={<Clock size={16} color="#10b981" />} label="On-time Delivery %" value={`${perfMetrics.onTime}%`} color={getColor(perfMetrics.onTime)} />
                            <StatRow icon={<AlertTriangle size={16} color="#ef4444" />} label="Rejection Rate" value={`${perfMetrics.rejection}%`} color={perfMetrics.rejection > 10 ? '#ef4444' : '#10b981'} />

                            <div className="grid-2" style={{ marginTop: 20, gap: 16 }}>
                                <div>
                                    <div style={{ fontWeight: 700, fontSize: '0.82rem', marginBottom: 8 }}>Alignment Score History</div>
                                    <div style={{ height: 180 }}>
                                        <ResponsiveContainer width="100%" height="100%">
                                            <LineChart data={alignmentHistory}>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                                <XAxis dataKey="sprint" tick={{ fontSize: 11 }} />
                                                <YAxis domain={[60, 100]} tick={{ fontSize: 11 }} />
                                                <Tooltip formatter={(v) => `${v}%`} />
                                                <Line type="monotone" dataKey="score" stroke="#3b82f6" strokeWidth={2} dot={{ fill: '#3b82f6', r: 4 }} />
                                            </LineChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>
                                <div>
                                    <div style={{ fontWeight: 700, fontSize: '0.82rem', marginBottom: 8 }}>Sprint Contribution Trend</div>
                                    <div style={{ height: 180 }}>
                                        <ResponsiveContainer width="100%" height="100%">
                                            <LineChart data={sprintContribution}>
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
                                <User size={18} style={{ color: '#8b5cf6' }} /> Behaviour
                            </span>
                            <span className="badge" style={{ background: '#8b5cf620', color: '#8b5cf6' }}>10% Weight</span>
                        </div>
                        <div className="card-body">
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 16 }}>
                                {[
                                    { label: 'Communication', val: behaviourScores.communication },
                                    { label: 'Ownership', val: behaviourScores.ownership },
                                    { label: 'Teamwork', val: behaviourScores.teamwork },
                                ].map(b => (
                                    <div key={b.label} style={{ textAlign: 'center', padding: '16px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)' }}>
                                        <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: 6 }}>{b.label}</div>
                                        <div style={{ fontWeight: 800, fontSize: '1.3rem', color: getColor(b.val * 10) }}>{b.val}/10</div>
                                    </div>
                                ))}
                            </div>
                            <div style={{ padding: '14px 18px', background: '#faf5ff', borderRadius: 'var(--radius-sm)', border: '1px solid #e9d5ff' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6, fontWeight: 600, fontSize: '0.82rem', color: '#7c3aed' }}>
                                    <MessageSquare size={14} /> Manager Comments
                                </div>
                                <div style={{ fontSize: '0.85rem', lineHeight: 1.6, color: '#4c1d95' }}>{behaviourScores.managerComment}</div>
                            </div>
                        </div>
                    </AnimatedCard>

                    {/* 🚨 Risk Section */}
                    <AnimatedCard delay={0.36} style={{ marginTop: 20 }}>
                        <div className="card-header">
                            <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <AlertTriangle size={18} style={{ color: '#ef4444' }} /> Risk Assessment
                            </span>
                        </div>
                        <div className="card-body">
                            <StatRow icon={<Zap size={16} color="#f59e0b" />} label="Overload Frequency (last 3 sprints)" value={`${riskData.overloadFreq} times`} />
                            <StatRow icon={<AlertTriangle size={16} color="#ef4444" />} label="Escalation Involvement" value={`${riskData.escalationInvolvement} escalation(s)`} />
                            <StatRow icon={<TrendingUp size={16} color={riskData.perfDrop < 0 ? '#ef4444' : '#10b981'} />} label="Performance Change %" value={`${riskData.perfDrop}%`} color={riskData.perfDrop < 0 ? '#ef4444' : '#10b981'} />
                        </div>
                    </AnimatedCard>

                    {/* 🏆 Promotion Section */}
                    <AnimatedCard delay={0.44} style={{ marginTop: 20, marginBottom: 20 }}>
                        <div className="card-header">
                            <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <Award size={18} style={{ color: '#f59e0b' }} /> Promotion
                            </span>
                        </div>
                        <div className="card-body">
                            <StatRow icon={<Shield size={16} color="#10b981" />} label="Eligibility Status" value={promoData.eligible ? '✓ Eligible' : '✗ Not Eligible'} color={promoData.eligible ? '#10b981' : '#ef4444'} />
                            <StatRow icon={<Zap size={16} color="#8b5cf6" />} label="AI Recommendation" value={promoData.aiRecommendation} color={promoData.aiRecommendation.includes('Strongly') ? '#10b981' : '#3b82f6'} />
                            <StatRow icon={<Clock size={16} color="#6b7280" />} label="Last Review Date" value={promoData.lastReview} />
                        </div>
                    </AnimatedCard>
                </>
            )}
        </div>
    );
}
