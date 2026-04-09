import React, { useState, useEffect } from 'react';
import { 
  Play, 
  RotateCcw, 
  ShieldCheck, 
  Zap, 
  AlertTriangle, 
  MapPin, 
  CloudRain, 
  Smartphone, 
  ArrowRight,
  ShieldAlert,
  Fingerprint,
  Activity
} from 'lucide-react';
import { supabase } from '../supabaseClient';

const SimulationSuite = () => {
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState(null);
  const [step, setStep] = useState(0); // 0: Ready, 1: Premium, 2: Event, 3: Claim, 4: Result

  useEffect(() => {
    fetchScenarios();
  }, []);

  const fetchScenarios = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/simulation/scenarios');
      const data = await res.json();
      setScenarios(data);
      if (data.length > 0) setSelectedScenario(data[0]);
    } catch (err) {
      console.error("Failed to fetch scenarios:", err);
    }
  };

  const runSimulation = async () => {
    if (!selectedScenario) return;
    setIsRunning(true);
    setResults(null);
    setStep(1);

    // Artificial delays for "visual demonstration" sequence
    setTimeout(() => setStep(2), 1500); 
    setTimeout(() => setStep(3), 3000);

    try {
      const res = await fetch(`http://localhost:8000/api/v1/simulation/run/${selectedScenario.id}`, {
        method: 'POST'
      });
      const data = await res.json();
      
      setTimeout(() => {
        setResults(data);
        setStep(4);
        setIsRunning(false);
      }, 4500);
    } catch (err) {
      console.error("Simulation error:", err);
      setIsRunning(false);
    }
  };

  const resetAll = () => {
    setStep(0);
    setResults(null);
    setIsRunning(false);
  };

  return (
    <div className="simulation-container">
      <div className="flex-between header-section">
        <div>
          <h1 className="page-title">Digital Twin & Simulation Mission Control</h1>
          <p className="text-muted">Live stress-testing of AI Fraud and Parametric Payout engines.</p>
        </div>
        <div className="flex-gap">
          <button className="secondary-btn" onClick={resetAll} disabled={isRunning}>
            <RotateCcw size={18} /> Reset Suite
          </button>
          <button className="primary-btn" onClick={runSimulation} disabled={isRunning}>
            <Play size={18} fill="currentColor" /> Run Full Simulation
          </button>
        </div>
      </div>

      <div className="grid-main">
        {/* Left Sidebar: Scenarios */}
        <div className="scenario-selector glass-card">
          <h3 className="card-title">Test Scenarios</h3>
          <div className="scenario-list">
            {scenarios.map((s) => (
              <div 
                key={s.id} 
                className={`scenario-item ${selectedScenario?.id === s.id ? 'active' : ''}`}
                onClick={() => !isRunning && setSelectedScenario(s)}
              >
                <div className="scenario-info">
                  <div className="scenario-name">{s.name}</div>
                  <div className="scenario-type">{s.fraud_type.replace('_', ' ')}</div>
                </div>
                {s.expected_outcome === 'auto_approve' ? 
                  <ShieldCheck size={16} color="var(--success)" /> : 
                  <ShieldAlert size={16} color="var(--danger)" />
                }
              </div>
            ))}
          </div>

          <div className="worker-profile mt-24">
            <h4 className="section-subtitle">Worker Profile Details</h4>
            {selectedScenario && (
              <div className="details-grid">
                <div className="detail-item">
                  <span className="label">ID:</span>
                  <span className="value">{selectedScenario.profile.worker_id}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Zone:</span>
                  <span className="value">{selectedScenario.profile.zone}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Trust:</span>
                  <span className="value">{(selectedScenario.profile.trust_score * 100).toFixed(0)}%</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Center: The Simulation Canvas */}
        <div className="simulation-canvas glass-card">
          <div className="canvas-header flex-between">
            <div className="flex-gap">
              <div className={`step-dot ${step >= 1 ? 'active' : ''}`}></div>
              <div className={`step-line ${step >= 2 ? 'active' : ''}`}></div>
              <div className={`step-dot ${step >= 2 ? 'active' : ''}`}></div>
              <div className={`step-line ${step >= 3 ? 'active' : ''}`}></div>
              <div className={`step-dot ${step >= 3 ? 'active' : ''}`}></div>
              <div className={`step-line ${step >= 4 ? 'active' : ''}`}></div>
              <div className={`step-dot ${step >= 4 ? 'active' : ''}`}></div>
            </div>
            <span className="status-label">{isRunning ? 'Running Simulation...' : 'Ready'}</span>
          </div>

          <div className="canvas-body">
            {/* Step 1: Premium Quote */}
            <div className={`stage-card ${step === 1 ? 'focused' : step > 1 ? 'completed' : 'pending'}`}>
              <div className="stage-icon"><Zap size={24} /></div>
              <div className="stage-content">
                <h4>Dynamic Premium Calc</h4>
                {step >= 1 && (
                  <div className="stage-data">
                    <p>Analyzing risk for {selectedScenario.profile.zone}...</p>
                    {results && <div className="result-val highlight">Premium: ₹{results.premium.weekly_premium}</div>}
                  </div>
                )}
              </div>
            </div>

            {/* Step 2: Parametric Event */}
            <div className={`stage-card ${step === 2 ? 'focused' : step > 2 ? 'completed' : 'pending'}`}>
              <div className="stage-icon"><CloudRain size={24} /></div>
              <div className="stage-content">
                <h4>Parametric Disruption</h4>
                {step >= 2 && (
                  <div className="stage-data">
                    <p>Trigger: {results?.trigger.label || 'Detecting...'}</p>
                    <div className="progress-mini"><div className="progress-bar active" style={{width: '70%'}}></div></div>
                  </div>
                )}
              </div>
            </div>

            {/* Step 3: Mobile App Submit */}
            <div className={`stage-card ${step === 3 ? 'focused' : step > 3 ? 'completed' : 'pending'}`}>
              <div className="stage-icon"><Smartphone size={24} /></div>
              <div className="stage-content">
                <h4>Mobile App Workflow</h4>
                <div className="mobile-view-mock">
                  <div className="mobile-inner">
                    <div className="mobile-header">GigKavach App</div>
                    {step === 3 && <div className="mobile-anim">Triggering Claim...</div>}
                    {step > 3 && <div className="mobile-success">Claim Submitted</div>}
                  </div>
                </div>
              </div>
            </div>

            {/* Step 4: AI Decision */}
            <div className={`stage-card ${step === 4 ? 'focused' : 'pending'}`}>
              <div className="stage-icon"><ShieldCheck size={24} /></div>
              <div className="stage-content">
                <h4>AI Fraud Decisions</h4>
                {results && (
                  <div className="decision-box">
                    <div className={`outcome ${results.claim.action}`}>
                      {results.claim.action_label}
                    </div>
                    <div className="score-meter">
                      Confidence: {results.claim.confidence_score}%
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Right: Detailed Fraud Analysis */}
        <div className="fraud-analysis glass-card">
          <h3 className="card-title">Multi-Signal Intelligence</h3>
          {results ? (
            <div className="signals-stack">
              {Object.entries(results.claim.validation_signals).map(([key, signal]) => (
                <div key={key} className="signal-row">
                  <div className="flex-between">
                    <span className="signal-key">{key.toUpperCase()}</span>
                    <span className={`signal-status ${signal.passed ? 'pass' : 'fail'}`}>
                      {signal.passed ? 'Pass' : 'Failed'}
                    </span>
                  </div>
                  <div className="signal-detail">{signal.detail}</div>
                </div>
              ))}
              <div className="final-verdict-box mt-24">
                <h4>System Reasoning</h4>
                <p className="reasoning-text">"{results.claim.rejection_reason || results.claim.review_reason || 'Patterns match expected worker behavior profiles.'}"</p>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <Fingerprint size={48} color="var(--border)" />
              <p>Execute simulation to see real-time fraud signal decomposition.</p>
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .simulation-container {
          padding: 24px;
        }
        .header-section { margin-bottom: 32px; }
        .grid-main {
          display: grid;
          grid-template-columns: 300px 1fr 350px;
          gap: 24px;
          height: calc(100vh - 180px);
        }
        .scenario-list { display: flex; flex-direction: column; gap: 12px; margin-top: 16px; }
        .scenario-item {
          padding: 12px;
          border: 1px solid var(--border);
          border-radius: 12px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          cursor: pointer;
          transition: 0.2s;
        }
        .scenario-item:hover { border-color: var(--primary); }
        .scenario-item.active { 
          background: var(--bg-surface);
          border-color: var(--primary);
          box-shadow: 0 0 0 1px var(--primary);
        }
        .scenario-name { font-weight: 600; font-size: 14px; }
        .scenario-type { font-size: 11px; color: var(--text-muted); text-transform: uppercase; }
        
        .stage-card {
          background: rgba(255,255,255,0.03);
          border: 1px solid var(--border);
          border-radius: 16px;
          padding: 20px;
          margin-bottom: 16px;
          display: flex;
          gap: 20px;
          align-items: center;
          transition: 0.4s;
        }
        .stage-card.focused { border-color: var(--primary); box-shadow: 0 0 20px rgba(71, 107, 255, 0.2); transform: scale(1.02); }
        .stage-card.completed { border-color: var(--success); opacity: 0.8; }
        .result-val { font-size: 18px; font-weight: 700; color: var(--primary); }
        
        .mobile-view-mock {
          width: 140px;
          height: 80px;
          background: #000;
          border-radius: 12px;
          padding: 4px;
          border: 2px solid #333;
        }
        .mobile-inner {
          background: white;
          height: 100%;
          border-radius: 8px;
          color: black;
          font-size: 9px;
          padding: 4px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        .mobile-header { font-weight: bold; margin-bottom: 4px; border-bottom: 1px solid #eee; width: 100%; text-align: center; }
        
        .signal-row {
          padding: 12px 0;
          border-bottom: 1px solid var(--border);
        }
        .signal-key { font-size: 12px; font-weight: 700; }
        .signal-status.pass { color: var(--success); font-weight: bold; }
        .signal-status.fail { color: var(--danger); font-weight: bold; }
        .signal-detail { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
        
        .outcome {
          padding: 8px 16px;
          border-radius: 20px;
          font-weight: 700;
          display: inline-block;
          margin-top: 12px;
        }
        .outcome.paid, .outcome.auto_approved { background: rgba(0, 200, 83, 0.1); color: var(--success); }
        .outcome.rejected { background: rgba(255, 23, 68, 0.1); color: var(--danger); }
        .outcome.soft_review { background: rgba(255, 171, 0, 0.1); color: var(--warning); }
      `}</style>
    </div>
  );
};

export default SimulationSuite;
