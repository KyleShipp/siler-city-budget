# Siler City, NC Budget Explorer

Interactive budget transparency tool for Siler City, North Carolina. Turns the adopted budget into searchable tables, interactive charts, department comparisons, a fund overview, selected fees, and a property tax receipt estimate.

**Live:** https://kyleshipp.github.io/siler-city-budget/

## Features

| Page | What it does |
|------|-------------|
| **Overview** | Dashboard with total budget, per-capita spending, revenue/department breakdown, and budget highlights |
| **Compare Years** | Side-by-side spending and revenue comparison across fiscal years with $ and % changes |
| **Tax Base** | Current parcel assessed-value mix by property type and gross rate-equivalent amounts |
| **Value per Acre** | Map parcel value density, draw a polygon to highlight fully encompassed properties, and estimate annual Town and County property taxes |
| **Your Receipt** | Look up your property via Chatham County GIS and estimate the Siler City portion of your tax bill |
| **Fund Overview** | Review all five annually budgeted funds |
| **Fee Schedule** | Searchable highlights from the adopted fee schedule |
| **About** | Methodology, data sources, and limitations |

## Parcel Area Analysis

The value-per-acre map is 720 pixels tall and preserves the current viewport
when drawing, completing, or clearing an analysis. Click to place vertices,
then double-click the final point to close and analyze, or use **Analyze
polygon** after placing at least three points. Normal double-click zoom is
disabled only while drawing. Results remove the selection sketch and shade
the exact counted parcel geometries purple; **Clear analysis** removes them.

Estimated annual taxes use the fiscal year and Town/County rates in
`public/data/taxbase.json`: selected assessed value divided by 100, multiplied
by each rate, with no collection-rate discount. Only Town tax goes to Siler
City. These are estimates, not actual bills or collections; parcel-specific
exemptions, relief, special districts, fees, and collection losses are not
modeled. Built floor area is unavailable in the map dataset and source CAMA
parcel service. Land acreage cannot substitute for building square footage.

## Data Coverage

| Fiscal Year | Status |
|-------------|--------|
| FY 2025-2026 | Adopted |
| FY 2026-2027 | Adopted |

The explorer's detailed views focus on the General Fund. FY 2026-2027 figures
are from the [adopted budget](https://www.silercity.gov/ArchiveCenter/ViewFile/Item/71),
unanimously approved by the Board of Commissioners on May 18, 2026. The
General Fund totals $15.0 million; the all-funds budget totals $33.3 million.

## Tech Stack

- **Next.js 14** (App Router, static export)
- **React 18** + **TypeScript**
- **Recharts** for charts
- **Tailwind CSS** for styling
- **Chatham County GIS** for parcel lookups and Siler City tax-district identification

## Running Locally

```bash
npm install
npm run dev     # http://localhost:3000
npm run build   # Static export to /out
```

## Updating Data

1. Update the extracted values in `build_data.py`
2. Run `python build_data.py` to regenerate the JSON files in `public/data/`:
   - `meta.json` — municipality info, tax rates, fiscal year definitions
   - `summary.json` — high-level FY summaries
   - `budget.json` — revenue line items and department expenditures
   - `fees.json` — selected fee schedule highlights
3. Run `python generate_taxbase.py` to refresh `taxbase.json` from Chatham County GIS
4. Run `python generate_value_per_acre.py` to refresh the parcel map GeoJSON
5. Run `npm run build`
6. Push to `main` — GitHub Actions deploys automatically

## Deployment

Deploys to GitHub Pages via `.github/workflows/deploy.yml` on push to `main`.
Production basePath: `/siler-city-budget`.

## Disclaimer

This is an independent civic data tool, not an official Town of Siler City publication. Data is sourced from publicly available budget documents. For official information, visit [silercity.gov](https://www.silercity.gov).
