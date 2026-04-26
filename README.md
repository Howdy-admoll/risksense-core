# RiskSense: Mamdani Fuzzy Inference System for Credit Risk Scoring

**Production-grade fuzzy logic model for fintech credit risk assessment in African markets**

> A rigorous, research-grade implementation of fuzzy inference for credit risk scoring in fintech lending. Built on peer-reviewed research methodologies and calibrated for African borrower archetypes.

---

## Overview

RiskSense is a **Mamdani fuzzy inference system (FIS)** that assesses credit risk for individual borrowers in fintech lending environments. Rather than binary classification or linear scoring models, RiskSense uses fuzzy logic to capture the nuanced, multi-dimensional nature of credit risk—particularly in African fintech contexts where traditional credit bureaus are thin, income documentation is variable, and borrower segments are diverse.

### Why Fuzzy Logic for Credit Risk?

Traditional credit scoring models (logistic regression, tree-based classifiers) assume clean data and stationary distributions. Fintech lending in Africa faces:
- **Thin credit files** (limited bureau history)
- **Informal income verification** (self-employed, gig workers)
- **Complex overlapping risk factors** (income + employment + debt burden)
- **Need for interpretability** (regulators, loan officers)

Mamdani fuzzy systems excel at:
1. **Capturing linguistic reasoning** ("high income" + "low debt" = "low risk")
2. **Graceful handling of uncertainty** in incomplete data
3. **Transparent, explainable rules** (not black-box)
4. **Smooth interpolation** across borrower profiles

---

## Features

### Core Model
- **4 Input Dimensions:**
  - Annual income (₦0–10M range, Nigerian fintech context)
  - Debt-to-income ratio (0–1, capped at 100% DTI)
  - Credit history score (0–100, normalized)
  - Employment stability (0–10, tenure + sector risk)

- **Single Output:**
  - Risk score (0–100) with linguistic mapping:
    - **Low Risk:** 0–35 (approve readily, standard terms)
    - **Medium Risk:** 36–65 (conditional approval, rate adjustment, enhanced monitoring)
    - **High Risk:** 66–100 (decline or enhanced due diligence)

### Fuzzy Logic Subsystem
- **32 core fuzzy rules** encoding financial heuristics
- **3-level fuzzy sets** per input (low/medium/high or poor/fair/good)
- **Triangular membership functions** for computational efficiency
- **Centroid defuzzification** (Mamdani output aggregation)

### Validation & Testing
- **8 comprehensive borrower profiles** covering:
  - Premium SME owners
  - Salaried professionals
  - Emerging traders
  - Gig economy workers
  - Recent graduates
  - Recovering borrowers
  - High-risk distressed borrowers
  - Stable business owners

- **Full pytest suite** with:
  - Input validation (bounds checking)
  - Profile-level assertions
  - Sensitivity analysis
  - Batch processing tests
  - Edge case handling

---

## Installation

### Requirements
- Python 3.9+
- `scikit-fuzzy` (fuzzy logic computation)
- `numpy` (numerical arrays)
- `pytest` (testing)

### Setup

```bash
# Clone repository
git clone https://github.com/admoll/risksense-core.git
cd risksense-core

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Basic Scoring

```python
from risksense import create_model

# Instantiate model
model = create_model()

# Score a single borrower
# Args: annual_income (₦M), debt_to_income (ratio), credit_score (0–100), employment_stability (0–10)
risk_score, risk_category = model.score(
    annual_income=2.5,           # ₦2.5M annual income
    debt_to_income=0.40,         # 40% DTI ratio
    credit_score=75,             # Good credit history
    employment_stability=8.5     # 8+ years tenure at reputable firm
)

print(f"Risk Score: {risk_score:.1f}")      # Risk Score: 28.3
print(f"Category: {risk_category}")          # Category: Low
```

### Batch Processing

```python
from risksense import create_model, get_profiles

model = create_model()
profiles = get_profiles()  # Get 8 test profiles

# Score multiple borrowers in batch
results = model.score_batch(profiles)

for result in results:
    print(f"{result['profile']} → {result['risk_category']} "
          f"({result['risk_score']:.1f})")
```

### Test Profile Inspection

```python
from risksense import get_profile_by_name, get_profiles_by_category

# Get single profile
profile = get_profile_by_name("Profile 1: Premium SME Owner")
print(profile['description'])

# Get all high-risk profiles
high_risk = get_profiles_by_category("High")
for p in high_risk:
    print(p['name'])
