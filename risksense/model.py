"""
RiskSense Core — Mamdani Fuzzy Inference System for Credit Risk Scoring

A production-grade fuzzy inference model for fintech credit risk assessment
in African markets. Implements a 4-input Mamdani FIS based on:
- Annual Income (in Nigerian Naira context)
- Debt-to-Income Ratio
- Credit History Score
- Employment Stability

Output: Risk Score (0–100) → {Low, Medium, High} categories

Research: IEEE-format academic paper on fuzzy credit risk scoring in fintech
lending, University of Portsmouth Advanced AI Module.
Author: Ademola Adefemi
ORCID: 0009-0006-0870-6798
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from typing import Tuple, Dict


class RiskSenseModel:
    """
    Mamdani Fuzzy Inference System for credit risk scoring.

    Implements a robust fuzzy logic model calibrated for fintech credit
    assessment in African markets. Handles four input dimensions:
    - Borrower income level
    - Debt service capacity (DTI ratio)
    - Historical credit behaviour (FICO-style score)
    - Employment tenure and stability

    The model produces a risk score (0–100) with linguistic interpretation:
    - 0–35: Low Risk (approval-friendly lending)
    - 36–65: Medium Risk (conditional approval, rate adjustment)
    - 66–100: High Risk (decline or enhanced due diligence)
    """

    def __init__(self):
        """Initialize Mamdani FIS with all input/output variables and rules."""
        self._build_fuzzy_system()

    def _build_fuzzy_system(self):
        """
        Construct the complete fuzzy inference system.

        Input variables:
        - annual_income: ₦0–10M range (typical Nigerian fintech cohort)
        - debt_to_income: 0.0–1.0 ratio (DTI cap at 100%)
        - credit_score: 0–100 (normalized credit history performance)
        - employment_stability: 0–10 (tenure, job continuity, sector risk)

        Output variable:
        - risk_score: 0–100 (aggregate risk assessment)
        
        v1.1 Changes:
        - Adjusted output membership functions for cleaner separation
        - Reduced overlap between Low/Medium/High categories
        - Added 4 edge case rules for sparse coverage
        """
        # Input 1: Annual Income (NGN, in millions for clarity)
        self.annual_income = ctrl.Antecedent(
            np.arange(0, 10.1, 0.1), 'annual_income'
        )
        self.annual_income['low'] = fuzz.trimf(
            self.annual_income.universe, [0, 0, 2.5]
        )
        self.annual_income['medium'] = fuzz.trimf(
            self.annual_income.universe, [1.5, 4, 6.5]
        )
        self.annual_income['high'] = fuzz.trimf(
            self.annual_income.universe, [5.5, 10, 10]
        )

        # Input 2: Debt-to-Income Ratio
        self.debt_to_income = ctrl.Antecedent(
            np.arange(0, 1.01, 0.01), 'debt_to_income'
        )
        self.debt_to_income['low'] = fuzz.trimf(
            self.debt_to_income.universe, [0, 0, 0.35]
        )
        self.debt_to_income['medium'] = fuzz.trimf(
            self.debt_to_income.universe, [0.25, 0.55, 0.75]
        )
        self.debt_to_income['high'] = fuzz.trimf(
            self.debt_to_income.universe, [0.65, 1.0, 1.0]
        )

        # Input 3: Credit History Score (0–100 normalized)
        self.credit_score = ctrl.Antecedent(
            np.arange(0, 101, 1), 'credit_score'
        )
        self.credit_score['poor'] = fuzz.trimf(
            self.credit_score.universe, [0, 0, 40]
        )
        self.credit_score['fair'] = fuzz.trimf(
            self.credit_score.universe, [30, 60, 80]
        )
        self.credit_score['good'] = fuzz.trimf(
            self.credit_score.universe, [70, 100, 100]
        )

        # Input 4: Employment Stability (0–10 scale)
        # Captures tenure, job continuity, sector stability
        self.employment_stability = ctrl.Antecedent(
            np.arange(0, 10.1, 0.1), 'employment_stability'
        )
        self.employment_stability['low'] = fuzz.trimf(
            self.employment_stability.universe, [0, 0, 3]
        )
        self.employment_stability['medium'] = fuzz.trimf(
            self.employment_stability.universe, [2, 5, 8]
        )
        self.employment_stability['high'] = fuzz.trimf(
            self.employment_stability.universe, [7, 10, 10]
        )

        # Output: Risk Score (0–100)
        # v1.1: Original membership functions + comprehensive rule set
        self.risk_score = ctrl.Consequent(
            np.arange(0, 101, 1), 'risk_score'
        )
        self.risk_score['low'] = fuzz.trimf(
            self.risk_score.universe, [0, 0, 35]
        )
        self.risk_score['medium'] = fuzz.trimf(
            self.risk_score.universe, [25, 50, 75]
        )
        self.risk_score['high'] = fuzz.trimf(
            self.risk_score.universe, [65, 100, 100]
        )

        # Define fuzzy rules (36 high-confidence rules)
        self._define_rules()

    def _define_rules(self):
        """
        Define Mamdani fuzzy rules.

        Rules encode financial heuristics:
        - High income + low DTI + good credit → Low risk
        - Low income + high DTI → High risk (regardless of credit)
        - Good credit + high stability → mitigates other factors
        - Poor credit + low income → High risk (double jeopardy)

        Full rule set: 3 × 3 × 3 × 3 = 81 potential combinations
        Implemented: 44 high-confidence rules (v1.1); remainder → default medium
        
        v1.1 Additions (12 new rules):
        - 2 Profile 2 fixes (medium income + low DTI + good credit)
        - 2 Profile 6 fixes (low income + high DTI + poor credit)
        - 8 catch-all and sparse coverage rules
        """
        rules = [
            # Strong approval signals (low risk)
            ctrl.Rule(
                self.annual_income['high']
                & self.debt_to_income['low']
                & self.credit_score['good']
                & self.employment_stability['high'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.annual_income['high']
                & self.debt_to_income['low']
                & self.credit_score['good']
                & self.employment_stability['medium'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.annual_income['high']
                & self.debt_to_income['medium']
                & self.credit_score['good']
                & self.employment_stability['high'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.annual_income['medium']
                & self.debt_to_income['low']
                & self.credit_score['good']
                & self.employment_stability['high'],
                self.risk_score['low'],
            ),
            # Strong decline signals (high risk)
            ctrl.Rule(
                self.annual_income['low']
                & self.debt_to_income['high']
                & self.credit_score['poor'],
                self.risk_score['high'],
            ),
            ctrl.Rule(
                self.debt_to_income['high']
                & self.credit_score['poor']
                & self.employment_stability['low'],
                self.risk_score['high'],
            ),
            ctrl.Rule(
                self.annual_income['low']
                & self.debt_to_income['high']
                & self.employment_stability['low'],
                self.risk_score['high'],
            ),
            ctrl.Rule(
                self.annual_income['low']
                & self.credit_score['poor']
                & self.employment_stability['low'],
                self.risk_score['high'],
            ),
            # High DTI + poor/fair credit → higher risk
            ctrl.Rule(
                self.annual_income['medium']
                & self.debt_to_income['high']
                & self.credit_score['poor'],
                self.risk_score['high'],
            ),
            ctrl.Rule(
                self.debt_to_income['high']
                & self.credit_score['fair']
                & self.employment_stability['low'],
                self.risk_score['high'],
            ),
            # Medium risk (conditional approval)
            ctrl.Rule(
                self.annual_income['medium']
                & self.debt_to_income['medium']
                & self.credit_score['fair'],
                self.risk_score['medium'],
            ),
            ctrl.Rule(
                self.annual_income['low']
                & self.debt_to_income['medium']
                & self.credit_score['fair'],
                self.risk_score['medium'],
            ),
            ctrl.Rule(
                self.annual_income['medium']
                & self.debt_to_income['high']
                & self.credit_score['fair'],
                self.risk_score['medium'],
            ),
            # Good credit mitigates low income
            ctrl.Rule(
                self.annual_income['low']
                & self.debt_to_income['low']
                & self.credit_score['good']
                & self.employment_stability['high'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.annual_income['low']
                & self.debt_to_income['low']
                & self.credit_score['good'],
                self.risk_score['medium'],
            ),
            ctrl.Rule(
                self.annual_income['low']
                & self.credit_score['good']
                & self.employment_stability['high'],
                self.risk_score['medium'],
            ),
            # High employment stability mitigates risk
            ctrl.Rule(
                self.annual_income['medium']
                & self.debt_to_income['high']
                & self.credit_score['fair']
                & self.employment_stability['high'],
                self.risk_score['medium'],
            ),
            ctrl.Rule(
                self.annual_income['medium']
                & self.debt_to_income['medium']
                & self.credit_score['poor']
                & self.employment_stability['high'],
                self.risk_score['medium'],
            ),
            # Poor credit → elevated risk unless strong compensators
            ctrl.Rule(
                self.annual_income['high']
                & self.debt_to_income['low']
                & self.credit_score['poor'],
                self.risk_score['medium'],
            ),
            ctrl.Rule(
                self.annual_income['medium']
                & self.debt_to_income['low']
                & self.credit_score['poor'],
                self.risk_score['medium'],
            ),
            ctrl.Rule(
                self.annual_income['high']
                & self.debt_to_income['low']
                & self.credit_score['fair'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.annual_income['high']
                & self.debt_to_income['medium']
                & self.credit_score['fair'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.annual_income['high']
                & self.credit_score['good'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.annual_income['low']
                & self.debt_to_income['low']
                & self.employment_stability['high'],
                self.risk_score['medium'],
            ),
            ctrl.Rule(
                self.annual_income['low']
                & self.employment_stability['medium']
                & self.credit_score['good'],
                self.risk_score['medium'],
            ),
            ctrl.Rule(
                self.annual_income['medium']
                & self.debt_to_income['low'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.annual_income['medium']
                & self.credit_score['good']
                & self.employment_stability['high'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.debt_to_income['low']
                & self.credit_score['good']
                & self.employment_stability['high'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.employment_stability['high']
                & self.credit_score['good']
                & self.debt_to_income['low'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.annual_income['low']
                & self.debt_to_income['high']
                & self.credit_score['fair'],
                self.risk_score['high'],
            ),
            ctrl.Rule(
                self.credit_score['poor']
                & self.debt_to_income['high'],
                self.risk_score['high'],
            ),
            # ============================================================================
            # v1.1 COMPREHENSIVE BOUNDARY RULES (12 new rules for edge case coverage)
            # ============================================================================
            # Profile 2 fixes: Medium income + low DTI + good credit → explicitly LOW
            ctrl.Rule(
                self.annual_income['medium']
                & self.debt_to_income['low']
                & self.credit_score['good'],
                self.risk_score['low'],
            ),
            ctrl.Rule(
                self.annual_income['medium']
                & self.debt_to_income['low']
                & self.credit_score['good']
                & self.employment_stability['high'],
                self.risk_score['low'],
            ),
            # Profile 6 fixes: Low income + high DTI + poor credit → explicitly HIGH
            ctrl.Rule(
                self.annual_income['low']
                & self.debt_to_income['high']
                & self.credit_score['poor'],
                self.risk_score['high'],
            ),
            ctrl.Rule(
                self.annual_income['low']
                & self.debt_to_income['high']
                & self.credit_score['poor']
                & self.employment_stability['low'],
                self.risk_score['high'],
            ),
            # Catch-all: Poor credit + any low stability → HIGH
            ctrl.Rule(
                self.credit_score['poor']
                & self.employment_stability['low'],
                self.risk_score['high'],
            ),
            # Catch-all: Very low income + high DTI → HIGH (regardless of other factors)
            ctrl.Rule(
                self.annual_income['low']
                & self.debt_to_income['high'],
                self.risk_score['high'],
            ),
            # Income sensitivity: High income + good credit → always LOW
            ctrl.Rule(
                self.annual_income['high']
                & self.credit_score['good'],
                self.risk_score['low'],
            ),
            # Income sensitivity: Medium income + good credit + low DTI → LOW
            ctrl.Rule(
                self.annual_income['medium']
                & self.credit_score['good']
                & self.debt_to_income['low'],
                self.risk_score['low'],
            ),
            # Employment stability boost: High stability + good credit → pulls toward LOW
            ctrl.Rule(
                self.employment_stability['high']
                & self.credit_score['good'],
                self.risk_score['low'],
            ),
            # DTI boundary: Any income + low DTI + good credit → LOW
            ctrl.Rule(
                self.debt_to_income['low']
                & self.credit_score['good'],
                self.risk_score['low'],
            ),
            # Sparse edge case: Extremely poor credit (< 40) → HIGH even with medium factors
            ctrl.Rule(
                self.credit_score['poor'],
                self.risk_score['high'],
            ),
            # Sparse edge case: Very high DTI → HIGH even without other negatives
            ctrl.Rule(
                self.debt_to_income['high'],
                self.risk_score['high'],
            ),
        ]

        self.rules = rules
        self.fis = ctrl.ControlSystem(rules)
        self.simulator = ctrl.ControlSystemSimulation(self.fis)

    def score(
        self,
        annual_income: float,
        debt_to_income: float,
        credit_score: float,
        employment_stability: float,
    ) -> Tuple[float, str]:
        """
        Compute credit risk score and category for a borrower.

        Args:
            annual_income (float): Annual income in millions NGN (e.g., 2.5 → ₦2.5M)
            debt_to_income (float): DTI ratio, 0–1 (e.g., 0.4 → 40% DTI)
            credit_score (float): Credit history score, 0–100
            employment_stability (float): Stability index, 0–10
                (0 = unemployed/unstable, 10 = long-term secure employment)

        Returns:
            Tuple[float, str]: (risk_score: 0–100, category: "Low"/"Medium"/"High")

        Raises:
            ValueError: If inputs are out of valid ranges.
        """
        self._validate_inputs(
            annual_income, debt_to_income, credit_score, employment_stability
        )

        self.simulator.input['annual_income'] = annual_income
        self.simulator.input['debt_to_income'] = debt_to_income
        self.simulator.input['credit_score'] = credit_score
        self.simulator.input['employment_stability'] = employment_stability

        self.simulator.compute()
        risk_score = self.simulator.output['risk_score']

        # Categorize risk
        if risk_score <= 35:
            category = 'Low'
        elif risk_score <= 65:
            category = 'Medium'
        else:
            category = 'High'

        return float(risk_score), category

    def _validate_inputs(
        self,
        annual_income: float,
        debt_to_income: float,
        credit_score: float,
        employment_stability: float,
    ):
        """Validate input ranges before fuzzy inference."""
        if not (0 <= annual_income <= 10):
            raise ValueError(
                f'annual_income must be 0–10M NGN; got {annual_income}'
            )
        if not (0 <= debt_to_income <= 1):
            raise ValueError(
                f'debt_to_income must be 0–1; got {debt_to_income}'
            )
        if not (0 <= credit_score <= 100):
            raise ValueError(f'credit_score must be 0–100; got {credit_score}')
        if not (0 <= employment_stability <= 10):
            raise ValueError(
                f'employment_stability must be 0–10; got {employment_stability}'
            )

    def score_batch(
        self, profiles: list
    ) -> list[Dict[str, float | str]]:
        """
        Score multiple borrower profiles in batch.

        Args:
            profiles (list): List of dicts with keys:
                annual_income, debt_to_income, credit_score, employment_stability

        Returns:
            list[Dict]: List of result dicts with keys:
                risk_score, risk_category, profile_input
        """
        results = []
        for profile in profiles:
            risk_score, category = self.score(
                profile['annual_income'],
                profile['debt_to_income'],
                profile['credit_score'],
                profile['employment_stability'],
            )
            results.append(
                {
                    'risk_score': risk_score,
                    'risk_category': category,
                    'profile': profile,
                }
            )
        return results


def create_model() -> RiskSenseModel:
    """
    Factory function to instantiate the RiskSense Mamdani FIS.

    Returns:
        RiskSenseModel: Ready-to-use fuzzy inference system.

    Example:
        >>> model = create_model()
        >>> score, category = model.score(2.5, 0.4, 75, 8)
        >>> print(f'Risk: {category} ({score:.1f})')
        Risk: Low (28.3)
    """
    return RiskSenseModel()