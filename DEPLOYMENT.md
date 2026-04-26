# RiskSense Deployment Guide

**Production-grade deployment instructions for the RiskSense Mamdani FIS microservice.**

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Cloud Platforms](#cloud-platforms)
6. [Monitoring & Logging](#monitoring--logging)
7. [API Usage](#api-usage)
8. [Performance Tuning](#performance-tuning)
9. [Security Considerations](#security-considerations)

---

## Quick Start

### Option 1: Local Python

```bash
# Clone repository
git clone https://github.com/admoll/risksense-core.git
cd risksense-core

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/test_model.py -v

# Run CLI
python -m risksense.cli score --income 2.5 --dti 0.4 --credit 75 --stability 8.0
```

### Option 2: Docker

```bash
# Build image
docker build -t risksense:latest .

# Run container
docker run -p 5000:5000 risksense:latest

# Health check
curl http://localhost:5000/api/health
```

### Option 3: Docker Compose (with monitoring)

```bash
# Start stack
docker-compose up -d

# APIs available:
# - RiskSense API: http://localhost:5000
# - Prometheus:    http://localhost:9090
# - Grafana:       http://localhost:3000 (admin/admin)
```

---

## Local Development

### Setup

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dev dependencies
make dev-install

# Run tests
make test

# Generate visualizations
make visualize
```

### Common Tasks

```bash
# Run examples
make examples

# Start API locally (debug mode)
make run-api

# CLI testing
make run-cli

# Code formatting
make format

# Run linter
make lint
```

---

## Docker Deployment

### Single Container

```bash
# Build
docker build -t risksense:latest .

# Run
docker run \
  --name risksense-api \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  risksense:latest

# With volume mounts (for batch processing)
docker run \
  --name risksense-api \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  risksense:latest
```

### With Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f risksense-api

# Stop services
docker-compose down

# Full cleanup (volumes, images)
docker-compose down -v
docker rmi risksense:latest
```

### Docker Environment Variables

```bash
FLASK_ENV=production          # Set to 'development' for debug mode
FLASK_DEBUG=0                 # Set to 1 for debug
PYTHONUNBUFFERED=1            # Recommended for container logging
```

---

## Kubernetes Deployment

### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: risksense-api
  namespace: fintech
spec:
  replicas: 3
  selector:
    matchLabels:
      app: risksense
  template:
    metadata:
      labels:
        app: risksense
    spec:
      containers:
      - name: risksense
        image: risksense:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: PYTHONUNBUFFERED
          value: "1"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: risksense-api
  namespace: fintech
spec:
  type: LoadBalancer
  selector:
    app: risksense
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: risksense-hpa
  namespace: fintech
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: risksense-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace fintech

# Apply deployment
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods -n fintech
kubectl logs -f deployment/risksense-api -n fintech

# Port forward for testing
kubectl port-forward -n fintech svc/risksense-api 5000:80
```

---

## Cloud Platforms

### AWS ECS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com

docker tag risksense:latest <ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/risksense:latest
docker push <ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/risksense:latest

# Create ECS task definition and service
# (Use AWS console or Terraform)
```

### Google Cloud Run

```bash
# Build and deploy
gcloud run deploy risksense \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000
```

### Azure Container Instances

```bash
# Build and push to ACR
az login
az acr build --registry <REGISTRY> --image risksense:latest .

# Deploy
az container create \
  --resource-group risksense \
  --name risksense-api \
  --image <REGISTRY>.azurecr.io/risksense:latest \
  --ports 5000 \
  --cpu 1 \
  --memory 1
```

---

## Monitoring & Logging

### Health Checks

```bash
# Basic health check
curl http://localhost:5000/api/health

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2025-04-26T...",
#   "service": "risksense",
#   "version": "0.1.0"
# }
```

### Logging

All logs should be structured JSON for easy parsing:

```python
import logging
import json
from datetime import datetime

logger = logging.getLogger('risksense')

# Log entry format:
logger.info(json.dumps({
    'timestamp': datetime.utcnow().isoformat(),
    'level': 'INFO',
    'service': 'risksense',
    'event': 'score_computed',
    'borrower_id': 'BRW001',
    'risk_score': 28.3,
    'risk_category': 'Low',
    'duration_ms': 45,
}))
```

### Prometheus Metrics

Basic metrics collection (extend as needed):

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
request_count = Counter('risksense_requests_total', 'Total requests')
request_duration = Histogram('risksense_request_duration_seconds', 'Request duration')
active_requests = Gauge('risksense_active_requests', 'Active requests')
model_accuracy = Gauge('risksense_model_accuracy', 'Model accuracy')

# Instrument endpoints
@app.before_request
def before_request():
    active_requests.inc()

@app.after_request
def after_request(response):
    active_requests.dec()
    request_count.inc()
    return response
```

### Grafana Dashboards

Key metrics to monitor:

- **API Latency**: p50, p95, p99 response times
- **Throughput**: Requests per second
- **Error Rate**: Failed requests / total requests
- **Model Performance**: Risk score distribution, category distribution
- **Resource Usage**: CPU, memory, disk I/O

---

## API Usage

### Single Borrower Scoring

```bash
curl -X POST http://localhost:5000/api/score \
  -H "Content-Type: application/json" \
  -d '{
    "annual_income": 2.5,
    "debt_to_income": 0.4,
    "credit_score": 75,
    "employment_stability": 8.0
  }'

# Response:
# {
#   "risk_score": 28.3,
#   "risk_category": "Low",
#   "timestamp": "2025-04-26T..."
# }
```

### Batch Scoring

```bash
curl -X POST http://localhost:5000/api/batch \
  -H "Content-Type: application/json" \
  -d '{
    "borrowers": [
      {
        "annual_income": 2.5,
        "debt_to_income": 0.4,
        "credit_score": 75,
        "employment_stability": 8.0
      },
      {
        "annual_income": 1.2,
        "debt_to_income": 0.6,
        "credit_score": 50,
        "employment_stability": 3.0
      }
    ]
  }'

# Response:
# {
#   "processed": 2,
#   "errors": 0,
#   "results": [
#     {"index": 0, "risk_score": 28.3, "risk_category": "Low"},
#     {"index": 1, "risk_score": 52.1, "risk_category": "Medium"}
#   ]
# }
```

### Model Information

```bash
curl http://localhost:5000/api/model/info

# Returns full model specification including:
# - Input ranges and descriptions
# - Output categories
# - Number of fuzzy rules
# - Author and version information
```

---

## Performance Tuning

### Model Optimization

The Mamdani FIS is already highly optimized:
- Triangular membership functions (fast computation)
- Centroid defuzzification (low overhead)
- ~30 fuzzy rules (not excessive)
- ~100ms per prediction (Python + NumPy)

### API Performance

```bash
# Benchmark single request
ab -n 1000 -c 10 \
  -p payload.json \
  -T application/json \
  http://localhost:5000/api/score

# Expected: 500+ req/sec on modern hardware
# Typical latency: 20–50ms p50, 100–200ms p95
```

### Scaling

For high-volume scoring:

1. **Horizontal scaling**: Run multiple API instances
   - Use load balancer (nginx, HAProxy)
   - Or deploy to Kubernetes with HPA

2. **Batch processing**: Use `/api/batch` endpoint
   - Better throughput than individual requests
   - 10–100 requests per batch recommended

3. **Async processing**: Use message queue (optional)
   - Submit batch jobs to Redis/RabbitMQ
   - Process asynchronously
   - Return results via webhook/polling

### Caching

Consider caching for identical inputs:

```python
from functools import lru_cache

@lru_cache(maxsize=10000)
def score_cached(income, dti, credit, stability):
    return model.score(income, dti, credit, stability)
```

---

## Security Considerations

### Input Validation

All inputs are validated:
- Numeric type checking
- Range bounds verification
- No SQL injection risk (no database)
- No arbitrary code execution

### API Security

**Recommended for production:**

```python
# 1. Rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/score')
@limiter.limit("100 per minute")
def score():
    pass

# 2. Authentication (if needed)
from flask_httpauth import HTTPTokenAuth
auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    return token == os.getenv('API_TOKEN')

# 3. CORS (if consuming from browser)
from flask_cors import CORS
CORS(app, origins=['https://trusted-domain.com'])

# 4. HTTPS (always in production)
# Use reverse proxy (nginx) or container with SSL cert
```

### Data Privacy

- No data persistence (model is stateless)
- No logging of PII (handle separately)
- Consider encryption for transit (TLS/HTTPS)
- Comply with local data protection regulations (NDPR, etc.)

### Model Governance

- Version control all model changes
- Test before deployment
- Monitor for model drift
- Regular recalibration (quarterly recommended)
- Audit trail for all scoring decisions

---

## Support & Issues

For questions or issues:

- **GitHub Issues**: [https://github.com/admoll/risksense-core/issues](https://github.com/admoll/risksense-core/issues)
- **Email**: hello@admoll.dev
- **ORCID**: [0009-0006-0870-6798](https://orcid.org/0009-0006-0870-6798)

---

**RiskSense — Production-ready fuzzy inference for African fintech.**
