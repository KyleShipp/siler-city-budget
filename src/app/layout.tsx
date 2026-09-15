import type { Metadata } from 'next';
import Nav from '@/components/Nav';
import './globals.css';

export const metadata: Metadata = {
  title: 'Siler City, NC Budget',
  description:
    'Explore the Siler City budget by department and revenue source, compare years, review fees, and estimate your Town property tax receipt.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Nav />
        <main className="max-w-7xl mx-auto px-4 py-8">{children}</main>
        <footer className="border-t mt-12 py-6 text-center text-sm text-gray-500">
          <p>
            An independent civic data tool. Not an official Town of Siler City
            publication.
          </p>
          <p className="mt-1">
            Data from published budget documents &middot;{' '}
            <a
              href="https://www.silercity.gov"
              className="underline hover:text-gray-700"
              target="_blank"
              rel="noopener noreferrer"
            >
              silercity.gov
            </a>
          </p>
        </footer>
      </body>
    </html>
  );
}
