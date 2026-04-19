'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { LayoutDashboard, Video, AlertTriangle, Shield, LogOut } from 'lucide-react'
import { clsx } from 'clsx'
import { useAuthStore } from '@/lib/auth-store'

const NAV_ITEMS = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/events', label: 'Händelser', icon: AlertTriangle },
  { href: '/cameras', label: 'Kameror', icon: Video },
  { href: '/compliance', label: 'Efterlevnad', icon: Shield },
]

export default function Nav() {
  const pathname = usePathname()
  const router = useRouter()
  const clearAuth = useAuthStore((s) => s.clearAuth)

  function handleLogout() {
    clearAuth()
    router.replace('/login')
  }

  return (
    <nav className="w-56 bg-gray-900 text-white flex flex-col">
      <div className="px-4 py-5 border-b border-gray-700">
        <span className="text-lg font-bold">SäkerSite</span>
        <p className="text-xs text-gray-400 mt-0.5">PPE-övervakning</p>
      </div>

      <div className="flex-1 py-4 space-y-1 px-2">
        {NAV_ITEMS.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={clsx(
              'flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors',
              pathname.startsWith(href)
                ? 'bg-blue-600 text-white'
                : 'text-gray-300 hover:bg-gray-800 hover:text-white'
            )}
          >
            <Icon size={16} />
            {label}
          </Link>
        ))}
      </div>

      <div className="px-2 py-4 border-t border-gray-700">
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-3 py-2 w-full rounded-md text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
        >
          <LogOut size={16} />
          Logga ut
        </button>
      </div>
    </nav>
  )
}
