#!/usr/bin/env python3
"""Offline CBOE peer screen. Run: python comps.py [--inputs PATH] [--output-dir PATH].
All financial amounts USD millions, share counts millions, price USD/share.
No API calls, estimates, peer median or target-price calculation.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path


def compute(data):
    rows, checks = [], []
    def check(label, value):
        checks.append({'check': label, 'pass': bool(value)})
        if not value:
            raise ValueError(label)
    check('same completed session for all prices', data['market_price_date'] == '2026-11-03')
    for p in data['peers']:
        t, c = p['ticker'], p['capital']
        fy, old, new = (p['periods'][k] for k in ['fy2025','ytd2025','ytd2026'])
        fields = ['net_revenue','gaap_ebit','d_and_a_ex_acquired_amortization',
                  'acquired_intangible_amortization','common_net_income_diluted_basis','diluted_eps']
        ttm = {k: fy[k] + new[k] - old[k] for k in fields}
        for k in fields:
            check(t + ' positive TTM ' + k, ttm[k] > 0)
        check(t + ' matching client cash and liabilities',
              c['clearing_client_cash_assets_excluded'] == c['clearing_client_cash_liabilities_excluded'])
        check(t + ' matching settlement assets and liabilities',
              c['other_matched_clearing_assets_excluded'] == c['other_matched_clearing_liabilities_excluded'])
        for period in p['periods'].values():
            if 'gross_revenue' in period:
                check(t+' revenue netting '+str(period['gross_revenue']), abs(period['gross_revenue'] - period['section31_fee_expense'] - period['liquidity_routing_clearing_expense'] - period['net_revenue']) < .001)
        normalization = sum(a['amount'] for a in p['ebit_normalization_adjustments'])
        normalized_ebit = ttm['gaap_ebit'] + normalization
        check(t+' no unsupported EBIT normalization', normalization == 0)
        check(t+' no fabricated exact close-date capitalization', p['actual_market_cap_on_price_date'] is None)
        price = p['price']
        proxy_cap = price * p['q3_diluted_weighted_average_shares']
        reported_shares = p['reported_actual_class_a_shares'] + p['reported_actual_class_b_shares']
        dated_count_cap = price * reported_shares
        cash_offset = c['cash_and_equivalents_ex_restricted'] - c['pass_through_fees_in_unrestricted_cash_reserved'] - c['additional_operating_cash_reserve']
        debt = c['short_term_debt'] + c['long_term_debt'] + c['finance_lease_liabilities']
        nci = c['noncontrolling_interests_book'] + c['redeemable_noncontrolling_interests']
        ev = proxy_cap + debt + nci - cash_offset
        prefunding = c['acquisition_prefunding_restricted_cash_offset_rounded']
        funding_neutral_ev = ev - prefunding
        d_and_a = ttm['d_and_a_ex_acquired_amortization'] + ttm['acquired_intangible_amortization']
        ebitda = ttm['gaap_ebit'] + d_and_a
        check(t+' cash offset not more than unrestricted cash', 0 <= cash_offset <= c['cash_and_equivalents_ex_restricted'])
        check(t+' prefunding offset cannot exceed restricted cash', 0 <= prefunding <= c['restricted_cash_ex_client'])
        r = {
            'ticker': t, 'issuer': p['issuer'], 'peer_role': p['peer_role'],
            'price_date': data['market_price_date'], 'price_usd': price,
            'ttm_end': data['financial_period_end'],
            'q3_diluted_share_proxy_m': p['q3_diluted_weighted_average_shares'],
            'market_cap_diluted_proxy_m': proxy_cap,
            'reported_actual_shares_m': reported_shares,
            'reported_actual_share_count_date': p['actual_share_count_date'],
            'capitalization_at_close_using_dated_outstanding_count_m': dated_count_cap,
            'exact_actual_market_cap_on_price_date_m': None,
            'balance_sheet_date': c['as_of'],
            'debt_including_finance_leases_m': debt,
            'unrestricted_cash_less_pass_through_reserve_m': cash_offset,
            'net_debt_screen_m': debt - cash_offset,
            'book_nci_and_redeemable_nci_m': nci,
            'ev_diluted_proxy_ex_restricted_cash_m': ev,
            'restricted_acquisition_prefunding_offset_rounded_m': prefunding,
            'ev_after_matched_prefunding_offset_sensitivity_m': funding_neutral_ev,
            'clearing_client_assets_and_matched_liabilities_removed_m': c['clearing_client_cash_assets_excluded'] + c['other_matched_clearing_assets_excluded'],
            'ttm_net_revenue_m': ttm['net_revenue'],
            'ttm_gaap_ebit_m': ttm['gaap_ebit'],
            'ttm_normalized_ebit_m': normalized_ebit,
            'ttm_ebit_normalization_m': normalization,
            'ttm_d_and_a_total_m': d_and_a,
            'ttm_acquired_amortization_retained_in_ebit_m': ttm['acquired_intangible_amortization'],
            'ttm_mechanical_ebitda_m': ebitda,
            'ttm_common_net_income_diluted_basis_m': ttm['common_net_income_diluted_basis'],
            'ttm_reported_diluted_eps_sum_usd': ttm['diluted_eps'],
            'ttm_gaap_ebit_margin_pct': 100*ttm['gaap_ebit']/ttm['net_revenue'],
            'ytd_net_revenue_growth_pct': 100*(new['net_revenue']/old['net_revenue']-1),
            'ytd_gaap_ebit_growth_pct': 100*(new['gaap_ebit']/old['gaap_ebit']-1),
            'ev_net_revenue_x': ev/ttm['net_revenue'],
            'ev_gaap_ebit_x': ev/ttm['gaap_ebit'],
            'ev_normalized_ebit_x': ev/normalized_ebit,
            'ev_mechanical_ebitda_x': ev/ebitda,
            'ev_ebit_after_matched_prefunding_sensitivity_x': funding_neutral_ev/ttm['gaap_ebit'],
            'pe_gaap_reported_eps_sum_x': price/ttm['diluted_eps'],
            'net_debt_gaap_ebit_x': (debt-cash_offset)/ttm['gaap_ebit'],
            'investment_view': 'Screening only; not a target multiple or normalized P/E',
            'price_source_url': data['sources'][p['price_source']]['url'],
            'latest_financial_source_url': data['sources'][c['source']]['url']
        }
        rows.append({k: round(v,8) if isinstance(v,float) else v for k,v in r.items()})
    return rows, checks


def main():
    parser = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    parser.add_argument('--inputs', type=Path, default=here/'comps_inputs.json')
    parser.add_argument('--output-dir', type=Path, default=here)
    parser.add_argument('--verify-private-sources', type=Path, metavar='DIR',
                        help='Optional: verify archived source files in DIR against stored hashes. Not required for public offline reproduction.')
    args = parser.parse_args()
    data = json.loads(args.inputs.read_text())
    rows, checks = compute(data)
    # Provenance hashes are factual input metadata, not runtime dependencies.
    # Default execution never searches for, opens, or downloads full source documents.
    source_hashes = {}
    for key, src in data['sources'].items():
        valid_url = isinstance(src.get('url'), str) and src['url'].startswith('https://')
        checks.append({'check': key+' source URL supplied', 'pass': valid_url})
        if not valid_url:
            raise ValueError(key+' missing HTTPS source URL')
        if 'archived_sha256' in src:
            recorded_hash = src['archived_sha256']
            valid_hash = len(recorded_hash) == 64 and all(c in '0123456789abcdef' for c in recorded_hash)
            checks.append({'check': key+' recorded provenance hash format', 'pass': valid_hash})
            if not valid_hash:
                raise ValueError(key+' invalid recorded source hash')
            source_hashes[key] = recorded_hash
            if args.verify_private_sources is not None:
                source = args.verify_private_sources/src['archive_filename']
                ok = source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest() == recorded_hash
                checks.append({'check': key+' optional private archive matches recorded hash', 'pass': ok})
                if not ok:
                    raise ValueError('Private source absent or hash mismatch: '+str(source))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = {
        'valuation_date': data['valuation_date'],
        'price_date': data['market_price_date'],
        'financial_period_end': data['financial_period_end'],
        'units': data['financial_units'],
        'posture': data['posture'],
        'ttm_formula': 'FY2025 + YTD2026 - YTD2025',
        'ev_formula': 'price * Q3 diluted weighted-average shares + carrying debt + finance lease liabilities + book NCI + redeemable NCI - unrestricted cash + reserved pass-through fees',
        'exact_price_date_capitalization_available': False,
        'rows': rows,
        'source_sha256': source_hashes,
        'source_hash_basis': 'Previously recorded provenance hashes from inputs; default offline reproduction does not reopen source documents.'
    }
    (args.output_dir/'comps.json').write_text(json.dumps(output,indent=2)+'\n')
    with (args.output_dir/'comps.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    qa={'passed':all(x['pass'] for x in checks),'check_count':len(checks),
        'mode':'private_source_verification' if args.verify_private_sources is not None else 'public_offline_inputs_only',
        'full_source_documents_required':args.verify_private_sources is not None,
        'checks':checks}
    (args.output_dir/'qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    print(json.dumps({'rows':len(rows),'checks':len(checks),'all_pass':qa['passed'],'metrics':[{'ticker':r['ticker'],'ev_ebit':r['ev_gaap_ebit_x'],'ev_net_revenue':r['ev_net_revenue_x'],'pe_gaap':r['pe_gaap_reported_eps_sum_x']} for r in rows]},indent=2))

if __name__ == '__main__':
    main()
