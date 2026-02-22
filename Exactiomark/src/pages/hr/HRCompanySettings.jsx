import { useState } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import { Settings, Building2, Shield, Sliders, Timer } from 'lucide-react';

export default function HRCompanySettings() {
    /* Company Info */
    const [company, setCompany] = useState({ name: 'Exactiomark', domain: 'exactiomark.com', industry: 'Technology', location: 'Bangalore, India' });

    /* Performance Weights */
    const [weights, setWeights] = useState({ sprint: 40, alignment: 30, delivery: 20, behaviour: 10 });
    const totalWeight = Object.values(weights).reduce((a, b) => a + b, 0);

    /* Sprint Policy */
    const [sprintPolicy, setSprintPolicy] = useState({ duration: 14, maxSP: 120, approvalSLA: 4 });

    /* Access Control */
    const [behaviourAssign, setBehaviourAssign] = useState(['PM', 'LEAD']);
    const [promotionWeightEdit, setPromotionWeightEdit] = useState(['HR', 'CEO']);

    const allRoles = ['CEO', 'HR', 'PM', 'LEAD', 'DEVELOPER', 'DEVOPS', 'QA'];

    const toggleRole = (list, setList, role) => {
        setList(prev => prev.includes(role) ? prev.filter(r => r !== role) : [...prev, role]);
    };

    return (
        <div>
            <div className="grid-2 mb-lg">
                {/* Company Info */}
                <AnimatedCard delay={0.1}>
                    <div className="card-header">
                        <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}><Building2 size={18} /> Company Info</span>
                    </div>
                    <div className="card-body">
                        <div style={{ display: 'grid', gap: 16 }}>
                            {Object.entries(company).map(([key, val]) => (
                                <div key={key}>
                                    <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: 4 }}>
                                        {key === 'name' ? 'Company Name' : key.charAt(0).toUpperCase() + key.slice(1)}
                                    </label>
                                    <input type="text" value={val}
                                        onChange={e => setCompany(prev => ({ ...prev, [key]: e.target.value }))}
                                        style={{ width: '100%', padding: '10px 14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', fontSize: '0.9rem' }} />
                                </div>
                            ))}
                        </div>
                    </div>
                </AnimatedCard>

                {/* Sprint Policy */}
                <AnimatedCard delay={0.18}>
                    <div className="card-header">
                        <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}><Timer size={18} /> Sprint Policy</span>
                    </div>
                    <div className="card-body">
                        <div style={{ display: 'grid', gap: 16 }}>
                            <div>
                                <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: 4 }}>Sprint Duration (days)</label>
                                <input type="number" value={sprintPolicy.duration}
                                    onChange={e => setSprintPolicy(prev => ({ ...prev, duration: Number(e.target.value) }))}
                                    style={{ width: '100%', padding: '10px 14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', fontSize: '0.9rem' }} />
                            </div>
                            <div>
                                <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: 4 }}>Max Story Points per Sprint</label>
                                <input type="number" value={sprintPolicy.maxSP}
                                    onChange={e => setSprintPolicy(prev => ({ ...prev, maxSP: Number(e.target.value) }))}
                                    style={{ width: '100%', padding: '10px 14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', fontSize: '0.9rem' }} />
                            </div>
                            <div>
                                <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: 4 }}>Approval SLA Time (hours)</label>
                                <input type="number" value={sprintPolicy.approvalSLA}
                                    onChange={e => setSprintPolicy(prev => ({ ...prev, approvalSLA: Number(e.target.value) }))}
                                    style={{ width: '100%', padding: '10px 14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', fontSize: '0.9rem' }} />
                            </div>
                        </div>
                    </div>
                </AnimatedCard>
            </div>

            {/* Performance Weights */}
            <AnimatedCard delay={0.26}>
                <div className="card-header">
                    <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}><Sliders size={18} /> Performance Weights</span>
                    <span className={`badge ${totalWeight === 100 ? 'badge-success' : 'badge-danger'}`}>
                        Total: {totalWeight}%{totalWeight !== 100 ? ' ⚠ Must equal 100%' : ' ✓'}
                    </span>
                </div>
                <div className="card-body">
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16 }}>
                        {[
                            { key: 'sprint', label: 'Sprint Contribution', color: '#3b82f6' },
                            { key: 'alignment', label: 'Alignment Score', color: '#10b981' },
                            { key: 'delivery', label: 'Delivery', color: '#f59e0b' },
                            { key: 'behaviour', label: 'Behaviour', color: '#8b5cf6' },
                        ].map(w => (
                            <div key={w.key} style={{ padding: '18px 20px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)', borderLeft: `4px solid ${w.color}` }}>
                                <div style={{ fontWeight: 700, fontSize: '0.85rem', marginBottom: 10, color: w.color }}>{w.label}</div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                                    <input type="range" min="0" max="100" value={weights[w.key]}
                                        onChange={e => setWeights(prev => ({ ...prev, [w.key]: Number(e.target.value) }))}
                                        style={{ flex: 1, accentColor: w.color }} />
                                    <span style={{ fontWeight: 800, fontSize: '1.1rem', color: w.color, minWidth: 45, textAlign: 'center' }}>{weights[w.key]}%</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </AnimatedCard>

            {/* Access Control */}
            <AnimatedCard delay={0.34} style={{ marginTop: 20 }}>
                <div className="card-header">
                    <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}><Shield size={18} /> Access Control</span>
                </div>
                <div className="card-body">
                    <div className="grid-2" style={{ gap: 24 }}>
                        <div>
                            <div style={{ fontWeight: 700, fontSize: '0.88rem', marginBottom: 12 }}>Who can assign Behaviour Marks?</div>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                                {allRoles.map(r => (
                                    <button key={r} onClick={() => toggleRole(behaviourAssign, setBehaviourAssign, r)}
                                        style={{
                                            padding: '6px 14px', borderRadius: 'var(--radius-xl)', fontSize: '0.82rem', fontWeight: 600, cursor: 'pointer', transition: 'all 0.15s ease',
                                            background: behaviourAssign.includes(r) ? '#3b82f6' : '#fff', color: behaviourAssign.includes(r) ? '#fff' : 'var(--text-secondary)',
                                            border: `1px solid ${behaviourAssign.includes(r) ? '#3b82f6' : 'var(--border-color)'}`
                                        }}>{r}</button>
                                ))}
                            </div>
                        </div>
                        <div>
                            <div style={{ fontWeight: 700, fontSize: '0.88rem', marginBottom: 12 }}>Who can edit Promotion Weights?</div>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                                {allRoles.map(r => (
                                    <button key={r} onClick={() => toggleRole(promotionWeightEdit, setPromotionWeightEdit, r)}
                                        style={{
                                            padding: '6px 14px', borderRadius: 'var(--radius-xl)', fontSize: '0.82rem', fontWeight: 600, cursor: 'pointer', transition: 'all 0.15s ease',
                                            background: promotionWeightEdit.includes(r) ? '#8b5cf6' : '#fff', color: promotionWeightEdit.includes(r) ? '#fff' : 'var(--text-secondary)',
                                            border: `1px solid ${promotionWeightEdit.includes(r) ? '#8b5cf6' : 'var(--border-color)'}`
                                        }}>{r}</button>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </AnimatedCard>

            <div style={{ marginTop: 20, display: 'flex', justifyContent: 'flex-end' }}>
                <button className="btn btn-primary" onClick={() => alert('Settings saved!')}>
                    Save All Settings
                </button>
            </div>
        </div>
    );
}
