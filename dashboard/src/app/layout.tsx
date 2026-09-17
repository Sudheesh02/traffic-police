import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SynchroClear-ITS | Raipur Police Commissionerate C2 Dashboard',
  description:
    'Sub-GHz RF & Edge-AI Emergency Vehicle Preemption System for Raipur Traffic Police Commissionerate',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground min-h-screen antialiased font-sans">
        {children}
      </body>
    </html>
  );
}
