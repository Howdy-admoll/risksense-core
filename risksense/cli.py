"""
RiskSense CLI — Command-line interface for credit risk scoring

Provides:
- Single borrower scoring
- Batch CSV processing
- Model introspection
- Sensitivity analysis
- Output formatting (JSON, CSV, table)

Usage:
    risksense score --income 2.5 --dti 0.4 --credit 75 --stability 8.0
    risksense batch --input borrowers.csv --output results.json
    risksense analyze --parameter income
    risksense inspect --verbose
"""

import argparse
import json
import csv
import sys
from pathlib import Path
from typing import Optional

from risksense import create_model, get_profiles


def score_single(args):
    """Score a single borrower."""
    model = create_model()

    try:
        score, category = model.score(
            annual_income=args.income,
            debt_to_income=args.dti,
            credit_score=args.credit,
            employment_stability=args.stability,
        )

        result = {
            'risk_score': round(score, 2),
            'risk_category': category,
            'inputs': {
                'annual_income': args.income,
                'debt_to_income': args.dti,
                'credit_score': args.credit,
                'employment_stability': args.stability,
            },
        }

        if args.format == 'json':
            print(json.dumps(result, indent=2))
        elif args.format == 'table':
            print("\n" + "=" * 60)
            print("RISKSENSE CREDIT RISK ASSESSMENT")
            print("=" * 60)
            print(f"Annual Income (₦M):      {args.income}")
            print(f"Debt-to-Income Ratio:    {args.dti:.2f}")
            print(f"Credit History Score:    {args.credit}")
            print(f"Employment Stability:    {args.stability}/10")
            print("-" * 60)
            print(f"RISK SCORE:              {score:.1f}/100")
            print(f"RISK CATEGORY:           {category}")
            print("=" * 60 + "\n")

        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def batch_score(args):
    """Score multiple borrowers from CSV."""
    model = create_model()

    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        return 1

    results = []

    try:
        with open(args.input, 'r') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                print("Error: CSV file is empty", file=sys.stderr)
                return 1

            required_fields = {
                'annual_income',
                'debt_to_income',
                'credit_score',
                'employment_stability',
            }
            if not required_fields.issubset(set(reader.fieldnames)):
                print(
                    f"Error: CSV must contain columns: {', '.join(required_fields)}",
                    file=sys.stderr,
                )
                return 1

            for i, row in enumerate(reader, 1):
                try:
                    score, category = model.score(
                        float(row['annual_income']),
                        float(row['debt_to_income']),
                        float(row['credit_score']),
                        float(row['employment_stability']),
                    )

                    result = {
                        'row_id': i,
                        'risk_score': round(score, 2),
                        'risk_category': category,
                        'input': row,
                    }
                    results.append(result)

                except ValueError as e:
                    print(
                        f"Warning: Row {i} skipped - {e}",
                        file=sys.stderr,
                    )
                    continue

        # Output results
        if args.output_format == 'json':
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✓ Scored {len(results)} borrowers → {args.output}")

        elif args.output_format == 'csv':
            if not results:
                print("Error: No valid results to write", file=sys.stderr)
                return 1

            with open(args.output, 'w', newline='') as f:
                fieldnames = ['row_id', 'risk_score', 'risk_category']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for result in results:
                    writer.writerow({
                        'row_id': result['row_id'],
                        'risk_score': result['risk_score'],
                        'risk_category': result['risk_category'],
                    })

            print(f"✓ Scored {len(results)} borrowers → {args.output}")

        return 0

    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def analyze_sensitivity(args):
    """Run sensitivity analysis on a parameter."""
    model = create_model()

    # Base case
    base = {
        'annual_income': 2.5,
        'debt_to_income': 0.5,
        'credit_score': 60,
        'employment_stability': 5.0,
    }

    print("\nSensitivity Analysis: {}".format(args.parameter.upper()))
    print("=" * 70)
    print(f"Base case: Income={base['annual_income']}, DTI={base['debt_to_income']}, "
          f"Credit={base['credit_score']}, Stability={base['employment_stability']}")
    print("-" * 70)

    if args.parameter == 'income':
        values = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]
        param_name = 'Annual Income (₦M)'
        for val in values:
            score, cat = model.score(val, **{k: v for k, v in base.items() if k != 'annual_income'})
            print(f"  {val:5.1f}  →  Risk: {score:5.1f}  [{cat:6s}]")

    elif args.parameter == 'dti':
        values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        param_name = 'Debt-to-Income Ratio'
        for val in values:
            score, cat = model.score(**{**base, 'debt_to_income': val})
            print(f"  {val:5.2f}  →  Risk: {score:5.1f}  [{cat:6s}]")

    elif args.parameter == 'credit':
        values = [20, 30, 40, 50, 60, 70, 80, 90, 100]
        param_name = 'Credit Score'
        for val in values:
            score, cat = model.score(**{**base, 'credit_score': val})
            print(f"  {val:5.0f}  →  Risk: {score:5.1f}  [{cat:6s}]")

    elif args.parameter == 'stability':
        values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        param_name = 'Employment Stability'
        for val in values:
            score, cat = model.score(**{**base, 'employment_stability': val})
            print(f"  {val:5.1f}  →  Risk: {score:5.1f}  [{cat:6s}]")

    print("=" * 70 + "\n")
    return 0


