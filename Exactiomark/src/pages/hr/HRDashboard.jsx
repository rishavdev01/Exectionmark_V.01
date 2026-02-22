import { useState, useEffect } from 'react';
import { dashboardAPI } from '../../services/api';
import { Users, Mail, UserPlus, Award, Send } from 'lucide-react';
import StatsCard from '../../components/StatsCard';
import AnimatedCard from '../../components/AnimatedCard';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

const recentInvitations = [
    { id: 1, name: 'Sarah Lee', email: 'sarah.lee@example.com', role: 'Scrum Master', status: 'Today', approved: true },
    { id: 2, name: 'Alex Johnson', email: 'alex.johnson@example.com', role: 'Team Member', status: 'Yesterday', approved: true },
    { id: 3, name: 'Emma Brooks', email: 'emma.brooks@example.com', role: 'Team Member', status: 'Yesterday', approved: false },
];

const onboardingPending = [
    { id: 1, name: 'Samuel Green', email: 'samuel.green@example.com', role: 'Pending Engineer', date: 'Apr 22' },
    { id: 2, name: 'Maria Bell', email: 'maria.bell@example.com', role: 'Backend Developer', date: 'Apr 20' },
    { id: 3, name: 'Clarence White', email: 'clarence.white@example.com', role: 'QA Tester', date: 'Apr 19' },
];

const weeklyData = [
    { week: 'Week 1', hires: 3, departures: 1 },
    { week: 'Week 2', hires: 5, departures: 0 },
    { week: 'Week 3', hires: 2, departures: 2 },
    { week: 'Week 4', hires: 7, departures: 1 },
];

export default function HRDashboard() {
    const [recentInvitations, setRecentInvitations] = useState([
        { id: 1, name: 'Sarah Lee', email: 'sarah.lee@example.com', role: 'Scrum Master', status: 'Today', approved: true },
        { id: 2, name: 'Alex Johnson', email: 'alex.johnson@example.com', role: 'Team Member', status: 'Yesterday', approved: true },
        { id: 3, name: 'Emma Brooks', email: 'emma.brooks@example.com', role: 'Team Member', status: 'Yesterday', approved: false },
    ]);
    const [onboardingPending, setOnboardingPending] = useState([
        { id: 1, name: 'Samuel Green', email: 'samuel.green@example.com', role: 'Pending Engineer', date: 'Apr 22' },
        { id: 2, name: 'Maria Bell', email: 'maria.bell@example.com', role: 'Backend Developer', date: 'Apr 20' },
    ]);
    const [weeklyData, setWeeklyData] = useState([
        { week: 'Week 1', hires: 3, departures: 1 }, { week: 'Week 2', hires: 5, departures: 0 },
        { week: 'Week 3', hires: 2, departures: 2 }, { week: 'Week 4', hires: 7, departures: 1 },
    ]);
    const [inviteEmail, setInviteEmail] = useState('');
    const [inviteRole, setInviteRole] = useState('');

    useEffect(() => {
        dashboardAPI.hr().then(data => {
            if (!data) return;
            if (data.recent_invitations?.length) setRecentInvitations(data.recent_invitations);
            if (data.onboarding_pending?.length) setOnboardingPending(data.onboarding_pending);
            if (data.weekly_data?.length) setWeeklyData(data.weekly_data);
        }).catch(() => { });
    }, []);

    const handleInvite = (e) => {
        e.preventDefault();
        alert(`Invitation sent to ${inviteEmail} as ${inviteRole}`);
        setInviteEmail('');
        setInviteRole('');
    };

    return (
        <div>
            {/* Stats */}
            <div className="stats-grid mb-lg">
                <StatsCard icon={<Users size={24} />} value="148" label="Total Employees" trend="+8 this month" trendDir="up" color="blue" delay={0} />
                <StatsCard icon={<Mail size={24} />} value="12" label="Pending Invitations" trend="5 new" trendDir="up" color="orange" delay={0.08} />
                <StatsCard icon={<UserPlus size={24} />} value="23" label="New Hires (Q1)" trend="+15%" trendDir="up" color="green" delay={0.16} />
                <StatsCard icon={<Award size={24} />} value="7" label="Promotions Pending" color="red" delay={0.24} />
            </div>

            <div className="grid-2 mb-lg">
                {/* Invite Section */}
                <AnimatedCard delay={0.3}>
                    <div className="card-header">
                        <span className="card-title">Invite New Employee</span>
                    </div>
                    <div className="card-body">
                        <form onSubmit={handleInvite}>
                            <div className="form-group">
                                <input
                                    className="form-input"
                                    type="email"
                                    placeholder="Employee Email"
                                    value={inviteEmail}
                                    onChange={e => setInviteEmail(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <select className="form-select" value={inviteRole} onChange={e => setInviteRole(e.target.value)} required>
                                    <option value="">Assign Role</option>
                                    <option value="Developer">Developer</option>
                                    <option value="Scrum Master">Scrum Master</option>
                                    <option value="QA Tester">QA Tester</option>
                                    <option value="Designer">Designer</option>
                                    <option value="DevOps">DevOps</option>
                                    <option value="PM">Sprint Master</option>
                                </select>
                            </div>
                            <button className="btn btn-primary w-full" type="submit">
                                <Send size={16} /> Send Invitation
                            </button>
                        </form>
                    </div>
                </AnimatedCard>

                {/* Recent Invitations */}
                <AnimatedCard delay={0.38}>
                    <div className="card-header">
                        <span className="card-title">Recent Invitations</span>
                        <span className="badge badge-neutral">Today</span>
                    </div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Sent</th>
                                </tr>
                            </thead>
                            <tbody>
                                {recentInvitations.map(inv => (
                                    <tr key={inv.id}>
                                        <td style={{ fontWeight: 600 }}>{inv.name}</td>
                                        <td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{inv.email}</td>
                                        <td>{inv.role}</td>
                                        <td>
                                            <span className={`badge ${inv.status === 'Today' ? 'badge-info' : 'badge-warning'}`}>
                                                {inv.status}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </AnimatedCard>
            </div>

            <div className="grid-2">
                {/* Onboarding Pending */}
                <AnimatedCard delay={0.46}>
                    <div className="card-header">
                        <span className="card-title">Onboarding Pending</span>
                        <div style={{ display: 'flex', gap: 8 }}>
                            <span className="badge badge-neutral">Sent Date</span>
                        </div>
                    </div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <table className="table">
                            <tbody>
                                {onboardingPending.map(person => (
                                    <tr key={person.id}>
                                        <td>
                                            <div style={{ fontWeight: 600 }}>{person.name}</div>
                                            <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>{person.email}</div>
                                        </td>
                                        <td>{person.role}</td>
                                        <td style={{ color: 'var(--text-secondary)' }}>{person.date}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </AnimatedCard>

                {/* Reports & Insights */}
                <AnimatedCard delay={0.54}>
                    <div className="card-header">
                        <span className="card-title">Reports & Insights</span>
                        <span className="badge badge-neutral">Last 4 Weeks</span>
                    </div>
                    <div className="card-body">
                        <div className="chart-container">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={weeklyData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                    <XAxis dataKey="week" tick={{ fontSize: 12 }} />
                                    <YAxis tick={{ fontSize: 12 }} />
                                    <Tooltip />
                                    <Legend />
                                    <Bar dataKey="hires" fill="#3b82f6" radius={[4, 4, 0, 0]} name="New Hires" />
                                    <Bar dataKey="departures" fill="#ef4444" radius={[4, 4, 0, 0]} name="Departures" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </AnimatedCard>
            </div>
        </div>
    );
}
