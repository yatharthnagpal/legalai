import { useState, useEffect } from 'react'

const NAV_ITEMS = [
    { id: 'chat', icon: '💬', label: 'Legal Counsel AI' },
    { id: 'upload', icon: '📥', label: 'E-Filing / Upload' },
    { id: 'dashboard', icon: '📊', label: 'Case Intelligence' },
    { id: 'risk', icon: '🚨', label: 'Liability Audit' },
    { id: 'compliance', icon: '⚖️', label: 'Statutory Check' },
    { id: 'draft', icon: '✍️', label: 'Draft Architect' },
]

export default function Sidebar({
    activeTab, setActiveTab, hasAnalysis, healthScore, user, onLogout, onLoadContract, selectedRole, setSelectedRole
}) {
    const [collapsed, setCollapsed] = useState(false)

    return (
        <aside style={{
            width: collapsed ? '80px' : '280px',
            background: 'var(--bg-glass)',
            backdropFilter: 'blur(40px)',
            borderRight: '1px solid var(--border-color)',
            display: 'flex',
            flexDirection: 'column',
            transition: 'width 0.3s cubic-bezier(0.23, 1, 0.32, 1)',
            position: 'relative',
            zIndex: 100,
            overflow: 'hidden'
        }}>
            {/* Branding */}
            <div style={{
                padding: '32px 24px',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                borderBottom: '1px solid var(--border-color)'
            }}>
                <div style={{
                    width: '36px', height: '36px',
                    borderRadius: '10px', background: 'var(--primary)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '20px', flexShrink: 0, border: '1px solid var(--accent)'
                }}>⚖️</div>
                {!collapsed && (
                    <div style={{ fontSize: '20px', fontWeight: '850', letterSpacing: '-0.02em', whiteSpace: 'nowrap' }}>
                        Legal<span className="text-gradient">AI</span>
                    </div>
                )}
            </div>

            {/* Role Perspective Selector */}
            {!collapsed && (
                <div style={{ padding: '24px 20px 10px' }}>
                    <div style={{ fontSize: '10px', fontWeight: '800', color: 'var(--text-muted)', marginBottom: '12px', letterSpacing: '1px' }}>WORKSPACE PERSPECTIVE</div>
                    <div style={{
                        display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '4px',
                        background: 'rgba(255,255,255,0.03)', padding: '4px', borderRadius: '12px'
                    }}>
                        {['Neutral', 'Company', 'Artist'].map((role) => (
                            <button
                                key={role}
                                onClick={() => setSelectedRole(role.toLowerCase())}
                                style={{
                                    padding: '8px 4px', borderRadius: '8px', border: 'none',
                                    fontSize: '10px', fontWeight: '700', cursor: 'pointer',
                                    background: selectedRole === role.toLowerCase() ? 'var(--primary)' : 'transparent',
                                    color: selectedRole === role.toLowerCase() ? 'white' : 'var(--text-secondary)',
                                    transition: 'all 0.2s', border: selectedRole === role.toLowerCase() ? '1px solid var(--accent)' : 'none'
                                }}
                            >
                                {role}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Navigation Section */}
            <nav style={{ flex: 1, padding: '20px 12px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {NAV_ITEMS.map((item) => {
                    const isActive = activeTab === item.id
                    const isDisabled = !hasAnalysis && ['dashboard', 'risk', 'compliance'].includes(item.id)

                    return (
                        <button
                            key={item.id}
                            onClick={() => !isDisabled && setActiveTab(item.id)}
                            disabled={isDisabled}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '14px',
                                padding: '14px 16px',
                                borderRadius: '14px',
                                border: 'none',
                                background: isActive ? 'rgba(184, 134, 11, 0.1)' : 'transparent',
                                color: isActive ? 'var(--accent)' : isDisabled ? 'var(--text-muted)' : 'var(--text-secondary)',
                                cursor: isDisabled ? 'not-allowed' : 'pointer',
                                transition: 'all 0.2s',
                                textAlign: 'left',
                                width: '100%',
                                opacity: isDisabled ? 0.4 : 1,
                                position: 'relative'
                            }}
                            onMouseEnter={e => !isDisabled && !isActive && (e.currentTarget.style.background = 'rgba(255,255,255,0.03)')}
                            onMouseLeave={e => !isDisabled && !isActive && (e.currentTarget.style.background = 'transparent')}
                        >
                            <span style={{ fontSize: '18px', filter: isDisabled ? 'grayscale(1)' : 'none' }}>{item.icon}</span>
                            {!collapsed && (
                                <span style={{ fontSize: '14px', fontWeight: isActive ? '700' : '500' }}>
                                    {item.label}
                                </span>
                            )}
                            {isActive && !collapsed && (
                                <div style={{
                                    position: 'absolute', right: '12px', width: '6px', height: '6px',
                                    borderRadius: '50%', background: 'var(--accent)', boxShadow: '0 0 10px var(--accent-glow)'
                                }} />
                            )}
                        </button>
                    )
                })}
            </nav>

            {/* Case Stats (Health Ring Mini) */}
            {!collapsed && hasAnalysis && (
                <div style={{ padding: '0 20px 24px' }}>
                    <div style={{
                        padding: '20px', borderRadius: '20px', background: 'rgba(184, 134, 11, 0.05)',
                        border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '16px'
                    }}>
                        <div className="loader loader-sm" style={{ borderTopColor: 'var(--accent)', animation: 'none', borderStyle: 'solid', borderColor: 'rgba(184, 134, 11, 0.2)', borderTopColor: 'var(--accent)' }}>
                            <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '12px', fontWeight: '800', color: 'var(--accent)' }}>{Math.round(healthScore)}</div>
                        </div>
                        <div>
                            <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', letterSpacing: '0.5px' }}>INTEGRITY</div>
                            <div style={{ fontSize: '14px', fontWeight: '700' }}>{healthScore > 70 ? 'Optimal' : healthScore > 40 ? 'Review' : 'Critical'}</div>
                        </div>
                    </div>
                </div>
            )}

            {/* Bottom Section - User Profile */}
            <div style={{
                padding: '24px 16px',
                borderTop: '1px solid var(--border-color)',
                background: 'rgba(0,0,0,0.2)'
            }}>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: collapsed ? 'center' : 'space-between',
                    gap: '12px'
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div style={{
                            width: '40px', height: '40px', borderRadius: '12px',
                            background: 'linear-gradient(135deg, var(--primary), #2a100c)',
                            border: '1px solid var(--accent)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontSize: '18px', fontWeight: '700'
                        }}>
                            {user?.full_name?.charAt(0) || '⚖️'}
                        </div>
                        {!collapsed && (
                            <div style={{ overflow: 'hidden' }}>
                                <div style={{ fontSize: '14px', fontWeight: '700', color: 'white', whiteSpace: 'nowrap', textOverflow: 'ellipsis' }}>
                                    {user?.full_name || 'Counsel'}
                                </div>
                                <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Senior Associate</div>
                            </div>
                        )}
                    </div>

                    {!collapsed && (
                        <button
                            onClick={onLogout}
                            title="Secure Sign Out"
                            style={{
                                background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.2)',
                                color: '#ef4444', cursor: 'pointer',
                                padding: '10px', borderRadius: '12px', fontSize: '18px',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                transition: 'all 0.3s cubic-bezier(0.23, 1, 0.32, 1)',
                                boxShadow: '0 4px 12px rgba(239, 68, 68, 0.1)'
                            }}
                            onMouseEnter={e => {
                                e.currentTarget.style.background = '#ef4444'
                                e.currentTarget.style.color = 'white'
                                e.currentTarget.style.boxShadow = '0 8px 24px rgba(239, 68, 68, 0.4)'
                            }}
                            onMouseLeave={e => {
                                e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)'
                                e.currentTarget.style.color = '#ef4444'
                                e.currentTarget.style.boxShadow = '0 4px 12px rgba(239, 68, 68, 0.1)'
                            }}
                        >
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                                <polyline points="16 17 21 12 16 7"></polyline>
                                <line x1="21" y1="12" x2="9" y2="12"></line>
                            </svg>
                        </button>
                    )}
                </div>
            </div>

            {/* Collapse Toggle */}
            <button
                onClick={() => setCollapsed(!collapsed)}
                style={{
                    position: 'absolute', top: '38px', right: '10px',
                    width: '24px', height: '24px', borderRadius: '6px',
                    background: 'var(--accent)', border: 'none',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    cursor: 'pointer', color: 'black', fontSize: '12px',
                    transform: collapsed ? 'rotate(180deg)' : 'none',
                    transition: 'transform 0.3s', zIndex: 10
                }}
            >
                ◀
            </button>
        </aside>
    )
}
