import { useState, useEffect, useRef } from 'react'
import { sendChatMessage, getChatHistory, uploadContract } from '../services/api'

export default function ChatPanel({ contractId, onDraftRequest, onAnalysisComplete, role = 'neutral' }) {
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [selectedFile, setSelectedFile] = useState(null)
    const inputRef = useRef(null)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        // Only load history if we have a contractId and we didn't just upload/analyze it locally
        if (contractId && messages.length === 0) {
            loadHistory()
        }
    }, [contractId])

    const loadHistory = async () => {
        if (!contractId) return
        setLoading(true)
        try {
            const history = await getChatHistory(contractId)
            setMessages(history.map(m => ({
                role: m.role,
                content: m.content
            })))
        } catch (err) {
            console.error('Failed to load history:', err)
        } finally {
            setLoading(false)
        }
    }

    useEffect(scrollToBottom, [messages])

    const handleFileSelect = (e) => {
        const file = e.target.files[0]
        if (file) {
            setSelectedFile(file)
            inputRef.current?.focus()
        }
    }

    const handleSend = async (e) => {
        e.preventDefault()
        const userText = input.trim()

        if ((!userText && !selectedFile) || loading) return

        let currentContractId = contractId

        setInput('')
        setLoading(true)

        if (selectedFile) {
            const fileToUpload = selectedFile
            setSelectedFile(null)

            setMessages(prev => [...prev, { role: 'user', content: `📤 Uploading document: ${fileToUpload.name}` }])
            try {
                const result = await uploadContract(fileToUpload, role)
                currentContractId = result.metadata?.id || result.id || result.contract_id || result.metadata?.contract_id

                setMessages(prev => [...prev, { role: 'assistant', content: `✅ Document "${fileToUpload.name}" uploaded and analyzed successfully.` }])
                onAnalysisComplete(result)

            } catch (error) {
                console.error('Upload failed:', error)
                setMessages(prev => [...prev, { role: 'assistant', content: '❌ System Error: Document upload and analysis failed. Please verify the file format and try again.' }])
                setLoading(false)
                return
            }
        }

        if (userText && currentContractId) {
            setMessages(prev => [...prev, { role: 'user', content: userText }])
            try {
                const response = await sendChatMessage(userText, currentContractId)
                setMessages(prev => [...prev, { role: 'assistant', content: response.response }])
            } catch (err) {
                setMessages(prev => [...prev, { role: 'assistant', content: '⚠️ Neural Link Interrupted: Unable to process legal query at this time.' }])
            }
        } else if (!userText && selectedFile) {
            setMessages(prev => [...prev, { role: 'assistant', content: "I am now ready to consult on this contract. What would you like to know?" }])
            setTimeout(() => inputRef.current?.focus(), 500)
        }

        setLoading(false)
    }

    const formatContent = (content) => {
        return content.split('\n').map((line, i) => {
            const bolded = line.replace(/\*\*(.*?)\*\*/g, '<b style="color:var(--accent-light)">$1</b>')
            return <div key={i} dangerouslySetInnerHTML={{ __html: bolded }} style={{ marginBottom: '8px' }} />
        })
    }

    const canSend = selectedFile || (contractId && input.trim())

    return (
        <div style={{
            display: 'flex', flexDirection: 'column', height: '100%',
            background: 'transparent', borderRadius: '32px', overflow: 'hidden'
        }}>
            {/* Chat History */}
            <div style={{
                flex: 1, overflowY: 'auto', padding: '24px',
                display: 'flex', flexDirection: 'column', gap: '20px'
            }}>
                {messages.length === 0 && !loading && (
                    <div style={{
                        marginTop: '100px', textAlign: 'center', opacity: 0.6
                    }}>
                        <div style={{ fontSize: '48px', marginBottom: '24px' }}>🏛️</div>
                        <h3 style={{ fontSize: '20px', fontWeight: '800' }}>Legal AI Counsel</h3>
                        <p style={{ maxWidth: '300px', margin: '8px auto', fontSize: '14px', lineHeight: '1.5' }}>
                            {contractId
                                ? "Ask regarding specific clauses, liability loopholes, or request a redraft."
                                : "Upload a document to initiate neural auditing and start consulting."
                            }
                        </p>
                        {!contractId && (
                            <button
                                type="button"
                                onClick={() => document.getElementById('chat-upload').click()}
                                className="btn btn-secondary"
                                style={{ marginTop: '24px', padding: '12px 24px', borderRadius: '12px' }}
                            >
                                📥 Select Document
                            </button>
                        )}
                    </div>
                )}

                {messages.map((m, i) => (
                    <div key={i} style={{
                        alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start',
                        maxWidth: '85%', display: 'flex', flexDirection: 'column',
                        alignItems: m.role === 'user' ? 'flex-end' : 'flex-start'
                    }}>
                        <div style={{
                            fontSize: '10px', fontWeight: '800', color: 'var(--text-muted)',
                            marginBottom: '6px', letterSpacing: '1px', textTransform: 'uppercase'
                        }}>
                            {m.role === 'user' ? 'Counsel' : 'LegalAI Advisor'}
                        </div>
                        <div style={{
                            padding: '16px 20px',
                            background: m.role === 'user' ? 'rgba(26, 17, 15, 0.95)' : 'var(--primary)',
                            backdropFilter: 'blur(10px)',
                            border: m.role === 'user' ? '1px solid var(--border-color)' : '1px solid var(--accent)',
                            borderRadius: m.role === 'user' ? '20px 4px 20px 20px' : '4px 20px 20px 20px',
                            color: 'white', fontSize: '15px', lineHeight: '1.6',
                            boxShadow: m.role === 'user' ? 'none' : '0 10px 30px rgba(74, 28, 22, 0.3)'
                        }}>
                            {formatContent(m.content)}
                        </div>
                    </div>
                ))}

                {loading && (
                    <div style={{ alignSelf: 'flex-start', display: 'flex', gap: '8px', padding: '12px' }}>
                        <div className="loader loader-sm" style={{ borderTopColor: 'var(--accent)' }}></div>
                        <span style={{ fontSize: '12px', color: 'var(--accent)', fontWeight: '800' }}>CONSULTING STATUTES...</span>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Floating Input Interface */}
            <div style={{ padding: '24px', background: 'transparent' }}>
                <form onSubmit={handleSend} style={{
                    position: 'relative', maxWidth: '800px', margin: '0 auto'
                }}>
                    {selectedFile && (
                        <div className="animate-fade-in" style={{
                            position: 'absolute', top: '-46px', left: '20px',
                            background: 'rgba(57, 24, 18, 0.95)', border: '1px solid var(--accent)',
                            padding: '8px 16px', borderRadius: '16px', fontSize: '13px',
                            color: 'white', display: 'flex', alignItems: 'center', gap: '12px',
                            boxShadow: '0 8px 24px rgba(0,0,0,0.3)', backdropFilter: 'blur(10px)'
                        }}>
                            <span style={{ fontSize: '16px' }}>📄</span>
                            <span style={{ fontWeight: '600' }}>{selectedFile.name}</span>
                            <button
                                type="button"
                                onClick={() => setSelectedFile(null)}
                                style={{
                                    background: 'rgba(255,255,255,0.1)', border: 'none',
                                    color: 'white', cursor: 'pointer', fontSize: '14px',
                                    width: '24px', height: '24px', borderRadius: '50%',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    marginLeft: '4px'
                                }}
                            >✕</button>
                        </div>
                    )}
                    <input
                        id="chat-upload"
                        type="file"
                        hidden
                        onChange={handleFileSelect}
                    />
                    <button
                        type="button"
                        onClick={() => document.getElementById('chat-upload').click()}
                        style={{
                            position: 'absolute', left: '10px', top: '50%',
                            transform: 'translateY(-50%)',
                            width: '40px', height: '40px', borderRadius: '12px',
                            background: selectedFile ? 'var(--accent)' : 'rgba(255,255,255,0.05)',
                            border: '1px solid var(--border-color)',
                            color: selectedFile ? 'white' : 'var(--text-secondary)', cursor: 'pointer',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            zIndex: 5, transition: 'all 0.2s'
                        }}
                    >
                        📎
                    </button>
                    <input
                        ref={inputRef}
                        value={input}
                        onChange={e => setInput(e.target.value)}
                        placeholder={
                            selectedFile
                                ? "Add a message about the document..."
                                : contractId
                                    ? "Inquire regarding liabilities or request amendments..."
                                    : "Upload a document to begin consultation..."
                        }
                        disabled={loading}
                        style={{
                            width: '100%', padding: '20px 80px 20px 60px',
                            borderRadius: '24px', border: '1px solid var(--border-color)',
                            background: 'rgba(10, 6, 5, 0.85)',
                            backdropFilter: 'blur(30px)', color: 'white',
                            fontSize: '15px', fontWeight: '500', outline: 'none',
                            boxShadow: '0 20px 50px rgba(0,0,0,0.4)',
                            transition: 'all 0.3s cubic-bezier(0.23, 1, 0.32, 1)',
                            opacity: loading ? 0.7 : 1
                        }}
                        className="premium-input focus-glow"
                    />
                    <button
                        type="submit"
                        disabled={loading || !canSend}
                        style={{
                            position: 'absolute', right: '12px', top: '50%',
                            transform: 'translateY(-50%)',
                            width: '48px', height: '48px', borderRadius: '16px',
                            background: (loading || !canSend) ? 'rgba(255,255,255,0.05)' : 'var(--primary)',
                            border: (loading || !canSend) ? '1px solid var(--border-color)' : '1px solid var(--accent)',
                            color: (loading || !canSend) ? 'var(--text-muted)' : 'white',
                            cursor: (loading || !canSend) ? 'not-allowed' : 'pointer',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            transition: 'all 0.2s', opacity: (canSend && !loading) ? 1 : 0.4
                        }}
                    >
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 1 9 22 2"></polygon>
                        </svg>
                    </button>
                </form>
            </div>
        </div>
    )
}
