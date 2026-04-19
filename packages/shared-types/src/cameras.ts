export interface Camera {
  id: string
  name: string
  location: string | null
  rtspUrl: string | null
  isActive: boolean
  createdAt: string
  updatedAt: string
}
