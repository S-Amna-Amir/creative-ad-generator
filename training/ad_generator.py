import torch
from transformers import pipeline

class AdGenerator:
    def __init__(self):
        self.generator = pipeline(
            "text-generation",
            model="gpt2",
            device=-1  # CPU only
        )

    def generate(self, product_name: str, description: str) -> str:
        prompt = (
            f"Create a short, catchy social media ad for the following product.\n"
            f"Product: {product_name}\n"
            f"Description: {description}\n"
            f"Ad:"
        )

        output = self.generator(
            prompt,
            max_length=80,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.9
        )

        return output[0]["generated_text"]
