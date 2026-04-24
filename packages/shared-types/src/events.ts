export type EventSeverity = 'low' | 'medium' | 'high' | 'critical'
export type EventStatus = 'new' | 'acknowledged' | 'resolved' | 'false_positive'

export interface Detection {
  id: string
  personId: number
  bbox: [number, number, number, number] | null
  hardhatDetected: boolean
  vestDetected: boolean
  confidence: number | null
}

export interface PPEEvent {
  id: string
  cameraId: string
  eventType: string
  severity: EventSeverity
  status: EventStatus
  startedAt: string
  endedAt: string | null
  clipS3Key: string | null
  thumbnailS3Key: string | null
  metadata: Record<string, unknown> | null
  createdAt: string
  detections: Detection[]
}

export interface WebSocketMessage {
  type: 'new_event'
  data: Omit<PPEEvent, 'detections'>
}
