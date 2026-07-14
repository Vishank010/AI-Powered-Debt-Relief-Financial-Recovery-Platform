import React from 'react'

const stressColors = {
  Low: 'bg-green-100 text-green-700',
  Moderate: 'bg-yellow-100 text-yellow-700',
  High: 'bg-orange-100 text-orange-700',
  Critical: 'bg-red-100 text-red-700',
}

export function StatCard({ label, value, sub, badge }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
      <p className="text-xs uppercase tracking-wide text-gray-500 font-medium">{label}</p>
      <p className="text-2xl font-bold text-gray-800 mt-1">{value}</p>
      {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
      {badge && (
        <span className={`inline-block mt-2 text-xs font-semibold px-2 py-1 rounded-full ${stressColors[badge] || 'bg-gray-100 text-gray-600'}`}>
          {badge}
        </span>
      )}
    </div>
  )
}
