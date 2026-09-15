export interface FiscalYearMeta {
  key: string;
  label: string;
  type: 'actual' | 'adopted' | 'recommended';
  startDate: string;
  endDate: string;
}

export interface TaxRateEntry {
  year: string;
  rate: number;
}

export interface ValueOfPennyEntry {
  year: string;
  value: number;
}

export interface MetaData {
  municipality: {
    name: string;
    state: string;
    county: string;
    type: string;
    founded: number;
    population: number;
    medianHomeValue: number;
    medianHouseholdIncome: number;
    website: string;
  };
  fiscalYears: FiscalYearMeta[];
  defaultFiscalYear: string;
  taxRateHistory: TaxRateEntry[];
  valueOfPenny: ValueOfPennyEntry[];
  collectionRate: number;
  fundBalancePolicy: number;
  lgcMinimum: number;
  fundBalance: {
    endingFY2425: number;
    assigned: number;
    unassigned: number;
  };
  sources: Array<{
    title: string;
    date: string;
    type: string;
    url?: string;
  }>;
}

export interface TimelineEntry {
  date: string;
  event: string;
  status: 'complete' | 'upcoming';
}

export interface FYSummary {
  totalRevenue: number;
  totalExpenditures: number;
  taxRate: number;
  valueOfPenny: number;
  collectionRate: number;
  fundBalanceAppropriated: number;
  revenueNeutralRate?: number;
  status?: 'recommended' | 'adopted' | 'actual';
  statusLabel?: string;
  statusDetail?: string;
  timeline?: TimelineEntry[];
  highlights?: string[];
}

export interface SummaryData {
  fiscalYears: Record<string, FYSummary>;
}

export interface RevenueLineItem {
  code: string;
  description: string;
  category: string;
  [key: string]: string | number; // FY amounts
}

export interface DepartmentAmounts {
  personnel: number;
  operating: number;
  capital: number;
  total: number;
}

export interface Department {
  id: string;
  name: string;
  deptCode: string;
  amounts: Record<string, DepartmentAmounts>;
  note?: string;
}

export interface RevenueCategory {
  category: string;
  [key: string]: string | number;
}

export interface ExpenditureTotals {
  personnel: number;
  operating: number;
  capital: number;
  debtService: number;
  total: number;
}

export interface BudgetData {
  revenues: RevenueLineItem[];
  revenueCategories: RevenueCategory[];
  departments: Department[];
  expenditureTotals: Record<string, ExpenditureTotals>;
}

export interface Fee {
  item: string;
  amount: number;
  unit: string;
}

export interface FeeSubcategory {
  name: string;
  note?: string;
  fees: Fee[];
}

export interface FeeCategory {
  name: string;
  description?: string;
  note?: string;
  fees?: Fee[];
  subcategories?: FeeSubcategory[];
}

export interface FeesData {
  fiscalYear: string;
  adoptionDate: string;
  keyChange: string;
  categories: FeeCategory[];
}
