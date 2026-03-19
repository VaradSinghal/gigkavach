import React, { useState } from 'react';
import { Search, Filter, CheckCircle, XCircle, Clock } from 'lucide-react';

const claimsData = [
  { id: 'CLM-8925', date: 'Oct 24, 14:30', worker: 'Ravi Kumar', trigger: 'Heavy Rainfall Zone A', amount: '₹420', status: 'Paid Automatically', time: '1.2s' },
  { id: 'CLM-8924', date: 'Oct 24, 14:15', worker: 'Suresh P', trigger: 'Severe AQI Level', amount: '₹350', status: 'Flagged for Review', time: '-' },
  { id: 'CLM-8923', date: 'Oct 24, 13:50', worker: 'Amit Sharma', trigger: 'Heavy Rainfall Zone B', amount: '₹420', status: 'Paid Automatically', time: '0.8s' },
  { id: 'CLM-8922', date: 'Oct 24, 12:10', worker: 'Karthik S', trigger: 'Flooding Alert', amount: '₹800', status: 'Paid Automatically', time: '1.5s' },
  { id: 'CLM-8921', date: 'Oct 24, 11:45', worker: 'Deepak M', trigger: 'Flooding Alert', amount: '₹800', status: 'Denied', time: '-' },
  { id: 'CLM-8920', date: 'Oct 24, 09:30', worker: 'Vijay R', trigger: 'Heatwave', amount: '₹250', status: 'Paid Automatically', time: '1.1s' },
];

const Claims = () => {
  const [filter, setFilter] = useState('All');

  return (
    <div>
      <div className="page-title">
        Claims & Payouts Engine
      </div>

      <div className="grid-cols-3">
        <div className="glass-card stat-card">
          <div className="stat-header">
            <span className="stat-title">Zero-Touch Payouts</span>
            <div className="stat-icon" style={{ background: 'rgba(0, 184, 148, 0.15)', color: 'var(--success)' }}>
              <CheckCircle size={20} />
            </div>
          </div>
          <div className="stat-value">94.2%</div>
          <div className="stat-trend trend-up">Processing without human intervention</div>
        </div>

        <div className="glass-card stat-card">
          <div className="stat-header">
            <span className="stat-title">Avg Payout Time</span>
            <div className="stat-icon" style={{ background: 'rgba(108, 92, 231, 0.15)', color: 'var(--primary)' }}>
              <Clock size={20} />
            </div>
          </div>
          <div className="stat-value">1.1s</div>
          <div className="stat-trend trend-up">From trigger to wallet deposit</div>
        </div>

        <div className="glass-card stat-card">
          <div className="stat-header">
            <span className="stat-title">Flagged for Review</span>
            <div className="stat-icon" style={{ background: 'rgba(253, 170, 73, 0.15)', color: 'var(--warning)' }}>
              <Filter size={20} />
            </div>
          </div>
          <div className="stat-value">5.8%</div>
          <div className="stat-trend trend-down">Routed to fraud team</div>
        </div>
      </div>

      <div className="glass-card">
        <div className="flex-between" style={{ marginBottom: '24px' }}>
          <div className="card-title" style={{ margin: 0 }}>Recent Claims Log</div>
          
          <div style={{ display: 'flex', gap: '12px' }}>
            <div className="header-search" style={{ width: '250px' }}>
              <Search size={16} color="var(--text-secondary)" />
              <input type="text" placeholder="Search claims..." />
            </div>
            <select 
              style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)', padding: '8px 12px', borderRadius: '8px', outline: 'none' }}
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            >
              <option>All Claims</option>
              <option>Paid Automatically</option>
              <option>Flagged</option>
              <option>Denied</option>
            </select>
          </div>
        </div>

        <table className="data-table">
          <thead>
            <tr>
              <th>Claim ID</th>
              <th>Date & Time</th>
              <th>Worker</th>
              <th>Parametric Trigger</th>
              <th>Amount</th>
              <th>Latency / Status</th>
            </tr>
          </thead>
          <tbody>
            {claimsData.map((claim, i) => (
              <tr key={i}>
                <td style={{ color: 'var(--primary)', fontWeight: 500 }}>{claim.id}</td>
                <td style={{ color: 'var(--text-secondary)' }}>{claim.date}</td>
                <td>{claim.worker}</td>
                <td>
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'var(--bg-surface)', padding: '4px 8px', borderRadius: '6px', fontSize: '12px' }}>
                    {claim.trigger}
                  </span>
                </td>
                <td style={{ fontWeight: 600 }}>{claim.amount}</td>
                <td>
                  {claim.status === 'Paid Automatically' ? (
                    <span className="status-chip status-success" style={{ display: 'flex', alignItems: 'center', gap: '6px', width: 'fit-content' }}>
                      <CheckCircle size={14} /> {claim.time}
                    </span>
                  ) : claim.status === 'Denied' ? (
                    <span className="status-chip status-danger" style={{ display: 'flex', alignItems: 'center', gap: '6px', width: 'fit-content' }}>
                      <XCircle size={14} /> Denied
                    </span>
                  ) : (
                    <span className="status-chip status-warning" style={{ display: 'flex', alignItems: 'center', gap: '6px', width: 'fit-content' }}>
                      <Clock size={14} /> Flagged
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Claims;
