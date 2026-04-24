import type { Metadata } from 'next'
import './globals.css'
import { Providers } from '@/components/providers'

export const metadata: Metadata = {
  title: 'SäkerSite',
  description: 'AI-powered PPE monitoring for Swedish construction sites',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="sv">
      <body className="font-sans">
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
