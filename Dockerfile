# ---------- Credit Risk Predictor (Streamlit) ----------
FROM python:3.12-slim

# Python behaviour: no .pyc files, unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# XGBoost needs the OpenMP runtime, which the slim image doesn't include
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

WORKDIR /srv

# Install dependencies first so this layer is cached between code changes
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy only what the app needs at runtime.
# model_loader.py resolves ../../artifacts relative to app/utils/,
# so app/ and artifacts/ must stay side by side.
COPY app/ ./app/
COPY artifacts/ ./artifacts/

# Run as a non-root user
RUN useradd --create-home --uid 1000 appuser && chown -R appuser /srv
USER appuser

# The app imports utils/, components/, pages/ relative to app/
WORKDIR /srv/app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "main.py","--server.address=0.0.0.0","--server.port=8501","--server.headless=true","--browser.gatherUsageStats=false"]
