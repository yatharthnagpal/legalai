import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { loginUser } from '../services/api'

export default function LoginPage() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const { login } = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            const data = await loginUser(email, password)
            login(data.access_token, data.user)
            navigate('/app')
        } catch (err) {
            setError(err.message || 'Authentication failed. Please check credentials.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div style={{
            minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: 'var(--bg-primary)', overflow: 'hidden', position: 'relative', padding: '20px'
        }}>
            {/* Dark Courtroom Layout */}
            <div className="mesh-bg" />
            <div className="courtroom-overlay" style={{ opacity: 0.4 }} />

            <div className="animate-fade-in" style={{
                width: '100%', maxWidth: '440px', background: 'rgba(20, 13, 11, 0.85)',
                backdropFilter: 'blur(30px)', border: '1px solid var(--border-color)',
                borderRadius: '32px', padding: '48px', position: 'relative', zIndex: 1,
                boxShadow: '0 40px 100px rgba(0,0,0,0.8), 0 0 40px rgba(184, 134, 11, 0.1)',
                margin: '0 auto'
            }}>
                {/* Logo with Brass Glow */}
                <div style={{ textAlign: 'center', marginBottom: '40px' }}>
                    <div style={{
                        width: '64px', height: '64px', borderRadius: '20px',
                        background: 'linear-gradient(135deg, var(--primary), #2a100c)',
                        border: '2px solid var(--accent)',
                        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: '28px', marginBottom: '20px', boxShadow: '0 12px 24px rgba(0,0,0,0.4)'
                    }}>⚖️</div>
                    <h1 style={{ fontSize: '32px', fontWeight: '850', letterSpacing: '-0.04em', marginBottom: '8px' }}>
                        LegalAI <span className="text-gradient">Portal</span>
                    </h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '14px', fontWeight: '500' }}>
                        Secure access to professional legal counsel
                    </p>
                </div>

                {error && (
                    <div className="animate-shake" style={{
                        padding: '12px 16px', borderRadius: '12px', marginBottom: '24px',
                        background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)',
                        color: '#f87171', fontSize: '13px', textAlign: 'center'
                    }}>{error}</div>
                )}

                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '1px' }}>
                            Attorney Email
                        </label>
                        <input
                            type="email" value={email} onChange={e => setEmail(e.target.value)} required
                            placeholder="attorney@firm.com"
                            style={{
                                width: '100%', padding: '16px', borderRadius: '14px', border: '1px solid var(--border-color)',
                                background: 'rgba(0,0,0,0.3)', color: 'white', fontSize: '15px', outline: 'none',
                                transition: 'all 0.2s', boxSizing: 'border-box'
                            }}
                            className="premium-input focus-glow"
                        />
                    </div>

                    <div style={{ marginBottom: '32px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                            <label style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>
                                Security Key
                            </label>
                            <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--accent)', cursor: 'pointer' }}>Recover Key</span>
                        </div>
                        <input
                            type="password" value={password} onChange={e => setPassword(e.target.value)} required
                            placeholder="••••••••"
                            style={{
                                width: '100%', padding: '16px', borderRadius: '14px', border: '1px solid var(--border-color)',
                                background: 'rgba(0,0,0,0.3)', color: 'white', fontSize: '15px', outline: 'none',
                                transition: 'all 0.2s', boxSizing: 'border-box'
                            }}
                            className="premium-input focus-glow"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            width: '100%', padding: '16px', borderRadius: '16px', border: '1px solid var(--accent)',
                            background: loading ? 'var(--bg-secondary)' : 'linear-gradient(135deg, var(--primary), #2a100c)',
                            color: 'white', fontSize: '16px', fontWeight: '800', cursor: loading ? 'wait' : 'pointer',
                            transition: 'all 0.3s', boxShadow: '0 8px 24px rgba(74, 28, 22, 0.4)'
                        }}
                    >
                        {loading ? 'CONSULTING STATUTES...' : 'SIGN IN TO WORKSTATION'}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: '32px', color: 'var(--text-muted)', fontSize: '14px' }}>
                    New associate?{' '}
                    <Link to="/signup" style={{ color: 'var(--accent)', textDecoration: 'none', fontWeight: '700' }}>
                        Enroll Now
                    </Link>
                </div>
            </div>

            {/* Sub-Footer */}
            <div style={{
                position: 'fixed', bottom: '30px', left: '0', right: '0', textAlign: 'center',
                color: 'rgba(255,255,255,0.1)', fontSize: '11px', letterSpacing: '2px', fontWeight: '600'
            }}>
                BRASS-ENCRYPTED SECURE NEURAL LINK
            </div>
        </div>
    )
}
