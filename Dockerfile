FROM python:3.11-slim

LABEL maintainer="Ademola Adefemi <hello@admoll.dev>"
LABEL description="RiskSense: Mamdani FIS for fintech credit risk scoring"
LABEL version="0.1.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn flask

# Copy application code
COPY risksense/ ./risksense/
COPY risksense/cli.py ./
COPY tests/ ./tests/

# Create non-root user
RUN useradd -m -u 1000 risksense && \
    chown -R risksense:risksense /app

USER risksense

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from risksense import create_model; model = create_model(); \
                   score, cat = model.score(2.5, 0.4, 75, 8.0); \
                   exit(0 if cat == 'Low' else 1)"

# Default to Python (can be overridden)
ENTRYPOINT ["python", "-m", "risksense.cli"]
CMD ["--help"]
