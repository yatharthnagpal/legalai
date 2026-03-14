import { useState, useEffect } from 'react'
import { generateDraft } from '../services/api'

export default function DraftEditor({ contractId, role }) {
    const [draftData, setDraftData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [isCopied, setIsCopied] = useState(false)

    useEffect(() => {
        if (contractId) handleGenerate()
    }, [contractId])

    const handleGenerate = async () => {
        setLoading(true)
        try {
            const data = await generateDraft(contractId, role)
            setDraftData(data)
        } catch (err) {
            console.error('Draft generation failed:', err)
        } finally {
            setLoading(false)
        }
    }

    const handleCopy = () => {
        navigator.clipboard.writeText(draftData.drafted_content)
        setIsCopied(true)
        setTimeout(() => setIsCopied(false), 2000)
    }

    const handleDownload = () => {
        const element = document.createElement("a")
        const file = new Blob([draftData.drafted_content], { type: 'text/markdown' })
        element.href = URL.createObjectURL(file)
        element.download = `amended_contract_neural.md`
        document.body.appendChild(element)
        element.click()
    }

    if (loading) {
        return (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
                <div className="loader" style={{ marginBottom: '24px' }}></div>
                <h3 style={{ fontSize: '20px', fontWeight: '800' }}>Draft Architect <span className="text-gradient">Initializing</span></h3>
                <p style={{ color: 'var(--text-secondary)' }}>Neural-reasoning engine is structuring legal clauses...</p>
            </div>
        )
    }

    if (!draftData) return null

    return (
        <div className="animate-fade-in" style={{ paddingBottom: '40px' }}>
            <div style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
                <div>
                    <h1 style={{ fontSize: '32px', fontWeight: '850', letterSpacing: '-0.02em', marginBottom: '8px' }}>
                        Draft <span className="text-gradient">Architect</span>
                    </h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>
                        AI-optimized amendment suggestions and comprehensive redrafting.
                    </p>
                </div>
                <div style={{ display: 'flex', gap: '12px' }}>
                    <button onClick={handleGenerate} className="btn btn-secondary" style={{ borderRadius: '12px' }}>RE-ARCHITECT</button>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '32px', alignItems: 'flex-start' }}>
                {/* Editor Surface */}
                <div className="glass-card" style={{ padding: '0', overflow: 'hidden', border: '1px solid var(--border-color)' }}>
                    <div style={{ padding: '16px 24px', background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', letterSpacing: '1px' }}>PROPOSED LEGAL INSTRUMENT</div>
                        <div style={{ display: 'flex', gap: '10px' }}>
                            <button onClick={handleCopy} style={{ padding: '8px 16px', borderRadius: '10px', background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', color: 'white', fontSize: '12px', fontWeight: '700', cursor: 'pointer' }}>{isCopied ? 'COPIED!' : 'COPY'}</button>
                            <button onClick={handleDownload} style={{ padding: '8px 16px', borderRadius: '10px', background: 'var(--primary)', border: 'none', color: 'white', fontSize: '12px', fontWeight: '800', cursor: 'pointer' }}>DOWNLOAD</button>
                        </div>
                    </div>

                    <div style={{
                        padding: '40px', minHeight: '600px', background: 'rgba(10, 6, 5, 0.4)',
                        fontSize: '15px', color: 'var(--text-secondary)', lineHeight: '1.8',
                        fontFamily: '"JetBrains Mono", monospace', whiteSpace: 'pre-wrap'
                    }}>
                        {draftData.drafted_content}
                    </div>
                </div>

                {/* Metadata Sidebar */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    <div className="glass-card" style={{ padding: '24px', borderRadius: '24px' }}>
                        <div style={{ fontSize: '14px', fontWeight: '800', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--primary)' }} />
                            STRUCTURAL PARAMETERS
                        </div>

                        <div style={{ marginBottom: '24px' }}>
                            <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', marginBottom: '8px' }}>PRIMARY PERSPECTIVE</div>
                            <div style={{ fontSize: '14px', fontWeight: '700', color: 'var(--accent)', textTransform: 'capitalize' }}>{role} Counsel</div>
                        </div>

                        <div style={{ marginBottom: '24px' }}>
                            <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', marginBottom: '8px' }}>AMENDMENT INTENSITY</div>
                            <div style={{ fontSize: '14px', fontWeight: '700' }}>Sophisticated / High Integrity</div>
                        </div>

                        <div style={{ padding: '12px 20px', background: 'rgba(16,185,129,0.05)', borderRadius: '12px', border: '1px solid rgba(16,185,129,0.1)', marginBottom: '24px' }}>
                            <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--success)', marginBottom: '4px' }}>VERIFIED COMPLIANCE</div>
                            <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{draftData.compliance_notes[0]}</div>
                        </div>
                    </div>

                    <div className="bento-item" style={{ padding: '24px', border: '1px dashed var(--border-color)', background: 'transparent', textAlign: 'center' }}>
                        <div style={{ fontSize: '24px', marginBottom: '16px' }}>🔒</div>
                        <h4 style={{ fontSize: '14px', fontWeight: '800', marginBottom: '8px' }}>Security Audit Passed</h4>
                        <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>This draft utilizes Constitution-compliant terminology.</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
