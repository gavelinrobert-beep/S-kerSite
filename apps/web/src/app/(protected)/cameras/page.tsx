'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiFetch, apiFetchPost, apiFetchPatch, apiFetchDelete } from '@/lib/api'
import { useAuthStore } from '@/lib/auth-store'
import { Button } from '@/components/ui/button'
import Nav from '@/components/layout/nav'

interface Camera {
  id: string
  name: string
  location: string | null
  rtsp_url: string | null
  is_active: boolean
}

export default function CamerasPage() {
  const token = useAuthStore((s) => s.accessToken)
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [name, setName] = useState('')
  const [location, setLocation] = useState('')
  const [rtspUrl, setRtspUrl] = useState('')

  const { data: cameras, isLoading } = useQuery({
    queryKey: ['cameras'],
    queryFn: () => apiFetch<Camera[]>('/cameras', token),
    enabled: !!token,
  })

  const createMutation = useMutation({
    mutationFn: () =>
      apiFetchPost('/cameras', { name, location: location || null, rtsp_url: rtspUrl || null }, token),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cameras'] })
      setShowForm(false)
      setName('')
      setLocation('')
      setRtspUrl('')
    },
  })

  const toggleMutation = useMutation({
    mutationFn: ({ id, is_active }: { id: string; is_active: boolean }) =>
      apiFetchPatch(`/cameras/${id}`, { is_active }, token),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['cameras'] }),
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => apiFetchDelete(`/cameras/${id}`, token),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['cameras'] }),
  })

  return (
    <div className="flex h-screen bg-gray-50">
      <Nav />
      <main className="flex-1 overflow-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Kameror</h1>
          <Button onClick={() => setShowForm(!showForm)}>+ Lägg till kamera</Button>
        </div>

        {showForm && (
          <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
            <h2 className="text-base font-semibold mb-3">Ny kamera</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <input
                placeholder="Namn *"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="border border-gray-300 rounded px-3 py-2 text-sm"
              />
              <input
                placeholder="Plats"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="border border-gray-300 rounded px-3 py-2 text-sm"
              />
              <input
                placeholder="RTSP URL"
                value={rtspUrl}
                onChange={(e) => setRtspUrl(e.target.value)}
                className="border border-gray-300 rounded px-3 py-2 text-sm"
              />
            </div>
            <div className="flex gap-2 mt-3">
              <Button
                onClick={() => createMutation.mutate()}
                disabled={!name || createMutation.isPending}
              >
                Spara
              </Button>
              <Button variant="ghost" onClick={() => setShowForm(false)}>Avbryt</Button>
            </div>
          </div>
        )}

        {isLoading ? (
          <p className="text-sm text-gray-400">Laddar...</p>
        ) : (
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Namn</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Plats</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Åtgärder</th>
                </tr>
              </thead>
              <tbody>
                {(cameras ?? []).map((cam) => (
                  <tr key={cam.id} className="border-b border-gray-100">
                    <td className="px-4 py-3 font-medium text-gray-900">{cam.name}</td>
                    <td className="px-4 py-3 text-gray-500">{cam.location ?? '—'}</td>
                    <td className="px-4 py-3">
                      <span
                        className={`text-xs px-2 py-1 rounded-full font-medium ${
                          cam.is_active
                            ? 'bg-green-100 text-green-700'
                            : 'bg-gray-100 text-gray-500'
                        }`}
                      >
                        {cam.is_active ? 'Aktiv' : 'Inaktiv'}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex gap-2">
                        <button
                          onClick={() =>
                            toggleMutation.mutate({ id: cam.id, is_active: !cam.is_active })
                          }
                          className="text-xs text-blue-600 hover:underline"
                        >
                          {cam.is_active ? 'Inaktivera' : 'Aktivera'}
                        </button>
                        <button
                          onClick={() => {
                            if (confirm('Ta bort kameran?')) deleteMutation.mutate(cam.id)
                          }}
                          className="text-xs text-red-600 hover:underline"
                        >
                          Ta bort
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {(cameras ?? []).length === 0 && (
              <p className="text-sm text-gray-400 text-center py-8">Inga kameror konfigurerade.</p>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
