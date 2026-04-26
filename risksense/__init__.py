"""
RiskSense Core — Mamdani Fuzzy Inference System for Credit Risk Scoring

A production-grade fuzzy inference model for fintech credit risk assessment
in African markets, published as part of academic research at the
University of Portsmouth.

Author: Ademola Adefemi
ORCID: 0009-0006-0870-6798
Website: admoll.dev

GitHub: https://github.com/admoll/risksense-core
Paper: https://ssrn.com (see SSRN profile for academic publication)
"""

from risksense.model import RiskSenseModel, create_model
from risksense.profiles import get_profiles, get_profile_by_name, get_profiles_by_category

__version__ = '0.1.0'
__author__ = 'Ademola Adefemi'
__orcid__ = '0009-0006-0870-6798'

__all__ = [
    'RiskSenseModel',
    'create_model',
    'get_profiles',
    'get_profile_by_name',
    'get_profiles_by_category',
]
