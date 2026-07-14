import React, { useEffect, useState } from 'react'
import api from '../api/client'

export default function Negotiation() {
  const [loans, setLoans] = useState([])
  const [selectedLoanId, setSelectedLoanId] = useState('')
  const [tone, setTone] = useState('professional')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api.get('/loans/').then(({ data }) => {
      setLoans(data)
      if (data.length > 0) setSelectedLoanId(String(data[0].LoanID))
    })
  }, [])

  const handleGenerate = async () => {
    if (!selectedLoanId) return
    setError('')
    setLoading(true)
    setResult(null)
    try {
      const { data } = await api.post('/negotiation/generate', {
        LoanID: parseInt(selectedLoanId),
        Tone: tone,
      })
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not generate negotiation letter.')
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = () => {
    if (result) navigator.clipboard.writeText(result.NegotiationLetter)
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-1">AI Negotiation Letter Generator</h1>
      <p className="text-gray-500 mb-6">Generate a lender-specific negotiation strategy and settlement letter, powered by Google Gemini.</p>

      {loans.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 text-gray-500 text-sm">
          Add a loan first from the <strong>Loans</strong> page to generate a negotiation letter.
        </div>
      ) : (
        <>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 mb-6">
            <div className="grid sm:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Select Loan</label>
                <select value={selectedLoanId} onChange={(e) => setSelectedLoanId(e.target.value)} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                  {loans.map((loan) => (
                    <option key={loan.LoanID} value={loan.LoanID}>
                      {loan.LenderName} · {loan.LoanType}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tone</label>
                <select value={tone} onChange={(e) => setTone(e.target.value)} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                  <option value="professional">Professional</option>
                  <option value="firm">Firm</option>
                  <option value="empathetic">Empathetic</option>
                </select>
              </div>
            </div>
            <button onClick={handleGenerate} disabled={loading} className="bg-brand-600 hover:bg-brand-700 text-white font-medium px-5 py-2.5 rounded-lg transition disabled:opacity-60">
              {loading ? 'Generating with AI...' : 'Generate Negotiation Letter'}
            </button>
            {error && <div className="bg-red-50 text-red-700 text-sm rounded-md px-3 py-2 mt-3">{error}</div>}
          </div>

          {result && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
                <h2 className="font-semibold text-gray-700 mb-3">Negotiation Strategy</h2>
                <pre className="whitespace-pre-wrap text-sm text-gray-700 font-sans">{result.NegotiationStrategy}</pre>
              </div>
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
                <div className="flex justify-between items-center mb-3">
                  <h2 className="font-semibold text-gray-700">Negotiation Letter</h2>
                  <button onClick={copyToClipboard} className="text-sm text-brand-600 hover:underline">Copy to clipboard</button>
                </div>
                <pre className="whitespace-pre-wrap text-sm text-gray-700 font-sans bg-gray-50 rounded-lg p-4 border border-gray-100">{result.NegotiationLetter}</pre>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
