import { useNavigate, Link } from 'react-router-dom'

export default function LandingPage() {
    const navigate = useNavigate()

    return (
        <div style={{
            background: 'var(--bg-primary)',
            minHeight: '100vh',
            color: 'var(--text-primary)',
            overflowX: 'hidden',
            position: 'relative'
        }}>
            {/* Design Elements */}
            <div className="mesh-bg" />
            <div className="courtroom-overlay" />

            {/* Navigation */}
            <nav style={{
                padding: '24px 8%',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                position: 'relative',
                zIndex: 10,
                borderBottom: '1px solid var(--border-color)',
                backdropFilter: 'blur(10px)',
                background: 'rgba(10, 6, 5, 0.4)'
            }}>
                <div style={{ fontSize: '24px', fontWeight: '850', letterSpacing: '-0.04em', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{ width: '32px', height: '32px', background: 'var(--primary)', border: '1px solid var(--accent)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px' }}>⚖️</div>
                    Legal<span className="text-gradient">AI</span>
                </div>
                <div style={{ display: 'flex', gap: '40px', alignItems: 'center' }}>
                    <div className="nav-links" style={{ display: 'flex', gap: '32px', fontSize: '14px', fontWeight: '600', color: 'var(--text-secondary)' }}>
                        <span style={{ cursor: 'pointer' }}>Solutions</span>
                        <span style={{ cursor: 'pointer' }}>Statutes</span>
                        <span style={{ cursor: 'pointer' }}>Pricing</span>
                    </div>
                    <Link to="/login" className="btn btn-secondary" style={{ borderRadius: '12px', padding: '10px 24px', fontSize: '13px' }}>
                        Portal Access
                    </Link>
                </div>
            </nav>

            {/* Hero Section */}
            <header style={{
                padding: '120px 8% 80px',
                textAlign: 'center',
                position: 'relative',
                zIndex: 1
            }}>
                <div className="animate-fade-in">
                    <div style={{
                        display: 'inline-flex', alignItems: 'center', gap: '10px',
                        padding: '8px 16px', borderRadius: '40px',
                        background: 'rgba(184, 134, 11, 0.08)', border: '1px solid var(--border-color)',
                        color: 'var(--accent)', fontSize: '12px', fontWeight: '800',
                        letterSpacing: '1px', marginBottom: '32px', textTransform: 'uppercase'
                    }}>
                        <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--accent)' }} />
                        Next-Gen Indian Legal Intelligence
                    </div>

                    <h1 style={{
                        fontSize: 'clamp(40px, 8vw, 84px)',
                        fontWeight: '850',
                        lineHeight: 0.95,
                        letterSpacing: '-0.04em',
                        marginBottom: '32px',
                        maxWidth: '1100px',
                        margin: '0 auto 32px'
                    }}>
                        Modernizing Justice through <span className="text-gradient">Neural Logic</span>
                    </h1>

                    <p style={{
                        fontSize: 'clamp(16px, 2vw, 20px)',
                        color: 'var(--text-secondary)',
                        maxWidth: '700px',
                        margin: '0 auto 48px',
                        lineHeight: 1.6,
                        fontWeight: '500'
                    }}>
                        AI-powered contract intelligence, statutory compliance, and drafting workstation explicitly engineered for the Indian Legal Framework.
                    </p>

                    <div style={{ display: 'flex', gap: '16px', justifyContent: 'center' }}>
                        <button
                            onClick={() => navigate('/signup')}
                            className="btn btn-primary"
                            style={{ padding: '18px 40px', fontSize: '16px', borderRadius: '16px', fontWeight: '800' }}
                        >
                            Establish Digital Practice
                        </button>
                        <button className="btn btn-secondary" style={{ padding: '18px 40px', fontSize: '16px', borderRadius: '16px', fontWeight: '700' }}>
                            View Case Studies
                        </button>
                    </div>
                </div>

                {/* Hero Feature Image (Scales of Justice) */}
                <div className="animate-slide-up" style={{
                    marginTop: '80px', position: 'relative', maxWidth: '1000px', margin: '80px auto 0'
                }}>
                    <div style={{
                        position: 'absolute', inset: '-20px', background: 'var(--accent)',
                        opacity: 0.05, filter: 'blur(100px)', zIndex: -1
                    }} />
                    <img
                        src="/assets/scales_of_justice.png"
                        alt="Scales of Justice"
                        style={{
                            width: '100%', borderRadius: '24px 24px 0 0',
                            border: '1px solid var(--border-color)',
                            boxShadow: '0 40px 80px rgba(0,0,0,0.8)',
                            maskImage: 'linear-gradient(to bottom, black 85%, transparent 100%)'
                        }}
                    />
                </div>
            </header>

            {/* Feature Grid (Bento) */}
            <section style={{ padding: '100px 8%', background: 'rgba(26, 17, 15, 0.4)', position: 'relative', zIndex: 1, borderTop: '1px solid var(--border-color)' }}>
                <div className="bento-grid">
                    <div className="bento-item animate-fade-in" style={{ gridColumn: 'span 8', padding: '48px', minHeight: '400px', display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', background: 'linear-gradient(transparent, var(--bg-primary)), url("/assets/courtroom_bg.png") center/cover' }}>
                        <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--accent)', letterSpacing: '2px', marginBottom: '12px' }}>CORE INTELLIGENCE</div>
                        <h3 style={{ fontSize: '32px', fontWeight: '800', marginBottom: '16px', maxWidth: '400px' }}>Statutory Alignment Engine</h3>
                        <p style={{ color: 'var(--text-secondary)', maxWidth: '450px', fontSize: '16px', lineHeight: '1.6' }}>
                            Instant verification against Indian Contract Act, IT Act, and regional amendments with 99.4% accuracy.
                        </p>
                    </div>

                    <div className="bento-item animate-fade-in" style={{ gridColumn: 'span 4', padding: '32px', background: 'linear-gradient(135deg, rgba(184, 134, 11, 0.08), transparent)' }}>
                        <div style={{ fontSize: '32px', marginBottom: '20px' }}>📜</div>
                        <h3 style={{ fontSize: '24px', fontWeight: '850', marginBottom: '12px' }}>Draft Architect</h3>
                        <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>
                            Generate legally binding documents in seconds using neural templates optimized for Indian courts.
                        </p>
                    </div>

                    <div className="bento-item animate-fade-in" style={{ gridColumn: 'span 4', padding: '32px' }}>
                        <div style={{ fontSize: '32px', marginBottom: '20px' }}>🛡️</div>
                        <h3 style={{ fontSize: '24px', fontWeight: '850', marginBottom: '12px' }}>Risk Insulation</h3>
                        <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>
                            Neural scanning for hidden liabilities and grey-area clauses that modern legal teams often overlook.
                        </p>
                    </div>

                    <div className="bento-item animate-fade-in" style={{ gridColumn: 'span 8', padding: '48px', display: 'flex', alignItems: 'center', gap: '40px' }}>
                        <div style={{ flex: 1 }}>
                            <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--accent)', letterSpacing: '2px', marginBottom: '12px' }}>PRO WORKFLOW</div>
                            <h3 style={{ fontSize: '28px', fontWeight: '850', marginBottom: '16px' }}>Collaborative Justice</h3>
                            <p style={{ color: 'var(--text-secondary)', fontSize: '16px', lineHeight: '1.6' }}>
                                Secure, end-to-end encrypted workstation for modern firms to manage high-stakes document review.
                            </p>
                        </div>
                        <div style={{ width: '200px', height: '140px', background: 'var(--bg-secondary)', borderRadius: '16px', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '40px' }}>🏛️</div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer style={{ padding: '80px 8%', borderTop: '1px solid var(--border-color)', background: 'var(--bg-primary)', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: '850', marginBottom: '32px' }}>Legal<span className="text-gradient">AI</span></div>
                <div style={{ color: 'var(--text-muted)', fontSize: '14px', maxWidth: '600px', margin: '0 auto 40px', lineHeight: 1.6 }}>
                    Redefining the legal landscape through artificial intelligence and constitutional integrity. Designed and engineered for the prestigious legal community of India.
                </div>
                <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '32px', fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>
                    &copy; 2026 LegalAI Technology. All Rights Reserved.
                </div>
            </footer>
        </div>
    )
}
