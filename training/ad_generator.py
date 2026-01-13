from transformers import pipeline

class AdGenerator:
    def __init__(self, model_name="google/flan-t5-small"):
        self.generator = pipeline(
            task="text2text-generation",
            model=model_name,
            device=-1  # CPU
        )

    def generate(self, product_name: str, description: str) -> str:
        prompt = f"Create a short catchy ad for {product_name}. Description: {description}"
        result = self.generator(
            prompt,
            max_length=60,
            do_sample=True,
            temperature=0.9,
            top_p=0.95
        )
        return result[0]["generated_text"]
