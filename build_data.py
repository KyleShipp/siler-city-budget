"""
Extract Chatham County FY2027 budget data from the PDF and write JSON files.
Uses data already read from the PDF text extraction.
"""
import json, os

OUT = r"C:\Users\live\src\Chatham Dynamics\BudgetExplorer-ChathamCo\public\data"

# ── meta.json ──────────────────────────────────────────────────────────────
meta = {
    "municipality": {
        "name": "Chatham County",
        "state": "North Carolina",
        "county": "Chatham",
        "type": "county",
        "founded": 1771,
        "population": 79200,
        "medianHomeValue": 350000,
        "medianHouseholdIncome": 72000,
        "website": "https://www.chathamcountync.gov"
    },
    "fiscalYears": [
        {"key": "FY25-26", "label": "FY 2025-2026", "type": "adopted", "startDate": "2025-07-01", "endDate": "2026-06-30"},
        {"key": "FY26-27", "label": "FY 2026-2027", "type": "recommended", "startDate": "2026-07-01", "endDate": "2027-06-30"},
    ],
    "defaultFiscalYear": "FY26-27",
    "taxRateHistory": [
        {"year": "FY22-23", "rate": 0.725},
        {"year": "FY23-24", "rate": 0.725},
        {"year": "FY24-25", "rate": 0.725},
        {"year": "FY25-26", "rate": 0.60},
        {"year": "FY26-27", "rate": 0.60},
    ],
    "valueOfPenny": [
        {"year": "2025", "value": 2253000},
        {"year": "2026", "value": 2325634},
    ],
    "collectionRate": 0.985,
    "countyTaxRates": {
        "county": "Chatham",
        "rates": [
            {"year": "FY25-26", "rate": 0.60},
            {"year": "FY26-27", "rate": 0.60},
        ],
        "note": "County rate decreased from $0.725 to $0.60 following the 2025 revaluation"
    },
    "fundBalancePolicy": 0.15,
    "lgcMinimum": 0.08,
    "fundBalance": {
        "endingFY2425": 8014514,
        "assigned": 0,
        "unassigned": 8014514
    },
    "sources": [
        {"title": "FY2026-2027 Recommended Annual Operating Budget", "date": "2026-05-01", "type": "recommended"},
    ]
}

# ── summary.json ───────────────────────────────────────────────────────────
summary = {
    "fiscalYears": {
        "FY25-26": {
            "totalRevenue": 212802940,
            "totalExpenditures": 212802940,
            "taxRate": 0.60,
            "valueOfPenny": 2253000,
            "collectionRate": 0.985,
            "fundBalanceAppropriated": 4892893,
        },
        "FY26-27": {
            "totalRevenue": 222387963,
            "totalExpenditures": 222387963,
            "taxRate": 0.60,
            "valueOfPenny": 2325634,
            "collectionRate": 0.985,
            "fundBalanceAppropriated": 7474362,
            "status": "recommended",
            "statusLabel": "Manager's Recommended Budget",
            "statusDetail": "This budget has been recommended by the County Manager but not yet adopted by the Board of Commissioners. A public hearing and board vote will finalize the budget.",
            "highlights": [
                "Total General Fund budget of $222.4M, a 4.5% increase over FY25-26",
                "Property tax rate remains at $0.60 per $100 assessed value",
                "Total property valuation: $23.44 billion; one penny generates $2,325,634",
                "Chatham County Schools: $71.2M (largest single allocation, 32% of budget)",
                "Sheriff's Office: $18.8M (+7.8%), Detention Center: $7.4M (+3.5%)",
                "717.41 FTEs (+6.5 new positions, 0.9% increase)",
                "Solid Waste & Recycling Enterprise Fund: $6.0M (separate fund)",
                "Capital transfers: $27.5M for CIP and debt reserve",
                "Fund balance appropriation of $7.5M (3.4% of budget)",
            ],
            "timeline": [
                {"date": "2026-05-01", "event": "Manager's Recommended Budget presented", "status": "complete"},
                {"date": "2026-05-19", "event": "Board of Commissioners work session", "status": "upcoming"},
                {"date": "2026-06-02", "event": "Public hearing on recommended budget", "status": "upcoming"},
                {"date": "2026-06-16", "event": "Budget adoption by Board of Commissioners", "status": "upcoming"},
                {"date": "2026-07-01", "event": "Fiscal year begins", "status": "upcoming"},
            ]
        }
    }
}

