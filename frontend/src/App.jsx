import { useState, useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Sidebar from './components/Sidebar'
import FileUpload from './components/FileUpload'
import Dashboard from './components/Dashboard'
import RiskReport from './components/RiskReport'
import ComplianceReport from './components/ComplianceReport'
import ChatPanel from './components/ChatPanel'
import DraftEditor from './components/DraftEditor'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'

function App() {
  const { user, loading, logout } = useAuth()
  const [activeTab, setActiveTab] = useState('chat')
  const [analysisData, setAnalysisData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [selectedRole, setSelectedRole] = useState('neutral')

  // Effect to load a default analysis for demo purposes if needed
  useEffect(() => {
    const saved = localStorage.getItem('last_analysis')
    if (saved) setAnalysisData(JSON.parse(saved))
  }, [])

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data)
    localStorage.setItem('last_analysis', JSON.stringify(data))
    // Only switch to dashboard if we're not currently using the Chat interface
    if (activeTab !== 'chat') {
      setActiveTab('dashboard')
    }
  }

  const handleLoadContract = (contract) => {
    setAnalysisData(contract.analysis_result)
    setActiveTab('dashboard')
  }

  if (loading) {
    return (
      <div style={{
        height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: 'var(--bg-primary)', color: 'var(--accent)'
      }}>
        <div className="loader" style={{ width: '60px', height: '60px' }}></div>
      </div>
    )
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    )
  }

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden', background: 'var(--bg-primary)' }}>
      <div className="mesh-bg" />
      <div className="courtroom-overlay" style={{ opacity: 0.25 }} />

      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        hasAnalysis={!!analysisData}
        healthScore={analysisData?.risk_report?.health_score || 0}
        user={user}
        onLogout={logout}
        onLoadContract={handleLoadContract}
        selectedRole={selectedRole}
        setSelectedRole={setSelectedRole}
      />

      <main style={{ flex: 1, overflowY: 'auto', position: 'relative', padding: '40px 60px' }}>
        {activeTab === 'upload' && (
          <FileUpload
            onAnalysisComplete={handleAnalysisComplete}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
            role={selectedRole}
            setRole={setSelectedRole}
          />
        )}

        {analysisData ? (
          <>
            {activeTab === 'dashboard' && <Dashboard data={analysisData} />}
            {activeTab === 'risk' && <RiskReport data={analysisData.risk_report} clauses={analysisData.clauses} />}
            {activeTab === 'compliance' && <ComplianceReport data={analysisData.compliance_report} />}
            {activeTab === 'draft' && (
              <DraftEditor
                contractId={analysisData.contract_id}
                role={selectedRole}
              />
            )}
          </>
        ) : (
          activeTab !== 'upload' && activeTab !== 'chat' && (
            <EmptyState
              icon="⚖️"
              title="Awaiting Instruction"
              description="Please upload or select a legal instrument from the repository to initiate neural auditing."
              action={() => setActiveTab('upload')}
              actionText="Access E-Filing"
            />
          )
        )}

        {activeTab === 'chat' && (
          <ChatPanel
            contractId={analysisData?.contract_id}
            role={selectedRole}
            onAnalysisComplete={handleAnalysisComplete}
            initialAnalysis={analysisData}
          />
        )}
      </main>
    </div>
  )
}

function EmptyState({ icon, title, description, action, actionText }) {
  return (
    <div className="animate-fade-in" style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      justifyContent: 'center', height: '80%', textAlign: 'center'
    }}>
      <div style={{
        width: '120px', height: '120px', borderRadius: '40px',
        background: 'rgba(184, 134, 11, 0.05)', border: '1px solid var(--border-color)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: '48px', marginBottom: '32px',
        boxShadow: '0 20px 40px rgba(0,0,0,0.6), 0 0 20px rgba(184, 134, 11, 0.1)'
      }}>{icon}</div>
      <h2 style={{ fontSize: '32px', fontWeight: '800', marginBottom: '12px', letterSpacing: '-0.02em' }}>{title}</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '32px', maxWidth: '450px', fontSize: '16px', lineHeight: '1.6' }}>
        {description}
      </p>
      <button onClick={action} className="btn btn-primary" style={{ padding: '14px 32px', borderRadius: '14px', fontSize: '15px' }}>
        {actionText}
      </button>
    </div>
  )
}

export default App
