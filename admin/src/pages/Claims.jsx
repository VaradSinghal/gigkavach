import React, { useState, useEffect } from 'react';
import { Search, Filter, CheckCircle, XCircle, Clock, ChevronDown, ChevronUp, Shield, Zap, Eye, ThumbsUp, ThumbsDown, Sliders } from 'lucide-react';
import { supabase } from '../supabase';
import SimulationModal from '../components/SimulationModal';

const triggerStats = [
  { name: 'Heavy Rainfall', count: 847, payout: '₹3.2L', color: '#74B9FF', pct: 42 },
  { name: 'Severe AQI', count: 412, payout: '₹1.4L', color: '#A29BFE', pct: 20 },
  { name: 'Flooding', count: 228, payout: '₹1.8L', color: '#FF6B6B', pct: 11 },
  { name: 'Extreme Heat', count: 356, payout: '₹0.9L', color: '#FDAA49', pct: 18 },
  { name: 'Civic Disruption', count: 180, payout: '₹0.7L', color: '#00CEC9', pct: 9 },
];

const Claims = () => {
  const [filter, setFilter] = useState('All');
  const [expandedRow, setExpandedRow] = useState(null);
  const [reviewActions, setReviewActions] = useState({});
  const [claimsData, setClaimsData] = useState([]);
  const [showSimulator, setShowSimulator] = useState(false);

  const handleSimulate = (newClaim) => {
    // Instantly inject the pure-JS simulation into the UI list for reviewers
    setClaimsData(prev => [newClaim, ...prev]);
  };

  useEffect(() => {
    // Initial Fetch
    const fetchClaims = async () => {
      const { data, error } = await supabase
        .from('claims')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(20);
      
      if (data) {
        const mapped = data.map(c => ({
          id: c.claim_id,
          date: new Date(c.created_at).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' }),
          worker: c.worker_id,
          zone: c.zone,
          trigger: c.trigger_label,
          triggerDetail: c.trigger_data,
          amount: c.payout_amount,
          status: c.status === 'approved' ? 'Auto-Approved' : c.status === 'soft_review' ? 'Soft Review' : 'Rejected',
          confidence: c.confidence_score,
          hours: c.inactive_hours,
          time: '3m 12s',
          signals: c.validation_signals || { env: {score:30,pass:true}, loc: {score:25,pass:true}, act:{score:20,pass:true}, time:{score:15,pass:true}, dev:{score:10,pass:true} }
        }));
        setClaimsData(mapped);
      } else {
        // Fallback demo data if unconnected
        setClaimsData([
          { id: 'CLM-100847', date: 'Mar 12, 14:22', worker: 'Ravi Kumar', zone: 'Adyar', trigger: 'Heavy Rainfall', triggerDetail: '48mm in 6hrs', amount: 420, status: 'Auto-Approved', confidence: 92, hours: 6, time: '4m 12s',
            signals: { env: { score: 30, pass: true }, loc: { score: 25, pass: true }, act: { score: 20, pass: true }, time: { score: 15, pass: true }, dev: { score: 2, pass: false } }
          }
        ]);
      }
    };
    fetchClaims();

    // Supabase Realtime Subscription
    const channel = supabase
      .channel('public:claims')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'claims' }, payload => {
        const c = payload.new;
        const mappedClaim = {
          id: c.claim_id,
          date: new Date(c.created_at).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' }),
          worker: c.worker_id,
          zone: c.zone,
          trigger: c.trigger_label,
          triggerDetail: c.trigger_data,
          amount: c.payout_amount,
          status: c.status === 'approved' ? 'Auto-Approved' : c.status === 'soft_review' ? 'Soft Review' : 'Rejected',
          confidence: c.confidence_score,
          hours: c.inactive_hours,
          time: '<1m',
          signals: c.validation_signals || { env: {score:30,pass:true}, loc: {score:25,pass:true}, act:{score:20,pass:true}, time:{score:15,pass:true}, dev:{score:10,pass:true} }
        };
        setClaimsData(prev => [mappedClaim, ...prev]);
      })
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  const handleAction = (claimId, action) => {
    setReviewActions(prev => ({ ...prev, [claimId]: action }));
    // In production: await supabase.from('claims').update({action}).eq('claim_id', claimId);
  };

  const getStatusChip = (claim) => {
    const action = reviewActions[claim.id];
    if (action === 'approved') return <span className="status-chip status-success" style={{ display: 'flex', alignItems: 'center', gap: '6px', width: 'fit-content' }}><CheckCircle size={14} /> Approved</span>;
    if (action === 'rejected') return <span className="status-chip status-danger" style={{ display: 'flex', alignItems: 'center', gap: '6px', width: 'fit-content' }}><XCircle size={14} /> Rejected</span>;

    if (claim.status === 'Auto-Approved') return <span className="status-chip status-success" style={{ display: 'flex', alignItems: 'center', gap: '6px', width: 'fit-content' }}><CheckCircle size={14} /> {claim.time}</span>;
    if (claim.status === 'Rejected') return <span className="status-chip status-danger" style={{ display: 'flex', alignItems: 'center', gap: '6px', width: 'fit-content' }}><XCircle size={14} /> Rejected</span>;
    return <span className="status-chip status-warning" style={{ display: 'flex', alignItems: 'center', gap: '6px', width: 'fit-content' }}><Clock size={14} /> Review</span>;
  };

  return (
    <div>
      <div className="page-title">Claims & Payouts Engine</div>

      <div className="grid-cols-3">
        <div className="glass-card stat-card">
          <div className="stat-header">
            <span className="stat-title">Zero-Touch Rate</span>
            <div className="stat-icon" style={{ background: 'rgba(0, 184, 148, 0.15)', color: 'var(--success)' }}><CheckCircle size={20} /></div>
          </div>
          <div className="stat-value">85.7%</div>
          <div className="stat-trend trend-up">6 of 7 claims auto-processed</div>
        </div>

        <div className="glass-card stat-card">
          <div className="stat-header">
            <span className="stat-title">Loss Ratio</span>
            <div className="stat-icon" style={{ background: 'rgba(108, 92, 231, 0.15)', color: 'var(--primary)' }}><Shield size={20} /></div>
          </div>
          <div className="stat-value">58.2%</div>
          <div className="stat-trend trend-up" style={{ color: 'var(--success)' }}>Target: 55-65% ✓</div>
        </div>

        <div className="glass-card stat-card">
          <div className="stat-header">
            <span className="stat-title">Avg Confidence</span>
            <div className="stat-icon" style={{ background: 'rgba(253, 170, 73, 0.15)', color: 'var(--warning)' }}><Zap size={20} /></div>
          </div>
          <div className="stat-value">79.3</div>
          <div className="stat-trend trend-up">ML fraud detection score</div>
        </div>
      </div>

      <div className="glass-card" style={{ marginBottom: '24px' }}>
        <div className="card-title">Trigger Analytics</div>
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          {triggerStats.map((t, i) => (
            <div key={i} style={{ flex: '1', minWidth: '150px', padding: '12px', background: 'var(--bg-surface)', borderRadius: '12px', borderLeft: `3px solid ${t.color}` }}>
              <div style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '4px' }}>{t.name}</div>
              <div style={{ fontSize: '20px', fontWeight: 700, color: 'var(--text-primary)' }}>{t.count}</div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '4px' }}>
                <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{t.payout} paid</span>
                <span style={{ fontSize: '12px', fontWeight: 600, color: t.color }}>{t.pct}%</span>
              </div>
              <div style={{ marginTop: '6px', height: '4px', background: 'var(--bg-card)', borderRadius: '2px', overflow: 'hidden' }}>
                <div style={{ height: '100%', width: `${t.pct}%`, background: t.color, borderRadius: '2px' }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="glass-card">
        <div className="flex-between" style={{ marginBottom: '24px' }}>
          <div className="card-title" style={{ margin: 0 }}>Live Claims Log</div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button 
              onClick={() => setShowSimulator(true)}
              style={{ padding: '8px 16px', background: 'var(--primary)', border: 'none', color: 'white', borderRadius: '8px', cursor: 'pointer', fontSize: '13px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}
            >
              <Sliders size={16} /> Simulate AI Payload
            </button>
            <div className="header-search" style={{ width: '250px' }}>
              <Search size={16} color="var(--text-secondary)" />
              <input type="text" placeholder="Search claims..." />
            </div>
            <select
              style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)', padding: '8px 12px', borderRadius: '8px', outline: 'none' }}
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            >
              <option value="All">All Claims</option>
              <option value="Auto-Approved">Auto-Approved</option>
              <option value="Soft Review">Soft Review</option>
              <option value="Rejected">Rejected</option>
            </select>
          </div>
        </div>

        {showSimulator && <SimulationModal onClose={() => setShowSimulator(false)} onSimulate={handleSimulate} />}

        <table className="data-table">
          <thead>
            <tr>
              <th></th>
              <th>Claim ID</th>
              <th>Date & Time</th>
              <th>Worker</th>
              <th>Trigger</th>
              <th>Confidence</th>
              <th>Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {claimsData
              .filter(c => filter === 'All' || c.status === filter)
              .map((claim, i) => (
              <React.Fragment key={i}>
                <tr onClick={() => setExpandedRow(expandedRow === i ? null : i)} style={{ cursor: 'pointer' }}>
                  <td>{expandedRow === i ? <ChevronUp size={16} color="var(--text-muted)" /> : <ChevronDown size={16} color="var(--text-muted)" />}</td>
                  <td style={{ color: 'var(--primary)', fontWeight: 500 }}>{claim.id}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>{claim.date}</td>
                  <td>
                    <div>{claim.worker}</div>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{claim.zone}</div>
                  </td>
                  <td>
                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'var(--bg-surface)', padding: '4px 8px', borderRadius: '6px', fontSize: '12px' }}>
                      {claim.trigger}
                    </span>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>{claim.triggerDetail}</div>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{
                        width: '36px', height: '36px', borderRadius: '50%',
                        background: `conic-gradient(${claim.confidence >= 80 ? 'var(--success)' : claim.confidence >= 50 ? 'var(--warning)' : 'var(--danger)'} ${claim.confidence}%, var(--bg-surface) 0)`,
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                      }}>
                        <div style={{ width: '28px', height: '28px', borderRadius: '50%', background: 'var(--bg-card)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '11px', fontWeight: 700, color: 'var(--text-primary)' }}>
                          {claim.confidence}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td style={{ fontWeight: 600 }}>₹{claim.amount}</td>
                  <td>{getStatusChip(claim)}</td>
                </tr>
                {expandedRow === i && (
                  <tr>
                    <td colSpan="8" style={{ padding: '0 20px 20px' }}>
                      <div style={{ background: 'var(--bg-surface)', borderRadius: '12px', padding: '16px' }}>
                        <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}>
                          Fraud Validation Breakdown — {claim.confidence}/100
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '8px', marginBottom: '16px' }}>
                          {[
                            { label: 'Environmental', key: 'env', max: 30 },
                            { label: 'Location', key: 'loc', max: 25 },
                            { label: 'Activity', key: 'act', max: 20 },
                            { label: 'Timing', key: 'time', max: 15 },
                            { label: 'Device', key: 'dev', max: 10 },
                          ].map((signal, j) => {
                            const s = claim.signals[signal.key] || { score: 0, pass: false };
                            return (
                              <div key={j} style={{ padding: '10px', background: 'var(--bg-card)', borderRadius: '8px', textAlign: 'center' }}>
                                <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '4px' }}>{signal.label}</div>
                                <div style={{ fontSize: '18px', fontWeight: 700, color: s.pass ? 'var(--success)' : 'var(--danger)' }}>
                                  {s.score}/{signal.max}
                                </div>
                                <div style={{ fontSize: '10px', color: s.pass ? 'var(--success)' : 'var(--danger)', marginTop: '2px' }}>
                                  {s.pass ? '✓ Passed' : '✗ Failed'}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                            Payout: {claim.hours}hrs × ₹70/hr × 70% = <strong>₹{claim.amount}</strong>
                          </div>
                          {claim.status === 'Soft Review' && !reviewActions[claim.id] && (
                            <div style={{ display: 'flex', gap: '8px' }}>
                              <button
                                onClick={(e) => { e.stopPropagation(); handleAction(claim.id, 'approved'); }}
                                style={{ padding: '6px 16px', background: 'var(--success)', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', fontWeight: 600 }}
                              >
                                <ThumbsUp size={14} /> Approve
                              </button>
                              <button
                                onClick={(e) => { e.stopPropagation(); handleAction(claim.id, 'rejected'); }}
                                style={{ padding: '6px 16px', background: 'var(--danger)', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', fontWeight: 600 }}
                              >
                                <ThumbsDown size={14} /> Reject
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Claims;
