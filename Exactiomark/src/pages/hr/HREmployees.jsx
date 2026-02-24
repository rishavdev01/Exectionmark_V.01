import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { Users, Search, UserCheck, AlertTriangle, TrendingUp } from 'lucide-react';
import { employeesAPI } from '../../services/api';


const riskColors = { Low: '#10b981', Medium: '#f59e0b', High: '#ef4444' };
const statusColors = { Active: '#10b981', 'On Leave': '#3b82f6', Probation: '#f59e0b' };
const getScoreColor = (s) => s >= 80 ? '#10b981' : s >= 65 ? '#f59e0b' : '#ef4444';

export default function HREmployees() {
    const navigate = useNavigate();
    const [search, setSearch] = useState('');
    const [deptFilter, setDeptFilter] = useState('All');
    const [employees, setEmployees] = useState([]);

    useEffect(() => {
        employeesAPI.getAll()
            .then(data => setEmployees(Array.isArray(data) ? data : []))
            .catch(() => { });
    }, []);

    const depts = ['All', ...new Set(employees.map(e => e.dept))];
    const filtered = employees.filter(e => {
        if (deptFilter !== 'All' && e.dept !== deptFilter) return false;
        if (search && !e.name.toLowerCase().includes(search.toLowerCase())) return false;
        return true;
    });

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<Users size={24} />} value={employees.length} label="Total Employees" trend="+2 this month" trendDir="up" color="blue" delay={0} />
                <StatsCard icon={<UserCheck size={24} />} value={employees.filter(e => e.status === 'Active').length} label="Active" color="green" delay={0.08} />
                <StatsCard icon={<AlertTriangle size={24} />} value={employees.filter(e => e.risk === 'High').length} label="High Risk" color="red" delay={0.16} />
                <StatsCard icon={<TrendingUp size={24} />} value="82.3%" label="Avg Performance" trend="+1.8%" trendDir="up" color="purple" delay={0.24} />
            </div>

            <AnimatedCard delay={0.3}>
                <div className="card-header">
                    <span className="card-title">All Employees</span>
                    <div style={{ display: 'flex', gap: 8 }}>
                        <div style={{ position: 'relative' }}>
                            <Search size={14} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)' }} />
                            <input type="text" placeholder="Search..." value={search} onChange={e => setSearch(e.target.value)}
                                style={{ paddingLeft: 30, padding: '6px 12px 6px 30px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', fontSize: '0.82rem', width: 160 }} />
                        </div>
                        <select value={deptFilter} onChange={e => setDeptFilter(e.target.value)}
                            style={{ padding: '6px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', fontSize: '0.82rem' }}>
                            {depts.map(d => <option key={d} value={d}>{d}</option>)}
                        </select>
                    </div>
                </div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Employee</th>
                                    <th>Department</th>
                                    <th>Project(s)</th>
                                    <th>Perf Score</th>
                                    <th>Behaviour</th>
                                    <th>Risk</th>
                                    <th>Sprint</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filtered.map(e => (
                                    <tr key={e.id} onClick={() => navigate(`/employees/${e.id}`)} style={{ cursor: 'pointer' }}>
                                        <td>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                                <div style={{ width: 34, height: 34, borderRadius: '50%', background: '#3b82f6', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '0.72rem', flexShrink: 0 }}>{e.avatar}</div>
                                                <div>
                                                    <div style={{ fontWeight: 600, fontSize: '0.85rem' }}>{e.name}</div>
                                                    <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>{e.role}</div>
                                                </div>
                                            </div>
                                        </td>
                                        <td>{e.dept}</td>
                                        <td style={{ fontSize: '0.8rem' }}>{e.projects.join(', ')}</td>
                                        <td><span style={{ fontWeight: 700, color: getScoreColor(e.perfScore) }}>{e.perfScore}%</span></td>
                                        <td><span style={{ fontWeight: 700, color: getScoreColor(e.behaviour * 10) }}>{e.behaviour}/10</span></td>
                                        <td><span className="badge" style={{ background: riskColors[e.risk], color: '#fff' }}>{e.risk}</span></td>
                                        <td style={{ fontWeight: 600, fontSize: '0.82rem' }}>{e.sprintContrib}</td>
                                        <td><span className="badge" style={{ background: `${statusColors[e.status]}20`, color: statusColors[e.status], fontWeight: 600 }}>{e.status}</span></td>
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
