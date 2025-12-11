import os
import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

# Path where a *fine-tuned* model would be saved
FINETUNED_MODEL_DIR = "models/caption_generator"
# Name of the base model to fallback to if fine-tuned model not found
BASE_MODEL_NAME = "gpt2"


class CaptionGenerator:
    def __init__(
        self,
        model_dir: str = FINETUNED_MODEL_DIR,
        device: str = None,
        use_pretrained_fallback: bool = True,
    ):
        """
        Tries to load a fine-tuned GPT-2 from `model_dir`.
        If not found and use_pretrained_fallback=True, it loads base 'gpt2' from Hugging Face.
        """

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device

        # Check if fine-tuned model exists (config.json is a good indicator)
        has_finetuned = (
            os.path.isdir(model_dir)
            and os.path.exists(os.path.join(model_dir, "config.json"))
        )

        if has_finetuned:
            print(f"[CaptionGenerator] Loading fine-tuned model from: {model_dir}")
            self.tokenizer = GPT2TokenizerFast.from_pretrained(model_dir)
            self.model = GPT2LMHeadModel.from_pretrained(model_dir)
        else:
            if not use_pretrained_fallback:
                raise FileNotFoundError(
                    f"Fine-tuned model not found at '{model_dir}'. "
                    f"Run the training script first, or enable fallback."
                )

            # Fallback: base GPT-2 from Hugging Face hub
            print(
                f"[CaptionGenerator] Fine-tuned model NOT found at '{model_dir}'.\n"
                f"[CaptionGenerator] Falling back to base model: '{BASE_MODEL_NAME}'."
            )
            self.tokenizer = GPT2TokenizerFast.from_pretrained(BASE_MODEL_NAME)
            self.model = GPT2LMHeadModel.from_pretrained(BASE_MODEL_NAME)

        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.to(self.device)

    def generate(
        self,
        topic: str,
        tone: str,
        campaign: str,
        max_new_tokens: int = 25,
        num_return_sequences: int = 3,
    ):
        """
        Generate meme captions given topic, tone, and campaign.
        """

        prompt = (
            f"topic: {topic} | "
            f"tone: {tone} | "
            f"campaign: {campaign} | "
            f"meme_caption:"
        )

        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                temperature=0.9,
                top_p=0.95,
                do_sample=True,
                num_return_sequences=num_return_sequences,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        captions = []
        for o in outputs:
            text = self.tokenizer.decode(o, skip_special_tokens=True)
            # keep only part after "meme_caption:"
            cap = text.split("meme_caption:")[-1].strip()
            cap = cap.split("\n")[0]
            captions.append(cap)
        return captions


if __name__ == "__main__":
    gen = CaptionGenerator()
    caps = gen.generate("road_safety", "humorous", "road_safety_bharat")
    for c in caps:
        print(">>", c)
