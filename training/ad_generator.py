from transformers import pipeline

class AdGenerator:
    def __init__(self, model_name="google/flan-t5-small"):
        self.generator = pipeline(
            task="text2text-generation",
            model=model_name,
            device=-1  # CPU only
        )

    def generate_ad(self, prompt: str, max_length: int = 60) -> str:
        result = self.generator(
            prompt,
            max_length=max_length,
            do_sample=True,
            temperature=0.9,
            top_p=0.95
        )
        return result[0]["generated_text"]
