'use client';

import { useState, useCallback, useEffect } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie,
} from 'recharts';
import { getMeta, getSummary, getBudget } from '@/lib/data';
import { formatCurrency } from '@/lib/format';
import { calculateTaxBill, allocateTaxReceipt } from '@/lib/calculations';
import { searchParcels, type ParcelResult } from '@/lib/parcel';

const meta = getMeta();
const summary = getSummary();
const budget = getBudget();

const COLORS = [
  '#1b4d7a', '#2563a0', '#3b7cc6', '#5a9bd5', '#7bb3e0',
  '#9fcbe8', '#c2ddf0', '#c9a227', '#d4b84e', '#e0c86a',
  '#9e9e9e', '#bdbdbd', '#e0e0e0',
];

const STORAGE_KEY = 'siler-city-receipt-parcel';

function loadSaved(): { parcel: ParcelResult | null; homeValue: number; addressQuery: string } {
  if (typeof window === 'undefined') return { parcel: null, homeValue: meta.municipality.medianHomeValue, addressQuery: '' };
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return { parcel: null, homeValue: meta.municipality.medianHomeValue, addressQuery: '' };
}

export default function ReceiptPage() {
  const fy = meta.defaultFiscalYear;
  const fyData = summary.fiscalYears[fy];
  const saved = loadSaved();
  const [homeValue, setHomeValue] = useState(saved.homeValue);
  const [addressQuery, setAddressQuery] = useState(saved.addressQuery);
  const [results, setResults] = useState<ParcelResult[]>(saved.parcel ? [saved.parcel] : []);
  const [selectedParcel, setSelectedParcel] = useState<ParcelResult | null>(saved.parcel);
  const [searching, setSearching] = useState(false);
  const [searched, setSearched] = useState(!!saved.parcel);
  const [error, setError] = useState('');

  useEffect(() => {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
        parcel: selectedParcel,
        homeValue,
        addressQuery,
      }));
    } catch {}
  }, [selectedParcel, homeValue, addressQuery]);

  const handleSearch = useCallback(async () => {
    if (!addressQuery.trim()) return;
    setSearching(true);
    setError('');
    setSearched(true);
    try {
      const parcels = await searchParcels(addressQuery);
      setResults(parcels);
      if (parcels.length === 1) {
        setSelectedParcel(parcels[0]);
        setHomeValue(parcels[0].assessedValue);
      } else {
        setSelectedParcel(null);
      }
    } catch (e) {
      setError('Could not reach Chatham County GIS. Try the manual slider below.');
      setResults([]);
    } finally {
      setSearching(false);
    }
  }, [addressQuery]);

  function selectParcel(p: ParcelResult) {
    setSelectedParcel(p);
    setHomeValue(p.assessedValue);
  }

  const taxableValue = selectedParcel && !selectedParcel.inTown ? 0 : homeValue;
  const townTax = calculateTaxBill(taxableValue, fyData.taxRate, fyData.collectionRate);

  // Service allocations
  const serviceDepts = budget.departments
    .filter((d) => d.id !== 'debt-service' && (d.amounts[fy]?.total ?? 0) > 0)
    .map((d) => ({ id: d.id, name: d.name, total: d.amounts[fy]?.total ?? 0 }));
  const serviceTotal = serviceDepts.reduce((sum, d) => sum + d.total, 0);
  const debtTotal =
    budget.departments.find((d) => d.id === 'debt-service')?.amounts[fy]?.total ?? 0;
  const totalBudget = serviceTotal + debtTotal;

  const allocations = allocateTaxReceipt(townTax, serviceDepts, totalBudget);
  const debtAllocation = Math.round(townTax * (debtTotal / totalBudget) * 100) / 100;

  const chartData = [
    ...allocations.map((a) => ({ name: a.name, amount: a.amount })),
    { name: 'Debt Service', amount: debtAllocation },
  ].sort((a, b) => b.amount - a.amount);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">Your Property Tax Receipt</h1>
      <p className="text-gray-600 mb-8">
        Look up your property to see how your Siler City tax bill breaks down
        across Town services.
      </p>

      {/* Address Lookup */}
      <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
        <h2 className="text-lg font-semibold mb-3">Look Up Your Property</h2>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Enter your street address (e.g., 12 East St)"
            value={addressQuery}
            onChange={(e) => setAddressQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            className="flex-1 border rounded-lg px-4 py-2 text-sm"
          />
          <button
            onClick={handleSearch}
            disabled={searching}
            className="bg-chatham-blue text-white px-5 py-2 rounded-lg text-sm font-medium hover:bg-chatham-dark disabled:opacity-50 transition"
          >
            {searching ? 'Searching...' : 'Search'}
          </button>
        </div>
        <p className="text-xs text-gray-400 mt-2">
          Searches Chatham County GIS parcel records in real time and identifies Siler City parcels
        </p>

        {error && (
          <p className="text-sm text-red-600 mt-3">{error}</p>
        )}

        {/* Search results */}
        {results.length > 1 && (
          <div className="mt-4">
            <p className="text-sm text-gray-600 mb-2">
              {results.length} properties found — select yours:
            </p>
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {results.map((p) => (
                <button
                  key={p.parcelNumber}
                  onClick={() => selectParcel(p)}
                  className={`w-full text-left border rounded-lg p-3 text-sm transition ${
                    selectedParcel?.parcelNumber === p.parcelNumber
                      ? 'border-chatham-blue bg-chatham-blue/5'
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="font-medium">{p.address}</div>
                  <div className="text-gray-500 text-xs mt-0.5">
                    {p.owner} · {formatCurrency(p.assessedValue)} assessed
                    · {p.taxDistrict}
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {searched && results.length === 0 && !searching && !error && (
          <p className="text-sm text-gray-500 mt-3">
            No properties found. Try a shorter search (e.g., just the street
            number and name).
          </p>
        )}
      </div>

      {/* Selected property info */}
      {selectedParcel && (
        <div className="bg-chatham-blue/5 border border-chatham-blue/20 rounded-xl p-5 mb-6">
          <div className="flex items-start justify-between">
            <div>
              <p className="font-semibold text-lg">{selectedParcel.address}</p>
              <p className="text-sm text-gray-600">{selectedParcel.owner}</p>
              <p className="text-xs text-gray-400 mt-1">
                Parcel #{selectedParcel.parcelNumber} · {selectedParcel.taxDistrict} ·{' '}
                {selectedParcel.landUse}
              </p>
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold">
                {formatCurrency(selectedParcel.assessedValue)}
              </p>
              <p className="text-xs text-gray-500">
                Land: {formatCurrency(selectedParcel.landValue)} · Building:{' '}
                {formatCurrency(selectedParcel.buildingValue)}
              </p>
            </div>
            {!selectedParcel.inTown && (
              <p className="mt-3 text-sm font-medium text-amber-700">
                This parcel is not identified as being in the Siler City tax district,
                so no Siler City municipal tax is estimated.
              </p>
            )}
          </div>
        </div>
      )}

      {/* Manual slider fallback */}
      {!selectedParcel && (
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Or enter your home&apos;s assessed value manually
          </label>
          <input
            type="range"
            min={50000}
            max={1500000}
            step={5000}
            value={homeValue}
            onChange={(e) => setHomeValue(Number(e.target.value))}
            className="w-full mb-2"
          />
          <div className="flex justify-between items-center">
            <input
              type="text"
              value={formatCurrency(homeValue)}
              onChange={(e) => {
                const num = Number(e.target.value.replace(/[^0-9]/g, ''));
                if (!isNaN(num)) setHomeValue(num);
              }}
              className="border rounded px-3 py-1.5 text-lg font-semibold w-44"
            />
            <p className="text-sm text-gray-500">
              Example starting value: {formatCurrency(meta.municipality.medianHomeValue)}
            </p>
          </div>
        </div>
      )}

      {/* Tax bill summary */}
      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-sm border p-6">
          <h2 className="text-lg font-semibold mb-1">Your Annual Siler City Tax</h2>
          <p className="text-3xl font-bold text-gray-900">
            {formatCurrency(Math.round(townTax))}
            <span className="text-base font-normal text-gray-400 ml-2">/ year</span>
          </p>
          <p className="text-sm text-gray-500 mb-4">
            Town rate: ${fyData.taxRate.toFixed(2)} per $100 assessed value
          </p>

          <div className="mt-4 pt-4 border-t text-xs text-gray-400">
            <p>
              Monthly: {formatCurrency(Math.round(townTax / 12))}
            </p>
            <p className="mt-1">
              Chatham County property tax is separate and is not shown here.
            </p>
          </div>
        </div>

        {/* Pie chart */}
        <div className="bg-white rounded-xl shadow-sm border p-6 flex flex-col items-center justify-center">
          <h2 className="text-lg font-semibold mb-2">
            Where Your Tax Goes
          </h2>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={chartData.slice(0, 8)}
                dataKey="amount"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                innerRadius={40}
                paddingAngle={2}
                label={false}
              >
                {chartData.slice(0, 8).map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(v: number) => formatCurrency(Math.round(v))} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Service breakdown */}
      <h2 className="text-xl font-bold mb-2">
        Your Tax: {formatCurrency(Math.round(townTax))} Breakdown
      </h2>
      <p className="text-xs text-gray-500 mb-4">
        This explanatory estimate allocates the tax proportionally according to
        each department&apos;s share of mapped General Fund appropriations.
      </p>

      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white rounded-xl shadow-sm border p-5">
          <h3 className="text-sm font-semibold text-gray-500 mb-3">
            Town Services
          </h3>
          <ResponsiveContainer
            width="100%"
            height={Math.max(300, chartData.length * 36)}
          >
            <BarChart
              data={chartData}
              layout="vertical"
              margin={{ left: 10, right: 30 }}
            >
              <XAxis
                type="number"
                tickFormatter={(v) => `$${v.toFixed(0)}`}
                fontSize={12}
              />
              <YAxis
                type="category"
                dataKey="name"
                width={170}
                fontSize={12}
              />
              <Tooltip formatter={(v: number) => `$${v.toFixed(2)}`} />
              <Bar dataKey="amount" radius={[0, 4, 4, 0]}>
                {chartData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-xl shadow-sm border p-5">
          <h3 className="text-sm font-semibold text-gray-500 mb-3">
            Detailed Breakdown
          </h3>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-gray-500">
                <th className="py-2">Service</th>
                <th className="py-2 text-right">Annual</th>
                <th className="py-2 text-right">Monthly</th>
                <th className="py-2 text-right">Share</th>
              </tr>
            </thead>
            <tbody>
              {allocations.map((a) => {
                return (
                  <tr key={a.name} className="border-b">
                    <td className="py-2">{a.name}</td>
                    <td className="py-2 text-right">
                      ${a.amount.toFixed(2)}
                    </td>
                    <td className="py-2 text-right">
                      ${(a.amount / 12).toFixed(2)}
                    </td>
                    <td className="py-2 text-right text-gray-500">
                      {a.share.toFixed(1)}%
                    </td>
                  </tr>
                );
              })}
              <tr className="border-b">
                <td className="py-2">Debt Service</td>
                <td className="py-2 text-right">
                  ${debtAllocation.toFixed(2)}
                </td>
                <td className="py-2 text-right">
                  ${(debtAllocation / 12).toFixed(2)}
                </td>
                <td className="py-2 text-right text-gray-500">
                  {((debtTotal / totalBudget) * 100).toFixed(1)}%
                </td>
              </tr>
              <tr className="font-semibold bg-gray-50">
                <td className="py-2">Town Total</td>
                <td className="py-2 text-right">
                  {formatCurrency(Math.round(townTax))}
                </td>
                <td className="py-2 text-right">
                  {formatCurrency(Math.round(townTax / 12))}
                </td>
                <td className="py-2 text-right">100%</td>
              </tr>
            </tbody>
          </table>
          <p className="text-xs text-gray-400 mt-3">
            This is an explanatory estimate, not your official tax bill.
            Property taxes fund a portion of the General Fund — the rest
            comes from sales tax, intergovernmental revenue, fees, and other
            sources. The allocations above show each department&apos;s proportional
            share applied to your tax bill. Chatham County taxes and other charges
            are not included.
          </p>
        </div>
      </div>
    </div>
  );
}
