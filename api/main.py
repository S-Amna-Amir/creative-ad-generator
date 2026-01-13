from fastapi import FastAPI
from pydantic import BaseModel
import time
import re

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)
from starlette.responses import Response

from training.ad_generator import AdGenerator

app = FastAPI(title="Ad Creative Generator")

generator = AdGenerator()

# --------------------
# Prometheus Metrics
# --------------------

REQUEST_COUNT = Counter(
    "ad_requests_total",
    "Total number of ad generation requests"
)

REQUEST_LATENCY = Histogram(
    "ad_request_latency_seconds",
    "Latency for ad generation"
)

CONTENT_VALIDITY = Gauge(
    "ad_content_validity_score",
    "Heuristic-based content quality score"
)

# --------------------
# Schemas
# --------------------

class AdRequest(BaseModel):
    product_name: str
    description: str

class AdResponse(BaseModel):
    ad_text: str

# --------------------
# Helpers
# --------------------

def compute_validity_score(text: str) -> float:
    score = 0.0
    if len(text) > 20:
        score += 0.4
    if re.search(r"(buy|shop|order|discover|limited)", text.lower()):
        score += 0.3
    if len(text.split()) < 80:
        score += 0.3
    return min(score, 1.0)

# --------------------
# Endpoints
# --------------------

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    return {"ready": True}

@app.post("/generate_ad", response_model=AdResponse)
def generate_ad(req: AdRequest):
    start_time = time.time()
    REQUEST_COUNT.inc()

    ad_text = generator.generate(req.product_name, req.description)

    latency = time.time() - start_time
    REQUEST_LATENCY.observe(latency)

    CONTENT_VALIDITY.set(compute_validity_score(ad_text))

    return {"ad_text": ad_text}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
