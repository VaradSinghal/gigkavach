import React from 'react';
import { BrowserRouter, Routes, Route, NavLink, useLocation } from 'react-router-dom';
import { Shield, Home, AlertCircle, Map, Zap, Search, Bell, Settings, Users, Cpu } from 'lucide-react';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Claims from './pages/Claims';
import RiskMap from './pages/RiskMap';
import Fraud from './pages/Fraud';
import SimulationSuite from './pages/SimulationSuite';
import Workers from './pages/Workers';

const SentinelLayout = ({ children }) => {
  const location = useLocation();
  const isLanding = location.pathname === '/';
  
  const [notifications, setNotifications] = React.useState([]);
  const [toasts, setToasts] = React.useState([]);
  const seenIds = React.useRef(new Set());

  React.useEffect(() => {
    if (isLanding) return;
    
    let interval;
    const fetchNotifications = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/v1/notifications');
        const data = await res.json();
        
        data.notifications.forEach(notif => {
          if (!seenIds.current.has(notif.id)) {
            seenIds.current.add(notif.id);
            // Push new toast
            const toastId = Date.now() + Math.random();
            setToasts(prev => [...prev, { ...notif, t_id: toastId }]);
            
            // Auto remove toast after 5 seconds
            setTimeout(() => {
              setToasts(prev => prev.filter(t => t.t_id !== toastId));
            }, 5000);
          }
        });
        setNotifications(data.notifications);
      } catch (err) {
        // Silently fail if backend offline
      }
    };
    
    interval = setInterval(fetchNotifications, 3000);
    return () => clearInterval(interval);
  }, [isLanding]);

  if (isLanding) return <>{children}</>;

  return (
    <div className="sentinel-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="sidebar-brand">
            <div className="brand-icon">
              <Shield size={20} color="white" />
            </div>
            <span>SENTINEL</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/dashboard" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Home size={20} /> Dashboard
          </NavLink>
          <NavLink to="/claims" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
             <Zap size={20} /> Claims Registry
          </NavLink>
          <NavLink to="/risk" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Map size={20} /> Risk Map
          </NavLink>
          <NavLink to="/fraud" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <AlertCircle size={20} /> Fraud Core
          </NavLink>
          <NavLink to="/simulation" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Cpu size={20} /> Simulation
          </NavLink>

          <div style={{ margin: '32px 0 16px', fontSize: '12px', fontFamily: 'var(--font-sans)', color: 'var(--text-muted-dark)', fontWeight: 600, padding: '0 16px' }}>Operations</div>

          <NavLink to="/workers" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Users size={20} /> Workers
          </NavLink>
          <a href="#" className="nav-item">
            <Settings size={20} /> Settings
          </a>
        </nav>
        
        <div style={{ padding: '24px', borderTop: '1px solid var(--border-dark)', fontSize: '13px', fontFamily: 'var(--font-sans)', color: 'var(--text-muted-dark)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div className="pulse-indicator" />
            SYSTEM STABLE
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-wrapper">
        <header className="content-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
             <h2 className="page-title" style={{ margin: 0, fontSize: '20px' }}>Command Center</h2>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
            <button className="icon-btn" style={{ background: 'transparent', border: 'none', color: 'var(--text-dark)', cursor: 'pointer' }}>
              <Bell size={20} />
            </button>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', paddingLeft: '24px', borderLeft: '1px solid var(--border-light)' }}>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '14px', fontFamily: 'var(--font-sans)', fontWeight: 600 }}>Sentinel Admin</div>
                <div style={{ fontSize: '12px', color: 'var(--text-muted-light)' }}>Administrator</div>
              </div>
              <div className="brand-icon" style={{ width: '36px', height: '36px', borderRadius: '56px' }}>
                SA
              </div>
            </div>
          </div>
        </header>

        <div style={{ padding: '40px' }}>
          {children}
        </div>
      </main>

      {/* Global Toast Container */}
      <div style={{ position: 'fixed', bottom: '24px', right: '24px', zIndex: 9999, display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {toasts.map(toast => (
          <div key={toast.t_id} className="glass-card dark" style={{ width: '350px', padding: '16px', display: 'flex', gap: '16px', animation: 'slideInRight 0.3s ease-out' }}>
             <div style={{ padding: '8px', borderRadius: '8px', background: toast.type === 'geo_risk' ? 'rgba(255,100,100,0.1)' : 'rgba(9,133,81,0.1)', color: toast.type === 'geo_risk' ? 'var(--danger)' : 'var(--success)' }}>
               {toast.type === 'geo_risk' ? <AlertCircle size={24} /> : <Zap size={24} />}
             </div>
             <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, fontSize: '14px', marginBottom: '4px', color: '#fff' }}>{toast.title}</div>
                <div style={{ fontSize: '12px', color: 'var(--text-muted-dark)', lineHeight: 1.4 }}>{toast.message}</div>
             </div>
          </div>
        ))}
      </div>
      
    </div>
  );
};

function App() {
  return (
    <BrowserRouter>
      <SentinelLayout>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/claims" element={<Claims />} />
          <Route path="/risk" element={<RiskMap />} />
          <Route path="/fraud" element={<Fraud />} />
          <Route path="/simulation" element={<SimulationSuite />} />
          <Route path="/workers" element={<Workers />} />
        </Routes>
      </SentinelLayout>
    </BrowserRouter>
  );
}

export default App;
