import React, { useEffect, useState } from 'react'
import api from '../api/client'

const typeColors = {
  settlement: 'bg-blue-100 text-blue-700',
  negotiation: 'bg-purple-100 text-purple-700',
}

export default function History() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/history/').then(({ data }) => {
      setHistory(data)
      setLoading(false)
    })
  }, [])

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-1">AI History</h1>
      <p className="text-gray-500 mb-6">A log of every AI-generated settlement prediction and negotiation letter.</p>

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : history.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 text-gray-500 text-sm">
          No AI activity yet. Try the Settlement Predictor or AI Negotiation tool.
        </div>
      ) : (
        <div className="space-y-3">
          {history.map((h) => (
            <div key={h.HistoryID} className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <div className="flex justify-between items-start gap-3">
                <p className="text-sm text-gray-700 flex-1">{h.GeneratedContent}</p>
                <span className={`text-xs font-semibold px-2 py-1 rounded-full shrink-0 ${typeColors[h.QueryType] || 'bg-gray-100 text-gray-600'}`}>
                  {h.QueryType}
                </span>
              </div>
              <p className="text-xs text-gray-400 mt-2">{new Date(h.Timestamp).toLocaleString()}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
