import type { MetaData, SummaryData, BudgetData, FeesData, TaxBaseData } from '@/types/budget';

import metaJson from '../../public/data/meta.json';
import summaryJson from '../../public/data/summary.json';
import budgetJson from '../../public/data/budget.json';
import feesJson from '../../public/data/fees.json';
import taxBaseJson from '../../public/data/taxbase.json';

export function getMeta(): MetaData {
  return metaJson as MetaData;
}

export function getSummary(): SummaryData {
  return summaryJson as SummaryData;
}

export function getBudget(): BudgetData {
  return budgetJson as BudgetData;
}

export function getFees(): FeesData {
  return feesJson as FeesData;
}

export function getTaxBase(): TaxBaseData {
  return taxBaseJson as TaxBaseData;
}
