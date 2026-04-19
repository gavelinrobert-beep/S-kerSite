import { clsx } from 'clsx'

interface CardProps {
  children: React.ReactNode
  className?: string
}

export function Card({ children, className }: CardProps) {
  return (
    <div
      className={clsx(
        'bg-white border border-gray-200 rounded-lg p-5 shadow-sm',
        className
      )}
    >
      {children}
    </div>
  )
}
