export default function ComplianceReport({ data }) {
    const { total_issues, statutes_checked, issues, violations, warnings } = data

    return (
        <div className="animate-fade-in" style={{ paddingBottom: '40px' }}>
            {/* Header */}
            <div style={{ marginBottom: '32px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: '850', letterSpacing: '-0.02em', marginBottom: '8px' }}>
                    Statutory <span className="text-gradient">Alignment</span>
                </h1>
                <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>
                    Verification against Indian Contract Act & Regional Regulatory Statutes.
                </p>
            </div>

            <div className="bento-grid">
                {/* Stats Overview */}
                <div className="bento-item" style={{ gridColumn: 'span 4', padding: '32px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
                    <div style={{ fontSize: '48px', fontWeight: '850', color: violations > 0 ? '#ef4444' : warnings > 0 ? '#f59e0b' : '#10b981', marginBottom: '8px' }}>{total_issues}</div>
                    <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', letterSpacing: '1px' }}>STATUTORY DISCREPANCIES</div>
                </div>

                <div className="bento-item" style={{ gridColumn: 'span 8', padding: '32px' }}>
                    <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', letterSpacing: '2px', marginBottom: '20px' }}>STATUTES IN SCOPE</div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '12px' }}>
                        {statutes_checked.map((statute, i) => (
                            <div key={i} className="bento-item" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                                <div style={{ color: 'var(--primary)' }}>🛡️</div>
                                <div style={{ fontSize: '13px', fontWeight: '700' }}>{statute}</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Violations List */}
                <div style={{ gridColumn: 'span 12' }}>
                    <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', letterSpacing: '2px', marginBottom: '24px', marginTop: '12px' }}>CRITICAL ALIGNMENT ISSUES</div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {issues.map((v, i) => (
                            <div key={i} className="glass-card" style={{ padding: '24px', display: 'flex', gap: '24px', alignItems: 'flex-start', borderLeft: `4px solid ${v.severity === 'violation' ? '#ef4444' : '#f59e0b'}` }}>
                                <div style={{
                                    width: '48px', height: '48px', borderRadius: '12px', background: v.severity === 'violation' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(245, 158, 11, 0.1)',
                                    color: v.severity === 'violation' ? '#ef4444' : '#f59e0b', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px', flexShrink: 0
                                }}>⚖️</div>
                                <div style={{ flex: 1 }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                                        <h4 style={{ fontSize: '18px', fontWeight: '800' }}>{v.issue}</h4>
                                        <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', background: 'rgba(255,255,255,0.05)', padding: '4px 10px', borderRadius: '6px' }}>
                                            {v.statute} - {v.section}
                                        </div>
                                    </div>
                                    <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '10px', fontStyle: 'italic' }}>
                                        Clause Extract: "{v.clause_text.substring(0, 150)}..."
                                    </p>
                                    <div style={{ padding: '16px', background: 'rgba(99, 102, 241, 0.05)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.1)' }}>
                                        <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--accent)', marginBottom: '6px' }}>REMEDIAL ACTION</div>
                                        <div style={{ fontSize: '13px', color: 'var(--text-primary)' }}>{v.recommendation}</div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
