import React, { useEffect, useState } from 'react'
import api from '../api/client'

const emptyForm = {
  LenderName: '',
  LoanType: 'Personal',
  OutstandingAmount: '',
  InterestRate: '',
  EMI: '',
  OverdueMonths: 0,
}

export default function Loans() {
  const [loans, setLoans] = useState([])
  const [form, setForm] = useState(emptyForm)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const loadLoans = async () => {
    const { data } = await api.get('/loans/')
    setLoans(data)
  }

  useEffect(() => {
    loadLoans()
  }, [])

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await api.post('/loans/', {
        ...form,
        OutstandingAmount: parseFloat(form.OutstandingAmount),
        InterestRate: parseFloat(form.InterestRate),
        EMI: parseFloat(form.EMI),
        OverdueMonths: parseInt(form.OverdueMonths) || 0,
      })
      setForm(emptyForm)
      await loadLoans()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add loan.')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (loanId) => {
    if (!confirm('Delete this loan record?')) return
    await api.delete(`/loans/${loanId}`)
    await loadLoans()
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-1">Loan Management</h1>
      <p className="text-gray-500 mb-6">Add and manage your loan accounts.</p>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <h2 className="font-semibold text-gray-700 mb-4">Add New Loan</h2>
          {error && <div className="bg-red-50 text-red-700 text-sm rounded-md px-3 py-2 mb-4">{error}</div>}
          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Lender Name</label>
              <input required value={form.LenderName} onChange={update('LenderName')} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Loan Type</label>
              <select value={form.LoanType} onChange={update('LoanType')} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option>Personal</option>
                <option>Credit Card</option>
                <option>Auto</option>
                <option>Home</option>
                <option>Education</option>
                <option>Other</option>
              </select>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Outstanding Amount</label>
                <input type="number" step="0.01" required value={form.OutstandingAmount} onChange={update('OutstandingAmount')} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Interest Rate (%)</label>
                <input type="number" step="0.01" required value={form.InterestRate} onChange={update('InterestRate')} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Monthly EMI</label>
                <input type="number" step="0.01" required value={form.EMI} onChange={update('EMI')} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Overdue Months</label>
                <input type="number" value={form.OverdueMonths} onChange={update('OverdueMonths')} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
              </div>
            </div>
            <button disabled={loading} className="w-full bg-brand-600 hover:bg-brand-700 text-white font-medium py-2.5 rounded-lg transition disabled:opacity-60">
              {loading ? 'Adding...' : 'Add Loan'}
            </button>
          </form>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <h2 className="font-semibold text-gray-700 mb-4">Your Loans ({loans.length})</h2>
          <div className="space-y-3 max-h-[520px] overflow-y-auto">
            {loans.length === 0 && <p className="text-gray-400 text-sm">No loans added yet.</p>}
            {loans.map((loan) => (
              <div key={loan.LoanID} className="border border-gray-100 rounded-lg p-3 flex justify-between items-start">
                <div>
                  <p className="font-medium text-gray-800">{loan.LenderName} · {loan.LoanType}</p>
                  <p className="text-sm text-gray-500">
                    Outstanding ₹{loan.OutstandingAmount.toLocaleString()} · EMI ₹{loan.EMI.toLocaleString()} · {loan.InterestRate}% · {loan.OverdueMonths} mo overdue
                  </p>
                </div>
                <button onClick={() => handleDelete(loan.LoanID)} className="text-red-500 text-sm hover:underline shrink-0 ml-3">
                  Delete
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
