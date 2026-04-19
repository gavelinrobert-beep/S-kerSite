'use client'

import { useEffect, useRef } from 'react'
import { useAuthStore } from './auth-store'

const WS_BASE = (process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000')
  .replace(/^http/, 'ws')

interface WSMessage {
  type: string
  data: unknown
}

export function useWebSocket(onMessage: (msg: WSMessage) => void) {
  const token = useAuthStore((s) => s.accessToken)
  const wsRef = useRef<WebSocket | null>(null)
  const onMessageRef = useRef(onMessage)
  onMessageRef.current = onMessage

  useEffect(() => {
    if (!token) return

    const connect = () => {
      const ws = new WebSocket(`${WS_BASE}/ws/alerts`)
      wsRef.current = ws

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data) as WSMessage
          onMessageRef.current(msg)
        } catch {
          // ignore parse errors
        }
      }

      ws.onerror = () => ws.close()

      ws.onclose = () => {
        // Reconnect after 5 seconds
        setTimeout(connect, 5000)
      }
    }

    connect()

    return () => {
      wsRef.current?.close()
    }
  }, [token])
}
