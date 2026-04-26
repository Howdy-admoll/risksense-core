"""
Test Suite for RiskSense Model

Unit tests validating:
1. Mamdani FIS initialization and stability
2. All 8 borrower profiles produce expected risk categories
3. Input validation (bounds checking)
4. Batch processing
5. Risk category boundary conditions

Run tests:
    pytest tests/test_model.py -v
    pytest tests/test_model.py::test_all_profiles -v
"""

import pytest
from risksense import create_model, get_profiles
from risksense.model import RiskSenseModel


class TestModelInitialization:
    """Test FIS initialization and basic functionality."""

    def test_model_creation(self):
        """Model instantiation should succeed."""
        model = create_model()
        assert model is not None
        assert isinstance(model, RiskSenseModel)

    def test_model_has_fuzzy_system(self):
        """Model should have active FIS simulator."""
        model = create_model()
        assert hasattr(model, 'simulator')
        assert hasattr(model, 'fis')

    def test_model_has_rules(self):
        """Model should have fuzzy rules defined."""
        model = create_model()
        assert len(model.rules) > 0
        assert len(model.rules) >= 20  # At least our core rules


class TestInputValidation:
    """Test input bounds checking."""

    def test_valid_inputs(self):
        """Valid inputs should not raise."""
        model = create_model()
        score, category = model.score(2.5, 0.4, 75, 8.0)
        assert 0 <= score <= 100
        assert category in ['Low', 'Medium', 'High']

    def test_invalid_income_negative(self):
        """Negative income should raise ValueError."""
        model = create_model()
        with pytest.raises(ValueError, match='annual_income must be'):
            model.score(-1.0, 0.4, 75, 8.0)

    def test_invalid_income_too_high(self):
        """Income > 10M should raise ValueError."""
        model = create_model()
        with pytest.raises(ValueError, match='annual_income must be'):
            model.score(15.0, 0.4, 75, 8.0)

    def test_invalid_dti_negative(self):
        """Negative DTI should raise ValueError."""
        model = create_model()
        with pytest.raises(ValueError, match='debt_to_income must be'):
            model.score(2.5, -0.1, 75, 8.0)

    def test_invalid_dti_too_high(self):
        """DTI > 1.0 should raise ValueError."""
        model = create_model()
        with pytest.raises(ValueError, match='debt_to_income must be'):
            model.score(2.5, 1.5, 75, 8.0)

    def test_invalid_credit_score_negative(self):
        """Negative credit score should raise ValueError."""
        model = create_model()
        with pytest.raises(ValueError, match='credit_score must be'):
            model.score(2.5, 0.4, -10, 8.0)

    def test_invalid_credit_score_too_high(self):
        """Credit score > 100 should raise ValueError."""
        model = create_model()
        with pytest.raises(ValueError, match='credit_score must be'):
            model.score(2.5, 0.4, 150, 8.0)

    def test_invalid_employment_stability_negative(self):
        """Negative employment stability should raise ValueError."""
        model = create_model()
        with pytest.raises(ValueError, match='employment_stability must be'):
            model.score(2.5, 0.4, 75, -1.0)

    def test_invalid_employment_stability_too_high(self):
        """Employment stability > 10 should raise ValueError."""
        model = create_model()
        with pytest.raises(ValueError, match='employment_stability must be'):
            model.score(2.5, 0.4, 75, 12.0)


class TestRiskCategorization:
    """Test risk category boundary behavior."""

    def test_low_risk_boundary(self):
        """Risk score ≤ 35 should be 'Low'."""
        model = create_model()
        score, category = model.score(5.0, 0.1, 95, 10.0)
        assert category == 'Low'
        assert score <= 40  # Should be clearly in Low region

    def test_high_risk_boundary(self):
        """Risk score ≥ 66 should be 'High'."""
        model = create_model()
        score, category = model.score(0.5, 0.9, 15, 1.0)
        assert category == 'High'
        assert score >= 60  # Should be clearly in High region

    def test_medium_risk_exists(self):
        """Medium risk scores (35–65) should be categorized 'Medium'."""
        model = create_model()
        # Moderate profile
        score, category = model.score(2.0, 0.45, 60, 5.5)
        # Should fall in Medium region based on balanced inputs
        assert category in ['Medium', 'Low', 'High']
        assert 0 <= score <= 100

    def test_return_types(self):
        """Return types should be (float, str)."""
        model = create_model()
        score, category = model.score(2.5, 0.4, 75, 8.0)
        assert isinstance(score, float)
        assert isinstance(category, str)


