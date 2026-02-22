import AnimatedCard from '../../components/AnimatedCard';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { FileText, Download } from 'lucide-react';

const reports = [
    { id: 1, title: 'Monthly Performance Report', date: 'Feb 2026', type: 'Performance' },
    { id: 2, title: 'Sprint Velocity Analysis', date: 'Jan 2026', type: 'Engineering' },
    { id: 3, title: 'Budget Utilization Report', date: 'Jan 2026', type: 'Finance' },
    { id: 4, title: 'Employee Satisfaction Survey', date: 'Dec 2025', type: 'HR' },
    { id: 5, title: 'Infrastructure Cost Analysis', date: 'Dec 2025', type: 'DevOps' },
    { id: 6, title: 'Q4 Executive Summary', date: 'Dec 2025', type: 'Executive' },
];

const chartData = [
    { month: 'Sep', generated: 12 }, { month: 'Oct', generated: 15 },
    { month: 'Nov', generated: 10 }, { month: 'Dec', generated: 18 },
    { month: 'Jan', generated: 14 }, { month: 'Feb', generated: 8 },
];

export default function ReportsPage() {
    return (
        <div>
            <div className="grid-2 mb-lg">
                <AnimatedCard delay={0}>
                    <div className="card-header"><span className="card-title">Report Generation Trend</span></div>
                    <div className="card-body"><div className="chart-container"><ResponsiveContainer width="100%" height="100%"><BarChart data={chartData}><CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" /><XAxis dataKey="month" tick={{ fontSize: 12 }} /><YAxis tick={{ fontSize: 12 }} /><Tooltip /><Bar dataKey="generated" fill="#c0392b" radius={[4, 4, 0, 0]} name="Reports" /></BarChart></ResponsiveContainer></div></div>
                </AnimatedCard>
                <AnimatedCard delay={0.1}>
                    <div className="card-header"><span className="card-title">Quick Actions</span></div>
                    <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                        <button className="btn btn-primary w-full"><FileText size={16} /> Generate New Report</button>
                        <button className="btn btn-secondary w-full"><Download size={16} /> Export All Reports</button>
                        <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', textAlign: 'center', marginTop: 8 }}>Reports are auto-generated weekly and on-demand.</p>
                    </div>
                </AnimatedCard>
            </div>
            <AnimatedCard delay={0.2}>
                <div className="card-header"><span className="card-title">All Reports</span><span className="badge badge-neutral">{reports.length} reports</span></div>
                <div className="card-body" style={{ padding: 0 }}>
                    <table className="table"><thead><tr><th>Report</th><th>Type</th><th>Date</th><th>Action</th></tr></thead>
                        <tbody>{reports.map(r => <tr key={r.id}><td style={{ fontWeight: 600 }}>{r.title}</td><td><span className="badge badge-neutral">{r.type}</span></td><td style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{r.date}</td><td><button className="btn btn-sm btn-secondary"><Download size={14} /></button></td></tr>)}</tbody></table>
                </div>
            </AnimatedCard>
        </div>
    );
}
