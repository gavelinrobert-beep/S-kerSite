import { clsx } from 'clsx'

interface BadgeProps {
  severity?: string
  status?: string
  className?: string
}

const SEVERITY_CLASSES: Record<string, string> = {
  low: 'bg-blue-100 text-blue-700',
  medium: 'bg-yellow-100 text-yellow-700',
  high: 'bg-orange-100 text-orange-700',
  critical: 'bg-red-100 text-red-700',
}

const STATUS_CLASSES: Record<string, string> = {
  new: 'bg-purple-100 text-purple-700',
  acknowledged: 'bg-blue-100 text-blue-700',
  resolved: 'bg-green-100 text-green-700',
  false_positive: 'bg-gray-100 text-gray-600',
}

const SEVERITY_LABELS: Record<string, string> = {
  low: 'Låg',
  medium: 'Medium',
  high: 'Hög',
  critical: 'Kritisk',
}

const STATUS_LABELS: Record<string, string> = {
  new: 'Ny',
  acknowledged: 'Bekräftad',
  resolved: 'Löst',
  false_positive: 'Falskt larm',
}

export function Badge({ severity, status, className }: BadgeProps) {
  const label = severity
    ? (SEVERITY_LABELS[severity] ?? severity)
    : (STATUS_LABELS[status ?? ''] ?? status ?? '')

  const colorClass = severity
    ? (SEVERITY_CLASSES[severity] ?? 'bg-gray-100 text-gray-700')
    : (STATUS_CLASSES[status ?? ''] ?? 'bg-gray-100 text-gray-700')

  return (
    <span
      className={clsx(
        'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
        colorClass,
        className
      )}
    >
      {label}
    </span>
  )
}