```

---

## Running Tests

### All Tests
```bash
pytest tests/test_model.py -v
```

### Specific Test Class
```bash
pytest tests/test_model.py::TestAllProfiles -v
```

### Specific Test (e.g., Profile 1)
```bash
pytest tests/test_model.py::TestAllProfiles::test_profile_1_premium_sme_owner -v
```

### Coverage Report
```bash
pytest tests/test_model.py --cov=risksense --cov-report=html
```

---

## Research Methodology

### Research Foundation

RiskSense is built on the methodologies presented in:

**"Mamdani and Sugeno Fuzzy Inference Systems for Credit Risk Scoring in Fintech Lending"**

- Author: Ademola Adefemi
- ORC ID: 0009-0006-0870-6798
- Module: Advanced Artificial Intelligence
- Format: IEEE-style research paper
- Publication: SSRN (Social Science Research Network)

**SSRN Profile:** [https://ssrn.com](https://ssrn.com) (search: Ademola Adefemi)

### Fuzzy Rule Base

The 32 core rules encode the following financial heuristics:

| Income | DTI | Credit | Stability | Risk | Rationale |
|--------|-----|--------|-----------|------|-----------|
| High | Low | Good | High | **Low** | Strong capacity, clean history, stable employment |
| High | Medium | Good | High | **Low** | Good income buffers moderate debt service |
| Medium | Low | Good | High | **Low** | Solid fundamentals, low leverage |
| Low | Low | Good | High | **Low** | Good credit mitigates low income if stable |
| Low | High | Poor | Low | **High** | Double jeopardy: low income + high debt + thin credit |
| Medium | High | Fair | Low | **Medium** | Conditional risk; rate adjustment needed |
| Low | Low | Poor | Low | **Medium** | Good debt metrics override poor credit if income stable |
| Medium | Medium | Fair | Medium | **Medium** | Balanced profile; monitoring required |

*(Full rule set: 32 rules covering key combinations)*

### Fuzzy Sets

**Income (₦M):**
- Low: [0, 0, 2.5]
- Medium: [1.5, 4, 6.5]
- High: [5.5, 10, 10]

**DTI Ratio:**
- Low: [0, 0, 0.35]
- Medium: [0.25, 0.55, 0.75]
- High: [0.65, 1.0, 1.0]

**Credit Score:**
- Poor: [0, 0, 40]
- Fair: [30, 60, 80]
- Good: [70, 100, 100]

**Employment Stability (0–10):**
- Low: [0, 0, 3]
- Medium: [2, 5, 8]
- High: [7, 10, 10]

---

## Borrower Profiles (Test Suite)

The model is validated on 8 synthetic profiles representing real-world fintech borrower archetypes:

| # | Profile | Income (₦M) | DTI | Credit | Stability | Expected Category |
|---|---------|-------------|-----|--------|-----------|-------------------|
| 1 | Premium SME Owner | 4.2 | 0.25 | 85 | 9.0 | **Low** |
| 2 | Mid-Market Salaried | 2.8 | 0.40 | 72 | 8.5 | **Low** |
| 3 | Emerging Trader | 1.8 | 0.55 | 58 | 5.5 | **Medium** |
| 4 | Gig Economy Worker | 0.9 | 0.60 | 42 | 4.0 | **Medium** |
| 5 | Recent Graduate | 1.2 | 0.35 | 50 | 3.0 | **Medium** |
| 6 | Recovering Borrower | 1.5 | 0.65 | 45 | 4.5 | **High** |
| 7 | High-Risk Distressed | 0.4 | 0.75 | 28 | 2.0 | **High** |
| 8 | Business Owner | 3.1 | 0.50 | 65 | 6.5 | **Medium** |

All profiles pass their respective category assertions in the test suite.

---

## Project Structure

```
risksense-core/
├── risksense/
│   ├── __init__.py           # Package exports
│   ├── model.py              # Mamdani FIS implementation
│   └── profiles.py           # 8 test borrower profiles
├── tests/
│   ├── __init__.py
│   └── test_model.py         # Comprehensive test suite
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore
```

---

## API Reference

### `RiskSenseModel` Class

#### `__init__()`
Initialize the Mamdani FIS with all fuzzy variables and rules.

#### `score(annual_income, debt_to_income, credit_score, employment_stability) → (float, str)`
Compute risk score and category for a single borrower.

**Parameters:**
- `annual_income` (float): Annual income in millions NGN (0–10)
- `debt_to_income` (float): DTI ratio (0–1)
- `credit_score` (float): Credit history score (0–100)
- `employment_stability` (float): Stability index (0–10)

**Returns:**
- `(risk_score, risk_category)` tuple
  - `risk_score` (float): 0–100
  - `risk_category` (str): "Low", "Medium", or "High"

**Raises:**
- `ValueError`: If any input is out of bounds

**Example:**
```python
model = create_model()
score, category = model.score(2.5, 0.4, 75, 8.0)
# Returns: (28.3, 'Low')
```

#### `score_batch(profiles) → list[dict]`
Score multiple borrowers efficiently.

**Parameters:**
- `profiles` (list): List of dicts with keys: `annual_income`, `debt_to_income`, `credit_score`, `employment_stability`

**Returns:**
- List of result dicts with keys:
  - `risk_score` (float): 0–100
  - `risk_category` (str): "Low", "Medium", or "High"
  - `profile` (dict): Original input profile

### Module Functions

#### `create_model() → RiskSenseModel`
Factory function to instantiate the FIS.

```python
from risksense import create_model
model = create_model()
```

#### `get_profiles() → list[dict]`
Return all 8 test profiles.

```python
from risksense import get_profiles
profiles = get_profiles()
```

#### `get_profile_by_name(name: str) → dict | None`
Retrieve a single profile by name.

```python
profile = get_profile_by_name("Profile 1: Premium SME Owner")
```

#### `get_profiles_by_category(category: str) → list[dict]`
Filter profiles by risk category.

```python
high_risk = get_profiles_by_category("High")
```

---

## Author & Publication Credentials

**Ademola "Admoll" Adefemi**

- **Current Role:** SRE (Site Reliability Engineer), Card Payment Team, Moniepoint Inc.
- **Background:** Credit Analytics & Engineering, Indicina Technologies Limited
- **ORCID:** [0009-0006-0870-6798](https://orcid.org/0009-0006-0870-6798)
- **Website:** [admoll.dev](https://admoll.dev)
- **GitHub:** [@Howdy-admoll](https://github.com/Howdy-admoll)

### Research Interests
- Fuzzy inference systems for credit risk
- Fintech infrastructure and payment systems
- Nigerian regulatory environment (CBN guidelines)
- Card BIN management and processor routing
- Startup: RiskSense (Arhesus brand) — fuzzy logic credit scoring for African fintech

---

## References

1. **Mamdani, E. H., & Assilian, S.** (1975). "An experiment in linguistic synthesis with a fuzzy logic controller." *International Journal of Man-Machine Studies*, 7(1), 1–13.

2. **Ross, T. J.** (2016). *Fuzzy Logic with Engineering Applications* (4th ed.). Wiley.

3. **Adefemi, A.** (2025). "Mamdani and Sugeno Fuzzy Inference Systems for Credit Risk Scoring in Fintech Lending." IEEE-format research paper, Advanced AI Module. SSRN.

4. **CBN Guidelines.** Central Bank of Nigeria. *Guidelines for Fintech Credit Operations*. Latest edition.

5. **Hand, D. J., & Henley, W. E.** (1997). "Statistical classification methods in consumer credit scoring: A review." *Journal of the Royal Statistical Society*, 160(3), 523–541.

---

## License

This project is available under the MIT License. See `LICENSE` file for details.

---

## Disclaimer

RiskSense is a research implementation for educational and testing purposes. While built on rigorous fuzzy logic methodology, credit risk assessment in production environments requires:
- Regulatory compliance with CBN and applicable jurisdictions
- Integration with verified credit bureau data
- Human review by trained credit officers
- Appropriate risk management and loan monitoring frameworks
- Ongoing model validation and recalibration

**Not for unsupervised production lending without regulatory approval and additional validation.**

---

## Contact & Collaboration

For questions, suggestions, or collaboration opportunities:

- **Email:** [admoll.adefemi@gmail.com]
- **Twitter/X:** [@officialadmoll](https://twitter.com/officialadmoll)
- **LinkedIn:** [Admoll Adefemi]
- **SSRN:** [SSRN Profile](https://hq.ssrn.com/Participantfirst.cfm?PartId=11289508)

---

**RiskSense — Bringing fuzzy logic rigor to fintech credit assessment in Africa.**

*"Credit risk is not binary. It's a spectrum. Treat it like one."*
