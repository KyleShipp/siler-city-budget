'use client';

import { formatCurrency, formatPercent } from '@/lib/format';
import type { DepartmentAmounts } from '@/types/budget';

interface DeptDetailProps {
  dept: {
    id: string;
    name: string;
    amounts: Record<string, DepartmentAmounts>;
    note?: string;
  };
  fiscalYears: string[];
  onClose: () => void;
}

export default function DeptDetail({ dept, fiscalYears, onClose }: DeptDetailProps) {
  const currentFY = fiscalYears[fiscalYears.length - 1];
  const prevFY = fiscalYears.length > 1 ? fiscalYears[fiscalYears.length - 2] : null;
  const current = dept.amounts[currentFY];
  const prev = prevFY ? dept.amounts[prevFY] : null;

  function pctChange(cur: number, prv: number | undefined) {
    if (!prv || prv === 0) return '';
    return formatPercent(((cur - prv) / prv) * 100);
  }

  const breakdownRows = [{ label: 'Adopted Department Total', key: 'total' as const }];

  return (
    <div className="bg-white rounded-xl shadow-sm border p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold">{dept.name}</h3>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
          aria-label="Close"
        >
          &times;
        </button>
      </div>

      {dept.note && (
        <p className="text-sm text-gray-500 mb-4 italic">{dept.note}</p>
      )}

      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-left text-gray-500">
            <th className="py-2 pr-4">Category</th>
            {fiscalYears.map((fy) => (
              <th key={fy} className="py-2 px-3 text-right">{fy}</th>
            ))}
            {prev && <th className="py-2 px-3 text-right">Change</th>}
          </tr>
        </thead>
        <tbody>
          {breakdownRows.map((row) => (
            <tr
              key={row.key}
              className={`border-b ${row.key === 'total' ? 'font-semibold bg-gray-50' : ''}`}
            >
              <td className="py-2 pr-4">{row.label}</td>
              {fiscalYears.map((fy) => (
                <td key={fy} className="py-2 px-3 text-right">
                  {formatCurrency(dept.amounts[fy]?.[row.key] ?? 0)}
                </td>
              ))}
              {prev && (
                <td className="py-2 px-3 text-right">
                  {pctChange(current[row.key], prev[row.key])}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>

    </div>
  );
}
