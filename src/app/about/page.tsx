import { getMeta } from '@/lib/data';

const meta = getMeta();

export default function AboutPage() {
  return (
    <div className="max-w-3xl">
      <h1 className="text-3xl font-bold mb-6">About This Project</h1>

      <div className="prose prose-gray">
        <h2 className="text-xl font-semibold mt-6 mb-3">
          What is Siler City, NC Budget?
        </h2>
        <p className="text-gray-700 mb-4">
          Siler City, NC Budget is an independent civic data tool that
          turns published Town budget documents into searchable
          tables, interactive charts, department drilldowns, year-over-year
          comparisons, and a property tax receipt view.
        </p>

        <h2 className="text-xl font-semibold mt-6 mb-3">What you can do</h2>
        <ul className="list-disc pl-6 text-gray-700 space-y-1 mb-4">
          <li>Compare budgeted spending across fiscal years</li>
          <li>Explore adopted spending by department</li>
          <li>See which departments drive changes over time</li>
          <li>
            Estimate how your Town property tax bill is distributed across services
          </li>
          <li>Review all five annually budgeted funds</li>
          <li>Search selected Fee Schedule highlights</li>
        </ul>

        <h2 className="text-xl font-semibold mt-6 mb-3">Data Sources</h2>
        <div className="bg-white rounded-xl border p-4 mb-4">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-gray-500">
                <th className="py-2">Document</th>
                <th className="py-2">Date</th>
                <th className="py-2">Type</th>
              </tr>
            </thead>
            <tbody>
              {meta.sources.map((s) => (
                <tr key={s.title} className="border-b">
                  <td className="py-2">
                    {s.url ? (
                      <a
                        href={s.url}
                        className="text-chatham-blue underline"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {s.title}
                      </a>
                    ) : (
                      s.title
                    )}
                  </td>
                  <td className="py-2 text-gray-500">{s.date}</td>
                  <td className="py-2 text-gray-500 capitalize">{s.type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <h2 className="text-xl font-semibold mt-6 mb-3">Methodology</h2>
        <p className="text-gray-700 mb-2">
          Budget data is extracted from published PDF budget documents and
          organized into a consistent multi-year dataset. Revenue and
          expenditure line items are mapped to categories and departments
          following the Town&apos;s published budget ordinance and department schedule.
        </p>
        <p className="text-gray-700 mb-2">
          The property tax receipt estimates how a property tax bill maps to
          General Fund services. It uses the entered property value, the
          applicable Siler City property tax rate, and the relative share of
          General Fund spending by department.
        </p>
        <p className="text-gray-700 mb-4">
          FY 2025-2026 and FY 2026-2027 figures are adopted budget amounts. The
          Board of Commissioners unanimously adopted the FY 2026-2027 budget on
          May 18, 2026.
        </p>

        <h2 className="text-xl font-semibold mt-6 mb-3">Limitations</h2>
        <ul className="list-disc pl-6 text-gray-700 space-y-1 mb-4">
          <li>
            This is not an official Town of Siler City publication and should not
            replace adopted budget documents or annual financial reports
          </li>
          <li>
            The explorer is only as accurate as the source documents
          </li>
          <li>
            Budget categories may change over time, so some comparisons require
            judgment
          </li>
          <li>
            This explorer&apos;s department and revenue detail focuses on the General
            Fund; the fund overview summarizes the other annually budgeted funds
          </li>
          <li>
            Department drilldowns show adopted totals; consult the official
            document for complete account-level detail
          </li>
          <li>
            Receipt estimates are explanatory allocations, not official tax bills
          </li>
          <li>
            The $200,000 manual estimate is an example starting value, not a published
            median
          </li>
        </ul>

        <h2 className="text-xl font-semibold mt-6 mb-3">Official Resources</h2>
        <p className="text-gray-700">
          For official budget documents and financial reports, visit{' '}
          <a
            href="https://www.silercity.gov/Archive.aspx?AMID=39"
            className="text-chatham-blue underline"
            target="_blank"
            rel="noopener noreferrer"
          >
            silercity.gov
          </a>
          .
        </p>
      </div>
    </div>
  );
}