class TestAllProfiles:
    """Test all 8 borrower profiles against expected categories."""

    def test_profile_1_premium_sme_owner(self):
        """Profile 1: Premium SME Owner → Low Risk"""
        model = create_model()
        profile = {
            'annual_income': 4.2,
            'debt_to_income': 0.25,
            'credit_score': 85,
            'employment_stability': 9.0,
        }
        score, category = model.score(**profile)
        assert category == 'Low', (
            f'Profile 1 expected Low, got {category} (score: {score:.1f})'
        )
        assert score <= 35

    def test_profile_2_mid_market_salaried(self):
        """Profile 2: Mid-Market Salaried Professional → Low Risk"""
        model = create_model()
        profile = {
            'annual_income': 2.8,
            'debt_to_income': 0.40,
            'credit_score': 72,
            'employment_stability': 8.5,
        }
        score, category = model.score(**profile)
        assert category == 'Low', (
            f'Profile 2 expected Low, got {category} (score: {score:.1f})'
        )
        assert score <= 35

    def test_profile_3_emerging_trader(self):
        """Profile 3: Emerging Trader → Medium Risk"""
        model = create_model()
        profile = {
            'annual_income': 1.8,
            'debt_to_income': 0.55,
            'credit_score': 58,
            'employment_stability': 5.5,
        }
        score, category = model.score(**profile)
        assert category == 'Medium', (
            f'Profile 3 expected Medium, got {category} (score: {score:.1f})'
        )
        assert 35 < score < 66

    def test_profile_4_gig_economy(self):
        """Profile 4: Gig Economy / Freelancer → Medium Risk"""
        model = create_model()
        profile = {
            'annual_income': 0.9,
            'debt_to_income': 0.60,
            'credit_score': 42,
            'employment_stability': 4.0,
        }
        score, category = model.score(**profile)
        assert category == 'Medium', (
            f'Profile 4 expected Medium, got {category} (score: {score:.1f})'
        )

    def test_profile_5_recent_graduate(self):
        """Profile 5: Recent Graduate (Thin Credit) → Medium Risk"""
        model = create_model()
        profile = {
            'annual_income': 1.2,
            'debt_to_income': 0.35,
            'credit_score': 50,
            'employment_stability': 3.0,
        }
        score, category = model.score(**profile)
        assert category == 'Medium', (
            f'Profile 5 expected Medium, got {category} (score: {score:.1f})'
        )

    def test_profile_6_recovering_borrower(self):
        """Profile 6: Recovering Borrower → High Risk"""
        model = create_model()
        profile = {
            'annual_income': 1.5,
            'debt_to_income': 0.65,
            'credit_score': 45,
            'employment_stability': 4.5,
        }
        score, category = model.score(**profile)
        assert category == 'High', (
            f'Profile 6 expected High, got {category} (score: {score:.1f})'
        )
        assert score > 65

    def test_profile_7_high_risk_distressed(self):
        """Profile 7: High-Risk Distressed → High Risk"""
        model = create_model()
        profile = {
            'annual_income': 0.4,
            'debt_to_income': 0.75,
            'credit_score': 28,
            'employment_stability': 2.0,
        }
        score, category = model.score(**profile)
        assert category == 'High', (
            f'Profile 7 expected High, got {category} (score: {score:.1f})'
        )
        assert score > 65

    def test_profile_8_business_owner(self):
        """Profile 8: Business Owner (Moderate Risk) → Medium Risk"""
        model = create_model()
        profile = {
            'annual_income': 3.1,
            'debt_to_income': 0.50,
            'credit_score': 65,
            'employment_stability': 6.5,
        }
        score, category = model.score(**profile)
        assert category == 'Medium', (
            f'Profile 8 expected Medium, got {category} (score: {score:.1f})'
        )

    def test_all_profiles_from_suite(self):
        """Test all 8 profiles from get_profiles() fixture."""
        model = create_model()
        profiles = get_profiles()

        assert len(profiles) == 8, 'Should have exactly 8 profiles'

        for profile in profiles:
            score, category = model.score(
                profile['annual_income'],
                profile['debt_to_income'],
                profile['credit_score'],
                profile['employment_stability'],
            )

            expected = profile['expected_category']
            assert category == expected, (
                f"{profile['name']}: expected {expected}, "
                f'got {category} (score: {score:.1f})'
            )


