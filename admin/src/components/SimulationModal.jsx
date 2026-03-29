import React, { useState } from 'react';
import { Play, X, Sliders, Zap, CheckCircle, ShieldAlert } from 'lucide-react';

const SimulationModal = ({ onClose, onSimulate }) => {
  const [params, setParams] = useState({
    workerId: 'Ravi_K_72',
    triggerType: 'Heavy Rainfall',
    triggerData: '65mm/6hrs',
    inactiveHours: 6,
    hourlyRate: 70,
    coverage: 70,
    
    // AI Variables
    envVerified: true,
    gpsConsistent: true,
    activityCoherent: true,
    timingCorrelated: true,
    deviceClean: true
  });

  const [processing, setProcessing] = useState(false);
  const [step, setStep] = useState(0);

  const runSimulation = () => {
    setProcessing(true);
    
    // Animate the ML evaluation steps for the demo
    const steps = [
      () => setStep(1), // Parsing API
      () => setStep(2), // Feature Matrix
      () => setStep(3), // Model Inference
      () => {
        setProcessing(false);
        setStep(0);
        
        // Execute pure JS conversion of Python ML logic
        const envScore = params.envVerified ? 30 : 10;
        const locScore = params.gpsConsistent ? 25 : 5;
        const actScore = params.activityCoherent ? 20 : 5;
        const timeScore = params.timingCorrelated ? 15 : 5;
        const devScore = params.deviceClean ? 10 : 2;
        
        const confidence = envScore + locScore + actScore + timeScore + devScore;
        const amount = Math.round(params.inactiveHours * params.hourlyRate * (params.coverage / 100));

        const claim = {
          id: `CLM-${Math.floor(Math.random() * 900000) + 100000}`,
          date: new Date().toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' }),
          worker: params.workerId,
          zone: 'T. Nagar (Simulated)',
          trigger: params.triggerType,
          triggerDetail: params.triggerData,
          amount: amount,
          status: confidence >= 80 ? 'approved' : confidence >= 50 ? 'soft_review' : 'rejected',
          confidence: confidence,
          hours: params.inactiveHours,
          time: '1.2s (Simulated)',
          signals: {
            env: { score: envScore, pass: params.envVerified },
            loc: { score: locScore, pass: params.gpsConsistent },
            act: { score: actScore, pass: params.activityCoherent },
            time: { score: timeScore, pass: params.timingCorrelated },
            dev: { score: devScore, pass: params.deviceClean },
          }
        };

        onSimulate(claim);
        onClose();
      }
    ];

    setTimeout(steps[0], 500);
    setTimeout(steps[1], 1200);
    setTimeout(steps[2], 2000);
    setTimeout(steps[3], 2800);
  };

  const handlePrebuilt = (type) => {
    if (type === 'clean') {
      setParams({ ...params, triggerType: 'Flooding', triggerData: 'IMD Alert Active', envVerified: true, gpsConsistent: true, activityCoherent: true, timingCorrelated: true, deviceClean: true });
    } else if (type === 'suspicious') {
      setParams({ ...params, triggerType: 'Heavy Rainfall', triggerData: '40mm/6hrs', envVerified: true, gpsConsistent: false, activityCoherent: true, timingCorrelated: false, deviceClean: true });
    } else if (type === 'fraud') {
      setParams({ ...params, triggerType: 'Severe AQI', triggerData: 'AQI 450 (Spoofed)', envVerified: false, gpsConsistent: false, activityCoherent: false, timingCorrelated: false, deviceClean: false });
    }
  };

  return (
    <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(5px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999 }}>
      <div style={{ width: '600px', backgroundColor: 'var(--bg-card)', borderRadius: '16px', border: '1px solid var(--border-subtle)', overflow: 'hidden', display: 'flex', flexDirection: 'column', maxHeight: '90vh' }}>
        
        {/* Header */}
        <div style={{ padding: '20px', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'var(--bg-surface)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ backgroundColor: 'rgba(108, 92, 231, 0.15)', padding: '8px', borderRadius: '8px' }}>
              <Sliders size={20} color="var(--primary)" />
            </div>
            <div>
              <div style={{ fontSize: '18px', fontWeight: 600, color: 'var(--text-primary)' }}>AI Processing Simulator</div>
              <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Inject custom parameters to test the Zero-Touch AI without a Python backend.</div>
            </div>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}><X size={24} /></button>
        </div>

        {/* Content */}
        <div style={{ padding: '24px', overflowY: 'auto' }}>
          
          {/* Quick Presets */}
          <div style={{ marginBottom: '24px' }}>
            <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '10px' }}>Load Demo Scenario:</div>
            <div style={{ display: 'flex', gap: '12px' }}>
              <button onClick={() => handlePrebuilt('clean')} style={{ flex: 1, padding: '10px', background: 'rgba(0, 184, 148, 0.1)', border: '1px solid var(--success)', borderRadius: '8px', color: 'var(--success)', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                <CheckCircle size={16} /> Clean Claim
              </button>
              <button onClick={() => handlePrebuilt('suspicious')} style={{ flex: 1, padding: '10px', background: 'rgba(253, 170, 73, 0.1)', border: '1px solid var(--warning)', borderRadius: '8px', color: 'var(--warning)', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                <ShieldAlert size={16} /> Edge Case
              </button>
              <button onClick={() => handlePrebuilt('fraud')} style={{ flex: 1, padding: '10px', background: 'rgba(255, 107, 107, 0.1)', border: '1px solid var(--danger)', borderRadius: '8px', color: 'var(--danger)', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                <XCircle size={16} /> Fraud Ring
              </button>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            {/* Input Variables */}
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '8px' }}>Event Variables</div>
              
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '4px' }}>Trigger Type</label>
                <input value={params.triggerType} onChange={(e) => setParams({...params, triggerType: e.target.value})} style={{ width: '100%', padding: '8px 12px', borderRadius: '8px', background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)' }} />
              </div>
              
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '4px' }}>Observed Data</label>
                <input value={params.triggerData} onChange={(e) => setParams({...params, triggerData: e.target.value})} style={{ width: '100%', padding: '8px 12px', borderRadius: '8px', background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)' }} />
              </div>
            </div>

            {/* AI Flags */}
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '8px' }}>AI Validation Signals</div>
              
              {[
                { key: 'envVerified', label: 'Environmental APIs match claim' },
                { key: 'gpsConsistent', label: 'GPS stays strictly in targeted zone' },
                { key: 'activityCoherent', label: 'Prior app activity is coherent' },
                { key: 'timingCorrelated', label: 'Inactivity timing correlates to API' },
                { key: 'deviceClean', label: 'No VPN/Mock locations detected' }
              ].map((flag) => (
                <div key={flag.key} style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                  <input
                    type="checkbox"
                    id={flag.key}
                    checked={params[flag.key]}
                    onChange={(e) => setParams({...params, [flag.key]: e.target.checked})}
                    style={{ width: '16px', height: '16px', accentColor: 'var(--primary)', cursor: 'pointer' }}
                  />
                  <label htmlFor={flag.key} style={{ marginLeft: '8px', fontSize: '13px', color: 'var(--text-secondary)', cursor: 'pointer' }}>{flag.label}</label>
                </div>
              ))}
            </div>
          </div>

          {/* Processing Visuals */}
          {processing && (
            <div style={{ marginTop: '24px', padding: '16px', background: 'var(--bg-surface)', borderRadius: '12px', border: '1px solid var(--primary)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                <Zap size={18} color="var(--primary)" className="animate-pulse" />
                <span style={{ fontSize: '14px', fontWeight: 600, color: 'var(--primary)' }}>Simulating ML Validator...</span>
              </div>
              <div style={{ fontSize: '12px', color: 'var(--text-secondary)', fontFamily: 'monospace' }}>
                <div style={{ color: step >= 1 ? 'var(--text-primary)' : 'var(--text-muted)' }}>[1] Fetching Mock External API Data... {step >= 2 && 'OK'}</div>
                <div style={{ color: step >= 2 ? 'var(--text-primary)' : 'var(--text-muted)' }}>[2] Generating Feature Matrix [11x1]... {step >= 3 && 'OK'}</div>
                <div style={{ color: step >= 3 ? 'var(--text-primary)' : 'var(--text-muted)' }}>[3] Executing Random Forest Classification...</div>
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div style={{ padding: '20px', backgroundColor: 'var(--bg-surface)', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
          <button onClick={onClose} style={{ padding: '10px 16px', borderRadius: '8px', background: 'transparent', color: 'var(--text-primary)', border: '1px solid var(--border-subtle)', fontWeight: 600, cursor: 'pointer' }}>Cancel</button>
          <button onClick={runSimulation} disabled={processing} style={{ padding: '10px 20px', borderRadius: '8px', background: 'var(--primary)', color: 'white', border: 'none', fontWeight: 600, cursor: processing ? 'not-allowed' : 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Play size={16} /> Run Local ML Simulation
          </button>
        </div>
        
      </div>
    </div>
  );
};

export default SimulationModal;
