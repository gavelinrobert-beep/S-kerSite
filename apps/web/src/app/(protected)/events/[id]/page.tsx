'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useParams, useRouter } from 'next/navigation'
import { apiFetch, apiFetchPatch } from '@/lib/api'
import { useAuthStore } from '@/lib/auth-store'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import Nav from '@/components/layout/nav'

interface Detection {
  id: string
  person_id: number
  hardhat_detected: boolean
  vest_detected: boolean
  confidence: number | null
}

interface Event {
  id: string
  camera_id: string
  event_type: string
  severity: string
  status: string
  started_at: string
  ended_at: string | null
  detections: Detection[]
}

export default function EventDetailPage() {
  const { id } = useParams<{ id: string }>()
  const token = useAuthStore((s) => s.accessToken)
  const queryClient = useQueryClient()
  const router = useRouter()

  const { data: event, isLoading } = useQuery({
    queryKey: ['event', id],
    queryFn: () => apiFetch<Event>(`/events/${id}`, token),
    enabled: !!token && !!id,
  })

  const mutation = useMutation({
    mutationFn: (newStatus: string) =>
      apiFetchPatch(`/events/${id}`, { status: newStatus }, token),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['event', id] })
      queryClient.invalidateQueries({ queryKey: ['events'] })
    },
  })

  if (isLoading) return (
    <div className="flex h-screen bg-gray-50">
      <Nav />
      <main className="flex-1 p-6"><p className="text-gray-400">Laddar...</p></main>
    </div>
  )

  if (!event) return (
    <div className="flex h-screen bg-gray-50">
      <Nav />
      <main className="flex-1 p-6"><p className="text-red-500">Händelse hittades inte.</p></main>
    </div>
  )

  return (
    <div className="flex h-screen bg-gray-50">
      <Nav />
      <main className="flex-1 overflow-auto p-6">
        <button
          onClick={() => router.back()}
          className="text-sm text-blue-600 hover:underline mb-4 block"
        >
          ← Tillbaka
        </button>

        <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h1 className="text-xl font-bold text-gray-900">{event.event_type}</h1>
              <p className="text-sm text-gray-500 mt-1">
                Kamera: {event.camera_id} &bull;{' '}
                {new Date(event.started_at).toLocaleString('sv-SE')}
              </p>
            </div>
            <div className="flex gap-2">
              <Badge severity={event.severity} />
              <Badge status={event.status} />
            </div>
          </div>

          {/* Status actions */}
          <div className="flex gap-2 flex-wrap">
            {event.status === 'new' && (
              <Button
                onClick={() => mutation.mutate('acknowledged')}
                disabled={mutation.isPending}
              >
                Bekräfta
              </Button>
            )}
            {event.status !== 'resolved' && (
              <Button
                variant="success"
                onClick={() => mutation.mutate('resolved')}
                disabled={mutation.isPending}
              >
                Markera som löst
              </Button>
            )}
            {event.status !== 'false_positive' && (
              <Button
                variant="ghost"
                onClick={() => mutation.mutate('false_positive')}
                disabled={mutation.isPending}
              >
                Falskt larm
              </Button>
            )}
          </div>
        </div>

        {/* Detections */}
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Detektioner</h2>
        <div className="space-y-2">
          {event.detections.map((det) => (
            <div
              key={det.id}
              className="bg-white border border-gray-200 rounded-lg p-4"
            >
              <p className="text-sm font-medium text-gray-900">Person {det.person_id + 1}</p>
              <div className="flex gap-4 mt-2 text-sm">
                <span className={det.hardhat_detected ? 'text-green-600' : 'text-red-600'}>
                  {det.hardhat_detected ? '✓ Hjälm' : '✗ Ingen hjälm'}
                </span>
                <span className={det.vest_detected ? 'text-green-600' : 'text-red-600'}>
                  {det.vest_detected ? '✓ Väst' : '✗ Ingen väst'}
                </span>
                {det.confidence !== null && (
                  <span className="text-gray-400">
                    Konfidens: {(det.confidence * 100).toFixed(1)}%
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
