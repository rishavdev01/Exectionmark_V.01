import { useState, useEffect } from 'react';
import AnimatedCard from '../../components/AnimatedCard';
import StatsCard from '../../components/StatsCard';
import { Activity, Cpu, Server, Database, Globe, Clock, AlertTriangle, CheckCircle } from 'lucide-react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    BarChart, Bar, Cell, RadialBarChart, RadialBar, Legend,
    AreaChart, Area
} from 'recharts';
import { devopsAPI } from '../../services/api';

const services = [
    { name: 'API Gateway', cpu: 45, memory: 62, diskIO: 28, dbLatency: 12, apiResponse: 85, uptime: 99.97 },
    { name: 'Auth Service', cpu: 32, memory: 48, diskIO: 15, dbLatency: 8, apiResponse: 42, uptime: 99.99 },
    { name: 'DB Primary', cpu: 68, memory: 92, diskIO: 72, dbLatency: 25, apiResponse: null, uptime: 99.95 },
    { name: 'Cache Redis', cpu: 15, memory: 55, diskIO: 10, dbLatency: 2, apiResponse: null, uptime: 100 },
    { name: 'alpha-backend', cpu: 52, memory: 64, diskIO: 35, dbLatency: 18, apiResponse: 120, uptime: 99.92 },
    { name: 'beta-service', cpu: 78, memory: 85, diskIO: 55, dbLatency: 38, apiResponse: 245, uptime: 98.8 },
];

const uptimeHistory = [
    { week: 'W1', uptime: 99.95 }, { week: 'W2', uptime: 99.97 }, { week: 'W3', uptime: 99.80 },
    { week: 'W4', uptime: 99.99 }, { week: 'W5', uptime: 99.92 }, { week: 'W6', uptime: 99.96 },
];

const slaBreach = [
    { service: 'beta-service', breach: 'Uptime dropped below 99.9% SLA', time: 'Feb 19, 3:00 PM', severity: 'High' },
    { service: 'DB Primary', breach: 'Memory usage exceeded 90% threshold', time: 'Feb 20, 6:20 AM', severity: 'Medium' },
];

const dependencies = [
    { from: 'API Gateway', to: 'Auth Service', status: 'healthy' },
    { from: 'API Gateway', to: 'alpha-backend', status: 'healthy' },
    { from: 'alpha-backend', to: 'DB Primary', status: 'degraded' },
    { from: 'alpha-backend', to: 'Cache Redis', status: 'healthy' },
    { from: 'beta-service', to: 'DB Primary', status: 'unhealthy' },
    { from: 'beta-service', to: 'Cache Redis', status: 'healthy' },
];

const depStatusColor = { healthy: '#10b981', degraded: '#f59e0b', unhealthy: '#ef4444' };

const getUtilColor = (v) => v >= 80 ? '#ef4444' : v >= 60 ? '#f59e0b' : '#10b981';

