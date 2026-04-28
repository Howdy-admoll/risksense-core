# Contributing to RiskSense Core

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the RiskSense project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community. Please read and follow our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## How Can You Contribute?

### 1. Report Bugs
Found a bug? Open an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs. actual behavior
- Python version and environment

### 2. Suggest Enhancements
Have an idea? Open an issue with label `enhancement`:
- Problem statement
- Proposed solution
- Alternative approaches considered
- Use cases

### 3. Improve Documentation
- Fix typos in README, docstrings
- Add examples or tutorials
- Improve clarity of explanations
- Update outdated information

### 4. Submit Code Changes
- Bug fixes
- New features
- Performance improvements
- Code refactoring

---

## Development Setup

### Prerequisites
- Python 3.10+
- Git

### Setup Steps

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/risksense-core.git
cd risksense-core

# 3. Add upstream remote
git remote add upstream https://github.com/Howdy-admoll/risksense-core.git

# 4. Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# 5. Install development dependencies
pip install -e ".[dev]"
```

---

## Making Changes

### Branch Naming
Use descriptive branch names:
- `feature/add-sugeno-fis` — New features
- `fix/boundary-rule-overlap` — Bug fixes
- `docs/update-readme` — Documentation
- `test/add-profile-tests` — Tests

### Commit Messages
Follow conventional commits:
```
type(scope): description

[optional body]
[optional footer]
```

Examples:
```
feat(rules): add catch-all for good credit
fix(model): adjust DTI boundary to 0.45
docs(readme): add batch scoring example
test(profiles): add profile 9 high-income
```

### Code Style
- **Black**: Auto-format with `black risksense/ tests/`
- **Flake8**: Lint with `flake8 risksense/ tests/`
- **Type hints**: Use them liberally
- **Docstrings**: NumPy format for all functions

Example:
```python
def score(
    self,
    annual_income: float,
    debt_to_income: float,
    credit_score: float,
    employment_stability: float,
) -> Tuple[float, str]:
    """
    Compute credit risk score and category.

    Args:
        annual_income: Annual income in millions NGN
        debt_to_income: DTI ratio (0–1)
        credit_score: Credit history score (0–100)
        employment_stability: Stability index (0–10)

    Returns:
        Tuple[float, str]: (risk_score: 0–100, category: "Low"/"Medium"/"High")

    Raises:
        ValueError: If inputs are out of valid ranges.
    """
```

---

## Testing

### Run Tests
```bash
# All tests
pytest tests/test_model.py -v

# Specific test class
pytest tests/test_model.py::TestAllProfiles -v

# With coverage
pytest tests/test_model.py --cov=risksense --cov-report=html
```

### Write Tests
Add tests in `tests/test_model.py` following existing patterns:

```python
class TestMyFeature:
    """Tests for my new feature."""
    
    def test_specific_behavior(self):
        """Describe what this test checks."""
        model = create_model()
        score, category = model.score(2.5, 0.5, 70, 7.0)
        assert category == 'Low'
```

### Coverage Goal
- Aim for >80% code coverage
- All new code should have tests
- Check coverage: `pytest --cov=risksense --cov-report=term-missing`

---

## Pull Request Process

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests and code quality**:
   ```bash
   pytest tests/test_model.py -v
   black risksense/ tests/
   flake8 risksense/ tests/
   ```

3. **Update documentation** if needed:
   - README for user-facing changes
   - Docstrings for API changes
   - CHANGELOG.md for all changes

### Submit PR

1. Push to your fork: `git push origin feature/your-feature`
2. Open PR with:
   - Clear title and description
   - Link to related issues (Closes #123)
   - List of changes
   - Testing notes

### PR Guidelines

- **One feature per PR**: Keep scope focused
- **Size**: Aim for <500 LOC per PR
- **Tests**: All PRs must maintain or improve test coverage
- **Documentation**: Update docs for user-facing changes
- **Commits**: Squash into logical commits before merge

### Review Process

- At least one maintainer review required
- All CI checks must pass (tests, lint, coverage)
- Discussion may be requested for design decisions
- Once approved, PR will be merged to `develop` branch

---

## Fuzzy Model Development

### Adding Rules

Rules are defined in `risksense/model.py::_define_rules()`:

```python
# Example: Good income + good credit → Low risk
ctrl.Rule(
    self.annual_income['high']
    & self.credit_score['good'],
    self.risk_score['low'],
)
```

**Guidelines**:
- One rule per IF-THEN statement
- Comment explaining financial heuristic
- Test with `model.score()` on relevant profiles
- Verify no test regressions

### Adjusting Membership Functions

Membership functions define fuzzy sets (e.g., "low income", "good credit").

Current configuration in `_build_fuzzy_system()`:
```python
# Triangular membership function: [left, peak, right]
self.annual_income['low'] = fuzz.trimf([0, 0, 2.5])
```

**Guidelines**:
- Keep overlaps intentional (not accidental)
- Document membership ranges in docstrings
- Test boundary behavior
- Maintain symmetry where sensible

---

## Areas for Contribution

### High Priority
- [ ] Create REST API server (`risksense/api.py`)
- [ ] Web dashboard for visualization
- [ ] Model explainability reports
- [ ] Performance benchmarking

### Medium Priority
- [ ] Sugeno FIS alternative implementation
- [ ] Multi-language support (Hausa, Yoruba)
- [ ] A/B testing framework
- [ ] Model drift detection

### Documentation
- [ ] Detailed DESIGN.md explaining rule derivation
- [ ] Tutorial notebooks (Jupyter)
- [ ] API documentation
- [ ] Deployment guide (Docker, AWS)

---

## Questions?

- **GitHub Issues**: [Create an issue](https://github.com/Howdy-admoll/risksense-core/issues)
- **Email**: hello@admoll.dev
- **Discussions**: Use GitHub Discussions for Q&A

---

## Recognition

Contributors will be recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Release notes (CHANGELOG.md)
- GitHub contributors page

---

Thank you for making RiskSense better! 🚀