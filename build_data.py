"""Write verified Siler City FY2026-2027 budget data to JSON."""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "data")

meta = {
    "municipality": {
        "name": "Siler City",
        "state": "North Carolina",
        "county": "Chatham",
        "type": "town",
        "founded": 1887,
        "population": 7702,
        "medianHomeValue": 200000,
        "medianHouseholdIncome": 0,
        "website": "https://www.silercity.gov",
    },
    "fiscalYears": [
        {"key": "FY25-26", "label": "FY 2025-2026", "type": "adopted", "startDate": "2025-07-01", "endDate": "2026-06-30"},
        {"key": "FY26-27", "label": "FY 2026-2027", "type": "adopted", "startDate": "2026-07-01", "endDate": "2027-06-30"},
    ],
    "defaultFiscalYear": "FY26-27",
    "taxRateHistory": [
        {"year": "FY25-26", "rate": 0.54},
        {"year": "FY26-27", "rate": 0.54},
    ],
    "valueOfPenny": [
        {"year": "FY26-27", "value": 139899},
    ],
    "collectionRate": 1.0,
    "fundBalancePolicy": 0.20,
    "lgcMinimum": 0.08,
    "fundBalance": {
        "endingFY2425": 0,
        "assigned": 0,
        "unassigned": 0,
    },
    "sources": [
        {
            "title": "Fiscal Year 2026-2027 Adopted Budget",
            "date": "2026-05-18",
            "type": "adopted",
            "url": "https://www.silercity.gov/ArchiveCenter/ViewFile/Item/71",
        },
        {
            "title": "May 18, 2026 Board of Commissioners Minutes",
            "date": "2026-05-18",
            "type": "minutes",
            "url": "https://www.silercity.gov/AgendaCenter/ViewFile/Minutes/_05182026-881",
        },
    ],
}

summary = {
    "fiscalYears": {
        "FY25-26": {
            "totalRevenue": 13903098,
            "totalExpenditures": 13903098,
            "taxRate": 0.54,
            "valueOfPenny": 139899,
            "collectionRate": 1.0,
            "fundBalanceAppropriated": 283855,
            "status": "adopted",
        },
        "FY26-27": {
            "totalRevenue": 15036518,
            "totalExpenditures": 15036518,
            "taxRate": 0.54,
            "valueOfPenny": 139899,
            "collectionRate": 1.0,
            "fundBalanceAppropriated": 827294,
            "status": "adopted",
            "statusLabel": "Adopted Budget",
            "statusDetail": "The Board of Commissioners unanimously approved the FY2026-2027 budget on May 18, 2026. This explorer focuses on the $15.0M General Fund within the Town's $33.3M all-funds budget.",
            "highlights": [
                "Adopted General Fund budget of $15.0M, an 8.2% increase over FY25-26",
                "The Town's adopted all-funds budget totals $33.3M across five funds",
                "Property tax rate remains at $0.54 per $100 assessed value",
                "Police is the largest operating department at $3.29M",
                "Non-departmental appropriations total $4.54M",
                "Water and Sewer Fund totals $17.59M during the Tri-River Water transition",
                "General Fund uses $827,294 of appropriated fund balance",
            ],
            "timeline": [
                {"date": "2026-05-04", "event": "Manager's recommended budget presented", "status": "complete"},
                {"date": "2026-05-18", "event": "Public hearing and unanimous budget adoption", "status": "complete"},
                {"date": "2026-07-01", "event": "Fiscal year began", "status": "complete"},
            ],
        },
    }
}

revenue_categories = [
    {"category": "Ad Valorem Taxes", "FY25-26": 7219000, "FY26-27": 7537800},
    {"category": "Unrestricted Intergovernmental", "FY25-26": 4201000, "FY26-27": 4371129},
    {"category": "Sales & Services", "FY25-26": 965093, "FY26-27": 1044495},
    {"category": "Restricted Intergovernmental", "FY25-26": 771000, "FY26-27": 758500},
    {"category": "Fund Balance", "FY25-26": 283855, "FY26-27": 827294},
    {"category": "Investment Earnings", "FY25-26": 228950, "FY26-27": 304250},
    {"category": "Transfers In", "FY25-26": 170200, "FY26-27": 150200},
    {"category": "Permits & Fees", "FY25-26": 61000, "FY26-27": 37850},
    {"category": "Miscellaneous", "FY25-26": 1000, "FY26-27": 3000},
    {"category": "Other Taxes & Licenses", "FY25-26": 2000, "FY26-27": 2000},
]

revenues = [
    {
        "code": f"REV-{index + 1:02d}",
        "description": item["category"],
        "category": item["category"],
        "FY25-26": item["FY25-26"],
        "FY26-27": item["FY26-27"],
    }
    for index, item in enumerate(revenue_categories)
]

department_rows = [
    ("governing-body", "Governing Body", "400", 109115, 142061),
    ("administration", "Administration & Human Resources", "405", 636506, 683505),
    ("finance", "Finance", "410", 654142, 637838),
    ("planning", "Planning & Community Development", "490", 473618, 478305),
    ("buildings-grounds", "Buildings & Grounds", "500", 1277977, 1147539),
    ("police", "Police", "510", 3265873, 3294209),
    ("fire", "Fire", "530", 1200471, 1319805),
    ("garage", "Garage", "555", 122449, 114672),
    ("public-works", "Public Works / Streets", "560", 734194, 672343),
    ("sanitation", "Sanitation", "580", 715163, 1027894),
    ("parks-recreation", "Parks & Recreation", "620", 738745, 826552),
    ("airport", "Airport", "650", 74645, 74395),
    ("non-departmental", "Non-Departmental", "660", 3820700, 4537400),
    ("debt-service", "Debt / Transfers", "850", 79500, 80000),
]

