'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/lib/auth-store'
import { Badge } from '@/components/ui/badge'
import Nav from '@/components/layout/nav'

interface Event {
  id: string
  camera_id: string
  event_type: string
  severity: string
  status: string
  started_at: string
}

export default function EventsPage() {
  const token = useAuthStore((s) => s.accessToken)
  const router = useRouter()
  const [severityFilter, setSeverityFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')

  const params = new URLSearchParams({ limit: '100' })
  if (severityFilter) params.set('severity', severityFilter)
  if (statusFilter) params.set('status', statusFilter)

  const { data: events, isLoading } = useQuery({
    queryKey: ['events', severityFilter, statusFilter],
    queryFn: () => apiFetch<Event[]>(`/events?${params.toString()}`, token),
    enabled: !!token,
  })

  return (
    <div className="flex h-screen bg-gray-50">
      <Nav />
      <main className="flex-1 overflow-auto p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Händelser</h1>

        {/* Filters */}
        <div className="flex gap-3 mb-4">
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="border border-gray-300 rounded px-3 py-1.5 text-sm"
          >
            <option value="">Alla allvarlighetsgrader</option>
            <option value="low">Låg</option>
            <option value="medium">Medium</option>
            <option value="high">Hög</option>
            <option value="critical">Kritisk</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border border-gray-300 rounded px-3 py-1.5 text-sm"
          >
            <option value="">Alla statusar</option>
            <option value="new">Ny</option>
            <option value="acknowledged">Bekräftad</option>
            <option value="resolved">Löst</option>
            <option value="false_positive">Falskt larm</option>
          </select>
        </div>

        {/* Table */}
        {isLoading ? (
          <p className="text-sm text-gray-400">Laddar...</p>
        ) : (
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Typ</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Kamera</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Allvarlighet</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Tid</th>
                </tr>
              </thead>
              <tbody>
                {(events ?? []).map((event) => (
                  <tr
                    key={event.id}
                    onClick={() => router.push(`/events/${event.id}`)}
                    className="border-b border-gray-100 hover:bg-gray-50 cursor-pointer"
                  >
                    <td className="px-4 py-3 text-gray-900">{event.event_type}</td>
                    <td className="px-4 py-3 text-gray-500">{event.camera_id}</td>
                    <td className="px-4 py-3">
                      <Badge severity={event.severity} />
                    </td>
                    <td className="px-4 py-3">
                      <Badge status={event.status} />
                    </td>
                    <td className="px-4 py-3 text-gray-500">
                      {new Date(event.started_at).toLocaleString('sv-SE')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {(events ?? []).length === 0 && (
              <p className="text-sm text-gray-400 text-center py-8">Inga händelser hittades.</p>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
