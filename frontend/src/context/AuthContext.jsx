import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    const [token, setToken] = useState(localStorage.getItem('token'))
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (token) {
            // Verify token by fetching user profile
            fetch('/api/auth/me', {
                headers: { 'Authorization': `Bearer ${token}` }
            })
                .then(res => {
                    if (res.ok) return res.json()
                    throw new Error('Invalid token')
                })
                .then(data => {
                    setUser(data)
                    setLoading(false)
                })
                .catch(() => {
                    // Token expired or invalid
                    localStorage.removeItem('token')
                    setToken(null)
                    setUser(null)
                    setLoading(false)
                })
        } else {
            setLoading(false)
        }
    }, [token])

    const login = (accessToken, userData) => {
        localStorage.setItem('token', accessToken)
        setToken(accessToken)
        setUser(userData)
    }

    const logout = () => {
        localStorage.removeItem('token')
        setToken(null)
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, token, loading, login, logout, isAuthenticated: !!user }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext)
    if (!context) throw new Error('useAuth must be used within AuthProvider')
    return context
}

export default AuthContext
