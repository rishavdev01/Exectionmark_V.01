import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { ClipboardList, Send, CheckCircle, Clock, AlertCircle, Plus, X, Filter, Cpu } from 'lucide-react';
import { ROLE_CAN_ASSIGN_TO, ROLE_DISPLAY_NAMES } from '../../data/roleHierarchy';
import { employees as localEmployees } from '../../data/employeeData';
import { employeesAPI, tasksAPI } from '../../services/api';
import ConfirmToast from '../../components/ConfirmToast';

/*
 * Hierarchical task delegation (enforced by roleHierarchy.js):
 *   CEO  →  HR, PM, LEAD, DEVELOPER, DEVOPS, QA
 *   HR   →  PM, LEAD, DEVELOPER, DEVOPS, QA
 *   PM   →  LEAD, DEVELOPER, DEVOPS, QA
 *   LEAD →  DEVELOPER, DEVOPS, QA
 *   DEVELOPER, DEVOPS, QA → cannot assign
 */

/* ── Mock task data per role ── */
const ASSIGNED_TO_ME = {
    HR: [
        { id: 'T-051', title: 'Update Company Leave Policy', from: 'Rajesh Mehta (CEO)', type: 'Policy', priority: 'High', status: 'In Progress', due: 'Feb 22', est: '6h', actual: '4h', delay: 0 },
        { id: 'T-052', title: 'Conduct Q1 Performance Reviews', from: 'Rajesh Mehta (CEO)', type: 'HR', priority: 'Medium', status: 'To Do', due: 'Mar 01', est: '10h', actual: '—', delay: 0 },
        { id: 'T-053', title: 'Onboarding New Developers', from: 'Rajesh Mehta (CEO)', type: 'HR', priority: 'High', status: 'Done', due: 'Feb 15', est: '4h', actual: '3h', delay: 0 },
    ],
    PM: [
        { id: 'T-101', title: 'Finalize Q2 Sprint Roadmap', from: 'Rajesh Mehta (CEO)', type: 'Planning', priority: 'High', status: 'In Progress', due: 'Feb 22', est: '8h', actual: '5h', delay: 0 },
        { id: 'T-102', title: 'Prepare Board Presentation', from: 'Rajesh Mehta (CEO)', type: 'Report', priority: 'Critical', status: 'To Do', due: 'Feb 25', est: '6h', actual: '—', delay: 0 },
        { id: 'T-103', title: 'Review Resource Allocation', from: 'Rajesh Mehta (CEO)', type: 'Planning', priority: 'Medium', status: 'Done', due: 'Feb 18', est: '4h', actual: '4h', delay: 0 },
    ],
    LEAD: [
        { id: 'T-201', title: 'Sprint Alpha – Feature Development', from: 'Arjun Patel (PM)', type: 'Dev', priority: 'High', status: 'In Progress', due: 'Feb 20', est: '12h', actual: '10h', delay: 2 },
        { id: 'T-202', title: 'Code Review Standards Update', from: 'Arjun Patel (PM)', type: 'Process', priority: 'Medium', status: 'To Do', due: 'Feb 23', est: '4h', actual: '—', delay: 0 },
        { id: 'T-203', title: 'Team Performance Assessment', from: 'Arjun Patel (PM)', type: 'HR', priority: 'Low', status: 'In Progress', due: 'Feb 28', est: '5h', actual: '3h', delay: 0 },
        { id: 'T-204', title: 'Sprint Beta Planning Session', from: 'Arjun Patel (PM)', type: 'Planning', priority: 'High', status: 'Done', due: 'Feb 18', est: '3h', actual: '3h', delay: 0 },
    ],
    DEVELOPER: [
        { id: 'T-301', title: 'Implement OAuth2 Login Flow', from: 'Sneha Iyer (Scrum Master)', type: 'Dev', priority: 'High', status: 'In Progress', due: 'Feb 19', est: '8h', actual: '6h', delay: 3 },
        { id: 'T-302', title: 'Write Unit Tests for Payments', from: 'Sneha Iyer (Scrum Master)', type: 'QA', priority: 'Medium', status: 'To Do', due: 'Feb 21', est: '6h', actual: '—', delay: 0 },
        { id: 'T-303', title: 'Fix Pagination Bug on Dashboard', from: 'Sneha Iyer (Scrum Master)', type: 'Bug', priority: 'Low', status: 'Done', due: 'Feb 17', est: '2h', actual: '1.5h', delay: 0 },
        { id: 'T-304', title: 'API Documentation Update', from: 'Sneha Iyer (Scrum Master)', type: 'Doc', priority: 'Medium', status: 'In Review', due: 'Feb 22', est: '3h', actual: '3h', delay: 0 },
    ],
    DEVOPS: [
        { id: 'T-401', title: 'Set Up CI/CD for Sprint Beta', from: 'Sneha Iyer (Scrum Master)', type: 'DevOps', priority: 'High', status: 'In Progress', due: 'Feb 20', est: '10h', actual: '8h', delay: 4 },
        { id: 'T-402', title: 'Configure Monitoring Alerts', from: 'Sneha Iyer (Scrum Master)', type: 'DevOps', priority: 'Medium', status: 'To Do', due: 'Feb 22', est: '4h', actual: '—', delay: 0 },
        { id: 'T-403', title: 'Container Security Audit', from: 'Sneha Iyer (Scrum Master)', type: 'Security', priority: 'High', status: 'In Review', due: 'Feb 21', est: '6h', actual: '6h', delay: 0 },
    ],
    QA: [
        { id: 'T-601', title: 'Write Regression Tests for Auth Module', from: 'Sneha Iyer (Scrum Master)', type: 'QA', priority: 'High', status: 'In Progress', due: 'Feb 21', est: '8h', actual: '5h', delay: 0 },
        { id: 'T-602', title: 'Validate Sprint Alpha Release', from: 'Sneha Iyer (Scrum Master)', type: 'QA', priority: 'Medium', status: 'To Do', due: 'Feb 24', est: '6h', actual: '—', delay: 0 },
        { id: 'T-603', title: 'Performance Testing – API Endpoints', from: 'Sneha Iyer (Scrum Master)', type: 'QA', priority: 'High', status: 'Done', due: 'Feb 18', est: '5h', actual: '5h', delay: 0 },
        { id: 'T-604', title: 'Bug Report for Payment Module', from: 'Sneha Iyer (Scrum Master)', type: 'Bug', priority: 'Low', status: 'In Review', due: 'Feb 20', est: '2h', actual: '2h', delay: 0 },
    ],
};

