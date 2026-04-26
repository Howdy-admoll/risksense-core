#!/usr/bin/env python3
"""
RiskSense Example 1: Individual Borrower Scoring

Demonstrates:
- Instantiating the model
- Scoring single borrowers
- Interpreting results
- Generating detailed assessment reports

Use case: Loan officer reviewing a borrower application
"""

from risksense import create_model


def score_borrower(
    name: str,
    income: float,
    dti: float,
    credit: float,
    stability: float,
) -> str:
    """Score a borrower and generate a detailed report."""
    model = create_model()
    score, category = model.score(income, dti, credit, stability)

    # Determine lending recommendation
    if category == 'Low':
        recommendation = 'APPROVE'
        terms = 'Standard terms, competitive rates'
    elif category == 'Medium':
        recommendation = 'APPROVE (Conditional)'
        terms = 'Enhanced monitoring, rate premium of 2–3%, higher documentation'
    else:
        recommendation = 'DECLINE or Enhanced Due Diligence'
        terms = 'Requires senior review, may require collateral or guarantor'

    # Risk factors assessment
    risk_factors = []
    if income < 1.5:
        risk_factors.append('Low annual income (₦ < 1.5M)')
    if dti > 0.65:
        risk_factors.append('High debt burden (DTI > 65%)')
    if credit < 40:
        risk_factors.append('Poor credit history')
    if stability < 3:
        risk_factors.append('Unstable employment')

    positive_factors = []
    if income > 3.5:
        positive_factors.append('Strong annual income')
    if dti < 0.35:
        positive_factors.append('Conservative debt levels')
    if credit > 75:
        positive_factors.append('Good credit track record')
    if stability > 7.5:
        positive_factors.append('Stable long-term employment')

    # Generate report
    report = f"""
{'='*70}
RISKSENSE CREDIT RISK ASSESSMENT
{'='*70}
Borrower:                    {name}
Assessment Date:             (Current)

INPUTS
{'-'*70}
Annual Income (₦M):          {income:>6.2f}
Debt-to-Income Ratio:        {dti:>6.2%}
Credit History Score:        {credit:>6.0f}/100
Employment Stability (0–10): {stability:>6.1f}

ASSESSMENT RESULTS
{'-'*70}
Risk Score:                  {score:>6.1f}/100
Risk Category:               {category:>6s}
Lending Decision:            {recommendation}
Recommended Terms:           {terms}

RISK ANALYSIS
{'-'*70}
Risk Factors Identified:
"""

    if risk_factors:
        for rf in risk_factors:
            report += f"  ⚠ {rf}\n"
    else:
        report += "  ✓ No major risk factors detected\n"

    report += "\nPositive Factors:\n"
    if positive_factors:
        for pf in positive_factors:
            report += f"  ✓ {pf}\n"
    else:
        report += "  (Limited positive factors; focus on mitigating risks)\n"

    report += f"""
{'-'*70}
RATIONALE:
Based on Mamdani fuzzy inference analysis of income capacity, debt 
service ratio, credit behavior, and employment stability, the model 
assesses overall credit risk at {score:.1f}/100 ({category}).

Lending decisions should incorporate:
1. Regulatory compliance (CBN fintech guidelines)
2. Portfolio risk management objectives
3. Loan product type and tenor
4. Collateral availability and secondary recovery

{'='*70}
"""
    return report


if __name__ == '__main__':
    # Example borrowers
    borrowers = [
        {
            'name': 'Chinedu Okafor (Tech Startup Founder)',
            'income': 3.5,
            'dti': 0.35,
            'credit': 80,
            'stability': 7.0,
        },
        {
            'name': 'Amina Hassan (Small Trader)',
            'income': 1.2,
            'dti': 0.60,
            'credit': 50,
            'stability': 4.5,
        },
        {
            'name': 'Tunde Adeyemi (Salaried Professional)',
            'income': 2.8,
            'dti': 0.40,
            'credit': 72,
            'stability': 8.5,
        },
        {
            'name': 'Zainab Mohammed (Recent Grad, Gig Work)',
            'income': 0.8,
            'dti': 0.55,
            'credit': 35,
            'stability': 2.5,
        },
    ]

    print("\nRISKSENSE BATCH ASSESSMENT REPORT")
    print("=" * 70)
    print(f"Total Borrowers to Assess: {len(borrowers)}\n")

    for borrower in borrowers:
        report = score_borrower(**borrower)
        print(report)
