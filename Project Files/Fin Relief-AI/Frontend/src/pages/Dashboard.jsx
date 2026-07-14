import React, { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import api from '../api/client'
import { useAuth } from '../context/AuthContext'
import { StatCard } from '../components/StatCard'

export default function Dashboard() {
  const { user } = useAuth()
  const [profile, setProfile] = useState(null)
  const [loans, setLoans] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const [profileRes, loansRes] = await Promise.all([
          api.get('/financial/profile'),
          api.get('/loans/'),
        ])
        setProfile(profileRes.data)
        setLoans(loansRes.data)
      } catch (err) {
        setError('Could not load financial data.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const chartData = loans.map((l) => ({
    name: l.LenderName,
    EMI: l.EMI,
    Outstanding: l.OutstandingAmount,
  }))

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-1">Financial Health Dashboard</h1>
      <p className="text-gray-500 mb-6">Welcome back, {user?.Name}. Here's your current financial snapshot.</p>

      {error && <div className="bg-red-50 text-red-700 text-sm rounded-md px-3 py-2 mb-4">{error}</div>}

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <StatCard label="Monthly Income" value={`₹${user?.MonthlyIncome?.toLocaleString() ?? 0}`} />
            <StatCard label="EMI Ratio" value={`${profile?.EMI_Ratio ?? 0}%`} sub="of monthly income" />
            <StatCard label="DTI Ratio" value={`${profile?.DTI_Ratio ?? 0}%`} sub="debt-to-income" />
            <StatCard
              label="Stress Level"
              value={profile?.StressLevel ?? '—'}
              sub={`Surplus: ₹${profile?.MonthlySurplus?.toLocaleString() ?? 0}`}
              badge={profile?.StressLevel}
            />
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 mb-8">
            <h2 className="font-semibold text-gray-700 mb-4">EMI vs Outstanding Amount by Lender</h2>
            {chartData.length === 0 ? (
              <p className="text-gray-400 text-sm">No loans added yet. Add a loan to see your chart.</p>
            ) : (
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" fontSize={12} />
                  <YAxis fontSize={12} />
                  <Tooltip />
                  <Bar dataKey="EMI" fill="#2563eb" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="Outstanding" fill="#93c5fd" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h2 className="font-semibold text-gray-700 mb-4">Loan Summary</h2>
            {loans.length === 0 ? (
              <p className="text-gray-400 text-sm">No loans on record.</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-gray-500 border-b">
                      <th className="py-2 pr-4">Lender</th>
                      <th className="py-2 pr-4">Type</th>
                      <th className="py-2 pr-4">Outstanding</th>
                      <th className="py-2 pr-4">EMI</th>
                      <th className="py-2 pr-4">Overdue (mo)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {loans.map((l) => (
                      <tr key={l.LoanID} className="border-b last:border-0">
                        <td className="py-2 pr-4">{l.LenderName}</td>
                        <td className="py-2 pr-4">{l.LoanType}</td>
                        <td className="py-2 pr-4">₹{l.OutstandingAmount.toLocaleString()}</td>
                        <td className="py-2 pr-4">₹{l.EMI.toLocaleString()}</td>
                        <td className="py-2 pr-4">{l.OverdueMonths}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}