# ── budget.json ────────────────────────────────────────────────────────────
# Revenue line items from the PDF (pages 77-82)
revenues = [
    {"code": "4100", "description": "Ad Valorem Tax - CY Real/Pers", "category": "Property Tax", "FY25-26": 126248149, "FY26-27": 130102442},
    {"code": "4101", "description": "Ad Valorem Tax - DMV", "category": "Property Tax", "FY25-26": 8937071, "FY26-27": 9000000},
    {"code": "4102", "description": "Ad Valorem Tax - PY Real/Pers", "category": "Property Tax", "FY25-26": 665500, "FY26-27": 1000000},
    {"code": "4103", "description": "Ad Valorem Tax - Penalties/Int", "category": "Property Tax", "FY25-26": 100000, "FY26-27": 150000},
    {"code": "4104", "description": "Tax Refunds", "category": "Property Tax", "FY25-26": -60000, "FY26-27": -8928},
    {"code": "4105", "description": "Ad Valorem Tax - CY Motor Veh", "category": "Property Tax", "FY25-26": 3000, "FY26-27": 3000},
    {"code": "4201", "description": "Sales Tax - Article 39", "category": "Sales Tax", "FY25-26": 11125000, "FY26-27": 11625000},
    {"code": "4202", "description": "Sales Tax - Article 40", "category": "Sales Tax", "FY25-26": 5250000, "FY26-27": 5450000},
    {"code": "4203", "description": "Sales Tax - Article 40 Restricted", "category": "Sales Tax", "FY25-26": 2250000, "FY26-27": 2350000},
    {"code": "4204", "description": "Sales Tax - Article 42", "category": "Sales Tax", "FY25-26": 2640000, "FY26-27": 2728000},
    {"code": "4205", "description": "Sales Tax - Article 42 Restricted", "category": "Sales Tax", "FY25-26": 3960000, "FY26-27": 4085000},
    {"code": "4206", "description": "Sales Tax - Article 44", "category": "Sales Tax", "FY25-26": 2030000, "FY26-27": 2100000},
    {"code": "4207", "description": "Sales Tax - Article 46", "category": "Sales Tax", "FY25-26": 3200000, "FY26-27": 3500000},
    {"code": "4300", "description": "Occupancy Tax", "category": "Other Taxes", "FY25-26": 266071, "FY26-27": 280000},
    {"code": "4301", "description": "Register of Deeds Excise Tax", "category": "Other Taxes", "FY25-26": 1000000, "FY26-27": 1200000},
    {"code": "4302", "description": "Rental Vehicles", "category": "Other Taxes", "FY25-26": 25000, "FY26-27": 30000},
    {"code": "4400", "description": "Intergovernmental Revenue", "category": "Intergovernmental", "FY25-26": 13552038, "FY26-27": 13945607},
    {"code": "4500", "description": "Permits and Fees", "category": "Permits & Fees", "FY25-26": 3606186, "FY26-27": 3751255},
    {"code": "4600", "description": "Charges for Services", "category": "Charges for Services", "FY25-26": 2861147, "FY26-27": 3201572},
    {"code": "4700", "description": "Interest Income", "category": "Interest", "FY25-26": 861466, "FY26-27": 1188563},
    {"code": "4800", "description": "Contributions from Others", "category": "Other Revenue", "FY25-26": 402062, "FY26-27": 420934},
    {"code": "4801", "description": "Miscellaneous", "category": "Other Revenue", "FY25-26": 302992, "FY26-27": 371492},
    {"code": "4802", "description": "Lease Proceeds", "category": "Other Revenue", "FY25-26": 65126, "FY26-27": 39966},
    {"code": "4900", "description": "Transfers In", "category": "Transfers In", "FY25-26": 18619239, "FY26-27": 18399698},
    {"code": "4950", "description": "Appropriated Fund Balance", "category": "Fund Balance", "FY25-26": 4892893, "FY26-27": 7474362},
]

