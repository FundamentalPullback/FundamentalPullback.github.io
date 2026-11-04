# EAT historical ledger
USD millions except EPS. Three fiscal years and quarters/TTM derive from SEC companyfacts observations explicitly tagged to10-K/10-Q accession/date/start/end. Numeric inputs retain those source records; raw fullcompanyfacts is not distributed. Annual FY24/FY25/FY26 all52weeks. Q1FY27is13weeks;52weekTTM does not include future53rdweek inFY27.
Run rebuild_history.py offline. Annual andQ1/Q2/Q3 EPS are direct; Q4/TTM EPS are null, not annual-minus-nine-month arithmetic. D&A tag switches between Depreciation and CostOfGoodsAndServicesSoldDepreciationAndAmortization and is checked against displayed annual/Q1 totals. Cash capex excludes assets obtained through financeleases and restaurant acquisitions: add those separately where economically appropriate. CFO−PPE−SBC is not ownerFCF.
Annual source: https://www.sec.gov/Archives/edgar/data/703351/000070335126000029/eat-20260624.htm
Latest Q1: https://www.sec.gov/Archives/edgar/data/703351/000070335126000040/eat-20260923.htm
SECcompanyfacts: https://data.sec.gov/api/xbrl/companyfacts/CIK0000703351.json
Every raw observation in numeric_inputs.json retains filing accession, form, date and metric tag; quarter flows are differences of consecutive cumulative cashflow statements. Q4 is annual minus9M. Preserve reported rounding; do not treat normalized margins, taxes or discount rates as historical source facts.