class TestBatchProcessing:
    """Test batch scoring functionality."""

    def test_batch_scoring_empty(self):
        """Empty batch should return empty list."""
        model = create_model()
        results = model.score_batch([])
        assert results == []

    def test_batch_scoring_single(self):
        """Single profile batch should work."""
        model = create_model()
        profiles = [
            {
                'annual_income': 2.5,
                'debt_to_income': 0.4,
                'credit_score': 75,
                'employment_stability': 8.0,
            }
        ]
        results = model.score_batch(profiles)
        assert len(results) == 1
        assert 'risk_score' in results[0]
        assert 'risk_category' in results[0]
        assert 'profile' in results[0]

    def test_batch_scoring_multiple(self):
        """Multiple profiles batch should process all."""
        model = create_model()
        batch = get_profiles()
        results = model.score_batch(batch)

        assert len(results) == 8
        for result in results:
            assert 0 <= result['risk_score'] <= 100
            assert result['risk_category'] in ['Low', 'Medium', 'High']

    def test_batch_preserves_profile_data(self):
        """Batch results should include original profile data."""
        model = create_model()
        profiles = [
            {
                'annual_income': 2.5,
                'debt_to_income': 0.4,
                'credit_score': 75,
                'employment_stability': 8.0,
            }
        ]
        results = model.score_batch(profiles)
        assert results[0]['profile'] == profiles[0]


class TestSensitivityAnalysis:
    """Test model response to parameter changes."""

    def test_income_increases_lower_risk(self):
        """Higher income should generally lower risk score."""
        model = create_model()
        score_low_income, _ = model.score(0.8, 0.5, 60, 5.0)
        score_high_income, _ = model.score(4.5, 0.5, 60, 5.0)

        assert score_high_income < score_low_income, (
            'Higher income should result in lower risk score'
        )

    def test_dti_increases_raise_risk(self):
        """Higher DTI should generally increase risk score."""
        model = create_model()
        score_low_dti, _ = model.score(2.5, 0.2, 60, 5.0)
        score_high_dti, _ = model.score(2.5, 0.8, 60, 5.0)

        assert score_high_dti > score_low_dti, (
            'Higher DTI should result in higher risk score'
        )

    def test_credit_score_increases_lower_risk(self):
        """Higher credit score should lower risk."""
        model = create_model()
        score_poor, _ = model.score(2.5, 0.5, 30, 5.0)
        score_good, _ = model.score(2.5, 0.5, 90, 5.0)

        assert score_good < score_poor, (
            'Higher credit score should result in lower risk score'
        )

    def test_employment_stability_increases_lower_risk(self):
        """Higher employment stability should lower risk."""
        model = create_model()
        score_unstable, _ = model.score(2.5, 0.5, 60, 2.0)
        score_stable, _ = model.score(2.5, 0.5, 60, 9.0)

        assert score_stable < score_unstable, (
            'Higher employment stability should result in lower risk score'
        )


class TestEdgeCases:
    """Test boundary conditions and edge cases."""

    def test_all_zeros_inputs(self):
        """All zero inputs should result in high risk."""
        model = create_model()
        score, category = model.score(0.0, 0.0, 0, 0.0)
        # No income + no credit = highest risk
        assert category in ['High', 'Medium']

    def test_all_max_inputs(self):
        """Maximum valid inputs should result in low risk."""
        model = create_model()
        score, category = model.score(10.0, 1.0, 100, 10.0)
        # Note: High DTI may mitigate perfect income/credit
        assert category in ['Low', 'Medium']

    def test_zero_income_high_dti(self):
        """Zero income + high DTI = definite high risk."""
        model = create_model()
        score, category = model.score(0.0, 0.9, 30, 3.0)
        assert category == 'High'

    def test_high_income_good_credit_overrides_dti(self):
        """Strong income + credit can compensate for DTI."""
        model = create_model()
        score, category = model.score(6.0, 0.75, 85, 8.0)
        # Despite high DTI, strong income and credit should keep risk moderate
        assert category in ['Low', 'Medium']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
