import { useState, useEffect } from 'react';
import { Users, CheckSquare, Inbox, Cpu, TrendingUp } from 'lucide-react';
import { dashboardAPI } from '../../services/api';
import StatsCard from '../../components/StatsCard';
import AnimatedCard from '../../components/AnimatedCard';
import {
    BarChart, Bar, LineChart, Line,
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

const teamMembers = [
    { id: 1, name: 'Vikram Singh', role: 'Senior Developer', tasks: 8, completed: 5, status: 'Active' },
    { id: 2, name: 'Ravi Kumar', role: 'Developer', tasks: 6, completed: 4, status: 'Active' },
    { id: 3, name: 'Meera Joshi', role: 'Junior Developer', tasks: 5, completed: 3, status: 'Active' },
    { id: 4, name: 'Deepak Nair', role: 'QA Engineer', tasks: 7, completed: 6, status: 'On Leave' },
    { id: 5, name: 'Pooja Gupta', role: 'Developer', tasks: 6, completed: 2, status: 'Active' },
];

const workloadData = [
    { name: 'Vikram', assigned: 8, completed: 5 },
    { name: 'Ravi', assigned: 6, completed: 4 },
    { name: 'Meera', assigned: 5, completed: 3 },
    { name: 'Deepak', assigned: 7, completed: 6 },
    { name: 'Pooja', assigned: 6, completed: 2 },
];

const perfTrend = [
    { week: 'W1', score: 72 },
    { week: 'W2', score: 76 },
    { week: 'W3', score: 74 },
    { week: 'W4', score: 81 },
    { week: 'W5', score: 85 },
    { week: 'W6', score: 88 },
];

const reviewQueue = [
    { id: 1, title: 'PR #342 – Refactor auth middleware', author: 'Vikram Singh', priority: 'High', submitted: '2h ago' },
    { id: 2, title: 'PR #340 – Add pagination to user list', author: 'Ravi Kumar', priority: 'Medium', submitted: '5h ago' },
    { id: 3, title: 'PR #338 – Fix date picker timezone bug', author: 'Meera Joshi', priority: 'Low', submitted: '1d ago' },
    { id: 4, title: 'Task Review – Sprint planning doc', author: 'Pooja Gupta', priority: 'Medium', submitted: '1d ago' },
];

export default function LeadDashboard() {
    return (
        <div>
            {/* Stats */}
            <div className="stats-grid mb-lg">
                <StatsCard icon={<Users size={24} />} value="5" label="Team Members" color="blue" delay={0} />
                <StatsCard icon={<CheckSquare size={24} />} value="32" label="Active Tasks" trend="20 completed" trendDir="up" color="green" delay={0.08} />
                <StatsCard icon={<Inbox size={24} />} value="4" label="Review Queue" trend="2 urgent" color="orange" delay={0.16} />
                <StatsCard icon={<TrendingUp size={24} />} value="88%" label="Team Performance" trend="+7%" trendDir="up" color="green" delay={0.24} />
            </div>

            {/* Team Table + Review Queue */}
            <div className="grid-2 mb-lg">
                <AnimatedCard delay={0.3}>
                    <div className="card-header">
                        <span className="card-title">My Team</span>
                        <span className="badge badge-info">{teamMembers.length} members</span>
                    </div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <table className="table">
                            <thead>
                                <tr><th>Name</th><th>Role</th><th>Tasks</th><th>Status</th></tr>
                            </thead>
                            <tbody>
                                {teamMembers.map(m => (
                                    <tr key={m.id}>
                                        <td style={{ fontWeight: 600 }}>{m.name}</td>
                                        <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{m.role}</td>
                                        <td>
                                            <span style={{ fontWeight: 600 }}>{m.completed}</span>
                                            <span style={{ color: 'var(--text-tertiary)' }}>/{m.tasks}</span>
                                        </td>
                                        <td>
                                            <span className={`badge ${m.status === 'Active' ? 'badge-success' : 'badge-warning'}`}>{m.status}</span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </AnimatedCard>

                <AnimatedCard delay={0.38}>
                    <div className="card-header">
                        <span className="card-title">Review Queue</span>
                    </div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <table className="table">
                            <thead>
                                <tr><th>Item</th><th>Priority</th><th>Submitted</th></tr>
                            </thead>
                            <tbody>
                                {reviewQueue.map(r => (
                                    <tr key={r.id}>
                                        <td>
                                            <div style={{ fontWeight: 600, fontSize: '0.85rem' }}>{r.title}</div>
                                            <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>by {r.author}</div>
                                        </td>
                                        <td>
                                            <span className={`badge ${r.priority === 'High' ? 'badge-danger' : r.priority === 'Medium' ? 'badge-warning' : 'badge-info'}`}>
                                                {r.priority}
                                            </span>
                                        </td>
                                        <td style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{r.submitted}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </AnimatedCard>
            </div>

            {/* Charts */}
            <div className="grid-2">
                <AnimatedCard delay={0.46}>
                    <div className="card-header">
                        <span className="card-title">Workload Overview</span>
                    </div>
                    <div className="card-body">
                        <div className="chart-container">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={workloadData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                    <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                                    <YAxis tick={{ fontSize: 12 }} />
                                    <Tooltip />
                                    <Legend />
                                    <Bar dataKey="assigned" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Assigned" />
                                    <Bar dataKey="completed" fill="#10b981" radius={[4, 4, 0, 0]} name="Completed" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </AnimatedCard>

                <AnimatedCard delay={0.54}>
                    <div className="card-header">
                        <span className="card-title">Team Performance Trend</span>
                    </div>
                    <div className="card-body">
                        <div className="chart-container">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={perfTrend}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                    <XAxis dataKey="week" tick={{ fontSize: 12 }} />
                                    <YAxis tick={{ fontSize: 12 }} domain={[60, 100]} />
                                    <Tooltip formatter={(v) => `${v}%`} />
                                    <Line type="monotone" dataKey="score" stroke="#c0392b" strokeWidth={2.5} dot={{ r: 5, fill: '#c0392b' }} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </AnimatedCard>
            </div>
        </div>
    );
}