departments = [
    {
        "id": dept_id,
        "name": name,
        "deptCode": code,
        "amounts": {
            "FY25-26": {"personnel": 0, "operating": prior, "capital": 0, "total": prior},
            "FY26-27": {"personnel": 0, "operating": current, "capital": 0, "total": current},
        },
        "note": "The source budget publishes the adopted departmental total; line-item composition is available in the official budget document.",
    }
    for dept_id, name, code, prior, current in department_rows
]

budget = {
    "revenues": revenues,
    "revenueCategories": revenue_categories,
    "departments": departments,
    "expenditureTotals": {
        "FY25-26": {"personnel": 10002898, "operating": 3820700, "capital": 0, "debtService": 79500, "total": 13903098},
        "FY26-27": {"personnel": 10419118, "operating": 4537400, "capital": 0, "debtService": 80000, "total": 15036518},
    },
}

fees = {
    "fiscalYear": "FY26-27",
    "adoptionDate": "2026-05-18",
    "keyChange": "The adopted schedule includes updated recreation, planning, solid waste, and utility rates. The Board discussed Spring Chicken Festival vendor pricing before unanimously adopting the budget.",
    "categories": [
        {
            "name": "Parks & Recreation Programs",
            "fees": [
                {"item": "Youth Flag Football", "amount": 35, "unit": "participant"},
                {"item": "Tackle Football", "amount": 60, "unit": "participant"},
                {"item": "Youth Basketball", "amount": 20, "unit": "participant"},
                {"item": "Youth Baseball / Softball", "amount": 35, "unit": "participant"},
                {"item": "Swimming Lessons", "amount": 65, "unit": "participant"},
                {"item": "Swimming Pool Admission", "amount": 5, "unit": "person"},
                {"item": "Swimming Pool Family Season Pass", "amount": 230, "unit": "household"},
            ],
        },
        {
            "name": "Facility & Field Rentals",
            "fees": [
                {"item": "Ernest Ramsey Gym", "amount": 30, "unit": "hour"},
                {"item": "Park Pavilion", "amount": 25, "unit": "hour"},
                {"item": "Two-hour Pool Rental", "amount": 200, "unit": "event"},
                {"item": "Baseball / Softball Field without lights", "amount": 40, "unit": "hour"},
                {"item": "Baseball / Softball Field with lights", "amount": 75, "unit": "hour"},
                {"item": "Athletic Tournament Complex", "amount": 750, "unit": "day"},
            ],
        },
        {
            "name": "Community Development & Planning",
            "fees": [
                {"item": "Abatement Fee", "amount": 180, "unit": "case"},
                {"item": "Floodplain Development Permit", "amount": 100, "unit": "permit"},
                {"item": "Street Closing Petition (NCGS 160A-299)", "amount": 1700, "unit": "petition"},
                {"item": "Annexation Petition", "amount": 250, "unit": "petition"},
                {"item": "Conditional Zoning", "amount": 700, "unit": "application"},
                {"item": "Rezoning", "amount": 600, "unit": "application"},
                {"item": "Text Amendment", "amount": 1000, "unit": "application"},
                {"item": "Variance", "amount": 450, "unit": "application"},
                {"item": "Watershed Protection Permit", "amount": 50, "unit": "permit"},
                {"item": "Zoning Certification Letter", "amount": 150, "unit": "letter"},
                {"item": "New Single- or Two-Family Zoning Permit", "amount": 75, "unit": "permit"},
            ],
        },
        {
            "name": "Public Works & General Services",
            "fees": [
                {"item": "Residential Solid Waste and Recycling Cart", "amount": 269, "unit": "year"},
                {"item": "Commercial Solid Waste and Recycling Cart", "amount": 359, "unit": "year"},
                {"item": "Encroachment Agreement", "amount": 100, "unit": "agreement"},
                {"item": "Roll-Off Waste Container", "amount": 300, "unit": "container plus tipping"},
                {"item": "False Fire Alarm - Excessive Calls", "amount": 500, "unit": "call"},
                {"item": "Fingerprint Card - Town Resident", "amount": 5, "unit": "card"},
                {"item": "Yard Sale Permit", "amount": 5, "unit": "permit"},
            ],
        },
        {
            "name": "Utility Service Area",
            "description": "Published with the Town budget; utility operations are transitioning to Tri-River Water.",
            "fees": [
                {"item": "Account Deposit", "amount": 75, "unit": "account"},
                {"item": "Residential Water Base - Inside Town", "amount": 31.24, "unit": "month"},
                {"item": "Residential Water Usage - Inside Town", "amount": 6.35, "unit": "1,000 gallons"},
                {"item": "Residential Sewer Base - Inside Town", "amount": 21.21, "unit": "month"},
                {"item": "Residential Sewer Usage - Inside Town", "amount": 8.81, "unit": "1,000 gallons"},
                {"item": "3/4-inch Water Tap", "amount": 1350, "unit": "tap"},
                {"item": "4-inch Sewer Tap", "amount": 1750, "unit": "tap"},
                {"item": "Late Fee", "amount": 5, "unit": "occurrence"},
                {"item": "Delinquent Fee", "amount": 25, "unit": "occurrence"},
            ],
        },
    ],
}

for name, data in [
    ("meta.json", meta),
    ("summary.json", summary),
    ("budget.json", budget),
    ("fees.json", fees),
]:
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2)
        output.write("\n")
    print(f"Wrote {name} ({os.path.getsize(path):,} bytes)")
