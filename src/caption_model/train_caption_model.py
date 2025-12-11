# src/caption_model/train_caption_model.py
import os
import pandas as pd
from datasets import load_dataset, Dataset
from transformers import (
    GPT2TokenizerFast,
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)

DATA_PATH = "data/campaign_corpus.csv"
MODEL_NAME = "gpt2"          # or "gpt2-medium" if you have more GPU
OUTPUT_DIR = "models/caption_generator"

def load_campaign_dataset():
    df = pd.read_csv(DATA_PATH)
    # simple sanity clean
    df = df.dropna(subset=["topic", "tone", "campaign", "caption"])

    def to_text(row):
        # conditioning format
        return (
            f"topic: {row['topic']} | "
            f"tone: {row['tone']} | "
            f"campaign: {row['campaign']} | "
            f"meme_caption: {row['caption']}"
        )

    texts = [to_text(r) for _, r in df.iterrows()]
    return Dataset.from_dict({"text": texts})

def main():
    dataset = load_campaign_dataset()

    tokenizer = GPT2TokenizerFast.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=128,
            padding="max_length",
        )

    tokenized = dataset.map(tokenize, batched=True, remove_columns=["text"])
    tokenized.set_format("torch")

    model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
    model.resize_token_embeddings(len(tokenizer))

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        overwrite_output_dir=True,
        per_device_train_batch_size=4,
        num_train_epochs=3,
        learning_rate=5e-5,
        weight_decay=0.01,
        logging_steps=50,
        save_steps=500,
        save_total_limit=2,
        fp16=False,  # set True if GPU with mixed precision
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        data_collator=data_collator,
    )

    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

if __name__ == "__main__":
    main()