const ASSIGNED_BY_ME = {
    CEO: [
        { id: 'T-051', title: 'Update Company Leave Policy', to: 'Priya Sharma (HR)', type: 'Policy', priority: 'High', status: 'In Progress', due: 'Feb 22', est: '6h', actual: '4h', delay: 0 },
        { id: 'T-101', title: 'Finalize Q2 Sprint Roadmap', to: 'Arjun Patel (PM)', type: 'Planning', priority: 'High', status: 'In Progress', due: 'Feb 22', est: '8h', actual: '5h', delay: 0 },
        { id: 'T-102', title: 'Prepare Board Presentation', to: 'Arjun Patel (PM)', type: 'Report', priority: 'Critical', status: 'To Do', due: 'Feb 25', est: '6h', actual: '—', delay: 0 },
        { id: 'T-103', title: 'Review Resource Allocation', to: 'Arjun Patel (PM)', type: 'Planning', priority: 'Medium', status: 'Done', due: 'Feb 18', est: '4h', actual: '4h', delay: 0 },
    ],
    HR: [
        { id: 'T-H01', title: 'Coordinate Team Building Event', to: 'Sneha Iyer (Scrum Master)', type: 'Event', priority: 'Low', status: 'To Do', due: 'Mar 05', est: '4h', actual: '—', delay: 0 },
        { id: 'T-H02', title: 'Update Onboarding Documents', to: 'Vikram Singh (Developer)', type: 'Doc', priority: 'Medium', status: 'In Progress', due: 'Feb 26', est: '5h', actual: '3h', delay: 0 },
    ],
    PM: [
        { id: 'T-201', title: 'Sprint Alpha – Feature Development', to: 'Sneha Iyer (Scrum Master)', type: 'Dev', priority: 'High', status: 'In Progress', due: 'Feb 20', est: '12h', actual: '10h', delay: 2 },
        { id: 'T-202', title: 'Code Review Standards Update', to: 'Sneha Iyer (Scrum Master)', type: 'Process', priority: 'Medium', status: 'To Do', due: 'Feb 23', est: '4h', actual: '—', delay: 0 },
        { id: 'T-203', title: 'Team Performance Assessment', to: 'Sneha Iyer (Scrum Master)', type: 'HR', priority: 'Low', status: 'In Progress', due: 'Feb 28', est: '5h', actual: '3h', delay: 0 },
    ],
    LEAD: [
        { id: 'T-301', title: 'Implement OAuth2 Login Flow', to: 'Vikram Singh (Developer)', type: 'Dev', priority: 'High', status: 'In Progress', due: 'Feb 19', est: '8h', actual: '6h', delay: 3 },
        { id: 'T-302', title: 'Write Unit Tests for Payments', to: 'Vikram Singh (Developer)', type: 'QA', priority: 'Medium', status: 'To Do', due: 'Feb 21', est: '6h', actual: '—', delay: 0 },
        { id: 'T-401', title: 'Set Up CI/CD for Sprint Beta', to: 'Ananya Reddy (DevOps)', type: 'DevOps', priority: 'High', status: 'In Progress', due: 'Feb 20', est: '10h', actual: '8h', delay: 4 },
        { id: 'T-601', title: 'Write Regression Tests for Auth Module', to: 'Divya Menon (QA)', type: 'QA', priority: 'High', status: 'In Progress', due: 'Feb 21', est: '8h', actual: '5h', delay: 0 },
    ],
};

