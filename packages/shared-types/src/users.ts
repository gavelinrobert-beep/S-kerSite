export type UserRole = 'admin' | 'safety_manager' | 'supervisor' | 'viewer'

export interface User {
  id: string
  email: string
  fullName: string
  role: UserRole
  isActive: boolean
  createdAt: string
}
