import React from 'react';
import { Shield, TrendingUp, AlertTriangle, Users, Activity, Banknote } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend } from 'recharts';

// Mock Data
const revenueData = [
  { day: 'Mon', premium: 42000, payouts: 12000 },
  { day: 'Tue', premium: 43500, payouts: 15000 },
  { day: 'Wed', premium: 45000, payouts: 38000 }, // Rain event
  { day: 'Thu', premium: 46200, payouts: 18000 },
  { day: 'Fri', premium: 48000, payouts: 14000 },
  { day: 'Sat', premium: 51000, payouts: 22000 },
  { day: 'Sun', premium: 53500, payouts: 19000 },
];

const flagsData = [
  { id: 'CLM-8924', worker: 'Ravi Kumar', type: 'Spoofed Mock Location', status: 'High Risk', score: 12 },
  { id: 'CLM-8921', worker: 'Suresh P', type: 'Unusual Claim Velocity', status: 'Medium Risk', score: 45 },
  { id: 'CLM-8918', worker: 'Amit S', type: 'Device Fingerprint Mismatch', status: 'High Risk', score: 18 },
  { id: 'CLM-8905', worker: 'Deepak M', type: 'Syndicate Pattern Detect', status: 'Critical', score: 8 },
];

const Dashboard = () => {
  return (
    <div>
      <div className="page-title">
        Command Center
        <div style={{ display: 'flex', gap: '12px' }}>
          <button style={{ padding: '8px 16px', background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)', borderRadius: '8px', cursor: 'pointer', fontSize: '14px', fontWeight: 500 }}>
            Export Report
          </button>
          <button style={{ padding: '8px 16px', background: 'var(--primary)', border: 'none', color: 'white', borderRadius: '8px', cursor: 'pointer', fontSize: '14px', fontWeight: 500, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Activity size={16} /> Live Status
          </button>
        </div>
      </div>

      <div className="grid-cols-4">
        <div className="glass-card stat-card">
          <div className="stat-header">
            <span className="stat-title">Active Policies</span>
            <div className="stat-icon" style={{ background: 'rgba(108, 92, 231, 0.15)', color: 'var(--primary)' }}>
              <Shield size={20} />
            </div>
          </div>
          <div className="stat-value">124,592</div>
          <div className="stat-trend trend-up"><TrendingUp size={14} /> +12.5% this week</div>
        </div>
        
        <div className="glass-card stat-card">
          <div className="stat-header">
            <span className="stat-title">Premium Pool</span>
            <div className="stat-icon" style={{ background: 'rgba(0, 184, 148, 0.15)', color: 'var(--success)' }}>
              <Banknote size={20} />
            </div>
          </div>
          <div className="stat-value">₹8.4M</div>
          <div className="stat-trend trend-up"><TrendingUp size={14} /> +4.2% today</div>
        </div>

        <div className="glass-card stat-card">
          <div className="stat-header">
            <span className="stat-title">Claims Processing</span>
            <div className="stat-icon" style={{ background: 'rgba(253, 170, 73, 0.15)', color: 'var(--warning)' }}>
              <Activity size={20} />
            </div>
          </div>
          <div className="stat-value">1.2s avg</div>
          <div className="stat-trend trend-down" style={{ color: 'var(--success)' }}><TrendingUp size={14} style={{ transform: 'scaleY(-1)' }} /> -0.3s latency</div>
        </div>

        <div className="glass-card stat-card">
          <div className="stat-header">
            <span className="stat-title">Fraud Flags</span>
            <div className="stat-icon" style={{ background: 'rgba(255, 107, 107, 0.15)', color: 'var(--danger)' }}>
              <AlertTriangle size={20} />
            </div>
          </div>
          <div className="stat-value">342</div>
          <div className="stat-trend trend-down"><TrendingUp size={14} /> +18 anomalies</div>
        </div>
      </div>

      <div className="grid-cols-2">
        <div className="glass-card">
          <div className="card-title">Liquidity vs Payouts (7 Days)</div>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={revenueData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorPremium" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--primary)" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorPayout" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--danger)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--danger)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="day" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `₹${value/1000}k`} />
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" vertical={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--bg-card)', borderColor: 'var(--border-subtle)', borderRadius: '8px', color: 'var(--text-primary)' }}
                  itemStyle={{ color: 'var(--text-primary)' }}
                />
                <Legend iconType="circle" />
                <Area type="monotone" name="Collected Premiums" dataKey="premium" stroke="var(--primary)" strokeWidth={3} fillOpacity={1} fill="url(#colorPremium)" />
                <Area type="monotone" name="Claim Payouts" dataKey="payouts" stroke="var(--danger)" strokeWidth={3} fillOpacity={1} fill="url(#colorPayout)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-card">
          <div className="flex-between" style={{ marginBottom: '20px' }}>
            <div className="card-title" style={{ margin: 0 }}>Active Fraud Alerts</div>
            <a href="/fraud" style={{ color: 'var(--primary)', fontSize: '13px', textDecoration: 'none', fontWeight: 600 }}>View All</a>
          </div>
          
          <table className="data-table">
            <thead>
              <tr>
                <th>Claim ID</th>
                <th>Worker</th>
                <th>Flag Type</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {flagsData.map((flag, i) => (
                <tr key={i}>
                  <td style={{ color: 'var(--primary)', fontWeight: 500 }}>{flag.id}</td>
                  <td>{flag.worker}</td>
                  <td>{flag.type}</td>
                  <td>
                    <span className={`status-chip ${flag.status === 'Critical' ? 'status-danger' : flag.status === 'High Risk' ? 'status-warning' : 'status-primary'}`}>
                      {flag.score}/100
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
