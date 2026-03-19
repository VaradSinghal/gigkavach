import React from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { Shield, Home, AlertCircle, Map, DollarSign, Search, Bell, Settings, Users } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Claims from './pages/Claims';
import RiskMap from './pages/RiskMap';
import Fraud from './pages/Fraud';

const Layout = ({ children }) => {
  return (
    <div className="admin-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="sidebar-brand">
            <div className="sidebar-brand-icon">
              <Shield size={20} />
            </div>
            GigShield Admin
          </div>
        </div>
        
        <nav className="sidebar-nav">
          <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Home size={20} /> Dashboard
          </NavLink>
          <NavLink to="/claims" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <DollarSign size={20} /> Claims & Payouts
          </NavLink>
          <NavLink to="/risk" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Map size={20} /> Live Risk Map
          </NavLink>
          <NavLink to="/fraud" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <AlertCircle size={20} /> Fraud & Appeals
          </NavLink>
          
          <div style={{ margin: '32px 0 16px', fontSize: '11px', textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '1px', fontWeight: 700 }}>Management</div>
          
          <a href="#" className="nav-item">
            <Users size={20} /> Policyholders
          </a>
          <a href="#" className="nav-item">
            <Settings size={20} /> System Settings
          </a>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <header className="top-header">
          <div className="header-search">
            <Search size={18} color="var(--text-secondary)" />
            <input type="text" placeholder="Search workers, IDs, or claims..." />
          </div>
          
          <div className="header-actions">
            <button className="icon-btn">
              <Bell size={20} />
              <span className="badge">3</span>
            </button>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginLeft: '16px' }}>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '14px', fontWeight: 600 }}>Sarah Admin</div>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Risk Operations</div>
              </div>
              <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
                SA
              </div>
            </div>
          </div>
        </header>

        <div className="page-content">
          {children}
        </div>
      </main>
    </div>
  );
};

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/claims" element={<Claims />} />
          <Route path="/risk" element={<RiskMap />} />
          <Route path="/fraud" element={<Fraud />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
