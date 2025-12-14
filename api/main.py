from fastapi import FastAPI
from pydantic import BaseModel
import time

from training.ad_generator import AdGenerator
from training.quality_check import validity_score

app = FastAPI(
    title="E-Commerce Ad Creative Generator",
    description="Generates marketing ad creatives using a lightweight LLM",
    version="1.0"
)

generator = AdGenerator()

class AdRequest(BaseModel):
    product_name: str
    category: str
    description: str


class AdResponse(BaseModel):
    generated_ad: str
    quality_score: float
    latency_ms: float

@app.post("/generate-ad", response_model=AdResponse)
def generate_ad(request: AdRequest):
    start_time = time.time()

    prompt = (
        f"Generate a short promotional ad for the following product:\n"
        f"Product: {request.product_name}\n"
        f"Category: {request.category}\n"
        f"Description: {request.description}"
    )

    ad_text = generator.generate_ad(prompt)
    score = validity_score(ad_text)

    latency = (time.time() - start_time) * 1000

    return AdResponse(
        generated_ad=ad_text,
        quality_score=score,
        latency_ms=round(latency, 2)
    )