export default function DevOpsSystemHealth() {
    const [services, setServices] = useState([
        { name: 'API Gateway', cpu: 45, memory: 62, diskIO: 28, dbLatency: 12, apiResponse: 85, uptime: 99.97 },
        { name: 'Auth Service', cpu: 32, memory: 48, diskIO: 15, dbLatency: 8, apiResponse: 42, uptime: 99.99 },
        { name: 'DB Primary', cpu: 68, memory: 92, diskIO: 72, dbLatency: 25, apiResponse: null, uptime: 99.95 },
        { name: 'Cache Redis', cpu: 15, memory: 55, diskIO: 10, dbLatency: 2, apiResponse: null, uptime: 100 },
        { name: 'alpha-backend', cpu: 52, memory: 64, diskIO: 35, dbLatency: 18, apiResponse: 120, uptime: 99.92 },
        { name: 'beta-service', cpu: 78, memory: 85, diskIO: 55, dbLatency: 38, apiResponse: 245, uptime: 98.8 },
    ]);

    useEffect(() => {
        devopsAPI.systemHealth().then(data => {
            if (!data) return;
            // Backend returns flat array of services
            if (Array.isArray(data) && data.length) setServices(data);
            else if (data.services?.length) setServices(data.services);
        }).catch(() => { });
    }, []);

    const avgUptime = services.length ? (services.reduce((a, s) => a + s.uptime, 0) / services.length).toFixed(2) : '100.00';
    const criticalServices = services.filter(s => s.cpu > 70 || s.memory > 80).length;

    return (
        <div>
            <div className="stats-grid mb-lg">
                <StatsCard icon={<Activity size={24} />} value={`${avgUptime}%`} label="Avg Uptime" trend="Healthy" trendDir="up" color="green" delay={0} />
                <StatsCard icon={<Server size={24} />} value={services.length} label="Services Monitored" color="blue" delay={0.08} />
                <StatsCard icon={<AlertTriangle size={24} />} value={criticalServices} label="Critical CPU/Mem" color="red" delay={0.16} />
                <StatsCard icon={<CheckCircle size={24} />} value={slaBreach.length} label="SLA Breaches" color="orange" delay={0.24} />
            </div>

            {/* Resource Usage Table */}
            <AnimatedCard delay={0.3}>
                <div className="card-header"><span className="card-title">Service Resource Usage</span></div>
                <div className="card-body" style={{ padding: 0 }}>
                    <div className="table-wrapper">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Service</th><th>CPU %</th><th>Memory %</th><th>Disk I/O %</th>
                                    <th>DB Latency (ms)</th><th>API Response (ms)</th><th>Uptime %</th>
                                </tr>
                            </thead>
                            <tbody>
                                {services.map((s, i) => (
                                    <tr key={i}>
                                        <td style={{ fontWeight: 700, fontSize: '0.85rem' }}>{s.name}</td>
                                        {['cpu', 'memory', 'diskIO'].map(k => (
                                            <td key={k}>
                                                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                                    <div style={{ width: 50, height: 5, borderRadius: 3, background: '#e5e7eb' }}>
                                                        <div style={{ height: '100%', borderRadius: 3, width: `${s[k]}%`, background: getUtilColor(s[k]), transition: 'width 0.5s' }} />
                                                    </div>
                                                    <span style={{ fontWeight: 700, fontSize: '0.78rem', color: getUtilColor(s[k]) }}>{s[k]}%</span>
                                                </div>
                                            </td>
                                        ))}
                                        <td style={{ fontWeight: 600, fontSize: '0.82rem', color: s.dbLatency > 30 ? '#ef4444' : s.dbLatency > 15 ? '#f59e0b' : '#10b981' }}>
                                            {s.dbLatency}ms
                                        </td>
                                        <td>
                                            {s.apiResponse ? (
                                                <span style={{ fontWeight: 600, fontSize: '0.82rem', color: s.apiResponse > 200 ? '#ef4444' : s.apiResponse > 100 ? '#f59e0b' : '#10b981' }}>
                                                    {s.apiResponse}ms
                                                </span>
                                            ) : <span style={{ color: 'var(--text-tertiary)', fontSize: '0.78rem' }}>N/A</span>}
                                        </td>
                                        <td>
                                            <span style={{
                                                fontWeight: 700, fontSize: '0.82rem',
                                                color: s.uptime >= 99.95 ? '#10b981' : s.uptime >= 99.5 ? '#f59e0b' : '#ef4444'
                                            }}>{s.uptime}%</span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </AnimatedCard>

            <div className="grid-2 mb-lg" style={{ marginTop: 16 }}>
                {/* Uptime History */}
                <AnimatedCard delay={0.4}>
                    <div className="card-header"><span className="card-title">Historical Uptime</span></div>
                    <div className="card-body">
                        <div className="chart-container">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={uptimeHistory}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                    <XAxis dataKey="week" tick={{ fontSize: 12 }} />
                                    <YAxis domain={[99.5, 100]} tick={{ fontSize: 12 }} />
                                    <Tooltip formatter={(v) => `${v}%`} />
                                    <Area type="monotone" dataKey="uptime" stroke="#10b981" fill="#10b98120" strokeWidth={2.5} name="Uptime %" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </AnimatedCard>

                {/* Service Dependency Map */}
                <AnimatedCard delay={0.48}>
                    <div className="card-header"><span className="card-title">Service Dependency Map</span></div>
                    <div className="card-body">
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                            {dependencies.map((d, i) => (
                                <div key={i} style={{
                                    display: 'flex', alignItems: 'center', gap: 8, padding: '8px 12px',
                                    borderRadius: 'var(--radius-sm)', background: 'var(--bg-page)', fontSize: '0.82rem'
                                }}>
                                    <span style={{ fontWeight: 700, minWidth: 100 }}>{d.from}</span>
                                    <span style={{ color: depStatusColor[d.status], fontWeight: 600 }}>→</span>
                                    <span style={{ fontWeight: 600 }}>{d.to}</span>
                                    <span style={{ marginLeft: 'auto' }}>
                                        <span className="badge" style={{
                                            background: d.status === 'healthy' ? '#ecfdf5' : d.status === 'degraded' ? '#fffbeb' : '#fef2f2',
                                            color: depStatusColor[d.status], fontWeight: 600
                                        }}>
                                            {d.status === 'healthy' ? '🟢' : d.status === 'degraded' ? '🟡' : '🔴'} {d.status}
                                        </span>
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </AnimatedCard>
            </div>

            {/* SLA Breaches */}
            {slaBreach.length > 0 && (
                <AnimatedCard delay={0.56}>
                    <div className="card-header">
                        <span className="card-title">SLA Breach Alerts</span>
                        <span className="badge badge-danger">{slaBreach.length}</span>
                    </div>
                    <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                        {slaBreach.map((b, i) => (
                            <div key={i} style={{
                                padding: '12px 16px', borderRadius: 'var(--radius-sm)',
                                background: b.severity === 'High' ? '#fef2f2' : '#fffbeb',
                                borderLeft: `3px solid ${b.severity === 'High' ? '#ef4444' : '#f59e0b'}`,
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <div>
                                        <span style={{ fontWeight: 700, fontSize: '0.85rem' }}>{b.service}</span>
                                        <span style={{ fontSize: '0.82rem', marginLeft: 8, color: 'var(--text-secondary)' }}>— {b.breach}</span>
                                    </div>
                                    <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>{b.time}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </AnimatedCard>
            )}
        </div>
    );
}
