import { formatCurrency } from '@/lib/format';

const funds = [
  { name: 'General Fund', amount: 15036518, description: 'Core governmental services, including public safety, sanitation, recreation, planning, and administration.' },
  { name: 'Water & Sewer Fund', amount: 17593677, description: 'Utility operations during the transition to Tri-River Water, including management fees and debt service.' },
  { name: 'Powell Bill Fund', amount: 277500, description: 'State street-aid revenue for eligible street maintenance and related repayment obligations.' },
  { name: 'License Plate Agency Fund', amount: 248733, description: 'Local DMV license plate agency operations.' },
  { name: 'Municipal Tag Fee Fund', amount: 94500, description: 'The $15 vehicle registration fee dedicated to Town street improvements and maintenance.' },
];

const total = funds.reduce((sum, fund) => sum + fund.amount, 0);

export default function FundsPage() {

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">Fund Overview</h1>
      <p className="text-gray-600 mb-2">
        FY 2026-2027 adopted appropriations across all annually budgeted funds.
      </p>
      <p className="text-sm text-gray-400 mb-8">
        Project ordinance appropriations are separate and continue according to
        their governing ordinances.
      </p>
      <div className="grid gap-4 mb-8">
        {funds.map((fund) => (
          <div key={fund.name} className="bg-white rounded-xl shadow-sm border p-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <h2 className="text-lg font-semibold">{fund.name}</h2>
              <p className="text-xl font-bold text-chatham-blue">{formatCurrency(fund.amount)}</p>
            </div>
            <p className="text-sm text-gray-500 mt-2">{fund.description}</p>
          </div>
        ))}
      </div>
      <div className="bg-chatham-blue text-white rounded-xl p-6 flex items-center justify-between">
        <span className="font-semibold">All-Funds Total</span>
        <span className="text-2xl font-bold">{formatCurrency(total)}</span>
      </div>
    </div>
  );
}
