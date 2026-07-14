import React, { useEffect, useState } from 'react'
import api from '../api/client'

const riskColors = {
  Low: 'bg-green-100 text-green-700',
  Medium: 'bg-yellow-100 text-yellow-700',
  High: 'bg-red-100 text-red-700',
}

export default function Settlement() {
  const [loans, setLoans] = useState([])
  const [selectedLoanId, setSelectedLoanId] = useState('')
  const [predictions, setPredictions] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api.get('/loans/').then(({ data }) => {
      setLoans(data)
      if (data.length > 0) setSelectedLoanId(String(data[0].LoanID))
    })
  }, [])

  useEffect(() => {
    if (selectedLoanId) loadPredictions(selectedLoanId)
  }, [selectedLoanId])

  const loadPredictions = async (loanId) => {
    const { data } = await api.get(`/settlement/loan/${loanId}`)
    setPredictions(data)
  }

  const handlePredict = async () => {
    if (!selectedLoanId) return
    setError('')
    setLoading(true)
    try {
      await api.post(`/settlement/predict/${selectedLoanId}`)
      await loadPredictions(selectedLoanId)
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed.')
    } finally {
      setLoading(false)
    }
  }

  const selectedLoan = loans.find((l) => String(l.LoanID) === selectedLoanId)

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-1">Settlement Predictor</h1>
      <p className="text-gray-500 mb-6">Get an AI-driven suggested settlement amount for any loan account.</p>

      {loans.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 text-gray-500 text-sm">
          Add a loan first from the <strong>Loans</strong> page to run a settlement prediction.
        </div>
      ) : (
        <>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">Select Loan</label>
            <div className="flex gap-3 flex-wrap">
              <select value={selectedLoanId} onChange={(e) => setSelectedLoanId(e.target.value)} className="border border-gray-300 rounded-lg px-3 py-2 text-sm flex-1 min-w-[200px]">
                {loans.map((loan) => (
                  <option key={loan.LoanID} value={loan.LoanID}>
                    {loan.LenderName} · {loan.LoanType} · ₹{loan.OutstandingAmount.toLocaleString()}
                  </option>
                ))}
              </select>
              <button onClick={handlePredict} disabled={loading} className="bg-brand-600 hover:bg-brand-700 text-white font-medium px-5 py-2 rounded-lg transition disabled:opacity-60">
                {loading ? 'Predicting...' : 'Run Prediction'}
              </button>
            </div>
            {error && <div className="bg-red-50 text-red-700 text-sm rounded-md px-3 py-2 mt-3">{error}</div>}
            {selectedLoan && (
              <p className="text-xs text-gray-400 mt-2">
                {selectedLoan.OverdueMonths} month(s) overdue · {selectedLoan.InterestRate}% interest
              </p>
            )}
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h2 className="font-semibold text-gray-700 mb-4">Prediction History</h2>
            {predictions.length === 0 ? (
              <p className="text-gray-400 text-sm">No predictions yet for this loan.</p>
            ) : (
              <div className="space-y-3">
                {predictions.map((p) => (
                  <div key={p.SettlementID} className="border border-gray-100 rounded-lg p-4 flex justify-between items-center flex-wrap gap-2">
                    <div>
                      <p className="text-lg font-bold text-brand-700">₹{p.PredictedAmount.toLocaleString()}</p>
                      <p className="text-sm text-gray-500">{p.SuggestedSettlement}% of outstanding amount</p>
                    </div>
                    <span className={`text-xs font-semibold px-2 py-1 rounded-full ${riskColors[p.RiskCategory] || 'bg-gray-100 text-gray-600'}`}>
                      {p.RiskCategory} Risk
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}
