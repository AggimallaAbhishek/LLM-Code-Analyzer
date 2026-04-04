import { createContext, useContext, useState, useEffect, useCallback } from 'react'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Check authentication status on mount
  const checkAuth = useCallback(async () => {
    try {
      // Check URL for auth callback params
      const urlParams = new URLSearchParams(window.location.search)
      const authStatus = urlParams.get('auth')
      const token = urlParams.get('token')
      
      if (authStatus === 'success' && token) {
        // Store token and clear URL
        localStorage.setItem('auth_token', token)
        window.history.replaceState({}, document.title, window.location.pathname)
      } else if (authStatus === 'error') {
        setError('Authentication failed. Please try again.')
        window.history.replaceState({}, document.title, window.location.pathname)
      }

      // Check auth status from server
      const response = await fetch('/api/auth/status', {
        credentials: 'include',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token') || ''}`
        }
      })
      
      const data = await response.json()
      
      if (data.authenticated && data.user) {
        setUser(data.user)
      } else {
        setUser(null)
        localStorage.removeItem('auth_token')
      }
    } catch (err) {
      console.error('Auth check failed:', err)
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  const login = () => {
    // Redirect to Google OAuth
    window.location.href = '/api/auth/login'
  }

  const logout = async () => {
    try {
      await fetch('/api/auth/logout', {
        method: 'POST',
        credentials: 'include'
      })
      localStorage.removeItem('auth_token')
      setUser(null)
    } catch (err) {
      console.error('Logout failed:', err)
    }
  }

  const getAuthHeaders = () => {
    const token = localStorage.getItem('auth_token')
    return token ? { 'Authorization': `Bearer ${token}` } : {}
  }

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated: !!user,
    getAuthHeaders,
    checkAuth
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export default AuthContext
