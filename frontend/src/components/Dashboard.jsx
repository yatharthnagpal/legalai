export default function Dashboard({ data }) {
    const { risk_report, compliance_report, summary, clauses, filename, contract_id } = data
    const health = risk_report.health_score

    const getHealthColor = () => {
        if (health >= 80) return '#10b981'
        if (health >= 50) return 'var(--accent)'
        return '#ef4444'
    }

    const StatCard = ({ label, value, sub, icon, color }) => (
        <div className="bento-item animate-fade-in" style={{ padding: '24px', display: 'flex', gap: '20px' }}>
            <div style={{
                width: '56px', height: '56px', borderRadius: '16px',
                background: `${color}11`, border: `1px solid ${color}33`,
                display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px'
            }}>{icon}</div>
            <div>
                <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', letterSpacing: '1px', textTransform: 'uppercase', marginBottom: '4px' }}>{label}</div>
                <div style={{ fontSize: '28px', fontWeight: '850', color: 'white' }}>{value}</div>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>{sub}</div>
            </div>
        </div>
    )

    return (
        <div className="animate-fade-in" style={{ paddingBottom: '40px' }}>
            {/* Header Area */}
            <div style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
                <div>
                    <h1 style={{ fontSize: '32px', fontWeight: '850', letterSpacing: '-0.02em', marginBottom: '8px' }}>
                        Case <span className="text-gradient">Intelligence</span>
                    </h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>
                        Strategic overview of {filename}
                    </p>
                </div>
                <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--accent)', letterSpacing: '1px' }}>ID: {contract_id.substring(0, 8)}...</div>
                    <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Analyzed: {new Date().toLocaleDateString()}</div>
                </div>
            </div>

            <div className="bento-grid">
                {/* Health Score Main Card */}
                <div className="bento-item" style={{ gridColumn: 'span 4', gridRow: 'span 2', padding: '40px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', background: 'linear-gradient(135deg, rgba(184, 134, 11, 0.05), transparent)' }}>
                    <div className="health-ring" style={{ width: '180px', height: '180px', marginBottom: '24px' }}>
                        <svg viewBox="0 0 100 100" style={{ transform: 'rotate(-90deg)', width: '100%', height: '100%' }}>
                            <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
                            <circle cx="50" cy="50" r="45" fill="none" stroke={getHealthColor()} strokeWidth="8"
                                strokeDasharray="283" strokeDashoffset={283 - (283 * health) / 100}
                                strokeLinecap="round" style={{ transition: 'stroke-dashoffset 1s ease' }} />
                        </svg>
                        <div className="health-ring-text">
                            <div className="health-ring-score" style={{ fontSize: '48px', color: getHealthColor() }}>{Math.round(health)}</div>
                            <div className="health-ring-label">Integrity</div>
                        </div>
                    </div>
                    <h3 style={{ fontSize: '20px', fontWeight: '800', marginBottom: '12px' }}>Legal Soundness</h3>
                    <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
                        {health > 75 ? 'Contract exhibits high procedural integrity with minimal risk exposure.' :
                            health > 45 ? 'Moderately sound. Several clauses require careful statutory review.' :
                                'Critical vulnerabilities detected. Significant legal exposure identified.'}
                    </p>
                </div>

                {/* Primary Highlights */}
                <div style={{ gridColumn: 'span 8', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                    <StatCard label="Identified Clauses" value={clauses?.length || 0} sub="High-impact segments" icon="📋" color="#b8860b" />
                    <StatCard label="Risk Profiles" value={risk_report.high_risk_clauses + risk_report.medium_risk_clauses} sub="Active liabilities" icon="🚨" color="#ef4444" />
                    <StatCard label="Statutory Checks" value={compliance_report.total_issues} sub="Legal discrepancies" icon="⚖️" color="#f59e0b" />
                    <StatCard label="Contract Value" value={summary.contract_value || 'N/A'} sub="Financial weight" icon="💰" color="#10b981" />
                </div>

                {/* Abstract Summary Section */}
                <div className="bento-item" style={{ gridColumn: 'span 8', padding: '32px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
                        <div style={{ padding: '8px', background: 'var(--primary)', borderRadius: '8px', fontSize: '18px', border: '1px solid var(--accent)' }}>📝</div>
                        <h3 style={{ fontSize: '20px', fontWeight: '800' }}>Executive Counsel Summary</h3>
                    </div>
                    <div style={{ fontSize: '15px', color: 'var(--text-secondary)', lineHeight: '1.8', whiteSpace: 'pre-wrap', fontStyle: 'italic' }}>
                        "{summary.summary_text}"
                    </div>
                </div>

                {/* Key Risk Bars */}
                <div className="bento-item" style={{ gridColumn: 'span 12', padding: '32px' }}>
                    <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', letterSpacing: '2px', textTransform: 'uppercase', marginBottom: '24px' }}>Vulnerability Breakdown</div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '32px' }}>
                        {[
                            { label: 'Critical', value: risk_report.high_risk_clauses, max: risk_report.total_clauses, color: '#ef4444' },
                            { label: 'Medium', value: risk_report.medium_risk_clauses, max: risk_report.total_clauses, color: '#f59e0b' },
                            { label: 'Minor', value: risk_report.low_risk_clauses, max: risk_report.total_clauses, color: '#10b981' },
                            { label: 'Checked', value: risk_report.total_clauses, max: risk_report.total_clauses, color: 'var(--accent)' }
                        ].map((risk, i) => (
                            <div key={risk.label}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '13px', fontWeight: '700' }}>
                                    <span>{risk.label}</span>
                                    <span style={{ color: risk.color }}>{risk.value} Items</span>
                                </div>
                                <div style={{ height: '6px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px', overflow: 'hidden' }}>
                                    <div style={{ height: '100%', width: `${(risk.value / (risk.max || 1)) * 100}%`, background: risk.color, borderRadius: '3px' }} />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