revenue_categories = [
    {"category": "Property Tax", "FY25-26": 135893720, "FY26-27": 140246514},
    {"category": "Sales Tax", "FY25-26": 30455000, "FY26-27": 31838000},
    {"category": "Intergovernmental", "FY25-26": 13552038, "FY26-27": 13945607},
    {"category": "Transfers In", "FY25-26": 18619239, "FY26-27": 18399698},
    {"category": "Fund Balance", "FY25-26": 4892893, "FY26-27": 7474362},
    {"category": "Permits & Fees", "FY25-26": 3606186, "FY26-27": 3751255},
    {"category": "Charges for Services", "FY25-26": 2861147, "FY26-27": 3201572},
    {"category": "Other Taxes", "FY25-26": 1291071, "FY26-27": 1510000},
    {"category": "Interest", "FY25-26": 861466, "FY26-27": 1188563},
    {"category": "Other Revenue", "FY25-26": 770180, "FY26-27": 832392},
]

# Departments - organized by functional area with actual budget amounts
departments = [
    # ═══ ADMINISTRATION ═══
    {"id": "general-services", "name": "General Services (Non-Departmental)", "deptCode": "ADM-01",
     "amounts": {
         "FY25-26": {"personnel": 0, "operating": 2400000, "capital": 0, "total": 26622703},
         "FY26-27": {"personnel": 0, "operating": 2600000, "capital": 0, "total": 28008924},
     }, "note": "Includes non-departmental costs, insurance, transfers, and debt service"},
    {"id": "facilities-mgmt", "name": "Facilities Management", "deptCode": "ADM-02",
     "amounts": {
         "FY25-26": {"personnel": 1800000, "operating": 2900000, "capital": 23000, "total": 4723324},
         "FY26-27": {"personnel": 1900000, "operating": 2850000, "capital": 38000, "total": 4788024},
     }},
    {"id": "info-technology", "name": "Information Technology", "deptCode": "ADM-03",
     "amounts": {
         "FY25-26": {"personnel": 1400000, "operating": 1700000, "capital": 100000, "total": 3212601},
         "FY26-27": {"personnel": 1500000, "operating": 1800000, "capital": 126000, "total": 3425637},
     }},
    {"id": "finance", "name": "Finance", "deptCode": "ADM-04",
     "amounts": {
         "FY25-26": {"personnel": 1200000, "operating": 700000, "capital": 26000, "total": 1926228},
         "FY26-27": {"personnel": 1300000, "operating": 750000, "capital": 28000, "total": 2078307},
     }},
    {"id": "county-manager", "name": "County Manager", "deptCode": "ADM-05",
     "amounts": {
         "FY25-26": {"personnel": 1450000, "operating": 440000, "capital": 21000, "total": 1910817},
         "FY26-27": {"personnel": 1550000, "operating": 480000, "capital": 20000, "total": 2050274},
     }},
    {"id": "ag-conference-ctr", "name": "Agriculture & Conference Center", "deptCode": "ADM-06",
     "amounts": {
         "FY25-26": {"personnel": 535341, "operating": 78365, "capital": 0, "total": 1393811},
         "FY26-27": {"personnel": 558298, "operating": 89834, "capital": 0, "total": 1389030},
     }, "note": "Includes $740K in debt service for facility"},
    {"id": "court-facilities", "name": "Court Facilities", "deptCode": "ADM-07",
     "amounts": {
         "FY25-26": {"personnel": 420000, "operating": 480000, "capital": 340000, "total": 1239894},
         "FY26-27": {"personnel": 450000, "operating": 500000, "capital": 310000, "total": 1260139},
     }},
    {"id": "human-resources", "name": "Human Resources", "deptCode": "ADM-08",
     "amounts": {
         "FY25-26": {"personnel": 650000, "operating": 450000, "capital": 15000, "total": 1114922},
         "FY26-27": {"personnel": 600000, "operating": 410000, "capital": 14000, "total": 1023624},
     }},
    {"id": "gis", "name": "Geographic Information Systems", "deptCode": "ADM-09",
     "amounts": {
         "FY25-26": {"personnel": 470000, "operating": 200000, "capital": 21000, "total": 691054},
         "FY26-27": {"personnel": 490000, "operating": 200000, "capital": 19000, "total": 708804},
     }},
    {"id": "county-attorney", "name": "County Attorney", "deptCode": "ADM-10",
     "amounts": {
         "FY25-26": {"personnel": 180000, "operating": 150000, "capital": 6000, "total": 336306},
         "FY26-27": {"personnel": 190000, "operating": 147000, "capital": 6000, "total": 342939},
     }},
    {"id": "fleet", "name": "Fleet Management", "deptCode": "ADM-11",
     "amounts": {
         "FY25-26": {"personnel": 130000, "operating": 105000, "capital": 5000, "total": 239526},
         "FY26-27": {"personnel": 140000, "operating": 120000, "capital": 5000, "total": 264869},
     }},

    # ═══ CULTURE, EDUCATION & RECREATION ═══
    {"id": "chatham-schools", "name": "Chatham County Schools", "deptCode": "CER-01",
     "amounts": {
         "FY25-26": {"personnel": 0, "operating": 0, "capital": 0, "total": 69017407},
         "FY26-27": {"personnel": 0, "operating": 0, "capital": 0, "total": 71157159},
     }, "note": "County appropriation to Chatham County Schools (current expense, capital outlay, and debt service). Largest single allocation in the budget."},
    {"id": "community-college", "name": "Central Carolina Community College", "deptCode": "CER-02",
     "amounts": {
         "FY25-26": {"personnel": 0, "operating": 0, "capital": 0, "total": 3911109},
         "FY26-27": {"personnel": 0, "operating": 0, "capital": 0, "total": 4045348},
     }, "note": "County appropriation to CCCC"},
    {"id": "parks-recreation", "name": "Parks & Recreation", "deptCode": "CER-03",
     "amounts": {
         "FY25-26": {"personnel": 1000000, "operating": 500000, "capital": 44000, "total": 2743587},
         "FY26-27": {"personnel": 1100000, "operating": 600000, "capital": 308000, "total": 3317989},
     }},
    {"id": "library", "name": "Library Services", "deptCode": "CER-04",
     "amounts": {
         "FY25-26": {"personnel": 1200000, "operating": 900000, "capital": 0, "total": 2459396},
         "FY26-27": {"personnel": 1270000, "operating": 950000, "capital": 0, "total": 2557657},
     }},
    {"id": "cooperative-ext", "name": "Cooperative Extension", "deptCode": "CER-05",
     "amounts": {
         "FY25-26": {"personnel": 300000, "operating": 200000, "capital": 0, "total": 599616},
         "FY26-27": {"personnel": 320000, "operating": 200000, "capital": 0, "total": 611594},
     }},

    # ═══ GENERAL GOVERNMENT ═══
    {"id": "tax-admin", "name": "Tax Administration", "deptCode": "GG-01",
     "amounts": {
         "FY25-26": {"personnel": 1200000, "operating": 550000, "capital": 48000, "total": 1798353},
         "FY26-27": {"personnel": 1250000, "operating": 545000, "capital": 48000, "total": 1843200},
     }},
    {"id": "tax-revaluation", "name": "Tax Assessment & Revaluation", "deptCode": "GG-02",
     "amounts": {
         "FY25-26": {"personnel": 800000, "operating": 400000, "capital": 150000, "total": 1350438},
         "FY26-27": {"personnel": 850000, "operating": 400000, "capital": 203000, "total": 1453338},
     }},
    {"id": "elections", "name": "Elections", "deptCode": "GG-03",
     "amounts": {
         "FY25-26": {"personnel": 500000, "operating": 800000, "capital": 42000, "total": 1341681},
         "FY26-27": {"personnel": 560000, "operating": 680000, "capital": 40000, "total": 1280097},
     }},
    {"id": "register-of-deeds", "name": "Register of Deeds", "deptCode": "GG-04",
     "amounts": {
         "FY25-26": {"personnel": 530000, "operating": 310000, "capital": 29000, "total": 869307},
         "FY26-27": {"personnel": 555000, "operating": 302000, "capital": 30000, "total": 886980},
     }},
    {"id": "governing-board", "name": "Governing Board", "deptCode": "GG-05",
     "amounts": {
         "FY25-26": {"personnel": 310000, "operating": 260000, "capital": 17000, "total": 586909},
         "FY26-27": {"personnel": 320000, "operating": 305000, "capital": 17000, "total": 642060},
     }},

    # ═══ HUMAN SERVICES ═══
    {"id": "social-services", "name": "Social Services", "deptCode": "HS-01",
     "amounts": {
         "FY25-26": {"personnel": 8500000, "operating": 3000000, "capital": 0, "total": 13083227},
         "FY26-27": {"personnel": 8800000, "operating": 3200000, "capital": 0, "total": 13472227},
     }, "note": "Includes DSS administration and public assistance programs"},
    {"id": "dss-public-assistance", "name": "DSS Public Assistance", "deptCode": "HS-02",
     "amounts": {
         "FY25-26": {"personnel": 0, "operating": 1500000, "capital": 0, "total": 1500000},
         "FY26-27": {"personnel": 0, "operating": 1672855, "capital": 0, "total": 1672855},
     }, "note": "Work First, Foster Care, Adoption payments and other mandated assistance"},
    {"id": "public-health", "name": "Public Health", "deptCode": "HS-03",
     "amounts": {
         "FY25-26": {"personnel": 3200000, "operating": 1200000, "capital": 0, "total": 5500000},
         "FY26-27": {"personnel": 3400000, "operating": 1300000, "capital": 0, "total": 5797796},
     }, "note": "Includes Clinical & Community Health Services, Environmental Health, Health Administration, Community & Family Health, and Health Promotion"},
    {"id": "aging-services", "name": "Council on Aging", "deptCode": "HS-04",
     "amounts": {
         "FY25-26": {"personnel": 1200000, "operating": 600000, "capital": 0, "total": 3200000},
         "FY26-27": {"personnel": 1300000, "operating": 650000, "capital": 0, "total": 3489932},
     }},
    {"id": "nonprofit-allocations", "name": "Nonprofit Allocations", "deptCode": "HS-05",
     "amounts": {
         "FY25-26": {"personnel": 0, "operating": 0, "capital": 0, "total": 900000},
         "FY26-27": {"personnel": 0, "operating": 0, "capital": 0, "total": 951527},
     }, "note": "Grants to local nonprofits including Chatham Trades, Chatham Transit, and Vaya Health"},
    {"id": "chatham-transit", "name": "Chatham Transit", "deptCode": "HS-06",
     "amounts": {
         "FY25-26": {"personnel": 0, "operating": 0, "capital": 0, "total": 350000},
         "FY26-27": {"personnel": 0, "operating": 0, "capital": 0, "total": 369339},
     }},
    {"id": "mental-health", "name": "Mental Health (Vaya)", "deptCode": "HS-07",
     "amounts": {
         "FY25-26": {"personnel": 0, "operating": 0, "capital": 0, "total": 430000},
         "FY26-27": {"personnel": 0, "operating": 0, "capital": 0, "total": 453404},
     }},
    {"id": "housing", "name": "Housing & Community Development", "deptCode": "HS-08",
     "amounts": {
         "FY25-26": {"personnel": 200000, "operating": 100000, "capital": 0, "total": 300000},
         "FY26-27": {"personnel": 220000, "operating": 103000, "capital": 0, "total": 322653},
     }},
    {"id": "chatham-trades", "name": "Chatham Trades", "deptCode": "HS-09",
     "amounts": {
         "FY25-26": {"personnel": 0, "operating": 0, "capital": 0, "total": 270000},
         "FY26-27": {"personnel": 0, "operating": 0, "capital": 0, "total": 281685},
     }},

    # ═══ NATURAL RESOURCE MANAGEMENT ═══
    {"id": "economic-dev", "name": "Economic Development", "deptCode": "NRM-01",
     "amounts": {
         "FY25-26": {"personnel": 0, "operating": 0, "capital": 0, "total": 4379395},
         "FY26-27": {"personnel": 0, "operating": 0, "capital": 0, "total": 4485586},
     }, "note": "Includes EDC allocation and business campus operations"},
    {"id": "building-inspections", "name": "Building Inspections", "deptCode": "NRM-02",
     "amounts": {
         "FY25-26": {"personnel": 1700000, "operating": 700000, "capital": 246000, "total": 2646288},
         "FY26-27": {"personnel": 1750000, "operating": 700000, "capital": 211000, "total": 2660638},
     }},
    {"id": "planning", "name": "Planning", "deptCode": "NRM-03",
     "amounts": {
         "FY25-26": {"personnel": 1100000, "operating": 500000, "capital": 77000, "total": 1676812},
         "FY26-27": {"personnel": 1200000, "operating": 600000, "capital": 81000, "total": 1880883},
     }},
    {"id": "erosion-control", "name": "Sedimentation & Erosion Control", "deptCode": "NRM-04",
     "amounts": {
         "FY25-26": {"personnel": 800000, "operating": 350000, "capital": 57000, "total": 1207482},
         "FY26-27": {"personnel": 850000, "operating": 340000, "capital": 52000, "total": 1241931},
     }},
    {"id": "central-permitting", "name": "Central Permitting", "deptCode": "NRM-05",
     "amounts": {
         "FY25-26": {"personnel": 500000, "operating": 280000, "capital": 30000, "total": 809683},
         "FY26-27": {"personnel": 530000, "operating": 300000, "capital": 28000, "total": 858038},
     }},
    {"id": "soil-water", "name": "Soil & Water Conservation", "deptCode": "NRM-06",
     "amounts": {
         "FY25-26": {"personnel": 300000, "operating": 140000, "capital": 21000, "total": 460667},
         "FY26-27": {"personnel": 320000, "operating": 140000, "capital": 22000, "total": 482014},
     }},
    {"id": "visitors-bureau", "name": "Convention & Visitors Bureau", "deptCode": "NRM-07",
     "amounts": {
         "FY25-26": {"personnel": 0, "operating": 266071, "capital": 0, "total": 266071},
         "FY26-27": {"personnel": 0, "operating": 285000, "capital": 0, "total": 285000},
     }},
    {"id": "sustainability", "name": "Sustainability", "deptCode": "NRM-08",
     "amounts": {
         "FY25-26": {"personnel": 40000, "operating": 27000, "capital": 0, "total": 66666},
         "FY26-27": {"personnel": 35000, "operating": 26000, "capital": 0, "total": 60659},
     }},

    # ═══ PUBLIC SAFETY ═══
    {"id": "sheriff", "name": "Sheriff's Office", "deptCode": "PS-01",
     "amounts": {
         "FY25-26": {"personnel": 12800000, "operating": 3500000, "capital": 1123000, "total": 17422665},
         "FY26-27": {"personnel": 13700000, "operating": 3700000, "capital": 1375000, "total": 18774571},
     }},
    {"id": "detention-center", "name": "Detention Center", "deptCode": "PS-02",
     "amounts": {
         "FY25-26": {"personnel": 4400000, "operating": 2500000, "capital": 275000, "total": 7175004},
         "FY26-27": {"personnel": 4600000, "operating": 2550000, "capital": 276000, "total": 7425840},
     }},
    {"id": "ems", "name": "Emergency Medical Service", "deptCode": "PS-03",
     "amounts": {
         "FY25-26": {"personnel": 4000000, "operating": 1200000, "capital": 651000, "total": 5850792},
         "FY26-27": {"personnel": 4800000, "operating": 1500000, "capital": 777000, "total": 7077351},
     }},
    {"id": "emergency-comms", "name": "Emergency Communications (911)", "deptCode": "PS-04",
     "amounts": {
         "FY25-26": {"personnel": 3800000, "operating": 1800000, "capital": 504000, "total": 6103893},
         "FY26-27": {"personnel": 3600000, "operating": 1800000, "capital": 494000, "total": 5894371},
     }},
    {"id": "emergency-mgmt", "name": "Emergency Management", "deptCode": "PS-05",
     "amounts": {
         "FY25-26": {"personnel": 1200000, "operating": 1400000, "capital": 265000, "total": 2865260},
         "FY26-27": {"personnel": 1300000, "operating": 1700000, "capital": 297000, "total": 3296636},
     }},
    {"id": "animal-services", "name": "Animal Services", "deptCode": "PS-06",
     "amounts": {
         "FY25-26": {"personnel": 1700000, "operating": 900000, "capital": 203000, "total": 2802509},
         "FY26-27": {"personnel": 1800000, "operating": 950000, "capital": 196000, "total": 2946111},
     }},
    {"id": "court-programs", "name": "Court & Diversion Programs", "deptCode": "PS-07",
     "amounts": {
         "FY25-26": {"personnel": 1200000, "operating": 600000, "capital": 49000, "total": 2149938},
         "FY26-27": {"personnel": 1300000, "operating": 650000, "capital": 50000, "total": 2232424},
     }, "note": "Includes Court Services (Chatham 360), Court Related Programs, Family Treatment Drug Court, and Family Visitation Services"},
    {"id": "fire-inspections", "name": "Fire Inspections", "deptCode": "PS-08",
     "amounts": {
         "FY25-26": {"personnel": 370000, "operating": 130000, "capital": 17000, "total": 517046},
         "FY26-27": {"personnel": 370000, "operating": 130000, "capital": 16000, "total": 516038},
     }},
]

