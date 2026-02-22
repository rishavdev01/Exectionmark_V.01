import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import ActionModal from '../../components/ActionModal';
import { Inbox, AlertTriangle, CheckCircle, Cpu } from 'lucide-react';
import { pmAPI } from '../../services/api';

const riskColors = { Low: '#10b981', Medium: '#f59e0b', High: '#ef4444' };
const getColor = (v) => v >= 80 ? '#10b981' : v >= 60 ? '#f59e0b' : '#ef4444';
const leadBadgeStyle = (val) => ({
    background: val === 'Approved' ? '#10b98120' : val === 'Rejected' ? '#ef444420' : '#f59e0b20',
    color: val === 'Approved' ? '#10b981' : val === 'Rejected' ? '#ef4444' : '#f59e0b',
});

export default function PMReviewQueue() {
    const [data, setData] = useState([
        { id: 'ST-103', task: 'User Profile API', submittedBy: 'Vikram Singh', alignment: 88, leadApproval: 'Approved', delay: 0, risk: 'Low', aiComment: 'Code quality is high. Alignment within expected range.' },
        { id: 'ST-102', task: 'Setup CI/CD Pipeline', submittedBy: 'Ananya Reddy', alignment: 78, leadApproval: 'Pending', delay: 6, risk: 'High', aiComment: 'Significant delay detected. Pipeline config has 3 unresolved warnings.' },
        { id: 'ST-109', task: 'API Rate Limiting', submittedBy: 'Vikram Singh', alignment: 82, leadApproval: 'Approved', delay: 0, risk: 'Low', aiComment: 'Implementation follows best practices. Ready for merge.' },
        { id: 'ST-104', task: 'Dashboard UI Redesign', submittedBy: 'Rahul Verma', alignment: 65, leadApproval: 'Rejected', delay: 12, risk: 'High', aiComment: 'Alignment below threshold. 3 components deviate from design spec.' },
        { id: 'ST-106', task: 'Database Migration Script', submittedBy: 'Ananya Reddy', alignment: 72, leadApproval: 'Pending', delay: 3, risk: 'Medium', aiComment: 'Migration plan covers 80% of schemas. Missing rollback strategy.' },
        { id: 'ST-110', task: 'Monitoring Dashboard', submittedBy: 'Ananya Reddy', alignment: 70, leadApproval: 'Pending', delay: 4, risk: 'Medium', aiComment: 'Partially complete. Needs integration with alerting service.' },
    ]);
    const [modal, setModal] = useState(null); // { type, id, taskTitle }

    useEffect(() => {
        pmAPI.reviewQueue().then(d => { if (d?.length) setData(d); }).catch(() => { });
    }, []);


    const handleConfirm = (actionData) => {
        const { type, id } = modal;
        const statusMap = { approve: 'Approved', review: 'Revision', reject: 'Rejected' };
        const newStatus = statusMap[type];
        setData(prev => prev.map(q => q.id === id
            ? { ...q, leadApproval: newStatus, actionData }
            : q
        ));
        pmAPI.updateReviewItem(id, { action: type, leadApproval: newStatus, ...actionData }).catch(err => console.error('Failed to update review item:', err));
        setModal(null);
    };

    return (
        <div>
            {modal && (
                <ActionModal
                    type={modal.type}
                    storyTitle={modal.taskTitle}
                    onConfirm={handleConfirm}
                    onClose={() => setModal(null)}
                />
            )}

            <div className="stats-grid mb-lg">
                <StatsCard icon={<Inbox size={24} />} value={data.length} label="Pending Reviews" color="orange" delay={0} />
                <StatsCard icon={<AlertTriangle size={24} />} value={data.filter(q => q.risk === 'High').length} label="High Risk Items" color="red" delay={0.08} />
                <StatsCard icon={<CheckCircle size={24} />} value={data.filter(q => q.leadApproval === 'Approved').length} label="Lead Approved" color="green" delay={0.16} />
                <StatsCard icon={<Cpu size={24} />} value={`${Math.round(data.reduce((a, q) => a + q.alignment, 0) / data.length)}%`} label="Avg Alignment" color="purple" delay={0.24} />
            </div>

            <AnimatedCard delay={0.3}>
                <div className="card-header">
                    <span className="card-title">Review Queue</span>
                    <span className="badge badge-info">{data.length} items</span>
                </div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Task</th><th>Submitted By</th><th>Alignment Score</th>
                                    <th>Lead Approval</th><th>Delay (Hrs)</th><th>Risk</th><th>AI Comment</th><th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data.map(q => (
                                    <tr key={q.id}>
                                        <td>
                                            <div style={{ fontWeight: 600, fontSize: '0.85rem' }}>{q.task}</div>
                                            <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>{q.id}</div>
                                        </td>
                                        <td style={{ fontSize: '0.85rem' }}>{q.submittedBy}</td>
                                        <td><span style={{ fontWeight: 700, color: getColor(q.alignment) }}>{q.alignment}%</span></td>
                                        <td><span className="badge" style={leadBadgeStyle(q.leadApproval)}>{q.leadApproval}</span></td>
                                        <td>{q.delay > 0 ? <span style={{ color: '#ef4444', fontWeight: 700 }}>{q.delay}h</span> : <span style={{ color: '#10b981' }}>—</span>}</td>
                                        <td><span className="badge" style={{ background: riskColors[q.risk], color: '#fff' }}>{q.risk}</span></td>
                                        <td>
                                            <div style={{ fontSize: '0.78rem', color: '#4c1d95', background: '#f5f3ff', padding: '6px 10px', borderRadius: 'var(--radius-sm)', border: '1px solid #e9d5ff', maxWidth: 220 }}>
                                                <Cpu size={10} style={{ display: 'inline', marginRight: 4 }} />{q.aiComment}
                                            </div>
                                        </td>
                                        <td>
                                            <div style={{ display: 'flex', gap: 4 }}>
                                                <button title="Approve"
                                                    onClick={() => setModal({ type: 'approve', id: q.id, taskTitle: q.task })}
                                                    style={{ padding: '4px 10px', borderRadius: 6, border: 'none', background: '#10b98120', color: '#10b981', fontWeight: 700, fontSize: '0.75rem', cursor: 'pointer' }}>
                                                    Approve ✓
                                                </button>
                                                <button title="Request Changes"
                                                    onClick={() => setModal({ type: 'review', id: q.id, taskTitle: q.task })}
                                                    style={{ padding: '4px 10px', borderRadius: 6, border: 'none', background: '#3b82f620', color: '#3b82f6', fontWeight: 700, fontSize: '0.75rem', cursor: 'pointer' }}>
                                                    Changes
                                                </button>
                                                <button title="Reject"
                                                    onClick={() => setModal({ type: 'reject', id: q.id, taskTitle: q.task })}
                                                    style={{ padding: '4px 10px', borderRadius: 6, border: 'none', background: '#ef444420', color: '#ef4444', fontWeight: 700, fontSize: '0.75rem', cursor: 'pointer' }}>
                                                    Reject
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </AnimatedCard>
        </div>
    );
}
