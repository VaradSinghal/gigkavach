import React from 'react';
import { Map as MapIcon, CloudRain, AlertTriangle, Wind, Sun, Layers } from 'lucide-react';

const activeZones = [
  { id: 'Z-101', name: 'Velachery South', riskLevel: 82, status: 'Critical', activeTriggers: ['Heavy Rainfall', 'Flooding Alert'] },
  { id: 'Z-102', name: 'T. Nagar Central', riskLevel: 65, status: 'High', activeTriggers: ['Severe AQI'] },
  { id: 'Z-103', name: 'Adyar North', riskLevel: 45, status: 'Moderate', activeTriggers: ['Heatwave Warning'] },
  { id: 'Z-104', name: 'Guindy Industrial', riskLevel: 15, status: 'Low', activeTriggers: [] },
  { id: 'Z-105', name: 'OMR IT Corridor', riskLevel: 94, status: 'Critical', activeTriggers: ['Civic Protest', 'Route Blocks'] },
];

const RiskMap = () => {
  return (
    <div>
      <div className="page-title">
        Live City Risk Map
        <span className="status-chip status-success" style={{ fontSize: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--success)', display: 'inline-block' }}></span>
          Live Sync Active
        </span>
      </div>

      <div style={{ display: 'flex', gap: '24px', height: 'calc(100vh - 180px)' }}>
        {/* Map Area */}
        <div className="glass-card" style={{ flex: 1, padding: 0, overflow: 'hidden', position: 'relative' }}>
          {/* Placeholder for Mapbox/Leaflet */}
          <div style={{ position: 'absolute', inset: 0, background: '#11151c', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <MapIcon size={48} color="var(--primary)" style={{ opacity: 0.5, marginBottom: '16px' }} />
            <div style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>Mapbox Integration Layer</div>
            <div style={{ color: 'var(--text-muted)', fontSize: '12px', marginTop: '8px' }}>H3 Hexagonal Grid Rendered Here</div>
            
            {/* Fake Heatmap Blob */}
            <div style={{ position: 'absolute', top: '30%', left: '40%', width: '300px', height: '300px', background: 'radial-gradient(circle, rgba(232, 67, 147, 0.2) 0%, rgba(255, 107, 107, 0.1) 40%, transparent 70%)', borderRadius: '50%', pointerEvents: 'none' }}></div>
            <div style={{ position: 'absolute', top: '50%', left: '20%', width: '200px', height: '200px', background: 'radial-gradient(circle, rgba(253, 170, 73, 0.15) 0%, transparent 70%)', borderRadius: '50%', pointerEvents: 'none' }}></div>
          </div>
          
          {/* Map Controls */}
          <div style={{ position: 'absolute', top: '24px', left: '24px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <button style={{ width: '40px', height: '40px', background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: '8px', color: 'var(--text-primary)', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Layers size={20} />
            </button>
            <button style={{ width: '40px', height: '40px', background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: '8px', color: 'var(--text-primary)', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CloudRain size={20} />
            </button>
            <button style={{ width: '40px', height: '40px', background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: '8px', color: 'var(--text-primary)', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Wind size={20} />
            </button>
            <button style={{ width: '40px', height: '40px', background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: '8px', color: 'var(--text-primary)', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Sun size={20} />
            </button>
          </div>
        </div>

        {/* Sidebar Data */}
        <div style={{ width: '380px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="glass-card">
            <div className="card-title">Zone Disruption Alerts</div>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '16px' }}>
              H3 grid segments with active parametric insurance triggers.
            </p>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {activeZones.map(zone => (
                <div key={zone.id} style={{ padding: '12px', background: 'var(--bg-surface)', borderRadius: '8px', borderLeft: `3px solid ${zone.riskLevel >= 80 ? 'var(--critical)' : zone.riskLevel >= 60 ? 'var(--danger)' : zone.riskLevel >= 40 ? 'var(--warning)' : 'var(--success)'}` }}>
                  <div className="flex-between" style={{ marginBottom: '8px' }}>
                    <div style={{ fontWeight: 600, fontSize: '14px' }}>{zone.name}</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Score: <span style={{ color: 'var(--text-primary)', fontWeight: 'bold' }}>{zone.riskLevel}</span></div>
                  </div>
                  
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {zone.activeTriggers.length === 0 ? (
                      <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Clear conditions</span>
                    ) : (
                      zone.activeTriggers.map((t, i) => (
                        <span key={i} style={{ fontSize: '11px', background: 'var(--bg-dark)', padding: '2px 8px', borderRadius: '4px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <AlertTriangle size={10} color="var(--warning)" /> {t}
                        </span>
                      ))
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskMap;