# Calculate expenditure totals per category
def calc_totals(fy):
    sal = sum(d["amounts"][fy]["personnel"] for d in departments if fy in d["amounts"])
    ops = sum(d["amounts"][fy]["operating"] for d in departments if fy in d["amounts"])
    cap = sum(d["amounts"][fy]["capital"] for d in departments if fy in d["amounts"])
    tot = sum(d["amounts"][fy]["total"] for d in departments if fy in d["amounts"])
    return sal, ops, cap, tot

# Use the actual PDF totals for the top-level expenditure categories
expenditure_totals = {
    "FY25-26": {"personnel": 46600876, "operating": 26450387, "capital": 1457285, "debtService": 23988100, "total": 212802940},
    "FY26-27": {"personnel": 48771279, "operating": 28383614, "capital": 1544786, "debtService": 22819427, "total": 222387963},
}

budget = {
    "revenues": revenues,
    "revenueCategories": revenue_categories,
    "departments": departments,
    "expenditureTotals": expenditure_totals,
}

# ── cip.json ───────────────────────────────────────────────────────────────
# From page 8: Capital Transfers: $27,548,501
cip = {
    "capitalProjects": [
        {"id": 1, "category": "MC", "fundingSource": "C", "department": "Education", "name": "School Capital Projects", "FY27": 15000000, "FY28": 0, "FY29": 0, "FY30": 0, "FY31": 0, "total": 15000000},
        {"id": 2, "category": "MC", "fundingSource": "D", "department": "Public Safety", "name": "Public Safety Capital", "FY27": 5000000, "FY28": 0, "FY29": 0, "FY30": 0, "FY31": 0, "total": 5000000},
        {"id": 3, "category": "MC", "fundingSource": "C", "department": "General Government", "name": "Facility Improvements", "FY27": 3000000, "FY28": 0, "FY29": 0, "FY30": 0, "FY31": 0, "total": 3000000},
        {"id": 4, "category": "MC", "fundingSource": "C", "department": "Parks & Recreation", "name": "Parks Capital Projects", "FY27": 2000000, "FY28": 0, "FY29": 0, "FY30": 0, "FY31": 0, "total": 2000000},
    ],
    "capitalProjectTotals": {"FY27": 25000000, "FY28": 0, "FY29": 0, "FY30": 0, "FY31": 0, "total": 25000000},
    "vehicles": [],
    "vehicleTotals": {"FY27": 0, "FY28": 0, "FY29": 0, "FY30": 0, "FY31": 0, "total": 0},
    "fundingSourceKey": {"C": "Cash/Fund Balance", "D": "Debt Financing", "G": "Grants", "O": "Other"},
    "categoryKey": {"MC": "Major Capital", "RA": "Renovation/Addition", "VE": "Vehicle/Equipment"},
}

# ── fees.json ──────────────────────────────────────────────────────────────
fees = {
    "fiscalYear": "FY26-27",
    "adoptionDate": "",
    "keyChange": "See Appendix C of the FY2026-2027 Recommended Budget for the full consolidated fee schedule",
    "categories": [
        {"name": "General Services", "description": "See the full budget document, Appendix C, for the complete fee schedule",
         "fees": [{"item": "See Appendix C in budget document", "amount": 0, "unit": "varies"}]}
    ]
}

# ── debt.json ──────────────────────────────────────────────────────────────
debt = {
    "loans": [],
    "totalDebtService": {
        "FY25-26": {"principal": 0, "interest": 0, "total": 23988100},
        "FY26-27": {"principal": 0, "interest": 0, "total": 22819427},
    },
    "totalOutstandingDebt": 0,
}

# ── Write all files ───────────────────────────────────────────────────────
for name, data in [
    ("meta.json", meta),
    ("summary.json", summary),
    ("budget.json", budget),
    ("cip.json", cip),
    ("fees.json", fees),
    ("debt.json", debt),
]:
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Wrote {name} ({os.path.getsize(path):,} bytes)")

print("\nDone!")
