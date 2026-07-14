import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const navItems = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/loans', label: 'Loans' },
  { to: '/settlement', label: 'Settlement Predictor' },
  { to: '/negotiation', label: 'AI Negotiation' },
  { to: '/history', label: 'AI History' },
]

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  if (!user) return null

  return (
    <nav className="bg-brand-700 text-white shadow-md sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 flex items-center justify-between h-14">
        <Link to="/dashboard" className="font-bold text-lg tracking-tight">
          FinRelief <span className="text-brand-100">AI</span>
        </Link>
        <div className="hidden md:flex gap-6 text-sm font-medium">
          {navItems.map((item) => (
            <Link key={item.to} to={item.to} className="hover:text-brand-100 transition">
              {item.label}
            </Link>
          ))}
        </div>
        <div className="flex items-center gap-3 text-sm">
          <span className="hidden sm:inline opacity-90">Hi, {user.Name?.split(' ')[0]}</span>
          <button
            onClick={() => {
              logout()
              navigate('/login')
            }}
            className="bg-brand-600 hover:bg-brand-500 px-3 py-1.5 rounded-md transition"
          >
            Logout
          </button>
        </div>
      </div>
      <div className="md:hidden flex justify-around bg-brand-600 text-xs py-1">
        {navItems.map((item) => (
          <Link key={item.to} to={item.to} className="px-1 py-1">
            {item.label}
          </Link>
        ))}
      </div>
    </nav>
  )
}