def inspect_model(args):
    """Inspect model structure and rules."""
    model = create_model()

    print("\n" + "=" * 70)
    print("RISKSENSE MODEL INSPECTION")
    print("=" * 70)

    print(f"\nFuzzy Logic System:")
    print(f"  Fuzzy Rules:     {len(model.rules)}")
    print(f"  Input Variables: 4")
    print(f"    - annual_income (₦0–10M)")
    print(f"    - debt_to_income (0–1)")
    print(f"    - credit_score (0–100)")
    print(f"    - employment_stability (0–10)")
    print(f"  Output Variable: 1")
    print(f"    - risk_score (0–100)")

    print(f"\nFuzzy Sets:")
    print(f"  Income:           [Low, Medium, High]")
    print(f"  DTI:              [Low, Medium, High]")
    print(f"  Credit Score:     [Poor, Fair, Good]")
    print(f"  Employment:       [Low, Medium, High]")
    print(f"  Risk Score:       [Low (0–35), Medium (36–65), High (66–100)]")

    print(f"\nTest Profiles:")
    profiles = get_profiles()
    for i, p in enumerate(profiles, 1):
        score, cat = model.score(
            p['annual_income'],
            p['debt_to_income'],
            p['credit_score'],
            p['employment_stability'],
        )
        print(f"  {i}. {p['name']:<40} → {cat} ({score:.1f})")

    print("\n" + "=" * 70 + "\n")
    return 0


def main():
    """Parse arguments and dispatch to subcommands."""
    parser = argparse.ArgumentParser(
        description='RiskSense: Fuzzy inference credit risk scoring CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Score single borrower
  risksense score --income 2.5 --dti 0.4 --credit 75 --stability 8.0

  # Batch score from CSV
  risksense batch --input borrowers.csv --output results.json

  # Sensitivity analysis
  risksense analyze --parameter income

  # Model inspection
  risksense inspect --verbose
        ''',
    )

    subparsers = parser.add_subparsers(dest='command', help='Subcommand')

    # Score command
    score_parser = subparsers.add_parser('score', help='Score a single borrower')
    score_parser.add_argument(
        '--income',
        type=float,
        required=True,
        help='Annual income in millions NGN (0–10)',
    )
    score_parser.add_argument(
        '--dti',
        type=float,
        required=True,
        help='Debt-to-income ratio (0–1)',
    )
    score_parser.add_argument(
        '--credit',
        type=float,
        required=True,
        help='Credit score (0–100)',
    )
    score_parser.add_argument(
        '--stability',
        type=float,
        required=True,
        help='Employment stability (0–10)',
    )
    score_parser.add_argument(
        '--format',
        choices=['json', 'table'],
        default='table',
        help='Output format',
    )
    score_parser.set_defaults(func=score_single)

    # Batch command
    batch_parser = subparsers.add_parser(
        'batch', help='Batch score from CSV file'
    )
    batch_parser.add_argument(
        '--input',
        required=True,
        help='Input CSV file (required columns: annual_income, debt_to_income, credit_score, employment_stability)',
    )
    batch_parser.add_argument(
        '--output',
        required=True,
        help='Output file path',
    )
    batch_parser.add_argument(
        '--output-format',
        choices=['json', 'csv'],
        default='json',
        help='Output format',
    )
    batch_parser.set_defaults(func=batch_score)

    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze', help='Sensitivity analysis'
    )
    analyze_parser.add_argument(
        '--parameter',
        choices=['income', 'dti', 'credit', 'stability'],
        required=True,
        help='Parameter to analyze',
    )
    analyze_parser.set_defaults(func=analyze_sensitivity)

    # Inspect command
    inspect_parser = subparsers.add_parser(
        'inspect', help='Inspect model structure'
    )
    inspect_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output',
    )
    inspect_parser.set_defaults(func=inspect_model)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
