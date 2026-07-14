import React, { createContext, useContext, useState, useCallback } from 'react'
import api from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('finrelief_user')
    return stored ? JSON.parse(stored) : null
  })
  const [token, setToken] = useState(() => localStorage.getItem('finrelief_token'))

  const login = useCallback(async (email, password) => {
    const { data } = await api.post('/auth/login', { Email: email, Password: password })
    localStorage.setItem('finrelief_token', data.access_token)
    localStorage.setItem('finrelief_user', JSON.stringify(data.user))
    setToken(data.access_token)
    setUser(data.user)
    return data.user
  }, [])

  const register = useCallback(async (payload) => {
    const { data } = await api.post('/auth/register', payload)
    localStorage.setItem('finrelief_token', data.access_token)
    localStorage.setItem('finrelief_user', JSON.stringify(data.user))
    setToken(data.access_token)
    setUser(data.user)
    return data.user
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('finrelief_token')
    localStorage.removeItem('finrelief_user')
    setToken(null)
    setUser(null)
  }, [])

  const refreshUser = useCallback((updatedUser) => {
    localStorage.setItem('finrelief_user', JSON.stringify(updatedUser))
    setUser(updatedUser)
  }, [])

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
