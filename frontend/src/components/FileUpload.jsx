import { useState } from 'react'
import { uploadContract } from '../services/api'

export default function FileUpload({ onAnalysisComplete, isLoading, setIsLoading, role, setRole }) {
    const [file, setFile] = useState(null)
    const [dragActive, setDragActive] = useState(false)

    const handleUpload = async (e) => {
        e.preventDefault()
        if (!file) return

        setIsLoading(true)
        try {
            const result = await uploadContract(file, role)
            onAnalysisComplete(result)
        } catch (error) {
            console.error('Upload failed:', error)
            alert('Upload failed. Please check your network or try a different file.')
        } finally {
            setIsLoading(false)
        }
    }

    if (isLoading) {
        return (
            <div className="animate-fade-in" style={{
                display: 'flex', flexDirection: 'column', alignItems: 'center',
                justifyContent: 'center', height: '100%', minHeight: '60vh',
                textAlign: 'center'
            }}>
                <div style={{ position: 'relative', width: '200px', height: '200px', marginBottom: '40px' }}>
                    <div className="loader" style={{ width: '100%', height: '100%', borderTopColor: 'var(--accent)', borderWidth: '4px' }}></div>
                    <div style={{
                        position: 'absolute', inset: '10px', borderRadius: '50%',
                        background: 'radial-gradient(circle, var(--primary) 0%, transparent 70%)',
                        animation: 'pulse-badge 2s infinite', opacity: 0.3
                    }}></div>
                    <div style={{
                        position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: '48px'
                    }}>📑</div>
                </div>
                <h2 style={{ fontSize: '32px', fontWeight: '850', marginBottom: '12px' }}>Neural Scanning ...</h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '18px', maxWidth: '400px', margin: '0 auto', lineHeight: '1.6' }}>
                    Auditing document against {role === 'neutral' ? 'standard statutes' : role + ' perspective'} and Indian Contract Act...
                </p>
                <div style={{ marginTop: '24px', fontSize: '12px', fontWeight: '800', color: 'var(--accent)', letterSpacing: '2px' }}>AI-DRIVEN CONSTITUTIONAL ANALYSIS</div>
            </div>
        )
    }

    return (
        <div className="animate-fade-in" style={{ padding: '20px 0' }}>
            <div style={{ marginBottom: '40px' }}>
                <h1 style={{ fontSize: '36px', fontWeight: '850', letterSpacing: '-0.03em', marginBottom: '12px' }}>
                    Establish <span className="text-gradient">Legal Archive</span>
                </h1>
                <p style={{ color: 'var(--text-secondary)', fontSize: '18px', fontWeight: '500' }}>
                    Securely upload documents for neural-compliance verification.
                </p>
            </div>

            <div className="bento-grid">
                {/* Upload Zone */}
                <div className="bento-item" style={{ gridColumn: 'span 12', padding: '60px', textAlign: 'center' }}>
                    <div
                        onDragOver={(e) => { e.preventDefault(); setDragActive(true) }}
                        onDragLeave={() => setDragActive(false)}
                        onDrop={(e) => {
                            e.preventDefault();
                            setDragActive(false);
                            if (e.dataTransfer.files?.[0]) setFile(e.dataTransfer.files[0]);
                        }}
                        style={{
                            border: dragActive ? '2px dashed var(--accent)' : '2px dashed var(--border-color)',
                            background: dragActive ? 'rgba(184, 134, 11, 0.05)' : 'rgba(0,0,0,0.2)',
                            borderRadius: '32px', padding: '60px 40px', transition: 'all 0.3s cubic-bezier(0.23, 1, 0.32, 1)',
                            cursor: 'pointer'
                        }}
                        onClick={() => document.getElementById('file-input').click()}
                    >
                        <div style={{
                            width: '100px', height: '100px', borderRadius: '30px',
                            background: 'var(--primary)', border: '1px solid var(--accent)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontSize: '40px', margin: '0 auto 24px', boxShadow: '0 20px 40px rgba(0,0,0,0.4)'
                        }}>📥</div>
                        <h3 style={{ fontSize: '24px', fontWeight: '800', marginBottom: '8px' }}>
                            {file ? file.name : 'Select or Drop Document'}
                        </h3>
                        <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>
                            PDF, DOCX, or Image formats supported. Max 25MB.
                        </p>
                        <input id="file-input" type="file" style={{ display: 'none' }} onChange={(e) => setFile(e.target.files[0])} />
                    </div>

                    <div style={{ marginTop: '40px', display: 'flex', justifyContent: 'center', gap: '32px' }}>
                        <div>
                            <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-muted)', marginBottom: '12px', letterSpacing: '1px' }}>ANALYSIS PERSPECTIVE</div>
                            <div className="tab-nav" style={{ padding: '6px' }}>
                                {['neutral', 'company', 'artist'].map(r => (
                                    <button
                                        key={r}
                                        onClick={() => setRole(r)}
                                        className={`tab-btn ${role === r ? 'active' : ''}`}
                                        style={{ padding: '10px 24px', fontSize: '14px', textTransform: 'capitalize' }}
                                    >
                                        {r}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div style={{ display: 'flex', alignItems: 'flex-end' }}>
                            <button
                                onClick={handleUpload}
                                disabled={!file}
                                className="btn btn-primary"
                                style={{ padding: '15px 40px', borderRadius: '16px', fontSize: '16px', fontWeight: '800', opacity: file ? 1 : 0.4 }}
                            >
                                START CASE ANALYSIS
                            </button>
                        </div>
                    </div>
                </div>

                {/* Features Hint */}
                <div className="bento-item" style={{ gridColumn: 'span 4', padding: '32px', textAlign: 'center' }}>
                    <div style={{ fontSize: '32px', marginBottom: '16px' }}>⚖️</div>
                    <h4 style={{ fontWeight: '800', marginBottom: '8px' }}>Statutory Verification</h4>
                    <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Automatically check against Indian Contract Act standards.</p>
                </div>
                <div className="bento-item" style={{ gridColumn: 'span 4', padding: '32px', textAlign: 'center' }}>
                    <div style={{ fontSize: '32px', marginBottom: '16px' }}>🚨</div>
                    <h4 style={{ fontWeight: '800', marginBottom: '8px' }}>Risk Insulation</h4>
                    <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Detect hidden liabilities and unfavorable arbitration clauses.</p>
                </div>
                <div className="bento-item" style={{ gridColumn: 'span 4', padding: '32px', textAlign: 'center' }}>
                    <div style={{ fontSize: '32px', marginBottom: '16px' }}>📝</div>
                    <h4 style={{ fontWeight: '800', marginBottom: '8px' }}>Drafting Console</h4>
                    <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Neural-powered amendment suggestions and redrafting.</p>
                </div>
            </div>
        </div>
    )
}
