"""
RiskSense Test Profiles — 8 Borrower Archetypes

Synthetic profiles representing diverse borrower segments from the
fintech credit risk research dataset. Each profile is calibrated to
reflect real-world distribution patterns in African fintech lending:
- Tier 1 (SME formality): High income, established credit
- Tier 2 (Self-employed): Moderate income, variable credit
- Tier 3 (Gig/informal): Low income, thin credit files
- Edge cases: Stress scenarios, recovery arcs

These profiles are used for:
1. Unit test validation (assert correct risk categories)
2. Model calibration and sensitivity analysis
3. Academic paper case studies (IEEE format)
4. Product documentation and lender training

Research context: University of Portsmouth Advanced AI Module
IEEE format research paper on Mamdani fuzzy inference for fintech
"""


def get_profiles() -> list[dict]:
    """
    Return 8 representative borrower profiles.

    Each profile dict contains:
    - name (str): Profile identifier
    - description (str): Borrower context (Nigerian fintech cohort)
    - annual_income (float): Income in millions NGN
    - debt_to_income (float): DTI ratio (0–1)
    - credit_score (float): Credit history score (0–100)
    - employment_stability (float): Stability index (0–10)
    - expected_category (str): Expected risk outcome ("Low"/"Medium"/"High")

    Returns:
        list[dict]: Test profiles
    """
    return [
        {
            'name': 'Profile 1: Premium SME Owner',
            'description': (
                'Registered manufacturing SME in Lagos; ₦4.2M annual income; '
                'strong BVN history; 3-year loan repayment track record; '
                'stable business entity with 5+ employees'
            ),
            'annual_income': 4.2,
            'debt_to_income': 0.25,
            'credit_score': 85,
            'employment_stability': 9.0,
            'expected_category': 'Low',
        },
        {
            'name': 'Profile 2: Mid-Market Salaried Professional',
            'description': (
                'Banking sector employee; ₦2.8M annual gross salary; '
                'DTI 40% (mortgage + auto); FICO-equivalent 72; '
                '8 years tenure at reputable institution'
            ),
            'annual_income': 2.8,
            'debt_to_income': 0.40,
            'credit_score': 72,
            'employment_stability': 8.5,
            'expected_category': 'Low',
        },
        {
            'name': 'Profile 3: Emerging Trader (Conditional Risk)',
            'description': (
                'E-commerce/trading vendor; ₦1.8M estimated annual turnover; '
                'DTI 55% (supplier credit + personal loans); thin credit file (score 58); '
                '3 years business operation; moderate employment instability'
            ),
            'annual_income': 1.8,
            'debt_to_income': 0.55,
            'credit_score': 58,
            'employment_stability': 5.5,
            'expected_category': 'Medium',
        },
        {
            'name': 'Profile 4: Gig Economy / Freelancer',
            'description': (
                'Freelance/gig platform worker; ₦0.9M variable monthly (~₦10.8M annualized, '
                'but volatile); DTI 60% (multiple micro-loans); minimal formal credit history (42); '
                'no fixed employment; 2 years platform tenure'
            ),
            'annual_income': 0.9,
            'debt_to_income': 0.60,
            'credit_score': 42,
            'employment_stability': 4.0,
            'expected_category': 'Medium',
        },
        {
            'name': 'Profile 5: Recent Graduate (Thin Credit)',
            'description': (
                'Entry-level employee, ₦1.2M salary (< 2 years tenure); '
                'DTI 35% (student loan repayment); no prior credit history (score 50); '
                'low employment stability; represents growth-market segment'
            ),
            'annual_income': 1.2,
            'debt_to_income': 0.35,
            'credit_score': 50,
            'employment_stability': 3.0,
            'expected_category': 'Medium',
        },
        {
            'name': 'Profile 6: Recovering Borrower',
            'description': (
                'Previously defaulted; now re-employed; ₦1.5M income; '
                'DTI 65% (paying off old arrears); credit score recovering (45); '
                '18-month positive repayment history; moderate stability'
            ),
            'annual_income': 1.5,
            'debt_to_income': 0.65,
            'credit_score': 45,
            'employment_stability': 4.5,
            'expected_category': 'High',
        },
        {
            'name': 'Profile 7: High-Risk Distressed',
            'description': (
                'Informal sector worker; ₦0.4M estimated income; '
                'DTI 75% (overleveraged); poor credit history (28 — multiple defaults); '
                'unstable employment (seasonal/contract work); high default risk'
            ),
            'annual_income': 0.4,
            'debt_to_income': 0.75,
            'credit_score': 28,
            'employment_stability': 2.0,
            'expected_category': 'High',
        },
        {
            'name': 'Profile 8: Business Owner (Moderate Risk)',
            'description': (
                'Established small business (agro-processing); ₦3.1M annual revenue; '
                'DTI 50% (equipment finance + working capital loans); fair credit (65); '
                'business stability 6 years; moderate employment stability (rural context)'
            ),
            'annual_income': 3.1,
            'debt_to_income': 0.50,
            'credit_score': 65,
            'employment_stability': 6.5,
            'expected_category': 'Medium',
        },
    ]


def get_profile_by_name(name: str) -> dict | None:
    """
    Retrieve a single profile by name.

    Args:
        name (str): Profile name (e.g., "Profile 1: Premium SME Owner")

    Returns:
        dict | None: Profile dict, or None if not found
    """
    for profile in get_profiles():
        if profile['name'] == name:
            return profile
    return None


def get_profiles_by_category(category: str) -> list[dict]:
    """
    Filter profiles by expected risk category.

    Args:
        category (str): "Low", "Medium", or "High"

    Returns:
        list[dict]: Matching profiles
    """
    return [
        p for p in get_profiles() if p['expected_category'] == category
    ]
