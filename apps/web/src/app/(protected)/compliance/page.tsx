'use client'

import { useQuery } from '@tanstack/react-query'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/lib/auth-store'
import Nav from '@/components/layout/nav'

interface AuditLog {
  id: string
  user_id: string | null
  action: string
  resource_type: string
  resource_id: string | null
  ip_address: string | null
  created_at: string
}

export default function CompliancePage() {
  const token = useAuthStore((s) => s.accessToken)

  const { data: logs, isLoading } = useQuery({
    queryKey: ['audit-log'],
    queryFn: () => apiFetch<AuditLog[]>('/compliance/audit-log?limit=100', token),
    enabled: !!token,
  })

  return (
    <div className="flex h-screen bg-gray-50">
      <Nav />
      <main className="flex-1 overflow-auto p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Efterlevnad & Revision</h1>
        <p className="text-sm text-gray-500 mb-6">
          Alla åtgärder loggas enligt GDPR Art. 30 (behandlingsregister) och EU AI Act loggningskrav.
        </p>

        {/* Compliance notices */}
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-6">
          <h2 className="text-sm font-semibold text-amber-800 mb-1">⚠️ Juridiska påminnelser</h2>
          <ul className="text-xs text-amber-700 space-y-1 list-disc list-inside">
            <li>DPIA måste vara slutförd innan produktionsdriftsättning (GDPR Art. 35)</li>
            <li>MBL §§ 11 och 19 facklig samverkan krävs</li>
            <li>Skyltning om kamerabevakning måste finnas på alla platser</li>
            <li>Data raderas automatiskt efter {30} dagar (konfigurerbart)</li>
          </ul>
        </div>

        {/* Audit log */}
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Revisionslogg</h2>
        {isLoading ? (
          <p className="text-sm text-gray-400">Laddar...</p>
        ) : (
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Åtgärd</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Resurstyp</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Resurs-ID</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Tid</th>
                </tr>
              </thead>
              <tbody>
                {(logs ?? []).map((log) => (
                  <tr key={log.id} className="border-b border-gray-100">
                    <td className="px-4 py-3 font-mono text-xs text-gray-900">{log.action}</td>
                    <td className="px-4 py-3 text-gray-500">{log.resource_type}</td>
                    <td className="px-4 py-3 text-gray-400 font-mono text-xs">
                      {log.resource_id ?? '—'}
                    </td>
                    <td className="px-4 py-3 text-gray-500">
                      {new Date(log.created_at).toLocaleString('sv-SE')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {(logs ?? []).length === 0 && (
              <p className="text-sm text-gray-400 text-center py-8">Inga loggposter ännu.</p>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
