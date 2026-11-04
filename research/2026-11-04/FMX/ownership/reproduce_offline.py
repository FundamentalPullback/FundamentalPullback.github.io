#!/usr/bin/env python3
"""Recompute this ownership package from included minimal facts only.

Python 3.9+, standard library, no network or complete filings. Inputs are
read-only. Results and independent numerical checks are written to --output.
Reported facts, valuation assumptions and unresolved qualitative flags remain
inputs, not claims independently re-verified by this arithmetic reproduction.
"""
import argparse
import copy
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path
import sys

REQUIRED = (
    'ownership_minimal_inputs.json', 'kof_source_facts.csv',
    'kof_history_source_facts.csv', 'kof_ttm_inputs.csv',
    'kof_history_3fy_quarters.csv', 'capital_bridge.csv',
    'additional_equity_bridge.csv', 'kof_normalization_adjustments.csv',
    'october_dividends_bridge.csv', 'QA_Flags.csv',
)
TOL = Decimal('0.000001')
D = lambda x: Decimal(str(x))

def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames), list(reader)

def write_csv(path, fields, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def jsonable(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj == obj.to_integral_value() else float(obj)
    if isinstance(obj, dict):
        return {k: jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    return obj

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, default=None)
    args = parser.parse_args()
    base = args.input.resolve()
    out = (args.output or base / 'reproduced').resolve()
    if out == base:
        parser.error('--output must differ from --input; original inputs are read-only')
    missing = [name for name in REQUIRED if not (base / name).is_file()]
    if missing:
        parser.error('Missing required files: ' + ', '.join(missing))
    out.mkdir(parents=True, exist_ok=True)
    payload = json.loads((base / REQUIRED[0]).read_text(encoding='utf-8'), parse_float=Decimal)
    checks = []
    def check(name, actual, expected, tolerance=TOL):
        if actual is None or expected is None or expected == '':
            ok = (actual is None) and (expected is None or expected == '')
            delta = ''
        else:
            delta = D(actual) - D(expected)
            ok = abs(delta) <= tolerance
        checks.append({'check': name, 'actual': actual, 'expected': expected,
                       'difference': delta, 'status': 'PASS' if ok else 'FAIL'})
    def index_facts(filename):
        _, rows = read_csv(base / filename)
        facts = {}
        for row in rows:
            key = (row['metric'], row['period'])
            val = D(row['value'])
            if key in facts and facts[key] != val:
                raise ValueError('Conflicting minimal facts: ' + str(key))
            facts[key] = val
        return facts

    # TTM standalone series: source facts where available; selected rounded
    # lease/management series are clearly-labelled inputs in the TTM CSV.
    facts = index_facts('kof_source_facts.csv')
    fields, original_ttm = read_csv(base / 'kof_ttm_inputs.csv')
    ttm = []
    for original in original_ttm:
        row = dict(original)
        for period in ('FY2025', '9M2026', '9M2025'):
            if (row['metric'], period) in facts:
                row[period] = facts[row['metric'], period]
                check('TTM input ' + row['metric'] + ' ' + period,
                      row[period], original[period])
            else:
                row[period] = D(row[period]) if row[period] else None
        vals = [row[x] for x in ('FY2025', '9M2026', '9M2025')]
        row['TTM2026Q3'] = vals[0] + vals[1] - vals[2] if all(x is not None for x in vals) else None
        check('TTM ' + row['metric'], row['TTM2026Q3'], original['TTM2026Q3'])
        ttm.append(row)
    write_csv(out / 'kof_ttm_inputs.csv', fields, ttm)
    ttm_index = {x['metric']: x for x in ttm}

    # Annual and quarterly histories. Reported quarter facts are distinct from
    # quarters derived by differencing cumulative statements.
    history_facts = index_facts('kof_history_source_facts.csv')
    fields, original_history = read_csv(base / 'kof_history_3fy_quarters.csv')
    histories = {}
    derived_metrics = {'gross_cash_capex', 'cfo_less_gross_capex'}
    calc_periods = {'Q42025_derived_FY_less_9M', 'Q12026', 'Q22026', 'Q32026', 'TTM2026Q3'}
    period_fields = [x for x in fields if x not in ('metric', 'unit', 'note')]
    for original in original_history:
        if original['metric'] in derived_metrics:
            continue
        row = dict(original)
        for period in period_fields:
            if period not in calc_periods:
                row[period] = history_facts.get((row['metric'], period))
        row['Q42025_derived_FY_less_9M'] = row['FY2025'] - row['9M2025']
        row['Q12026'] = row['3M2026']
        row['Q22026'] = row['6M2026'] - row['3M2026']
        row['Q32026'] = row['9M2026'] - row['6M2026']
        row['TTM2026Q3'] = row['FY2025'] + row['9M2026'] - row['9M2025']
        histories[row['metric']] = row
    for original in original_history:
        key = original['metric']
        if key not in derived_metrics:
            continue
        row = dict(original)
        for period in period_fields:
            ppe = histories['cash_ppe_gross'][period]
            intangible = histories['cash_intangibles_gross'][period]
            cfo = histories['cfo'][period]
            if ppe is None or intangible is None or (key == 'cfo_less_gross_capex' and cfo is None):
                row[period] = None
            else:
                row[period] = ppe + intangible if key == 'gross_cash_capex' else cfo - ppe - intangible
        histories[key] = row
    ordered_history = []
    for original in original_history:
        row = histories[original['metric']]
        for period in period_fields:
            check('History ' + row['metric'] + ' ' + period, row[period], original[period])
        four_q = sum(row[x] for x in ('Q42025_derived_FY_less_9M', 'Q12026', 'Q22026', 'Q32026'))
        check('Four quarters tie ' + row['metric'], four_q, row['TTM2026Q3'])
        ordered_history.append(row)
    write_csv(out / 'kof_history_3fy_quarters.csv', fields, ordered_history)

    # Rebuild arithmetic balance-sheet differences without treating every
    # difference as a valid economic valuation adjustment.
    for filename, result_column in [('capital_bridge.csv', 'difference'),
                                    ('additional_equity_bridge.csv', 'ex_KOF_difference')]:
        fields, originals = read_csv(base / filename)
        rows = []
        for original in originals:
            row = dict(original)
            row['FEMSA'], row['KOF'] = D(row['FEMSA']), D(row['KOF'])
            row[result_column] = row['FEMSA'] - row['KOF']
            check(filename + ' ' + row['metric'], row[result_column], original[result_column])
            if filename == 'capital_bridge.csv' and row['metric'] in payload['capital']:
                check('Capital JSON ' + row['metric'], row[result_column],
                      payload['capital'][row['metric']]['ex_kof_difference'])
            rows.append(row)
        write_csv(out / filename, fields, rows)

    k, f = payload['kof'], payload['femsa_units']
    fraction = D(k['femsa_series_a_shares']) / D(k['total_common_shares'])
    shares_per_ads = D(k['shares_per_unit']) * D(k['units_per_ads'])
    # B unit: five B shares. BD unit: one B and four D shares.
    b_weight = D(5) * D(f['b_share_dividend_weight'])
    bd_weight = D(f['b_share_dividend_weight']) + D(4) * D(f['d_share_dividend_weight'])
    total_units = D(f['b_units']) + D(f['bd_units_outstanding'])
    ownership = {
        'kof_economic_fraction_exact': fraction,
        'kof_shares_per_ads': shares_per_ads,
        'kof_total_ads_equivalent': D(k['total_common_shares']) / shares_per_ads,
        'kof_stake_ads_equivalent': D(k['femsa_series_a_shares']) / shares_per_ads,
        'femsa_total_units_outstanding': total_units,
        'femsa_b_unit_dividend_weight': b_weight,
        'femsa_bd_unit_dividend_weight': bd_weight,
        'femsa_ads_distribution_equivalent': (D(f['bd_units_outstanding']) + D(f['b_units']) * b_weight / bd_weight) / D(f['ads_bd_units']),
        'femsa_ads_nominal_equivalent': total_units / D(f['ads_bd_units']),
    }
    for actual_key, expected in [
        ('kof_economic_fraction_exact', k['economic_fraction_exact']),
        ('kof_shares_per_ads', k['shares_per_ads']),
        ('kof_total_ads_equivalent', k['total_ads_equivalent']),
        ('kof_stake_ads_equivalent', k['femsa_stake_ads_equivalent']),
        ('femsa_total_units_outstanding', f['total_units_outstanding']),
        ('femsa_b_unit_dividend_weight', f['b_unit_dividend_weight']),
        ('femsa_bd_unit_dividend_weight', f['bd_unit_dividend_weight']),
        ('femsa_ads_distribution_equivalent', f['ads_distribution_equivalent']),
        ('femsa_ads_nominal_equivalent', f['ads_nominal_equivalent']),
    ]:
        check('Ownership ' + actual_key, ownership[actual_key], expected)
    check('Issued less treasury', D(f['total_units_issued']) - D(f['treasury_units']), total_units)
    cap = payload['capital']
    residual_nci = D(cap['nci_book']['fmx']) - D(cap['nci_book']['kof']) - D(cap['parent_equity_book']['kof']) * (1 - fraction)
    ownership['residual_ex_kof_nci_book'] = residual_nci
    check('Residual NCI', residual_nci, payload['other_nci_book_reconciliation']['residual_ex_kof_nci_book'])
    leases = {entity: D(cap['lease_current'][entity]) + D(cap['lease_noncurrent'][entity]) for entity in ('fmx', 'kof')}
    leases['ex_kof'] = leases['fmx'] - leases['kof']
    convention = payload['capital_convention']
    financial_debt = D(convention['ex_kof_debt_including_leases_pr_rounded']) - leases['ex_kof']
    net_cash = D(convention['ex_kof_cash_and_investments_pr_rounded']) - financial_debt
    check('Capital ex-KOF leases', leases['ex_kof'], convention['ex_kof_lease_liabilities'])
    check('Capital ex-KOF financial debt', financial_debt, convention['ex_kof_financial_debt_derived_approximate'])
    check('Capital ex-KOF net financial cash', net_cash, convention['ex_kof_net_financial_cash_derived_approximate'])

    # October cash bridge uses published per-unit dividends and September
    # share counts. It remains an estimate of FEMSA's actual October payout.
    div = payload['october_dividends_bridge']
    b_div = D(div['femsa_ordinary_per_b_unit']) + D(div['femsa_extraordinary_per_b_unit'])
    bd_div = D(div['femsa_ordinary_per_bd_unit']) + D(div['femsa_extraordinary_per_bd_unit'])
    fmx_out = (D(f['b_units']) * b_div + D(f['bd_units_outstanding']) * bd_div) / D(1000000)
    kof_out = D(k['total_common_shares']) * D(div['kof_per_share']) / D(1000000)
    kof_receipt = D(k['femsa_series_a_shares']) * D(div['kof_per_share']) / D(1000000)
    delta = kof_receipt - fmx_out
    for label, actual, expected in [
        ('FEMSA B unit dividend', b_div, div['femsa_total_per_b_unit']),
        ('FEMSA BD unit dividend', bd_div, div['femsa_total_per_bd_unit']),
        ('FEMSA October payout estimate', fmx_out, div['femsa_cash_outflow_estimate_using_september_shares']),
        ('KOF October payout', kof_out, div['kof_full_cash_distribution_calculated']),
        ('FEMSA receives KOF dividend', kof_receipt, div['receipt_at_femsa_calculated']),
        ('Ex-KOF October net cash delta', delta, div['ex_kof_net_october_cash_adjustment_estimated']),
    ]:
        check(label, actual, expected)
    fields, originals = read_csv(base / 'october_dividends_bridge.csv')
    events = {'KOF October distribution full company': -kof_out,
              'KOF distribution received by FEMSA': kof_receipt,
              'FEMSA dividend outflow': -fmx_out,
              'Net ex-KOF cash adjustment': delta}
    for row in originals:
        value = events[row['event']]
        check('Dividend CSV ' + row['event'], value, row['MXN_million'])
        row['MXN_million'] = value
    write_csv(out / 'october_dividends_bridge.csv', fields, originals)

    # Insurance removal is the selected reported-operating proxy. Arithmetic
    # reproduction does not resolve the disclosed IFRS perimeter differences.
    _, norm_rows = read_csv(base / 'kof_normalization_adjustments.csv')
    norm_facts = {(r['metric'], r['period']): D(r['value_mxn_million']) for r in norm_rows}
    insurance = (norm_facts['insurance_net_benefit_management', 'Q42025'] +
                 norm_facts['insurance_benefit_management', '9M2026'])
    normalized = ttm_index['ebit_ifrs_tag']['TTM2026Q3'] - insurance
    post_rent = normalized + ttm_index['rou_depreciation']['TTM2026Q3'] - ttm_index['lease_total_note']['TTM2026Q3']
    check('Insurance normalization proxy', insurance, payload['kof_normalization']['selected_ttm_insurance_adjustment_proxy'])
    check('EBIT after insurance proxy', normalized, payload['kof_normalization']['ttm_ebit_ex_insurance_proxy'])
    check('EBIT after insurance and rent proxies', post_rent, payload['kof_normalization']['ttm_cash_rent_ebit_ex_insurance_proxy'])
    calculations = {'as_of': payload['as_of'], 'ownership': ownership,
                    'capital': {'lease_liabilities': leases, 'ex_kof_financial_debt_approximate': financial_debt,
                                'ex_kof_net_financial_cash_approximate': net_cash},
                    'october_dividends': {'femsa_cash_out_estimate': fmx_out, 'kof_cash_out': kof_out,
                                         'femsa_receipt_from_kof': kof_receipt, 'net_ex_kof_cash_delta_estimate': delta},
                    'normalization': {'insurance_proxy': insurance, 'ebit_ex_insurance_proxy': normalized,
                                      'ebit_ex_insurance_cash_rent_proxy': post_rent},
                    'unresolved_input_gaps': copy.deepcopy(payload['normalization_gaps'])}
    (out / 'ownership_calculations.json').write_text(json.dumps(jsonable(calculations), indent=2) + '\n', encoding='utf-8')
    write_csv(out / 'Reproduction_Checks.csv', list(checks[0]), checks)
    qa_fields, qa_rows = read_csv(base / 'QA_Flags.csv')
    write_csv(out / 'QA_Flags.csv', qa_fields, qa_rows)
    failed = [x['check'] for x in checks if x['status'] == 'FAIL']
    report = {'status': 'PASS' if not failed else 'FAIL', 'checks': len(checks),
              'passed': len(checks) - len(failed), 'failed': failed,
              'input_files': {name: hashlib.sha256((base / name).read_bytes()).hexdigest() for name in REQUIRED},
              'network_used': False, 'complete_filings_required': False,
              'limitations': 'Arithmetic and cross-file checks only. Source authenticity, legal interpretations, selected model assumptions and qualitative QA flags are not independently re-verified. Unknown figures remain unknown.'}
    (out / 'reproduction_report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"{report['status']}: {report['passed']}/{len(checks)} checks. Outputs: {out}")
    return 0 if not failed else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as exc:
        print('Reproduction failed: ' + str(exc), file=sys.stderr)
        sys.exit(2)
