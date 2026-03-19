import React from 'react';
import { ShieldAlert, Crosshair, UserX, AlertOctagon, Check, X } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const fraudTrends = [
  { name: 'Mon', spoofing: 12, velocity: 5, syndicate: 2 },
  { name: 'Tue', spoofing: 15, velocity: 8, syndicate: 3 },
  { name: 'Wed', spoofing: 45, velocity: 22, syndicate: 12 }, // Storm day peak fraud
  { name: 'Thu', spoofing: 18, velocity: 9, syndicate: 4 },
  { name: 'Fri', spoofing: 14, velocity: 6, syndicate: 2 },
  { name: 'Sat', spoofing: 10, velocity: 4, syndicate: 1 },
  { name: 'Sun', spoofing: 9, velocity: 3, syndicate: 0 },
];

const flaggedClaims = [
  { id: 'FR-9912', claimRef: 'CLM-8924', worker: 'Suresh P', trustScore: 42, reason: 'GPS spoofing detected (impossible travel velocity observed)', status: 'Pending Review' },
  { id: 'FR-9911', claimRef: 'CLM-8918', worker: 'Amit S', trustScore: 28, reason: 'Multiple claims from identical device fingerprint across 4 accounts', status: 'Pending Review' },
  { id: 'FR-9910', claimRef: 'CLM-8905', worker: 'Deepak M', trustScore: 12, reason: 'Associated with known fraud syndicate (Node Graph match)', status: 'Pending Review' },
];

const Fraud = () => {
  return (
    <div>
      <div className="page-title">
        Fraud & Adversarial Defense
      </div>

      <div className="grid-cols-4">
        <div className="glass-card stat-card" style={{ borderTop: '3px solid var(--critical)' }}>
          <div className="stat-header">
            <span className="stat-title">GPS Spoofing Prevented</span>
            <div className="stat-icon" style={{ background: 'rgba(232, 67, 147, 0.15)', color: 'var(--critical)' }}>
              <Crosshair size={20} />
            </div>
          </div>
          <div className="stat-value">1,204</div>
          <div className="stat-trend trend-down">Attempts blocked this week</div>
        </div>

        <div className="glass-card stat-card" style={{ borderTop: '3px solid var(--danger)' }}>
          <div className="stat-header">
            <span className="stat-title">Syndicate Rings Detected</span>
            <div className="stat-icon" style={{ background: 'rgba(255, 107, 107, 0.15)', color: 'var(--danger)' }}>
              <UserX size={20} />
            </div>
          </div>
          <div className="stat-value">3</div>
          <div className="stat-trend trend-down">Through device fingerprinting</div>
        </div>

        <div className="glass-card stat-card" style={{ borderTop: '3px solid var(--warning)' }}>
          <div className="stat-header">
            <span className="stat-title">Manual Reviews Pending</span>
            <div className="stat-icon" style={{ background: 'rgba(253, 170, 73, 0.15)', color: 'var(--warning)' }}>
              <AlertOctagon size={20} />
            </div>
          </div>
          <div className="stat-value">42</div>
          <div className="stat-trend trend-up">Requires ops intervention</div>
        </div>

        <div className="glass-card stat-card" style={{ borderTop: '3px solid var(--success)' }}>
          <div className="stat-header">
            <span className="stat-title">Fraud Savings</span>
            <div className="stat-icon" style={{ background: 'rgba(0, 184, 148, 0.15)', color: 'var(--success)' }}>
              <ShieldAlert size={20} />
            </div>
          </div>
          <div className="stat-value">₹245k</div>
          <div className="stat-trend trend-up">Saved from pool leakage</div>
        </div>
      </div>

      <div className="grid-cols-2">
        <div className="glass-card">
          <div className="card-title">Attack Vectors (7 Days)</div>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={fraudTrends} margin={{ top: 20, right: 0, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" vertical={false} />
                <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  cursor={{ fill: 'var(--bg-surface)' }}
                  contentStyle={{ backgroundColor: 'var(--bg-card)', borderColor: 'var(--border-subtle)', borderRadius: '8px', color: 'var(--text-primary)' }}
                />
                <Legend />
                <Bar dataKey="spoofing" name="GPS Spoofing" stackId="a" fill="var(--warning)" radius={[0, 0, 4, 4]} />
                <Bar dataKey="velocity" name="Claim Velocity" stackId="a" fill="var(--danger)" />
                <Bar dataKey="syndicate" name="Syndicate Rings" stackId="a" fill="var(--critical)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-card">
          <div className="card-title">Priority Manual Reviews</div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {flaggedClaims.map(flag => (
              <div key={flag.id} style={{ padding: '16px', background: 'var(--bg-surface)', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
                <div className="flex-between" style={{ marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ color: 'var(--danger)', fontWeight: 600 }}>{flag.id}</span>
                    <span style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>Ref: {flag.claimRef}</span>
                  </div>
                  <span className="status-chip status-warning">{flag.status}</span>
                </div>
                
                <div style={{ display: 'flex', gap: '24px', marginBottom: '16px' }}>
                  <div>
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Worker</div>
                    <div style={{ fontWeight: 500, fontSize: '14px' }}>{flag.worker}</div>
                  </div>
                  <div>
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Trust Score</div>
                    <div style={{ fontWeight: 500, fontSize: '14px', color: flag.trustScore < 30 ? 'var(--critical)' : 'var(--warning)' }}>{flag.trustScore}/100</div>
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>AI Confidence Flag</div>
                    <div style={{ fontWeight: 500, fontSize: '14px' }}>{flag.reason}</div>
                  </div>
                </div>
                
                <div style={{ display: 'flex', gap: '12px' }}>
                  <button style={{ flex: 1, padding: '8px', background: 'var(--bg-dark)', border: '1px solid var(--border-subtle)', borderRadius: '6px', color: 'var(--success)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', cursor: 'pointer' }}>
                    <Check size={16} /> Approve Claim
                  </button>
                  <button style={{ flex: 1, padding: '8px', background: 'rgba(255, 107, 107, 0.1)', border: '1px solid rgba(255, 107, 107, 0.3)', borderRadius: '6px', color: 'var(--danger)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', cursor: 'pointer' }}>
                    <X size={16} /> Reject & Ban
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Fraud;