const statusCols = ['To Do', 'In Progress', 'In Review', 'Done'];
const statusColors = { 'To Do': '#6b7280', 'In Progress': '#3b82f6', 'In Review': '#f59e0b', Done: '#10b981' };
const priorityColors = { Low: '#6b7280', Medium: '#3b82f6', High: '#f59e0b', Critical: '#ef4444' };
const selectStyle = { padding: '4px 8px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', fontSize: '0.75rem', background: '#fff', cursor: 'pointer' };

export default function TaskManagement() {
    const { user } = useAuth();
    const role = user?.role;
    const canAssign = (ROLE_CAN_ASSIGN_TO[role] || []).length > 0;
    const canReceive = role !== 'CEO';

    const defaultTab = canReceive ? 'assigned' : 'assigning';
    const [tab, setTab] = useState(defaultTab);
    const [view, setView] = useState('board');

    /* Assigned to me state (mutable for status changes) */
    const [assignedTasks, setAssignedTasks] = useState(ASSIGNED_TO_ME[role] || []);
    const [assigningTasks, setAssigningTasks] = useState(ASSIGNED_BY_ME[role] || []);

    /* Filters */
    const [statusFilter, setStatusFilter] = useState('All');
    const [priorityFilter, setPriorityFilter] = useState('All');

    /* New-task form state */
    const [showForm, setShowForm] = useState(false);
    const [newTitle, setNewTitle] = useState('');
    const [newDescription, setNewDescription] = useState('');
    const [newPriority, setNewPriority] = useState('Medium');
    const [newAssignTo, setNewAssignTo] = useState('');
    const [newAssignName, setNewAssignName] = useState('');

    /* Members of the currently selected assignee role */
    const membersForRole = newAssignTo
        ? employees.filter(e => e.role === ROLE_DISPLAY_NAMES[newAssignTo])
        : [];

    const handleNewTask = (e) => {
        e.preventDefault();
        const displayName = ROLE_DISPLAY_NAMES[newAssignTo] || newAssignTo;
        const label = newAssignName ? `${newAssignName} (${displayName})` : displayName;
        const task = {
            id: `T-${Date.now().toString().slice(-4)}`,
            title: newTitle,
            to: label,
            type: 'Task',
            priority: newPriority,
            status: 'To Do',
            due: 'TBD',
            est: '—',
            actual: '—',
            delay: 0,
        };
        setAssigningTasks(prev => [task, ...prev]);
        tasksAPI.create(task).catch(err => console.error('Failed to create task:', err));
        setNewTitle(''); setNewDescription(''); setNewPriority('Medium'); setNewAssignTo(''); setNewAssignName(''); setShowForm(false);
    };

    const handleStatusChange = (id, newStatus, list) => {
        if (list === 'assigned') {
            setAssignedTasks(prev => prev.map(t => t.id === id ? { ...t, status: newStatus } : t));
        } else {
            setAssigningTasks(prev => prev.map(t => t.id === id ? { ...t, status: newStatus } : t));
        }
        tasksAPI.update(id, { status: newStatus }).catch(err => console.error('Failed to update task status:', err));
    };

    const filteredAssigned = assignedTasks.filter(t => {
        if (statusFilter !== 'All' && t.status !== statusFilter) return false;
        if (priorityFilter !== 'All' && t.priority !== priorityFilter) return false;
        return true;
    });

    const filteredAssigning = assigningTasks.filter(t => {
        if (statusFilter !== 'All' && t.status !== statusFilter) return false;
        if (priorityFilter !== 'All' && t.priority !== priorityFilter) return false;
        return true;
    });

    const currentTasks = tab === 'assigned' ? filteredAssigned : filteredAssigning;

    return (
        <div>
            {/* Stats */}
            <div className="stats-grid mb-lg">
                <StatsCard icon={<ClipboardList size={24} />} value={assignedTasks.length + assigningTasks.length} label="Total Tasks" color="blue" delay={0} />
                <StatsCard icon={<Clock size={24} />} value={(tab === 'assigned' ? assignedTasks : assigningTasks).filter(t => t.status === 'Done').length} label="Completed" color="green" delay={0.08} />
                <StatsCard icon={<AlertCircle size={24} />} value={(tab === 'assigned' ? assignedTasks : assigningTasks).filter(t => t.priority === 'High' || t.priority === 'Critical').length} label="High Priority" color="red" delay={0.16} />
                <StatsCard icon={<Cpu size={24} />} value={(tab === 'assigned' ? assignedTasks : assigningTasks).filter(t => t.status === 'In Progress').length} label="In Progress" color="purple" delay={0.24} />
            </div>

            {/* Tabs */}
            <div className="task-tabs mb-lg">
                {canReceive && (
                    <button className={`task-tab ${tab === 'assigned' ? 'active' : ''}`} onClick={() => setTab('assigned')}>
                        <ClipboardList size={16} /> Assigned to Me
                        <span className="task-tab-count">{assignedTasks.length}</span>
                    </button>
                )}
                {canAssign && (
                    <button className={`task-tab ${tab === 'assigning' ? 'active' : ''}`} onClick={() => setTab('assigning')}>
                        <Send size={16} /> Tasks I Assigned
                        <span className="task-tab-count">{assigningTasks.length}</span>
                    </button>
                )}
            </div>

            {/* Filters + View Toggle */}
            <AnimatedCard delay={0.25}>
                <div className="card-body" style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
                    <Filter size={16} color="var(--text-tertiary)" />
                    <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)} style={{ padding: '6px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', fontSize: '0.82rem' }}>
                        <option value="All">All Status</option>
                        {statusCols.map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                    <select value={priorityFilter} onChange={e => setPriorityFilter(e.target.value)} style={{ padding: '6px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', fontSize: '0.82rem' }}>
                        <option value="All">All Priority</option>
                        <option value="Low">Low</option>
                        <option value="Medium">Medium</option>
                        <option value="High">High</option>
                        <option value="Critical">Critical</option>
                    </select>
                    <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
                        {canAssign && tab === 'assigning' && (
                            <button className="btn btn-sm btn-primary" onClick={() => setShowForm(!showForm)} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                                {showForm ? <X size={14} /> : <Plus size={14} />} {showForm ? 'Close' : 'Assign Task'}
                            </button>
                        )}
                        <button className={`btn btn-sm ${view === 'board' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setView('board')}>Board</button>
                        <button className={`btn btn-sm ${view === 'list' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setView('list')}>List</button>
                    </div>
                </div>
            </AnimatedCard>

            {/* New Task Form */}
            {showForm && canAssign && tab === 'assigning' && (
                <AnimatedCard delay={0} className="mb-lg" style={{ marginTop: 16 }}>
                    <div className="card-header"><span className="card-title">Create & Assign New Task</span></div>
                    <div className="card-body">
                        <form onSubmit={handleNewTask} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                            <div className="form-group" style={{ gridColumn: '1 / -1' }}>
                                <label className="form-label">Task Title *</label>
                                <input className="form-input" placeholder="Describe the task…" value={newTitle} onChange={e => setNewTitle(e.target.value)} required />
                            </div>
                            <div className="form-group" style={{ gridColumn: '1 / -1' }}>
                                <label className="form-label">Task Description</label>
                                <textarea className="form-input" rows={3} placeholder="Enter detailed task description…" value={newDescription} onChange={e => setNewDescription(e.target.value)}
                                    style={{ resize: 'vertical', minHeight: 60 }} />
                            </div>
                            <div className="form-group">
                                <label className="form-label">Priority</label>
                                <select className="form-select" value={newPriority} onChange={e => setNewPriority(e.target.value)}>
                                    <option>Low</option><option>Medium</option><option>High</option><option>Critical</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Assign To Role *</label>
                                <select className="form-select" value={newAssignTo} onChange={e => { setNewAssignTo(e.target.value); setNewAssignName(''); }} required>
                                    <option value="">Select role…</option>
                                    {(ROLE_CAN_ASSIGN_TO[role] || []).map(r => (
                                        <option key={r} value={r}>{ROLE_DISPLAY_NAMES[r]}</option>
                                    ))}
                                </select>
                            </div>
                            {newAssignTo && (
                                <div className="form-group">
                                    <label className="form-label">Assign To Member{membersForRole.length > 0 ? ' *' : ''}</label>
                                    {membersForRole.length > 0 ? (
                                        <select className="form-select" value={newAssignName} onChange={e => setNewAssignName(e.target.value)} required>
                                            <option value="">Select member…</option>
                                            {membersForRole.map(m => (
                                                <option key={m.id} value={m.name}>{m.name}</option>
                                            ))}
                                        </select>
                                    ) : (
                                        <p style={{ fontSize: '0.82rem', color: 'var(--text-tertiary)', margin: '4px 0 0' }}>No members found for this role.</p>
                                    )}
                                </div>
                            )}
                            <div style={{ gridColumn: '1 / -1' }}>
                                <button className="btn btn-primary" type="submit"><Send size={16} /> Assign Task</button>
                            </div>
                        </form>
                    </div>
                </AnimatedCard>
            )}

            {/* Board View */}
            {view === 'board' && (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginTop: 20 }}>
                    {statusCols.map(col => (
                        <div key={col}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12, padding: '8px 12px', background: `${statusColors[col]}15`, borderRadius: 'var(--radius-sm)', borderLeft: `3px solid ${statusColors[col]}` }}>
                                <span style={{ fontWeight: 700, fontSize: '0.85rem', color: statusColors[col] }}>{col}</span>
                                <span className="badge" style={{ background: statusColors[col], color: '#fff', fontSize: '0.7rem' }}>{currentTasks.filter(s => s.status === col).length}</span>
                            </div>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                                {currentTasks.filter(s => s.status === col).map(s => (
                                    <div key={s.id} style={{ padding: '14px', background: '#fff', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', boxShadow: '0 1px 3px rgba(0,0,0,0.06)' }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                                            <span style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', fontWeight: 600 }}>{s.id}</span>
                                            <span className="badge" style={{ background: `${priorityColors[s.priority]}20`, color: priorityColors[s.priority], fontSize: '0.65rem', fontWeight: 600 }}>{s.priority}</span>
                                        </div>
                                        <div style={{ fontWeight: 700, fontSize: '0.85rem', marginBottom: 6 }}>{s.title}</div>
                                        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 8 }}>
                                            {s.type && <span className="badge badge-neutral" style={{ fontSize: '0.68rem' }}>{s.type}</span>}
                                        </div>
                                        <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: 6 }}>
                                            {tab === 'assigned' ? `From: ${s.from}` : `To: ${s.to}`}
                                        </div>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                                            <span>Due: {s.due}</span>
                                            <select value={s.status} onChange={e => handleStatusChange(s.id, e.target.value, tab)} style={selectStyle}>
                                                {statusCols.map(st => <option key={st} value={st}>{st}</option>)}
                                            </select>
                                        </div>
                                        {s.delay > 0 && (
                                            <div style={{ marginTop: 6, fontSize: '0.72rem', color: '#ef4444', fontWeight: 600, display: 'flex', alignItems: 'center', gap: 4 }}>
                                                <Clock size={12} /> Delayed by {s.delay}h
                                            </div>
                                        )}
                                    </div>
                                ))}
                                {currentTasks.filter(s => s.status === col).length === 0 && (
                                    <div style={{ padding: 16, textAlign: 'center', color: 'var(--text-tertiary)', fontSize: '0.8rem', border: '1px dashed var(--border-color)', borderRadius: 'var(--radius-sm)' }}>No tasks</div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* List View */}
            {view === 'list' && (
                <AnimatedCard delay={0.32} style={{ marginTop: 20 }}>
                    <div className="card-body" style={{ padding: 0 }}>
                        <div className="table-wrapper">
                            <table className="table">
                                <thead>
                                    <tr>
                                        <th>ID</th><th>Task</th><th>{tab === 'assigned' ? 'From' : 'Assigned To'}</th><th>Type</th>
                                        <th>Priority</th><th>Status</th><th>Due</th><th>Est vs Actual</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {currentTasks.map(s => (
                                        <tr key={s.id}>
                                            <td style={{ fontFamily: "'Courier New',monospace", fontWeight: 700, fontSize: '0.82rem', color: '#3b82f6' }}>{s.id}</td>
                                            <td style={{ fontWeight: 600 }}>{s.title}</td>
                                            <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{tab === 'assigned' ? s.from : s.to}</td>
                                            <td><span className="badge badge-neutral">{s.type || '—'}</span></td>
                                            <td><span className="badge" style={{ background: `${priorityColors[s.priority]}20`, color: priorityColors[s.priority], fontWeight: 600 }}>{s.priority}</span></td>
                                            <td>
                                                <select value={s.status} onChange={e => handleStatusChange(s.id, e.target.value, tab)} style={{ ...selectStyle, fontWeight: 600, color: statusColors[s.status], background: `${statusColors[s.status]}10` }}>
                                                    {statusCols.map(st => <option key={st} value={st}>{st}</option>)}
                                                </select>
                                            </td>
                                            <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{s.due}</td>
                                            <td style={{ fontSize: '0.8rem' }}>{s.est} → {s.actual}</td>
                                        </tr>
                                    ))}
                                    {currentTasks.length === 0 && (
                                        <tr><td colSpan={8} style={{ textAlign: 'center', padding: 32, color: 'var(--text-tertiary)' }}>No tasks found.</td></tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </AnimatedCard>
            )}
        </div>
    );
}
