"""
RiskSense REST API — Flask microservice

Provides RESTful endpoints for:
- Single borrower scoring: POST /api/score
- Batch scoring: POST /api/batch
- Model introspection: GET /api/model/info
- Health checks: GET /api/health

Usage:
    from risksense.api import app
    app.run(host='0.0.0.0', port=5000, debug=False)

Or with gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5000 'risksense.api:app'

Example requests:
    curl -X POST http://localhost:5000/api/score \
        -H "Content-Type: application/json" \
        -d '{
            "annual_income": 2.5,
            "debt_to_income": 0.4,
            "credit_score": 75,
            "employment_stability": 8.0
        }'
"""

try:
    from flask import Flask, request, jsonify
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

from risksense import create_model, get_profiles
from datetime import datetime


def create_app():
    """Create and configure Flask application."""
    if not HAS_FLASK:
        raise ImportError(
            'Flask required for API. Install: pip install flask'
        )

    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    # Initialize model (once at startup)
    app.model = create_model()

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'risksense',
            'version': '0.1.0',
        }), 200

    @app.route('/api/model/info', methods=['GET'])
    def model_info():
        """Get model information."""
        return jsonify({
            'model': 'Mamdani Fuzzy Inference System',
            'version': '0.1.0',
            'inputs': {
                'annual_income': {
                    'range': [0, 10],
                    'unit': '₦ Millions',
                    'description': 'Annual income',
                },
                'debt_to_income': {
                    'range': [0, 1],
                    'unit': 'ratio',
                    'description': 'Debt-to-income ratio',
                },
                'credit_score': {
                    'range': [0, 100],
                    'unit': '0-100',
                    'description': 'Credit history score',
                },
                'employment_stability': {
                    'range': [0, 10],
                    'unit': '0-10',
                    'description': 'Employment stability index',
                },
            },
            'output': {
                'risk_score': {
                    'range': [0, 100],
                    'categories': {
                        'low': [0, 35],
                        'medium': [36, 65],
                        'high': [66, 100],
                    },
                },
            },
            'rules': len(app.model.rules),
            'author': 'Ademola Adefemi',
            'orcid': '0009-0006-0870-6798',
        }), 200

    @app.route('/api/score', methods=['POST'])
    def score_borrower():
        """Score a single borrower."""
        try:
            data = request.get_json()

            if not data:
                return jsonify({'error': 'No JSON payload provided'}), 400

            required_fields = {
                'annual_income',
                'debt_to_income',
                'credit_score',
                'employment_stability',
            }
            if not required_fields.issubset(set(data.keys())):
                missing = required_fields - set(data.keys())
                return jsonify({
                    'error': f'Missing required fields: {", ".join(missing)}'
                }), 400

            try:
                score, category = app.model.score(
                    float(data['annual_income']),
                    float(data['debt_to_income']),
                    float(data['credit_score']),
                    float(data['employment_stability']),
                )

                return jsonify({
                    'risk_score': round(score, 2),
                    'risk_category': category,
                    'timestamp': datetime.utcnow().isoformat(),
                }), 200

            except ValueError as e:
                return jsonify({'error': str(e)}), 422

        except Exception as e:
            return jsonify({'error': f'Internal error: {str(e)}'}), 500

    @app.route('/api/batch', methods=['POST'])
    def batch_score():
        """Score multiple borrowers."""
        try:
            data = request.get_json()

            if not data or 'borrowers' not in data:
                return jsonify({
                    'error': 'Request must contain "borrowers" array'
                }), 400

            borrowers = data['borrowers']

            if not isinstance(borrowers, list):
                return jsonify({'error': '"borrowers" must be an array'}), 400

            results = []
            errors = []

            for i, borrower in enumerate(borrowers):
                try:
                    required_fields = {
                        'annual_income',
                        'debt_to_income',
                        'credit_score',
                        'employment_stability',
                    }
                    if not required_fields.issubset(set(borrower.keys())):
                        errors.append({
                            'index': i,
                            'error': f'Missing fields',
                        })
                        continue

                    score, category = app.model.score(
                        float(borrower['annual_income']),
                        float(borrower['debt_to_income']),
                        float(borrower['credit_score']),
                        float(borrower['employment_stability']),
                    )

                    results.append({
                        'index': i,
                        'risk_score': round(score, 2),
                        'risk_category': category,
                    })

                except (ValueError, TypeError) as e:
                    errors.append({
                        'index': i,
                        'error': str(e),
                    })

            return jsonify({
                'processed': len(results),
                'errors': len(errors),
                'results': results,
                'error_details': errors if errors else None,
                'timestamp': datetime.utcnow().isoformat(),
            }), 200

        except Exception as e:
            return jsonify({'error': f'Internal error: {str(e)}'}), 500

    @app.route('/api/profiles', methods=['GET'])
    def list_profiles():
        """Get test profiles."""
        profiles = get_profiles()
        return jsonify({
            'count': len(profiles),
            'profiles': [
                {
                    'name': p['name'],
                    'description': p['description'],
                    'expected_category': p['expected_category'],
                    'inputs': {
                        'annual_income': p['annual_income'],
                        'debt_to_income': p['debt_to_income'],
                        'credit_score': p['credit_score'],
                        'employment_stability': p['employment_stability'],
                    },
                }
                for p in profiles
            ],
        }), 200

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors."""
        return jsonify({'error': 'Method not allowed'}), 405

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
