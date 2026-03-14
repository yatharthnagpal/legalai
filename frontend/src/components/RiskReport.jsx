import { useState } from 'react'

export default function RiskReport({ data, clauses }) {
    const [expandedClause, setExpandedClause] = useState(null)
    const [filter, setFilter] = useState('all')

    const filteredClauses = clauses.filter(c => {
        if (filter === 'all') return true
        return c.risk_level === filter
    })

    const getRiskColor = (level) => {
        switch (level) {
            case 'critical': return '#ef4444'
            case 'high': return '#f97316'
            case 'medium': return '#f59e0b'
            default: return '#10b981'
        }
    }

    return (
        <div className="animate-fade-in" style={{ paddingBottom: '40px' }}>
            {/* Header */}
            <div style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                    <h1 style={{ fontSize: '32px', fontWeight: '850', letterSpacing: '-0.02em', marginBottom: '8px' }}>
                        Risk <span className="text-gradient">Intelligence</span>
                    </h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '15px', fontWeight: '500' }}>
                        Granular breakdown of potential legal liabilities and loophole detection.
                    </p>
                </div>
                <div style={{ display: 'flex', gap: '20px' }}>
                    <div style={{ textAlign: 'center', padding: '12px 20px', background: 'rgba(255,255,255,0.02)', borderRadius: '16px', border: '1px solid var(--border-color)' }}>
                        <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginBottom: '4px' }}>PROTECTION</div>
                        <div style={{ fontSize: '24px', fontWeight: '850', color: '#10b981' }}>{Math.round(data.health_score)}%</div>
                    </div>
                    <div style={{ textAlign: 'center', padding: '12px 20px', background: 'rgba(255,255,255,0.02)', borderRadius: '16px', border: '1px solid var(--border-color)' }}>
                        <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginBottom: '4px' }}>EXPOSURE</div>
                        <div style={{ fontSize: '24px', fontWeight: '850', color: getRiskColor(data.overall_risk_level) }}>{Math.round(data.overall_risk_score)}%</div>
                    </div>
                </div>
            </div>

            {/* Filter Pills */}
            <div style={{
                display: 'flex', gap: '8px', marginBottom: '32px', padding: '6px',
                background: 'rgba(255,255,255,0.02)', borderRadius: '16px', border: '1px solid var(--border-color)',
                width: 'fit-content'
            }}>
                {['all', 'critical', 'high', 'medium', 'low'].map(f => (
                    <button
                        key={f}
                        onClick={() => setFilter(f)}
                        style={{
                            padding: '10px 16px', borderRadius: '12px', border: 'none',
                            fontSize: '12px', fontWeight: '700', cursor: 'pointer',
                            textTransform: 'uppercase', letterSpacing: '0.5px',
                            background: filter === f ? 'var(--primary)' : 'transparent',
                            color: filter === f ? 'white' : 'var(--text-muted)',
                            transition: 'all 0.2s'
                        }}
                    >
                        {f} ({f === 'all' ? clauses.length : clauses.filter(c => c.risk_level === f).length})
                    </button>
                ))}
            </div>

            {/* Clause Grid/List */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {filteredClauses.map((clause, i) => (
                    <div
                        key={i}
                        className="glass-card"
                        style={{
                            padding: '20px 24px', cursor: 'pointer', borderLeft: `4px solid ${getRiskColor(clause.risk_level)}`,
                            transition: 'all 0.3s cubic-bezier(0.23, 1, 0.32, 1)',
                            transform: expandedClause === i ? 'scale(1.01)' : 'scale(1)',
                            background: expandedClause === i ? 'rgba(255,255,255,0.03)' : 'var(--bg-card)'
                        }}
                        onClick={() => setExpandedClause(expandedClause === i ? null : i)}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                                <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', opacity: 0.6 }}>#{clause.clause_index + 1}</div>
                                <div style={{ fontSize: '15px', fontWeight: '700', color: 'white' }}>{clause.clause_type}</div>
                                <div style={{
                                    padding: '2px 10px', borderRadius: '6px', fontSize: '10px',
                                    fontWeight: '800', background: `${getRiskColor(clause.risk_level)}22`,
                                    color: getRiskColor(clause.risk_level), border: `1px solid ${getRiskColor(clause.risk_level)}44`,
                                    textTransform: 'uppercase'
                                }}>{clause.risk_level}</div>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                <div style={{ textAlign: 'right' }}>
                                    <div style={{ fontSize: '10px', textTransform: 'uppercase', color: 'var(--text-muted)' }}>Severity</div>
                                    <div style={{ fontSize: '16px', fontWeight: '800', color: getRiskColor(clause.risk_level) }}>{Math.round(clause.risk_score)}%</div>
                                </div>
                                <div style={{
                                    transform: expandedClause === i ? 'rotate(180deg)' : 'rotate(0)',
                                    fontSize: '12px', color: 'var(--text-muted)', transition: 'transform 0.3s'
                                }}>▼</div>
                            </div>
                        </div>

                        {expandedClause === i && (
                            <div className="animate-fade-in" style={{ marginTop: '24px', paddingTop: '24px', borderTop: '1px solid var(--border-color)' }}>
                                <div style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '10px' }}>PROCESSED CLAUSE EXTRACT</div>
                                <div style={{
                                    padding: '16px', borderRadius: '14px', background: 'rgba(0,0,0,0.2)',
                                    fontSize: '14px', color: 'var(--text-secondary)', lineHeight: '1.7',
                                    fontStyle: 'italic', border: '1px solid var(--border-color)', marginBottom: '20px'
                                }}>
                                    "{clause.clause_text}"
                                </div>

                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                                    <div className="bento-item" style={{ padding: '16px', background: 'rgba(239, 68, 68, 0.03)', border: '1px solid rgba(239, 68, 68, 0.1)' }}>
                                        <div style={{ fontSize: '11px', fontWeight: '800', color: '#ef4444', marginBottom: '10px' }}>RISK FACTORS</div>
                                        {clause.risk_reasons.map((r, j) => (
                                            <div key={j} style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px', display: 'flex', gap: '8px' }}>
                                                <span>•</span> {r}
                                            </div>
                                        ))}
                                    </div>
                                    <div className="bento-item" style={{ padding: '16px', background: 'rgba(16, 185, 129, 0.03)', border: '1px solid rgba(16, 185, 129, 0.1)' }}>
                                        <div style={{ fontSize: '11px', fontWeight: '800', color: '#10b981', marginBottom: '10px' }}>COUNTER GUIDANCE</div>
                                        {clause.suggestions.map((s, j) => (
                                            <div key={j} style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px', display: 'flex', gap: '8px' }}>
                                                <span>•</span> {s}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {filteredClauses.length === 0 && (
                <div style={{ textAlign: 'center', padding: '80px', color: 'var(--text-muted)' }}>
                    No risks found matching the "{filter}" criteria.
                </div>
            )}
        </div>
    )
}
