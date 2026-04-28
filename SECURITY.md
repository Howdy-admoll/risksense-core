# Security Policy

## Reporting Security Vulnerabilities

**DO NOT** open public GitHub issues for security vulnerabilities.

If you discover a security vulnerability, please report it responsibly:

### How to Report

Email: **admoll.adefemi@gmail.com**

Include:
- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Suggested fix (if you have one)

### Timeline

- **Acknowledgment:** Within 48 hours
- **Investigation:** Within 1 week
- **Fix & Release:** As soon as possible (typically within 2 weeks)
- **Disclosure:** After patch is released

---

## Supported Versions

| Version | Status | Support Until |
|---------|--------|---------------|
| 1.0.x | Current | 2027-04-28 |
| < 1.0 | Deprecated | 2026-06-28 |

Security patches are released for:
- ✅ Current version (1.0.x)
- ✅ Previous version (limited support)

---

## Security Considerations

### Credit Risk Scoring

RiskSense Core provides **decision support only**:

⚠️ **DO NOT use for:**
- Final lending decisions without human review
- Compliance with lending regulations without legal counsel
- Replacement for established risk frameworks

✅ **Best practices:**
- Combine with domain expertise
- Implement proper audit trails
- Maintain human oversight
- Regular model validation

### Fair Lending Compliance

When using RiskSense Core:

- ✅ Monitor for disparate impact
- ✅ Validate fairness across demographic groups
- ✅ Document decision-making process
- ✅ Maintain audit logs
- ✅ Comply with local regulations (CBN, NDIC, etc.)

### Data Security

If you integrate RiskSense Core with real data:

- ✅ Encrypt sensitive data at rest and in transit
- ✅ Implement access controls
- ✅ Use HTTPS for API endpoints
- ✅ Sanitize logs (don't log sensitive data)
- ✅ Comply with data protection laws (GDPR, NDPR, etc.)

### Model Validation

Before using in production:

- ✅ Validate against historical data
- ✅ Test across demographic groups
- ✅ Monitor for model drift
- ✅ Regular retraining/updates
- ✅ Document assumptions and limitations

---

## Dependency Security

### Version Pinning

All dependencies are pinned to prevent unexpected breaking changes:

```
numpy==1.26.4
scikit-fuzzy==0.4.2
matplotlib==3.8.3
flask==3.0.0
```

### Updates

To check for security updates:

```bash
pip list --outdated
pip check  # Check for conflicts
```

To update dependencies (test thoroughly):

```bash
pip install --upgrade <package>==<new-version>
pytest tests/ -v  # Verify compatibility
```

---

## Known Issues

### Fuzzy Boundary Cases

4 test cases fail due to fuzzy logic boundary behavior (expected):
- Profile 2: DTI at membership boundary (0.40)
- Profile 6: Symmetric rule activations
- Employment stability: Floating-point symmetry

**Impact:** ⚠️ Medium (edge cases, may need manual review)

See [FUZZY_BOUNDARIES.md](FUZZY_BOUNDARIES.md) for details.

### scikit-fuzzy Deprecation

scikit-fuzzy uses deprecated libraries:
- `distutils` (removed in Python 3.12)
- `imp` module (deprecated)

**Status:** ✅ Mitigated (Python 3.10, 3.11 only)  
**Future:** Consider migration to newer fuzzy logic libraries

---

## Security Best Practices

### For Developers

- ✅ Use Python 3.10+ (avoid 3.12 due to distutils)
- ✅ Run tests before committing
- ✅ Use secure coding practices
- ✅ Keep dependencies updated
- ✅ Review security advisories regularly

### For Operators

- ✅ Use strong authentication
- ✅ Restrict API access
- ✅ Monitor logs for suspicious activity
- ✅ Regular backups
- ✅ Incident response plan

### For Users

- ✅ Don't trust risk scores blindly
- ✅ Combine with domain expertise
- ✅ Document all decisions
- ✅ Implement audit trails
- ✅ Regular model validation

---

## Compliance

### Applicable Regulations

**Nigeria:**
- CBN Lending Guidelines
- NDIC Risk Management Standards
- FIRS Tax Compliance
- Data Protection Regulation (NDPR)

**International:**
- GDPR (if processing EU data)
- Fair Lending Laws (if applicable)
- Basel III Guidelines (if applicable)

### Due Diligence

Use RiskSense Core with appropriate:
- Legal review
- Compliance audit
- Risk assessment
- Model validation
- Regular monitoring

---

## Incident Response

If a security incident occurs:

1. **Assess** — Determine scope and impact
2. **Contain** — Limit exposure if possible
3. **Notify** — Alert affected users
4. **Fix** — Develop and test patch
5. **Release** — Push security update
6. **Review** — Post-incident analysis

---

## Contact

**Security Issues:** admoll.adefemi@gmail.com 
**General Questions:** admoll.adefemi@gmail.com 
**GitHub:** [@Howdy-admoll](https://github.com/Howdy-admoll)

---

## Disclaimer

RiskSense Core is provided **AS-IS** without warranty. Users are responsible for:
- Compliance with applicable laws
- Proper use and validation
- Data security and privacy
- Documented decision-making

The authors are not liable for:
- Incorrect risk assessments
- Financial losses from using the model
- Regulatory violations
- Data breaches

---

**Last Updated:** 2026-04-28  
**Policy Version:** 1.0  
**Effective Date:** 2026-04-28