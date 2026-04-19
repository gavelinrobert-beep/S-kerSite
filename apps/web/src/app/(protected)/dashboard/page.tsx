'use client'

import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/lib/auth-store'
import { useWebSocket } from '@/lib/websocket'
import { Badge } from '@/components/ui/badge'
import { Card } from '@/components/ui/card'
import Nav from '@/components/layout/nav'

interface Event {
  id: string
  camera_id: string
  event_type: string
  severity: string
  status: string
  started_at: string
}

export default function DashboardPage() {
  const token = useAuthStore((s) => s.accessToken)
  const [liveEvents, setLiveEvents] = useState<Event[]>([])

  const { data: events } = useQuery({
    queryKey: ['events', 'recent'],
    queryFn: () => apiFetch<Event[]>('/events?limit=20', token),
    enabled: !!token,
    refetchInterval: 30000,
  })

  useWebSocket((msg) => {
    if (msg.type === 'new_event') {
      setLiveEvents((prev) => [msg.data as Event, ...prev].slice(0, 10))
    }
  })

  const allEvents = [...liveEvents, ...(events ?? [])].slice(0, 20)
  const newCount = allEvents.filter((e) => e.status === 'new').length
  const highCount = allEvents.filter((e) => e.severity === 'high').length

  return (
    <div className="flex h-screen bg-gray-50">
      <Nav />
      <main className="flex-1 overflow-auto p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <Card>
            <p className="text-sm text-gray-500">Nya händelser</p>
            <p className="text-3xl font-bold text-gray-900">{newCount}</p>
          </Card>
          <Card>
            <p className="text-sm text-gray-500">Hög prioritet</p>
            <p className="text-3xl font-bold text-red-600">{highCount}</p>
          </Card>
          <Card>
            <p className="text-sm text-gray-500">Totalt (senaste 20)</p>
            <p className="text-3xl font-bold text-gray-900">{allEvents.length}</p>
          </Card>
        </div>

        {/* Live feed */}
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Live-händelser</h2>
        <div className="space-y-2">
          {allEvents.length === 0 && (
            <p className="text-sm text-gray-400">Inga händelser ännu.</p>
          )}
          {allEvents.map((event) => (
            <div
              key={event.id}
              className="bg-white border border-gray-200 rounded-lg p-4 flex items-center justify-between"
            >
              <div>
                <span className="text-sm font-medium text-gray-900">{event.event_type}</span>
                <span className="text-xs text-gray-400 ml-2">
                  {new Date(event.started_at).toLocaleTimeString('sv-SE')}
                </span>
                <p className="text-xs text-gray-500">Kamera: {event.camera_id}</p>
              </div>
              <div className="flex gap-2">
                <Badge severity={event.severity} />
                <Badge status={event.status} />
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
