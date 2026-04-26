#!/usr/bin/env python3
"""
RiskSense Example 2: Batch Processing Portfolio

Demonstrates:
- Loading borrower data from CSV
- Batch scoring with efficiency
- Portfolio risk statistics
- Exporting results

Use case: Analyzing a lending portfolio for risk concentration,
regulatory reporting, and strategic adjustments
"""

import csv
import json
from pathlib import Path
from risksense import create_model


def create_sample_portfolio_csv(output_path: str = 'examples/sample_portfolio.csv'):
    """Create a sample portfolio CSV for demonstration."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Sample portfolio of 20 borrowers
    borrowers = [
        ('Borrower001', 4.5, 0.25, 85, 9.0),  # Low risk
        ('Borrower002', 3.2, 0.35, 78, 8.5),  # Low risk
        ('Borrower003', 2.8, 0.40, 72, 8.0),  # Low risk
        ('Borrower004', 2.5, 0.45, 68, 7.5),  # Medium risk
        ('Borrower005', 2.0, 0.50, 60, 6.5),  # Medium risk
        ('Borrower006', 1.8, 0.55, 58, 5.5),  # Medium risk
        ('Borrower007', 1.5, 0.60, 50, 4.5),  # Medium risk
        ('Borrower008', 1.2, 0.55, 48, 4.0),  # Medium risk
        ('Borrower009', 1.0, 0.65, 42, 3.5),  # Medium-High risk
        ('Borrower010', 0.8, 0.70, 35, 2.5),  # High risk
        ('Borrower011', 5.2, 0.20, 88, 9.5),  # Low risk
        ('Borrower012', 3.8, 0.38, 75, 8.2),  # Low risk
        ('Borrower013', 2.3, 0.48, 65, 6.8),  # Medium risk
        ('Borrower014', 1.6, 0.52, 55, 5.0),  # Medium risk
        ('Borrower015', 0.9, 0.72, 40, 3.0),  # High risk
        ('Borrower016', 4.0, 0.30, 82, 8.8),  # Low risk
        ('Borrower017', 2.2, 0.50, 62, 6.0),  # Medium risk
        ('Borrower018', 1.3, 0.58, 48, 4.2),  # Medium risk
        ('Borrower019', 0.7, 0.75, 30, 2.0),  # High risk
        ('Borrower020', 3.0, 0.42, 70, 7.5),  # Low-Medium risk
    ]

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['borrower_id', 'annual_income', 'debt_to_income', 'credit_score', 'employment_stability'])
        writer.writerows(borrowers)

    return output_path


def analyze_portfolio(csv_path: str):
    """Load and analyze a portfolio CSV."""
    model = create_model()

    # Load portfolio
    borrowers = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            borrowers.append({
                'id': row['borrower_id'],
                'income': float(row['annual_income']),
                'dti': float(row['debt_to_income']),
                'credit': float(row['credit_score']),
                'stability': float(row['employment_stability']),
            })

    print(f"\n{'='*70}")
    print(f"RISKSENSE PORTFOLIO ANALYSIS")
    print(f"{'='*70}")
    print(f"Portfolio Size: {len(borrowers)} borrowers\n")

    # Score all borrowers
    results = []
    for borrower in borrowers:
        score, category = model.score(
            borrower['income'],
            borrower['dti'],
            borrower['credit'],
            borrower['stability'],
        )
        results.append({
            'id': borrower['id'],
            'risk_score': score,
            'risk_category': category,
            'income': borrower['income'],
            'dti': borrower['dti'],
            'credit': borrower['credit'],
            'stability': borrower['stability'],
        })

    # Calculate statistics
    low_count = sum(1 for r in results if r['risk_category'] == 'Low')
    medium_count = sum(1 for r in results if r['risk_category'] == 'Medium')
    high_count = sum(1 for r in results if r['risk_category'] == 'High')

    avg_score = sum(r['risk_score'] for r in results) / len(results)
    min_score = min(r['risk_score'] for r in results)
    max_score = max(r['risk_score'] for r in results)

    avg_income = sum(r['income'] for r in results) / len(results)
    avg_dti = sum(r['dti'] for r in results) / len(results)
    avg_credit = sum(r['credit'] for r in results) / len(results)
    avg_stability = sum(r['stability'] for r in results) / len(results)

    # Print summary
    print(f"PORTFOLIO COMPOSITION")
    print(f"{'-'*70}")
    print(f"Low Risk:       {low_count:>3d}  ({100*low_count/len(results):>5.1f}%)")
    print(f"Medium Risk:    {medium_count:>3d}  ({100*medium_count/len(results):>5.1f}%)")
    print(f"High Risk:      {high_count:>3d}  ({100*high_count/len(results):>5.1f}%)")

    print(f"\nRISK STATISTICS")
    print(f"{'-'*70}")
    print(f"Average Risk Score:   {avg_score:>6.1f}/100")
    print(f"Min Risk Score:       {min_score:>6.1f}/100")
    print(f"Max Risk Score:       {max_score:>6.1f}/100")
    print(f"Risk Range:           {max_score - min_score:>6.1f}")

    print(f"\nBORROWER CHARACTERISTICS")
    print(f"{'-'*70}")
    print(f"Avg Annual Income:    ₦{avg_income:>6.2f}M")
    print(f"Avg DTI Ratio:        {100*avg_dti:>6.1f}%")
    print(f"Avg Credit Score:     {avg_credit:>6.1f}")
    print(f"Avg Employment Stab:  {avg_stability:>6.2f}/10")

    # Risk concentration by category
    print(f"\nCONCENTRATION ANALYSIS")
    print(f"{'-'*70}")
    if low_count > 0:
        low_avg_income = sum(r['income'] for r in results if r['risk_category'] == 'Low') / low_count
        print(f"Low Risk:     Avg Income ₦{low_avg_income:.2f}M, Count {low_count}")
    if medium_count > 0:
        med_avg_income = sum(r['income'] for r in results if r['risk_category'] == 'Medium') / medium_count
        print(f"Medium Risk:  Avg Income ₦{med_avg_income:.2f}M, Count {medium_count}")
    if high_count > 0:
        high_avg_income = sum(r['income'] for r in results if r['risk_category'] == 'High') / high_count
        print(f"High Risk:    Avg Income ₦{high_avg_income:.2f}M, Count {high_count}")

    # Export detailed results
    output_json = 'examples/portfolio_results.json'
    with open(output_json, 'w') as f:
        json.dump({
            'summary': {
                'total_borrowers': len(borrowers),
                'low_risk_count': low_count,
                'medium_risk_count': medium_count,
                'high_risk_count': high_count,
                'avg_risk_score': avg_score,
                'min_risk_score': min_score,
                'max_risk_score': max_score,
            },
            'results': results,
        }, f, indent=2)

    print(f"\n{'='*70}")
    print(f"✓ Detailed results exported to: {output_json}")
    print(f"{'='*70}\n")

    # Print top 5 highest risk
    print(f"TOP 5 HIGHEST RISK BORROWERS")
    print(f"{'-'*70}")
    top_risk = sorted(results, key=lambda x: x['risk_score'], reverse=True)[:5]
    for i, r in enumerate(top_risk, 1):
        print(f"{i}. {r['id']:<15} Risk: {r['risk_score']:>5.1f} ({r['risk_category']})")

    # Print recommendations
    print(f"\n{'='*70}")
    print(f"PORTFOLIO RECOMMENDATIONS")
    print(f"{'-'*70}")

    if high_count / len(results) > 0.15:
        print("⚠ High-risk concentration > 15% — consider risk mitigation:")
        print("  - Enhanced monitoring for high-risk segment")
        print("  - Collateral requirements or guarantor")
        print("  - Rate premium or loan size reduction")

    if avg_score > 55:
        print("⚠ Portfolio average risk score > 55 — portfolio is above median risk")
        print("  - Review origination criteria")
        print("  - Consider enhanced underwriting")

    if avg_dti > 0.55:
        print("⚠ Average DTI > 55% — borrowers heavily leveraged")
        print("  - Risk of simultaneous default if external shocks occur")

    print(f"\n{'='*70}\n")


if __name__ == '__main__':
    # Create sample portfolio
    csv_path = create_sample_portfolio_csv()
    print(f"✓ Created sample portfolio: {csv_path}")

    # Analyze it
    analyze_portfolio(csv_path)
