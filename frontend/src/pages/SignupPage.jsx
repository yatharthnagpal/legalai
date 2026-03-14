import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { signupUser } from '../services/api'

export default function SignupPage() {
    const [fullName, setFullName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const { login } = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        if (password !== confirmPassword) {
            setError('System mismatch: Passwords do not align.')
            return
        }
        if (password.length < 8) {
            setError('Security requirement: Password must be at least 8 characters.')
            return
        }
        setLoading(true)
        try {
            const data = await signupUser(email, password, fullName)
            login(data.access_token, data.user)
            navigate('/app')
        } catch (err) {
            setError(err.message || 'Registration failed. Network or system error.')
        } finally {
            setLoading(false)
        }
    }

    const inputContainerStyle = { marginBottom: '16px' }
    const labelStyle = {
        display: 'block', fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)',
        marginBottom: '6px', textTransform: 'uppercase', letterSpacing: '1px'
    }
    const inputStyle = {
        width: '100%', padding: '14px 16px', borderRadius: '12px', border: '1px solid var(--border-color)',
        background: 'rgba(0,0,0,0.3)', color: 'white', fontSize: '14px', outline: 'none',
        transition: 'all 0.2s', boxSizing: 'border-box'
    }

    return (
        <div style={{
            minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: 'var(--bg-primary)', overflow: 'hidden', position: 'relative', padding: '20px'
        }}>
            <div className="mesh-bg" />
            <div className="courtroom-overlay" style={{ opacity: 0.3 }} />

            <div className="animate-fade-in" style={{
                width: '100%', maxWidth: '500px', background: 'rgba(20, 13, 11, 0.9)',
                backdropFilter: 'blur(30px)', border: '1px solid var(--border-color)',
                borderRadius: '32px', padding: '40px 48px', position: 'relative', zIndex: 1,
                boxShadow: '0 40px 100px rgba(0,0,0,0.8), 0 0 40px rgba(184, 134, 11, 0.05)',
                margin: '0 auto'
            }}>
                <div style={{ textAlign: 'center', marginBottom: '32px' }}>
                    <div style={{
                        width: '64px', height: '64px', borderRadius: '20px',
                        background: 'linear-gradient(135deg, var(--primary), #2a100c)',
                        border: '2px solid var(--accent)',
                        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: '28px', marginBottom: '16px', boxShadow: '0 12px 24px rgba(0,0,0,0.4)'
                    }}>⚖️</div>
                    <h1 style={{ fontSize: '30px', fontWeight: '850', letterSpacing: '-0.03em', marginBottom: '8px', textAlign: 'center', width: '100%' }}>
                        Join <span className="text-gradient">LegalAI</span>
                    </h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '14px', fontWeight: '500' }}>
                        Initialize your professional legal workstation
                    </p>
                </div>

                {error && (
                    <div className="animate-shake" style={{
                        padding: '12px 16px', borderRadius: '12px', marginBottom: '20px',
                        background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)',
                        color: '#f87171', fontSize: '12px', textAlign: 'center'
                    }}>{error}</div>
                )}

                <form onSubmit={handleSubmit}>
                    <div style={inputContainerStyle}>
                        <label style={labelStyle}>Full Name</label>
                        <input type="text" value={fullName} onChange={e => setFullName(e.target.value)} required
                            placeholder="Adv. Rajesh Kumar" style={inputStyle} className="premium-input focus-glow" />
                    </div>

                    <div style={inputContainerStyle}>
                        <label style={labelStyle}>Email Address (Firm Subdomain)</label>
                        <input type="email" value={email} onChange={e => setEmail(e.target.value)} required
                            placeholder="rajesh@legal.in" style={inputStyle} className="premium-input focus-glow" />
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '24px' }}>
                        <div>
                            <label style={labelStyle}>Security Key</label>
                            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required
                                placeholder="••••••••" style={inputStyle} className="premium-input focus-glow" />
                        </div>
                        <div>
                            <label style={labelStyle}>Verification</label>
                            <input type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required
                                placeholder="••••••••" style={inputStyle} className="premium-input focus-glow" />
                        </div>
                    </div>

                    <button
                        type="submit" disabled={loading}
                        style={{
                            width: '100%', padding: '16px', borderRadius: '16px', border: '1px solid var(--accent)',
                            background: loading ? 'var(--bg-secondary)' : 'linear-gradient(135deg, var(--primary), #2a100c)',
                            color: 'white', fontSize: '15px', fontWeight: '800', cursor: loading ? 'wait' : 'pointer',
                            transition: 'all 0.3s', boxShadow: '0 8px 24px rgba(74, 28, 22, 0.4)'
                        }}
                    >
                        {loading ? 'INITIALIZING STATION...' : 'CREATE PRO ACCOUNT'}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: '24px', color: 'var(--text-muted)', fontSize: '14px' }}>
                    Already registered? {' '}
                    <Link to="/login" style={{ color: 'var(--accent)', textDecoration: 'none', fontWeight: '700' }}>
                        Sign In
                    </Link>
                </div>
            </div>

            <div style={{
                position: 'fixed', bottom: '30px', left: '0', right: '0', textAlign: 'center',
                color: 'rgba(255,255,255,0.05)', fontSize: '11px', letterSpacing: '2px', fontWeight: '600'
            }}>
                CONSTITUTION OF INDIA COMPLIANT DIGITAL INFRASTRUCTURE
            </div>
        </div>
    )
}
