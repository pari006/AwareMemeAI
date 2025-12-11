# src/vision/select_template.py

import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Tuple

from .build_image_index import build_index

# Compute absolute base dir
THIS_DIR = os.path.dirname(__file__)                     # ...\src\vision
BASE_DIR = os.path.dirname(os.path.dirname(THIS_DIR))    # ...\ (CaptionAI root)
INDEX_PATH = os.path.join(BASE_DIR, "models", "clip_image_index.pkl")


class TemplateSelector:
    def __init__(self, index_path: str = INDEX_PATH):
        # Auto-build index if missing
        if not os.path.exists(index_path):
            print(f"[TemplateSelector] Index not found at '{index_path}'. Building it...")
            build_index()

        if not os.path.exists(index_path):
            raise FileNotFoundError(
                f"[TemplateSelector] Failed to find or build index at '{index_path}'. "
                f"Check that you have valid images in 'data/templates'."
            )

        try:
            with open(index_path, "rb") as f:
                data = pickle.load(f)
        except EOFError:
            raise RuntimeError(
                f"[TemplateSelector] Index file '{index_path}' is empty or corrupted. "
                f"Delete it and run 'python src/vision/build_image_index.py' again."
            )

        self.filenames = data.get("filenames", [])
        self.image_embeddings = data.get("embeddings", None)
        self.model_name = data.get("model_name", "clip-ViT-B-32")

        print(f"[TemplateSelector] Loaded index with {len(self.filenames)} templates.")

        if self.image_embeddings is None or len(self.filenames) == 0:
            raise ValueError(
                "Template index contains no embeddings or filenames. "
                "Ensure there are valid images in data/templates and rebuild the index."
            )

        self.model = SentenceTransformer(self.model_name)
        self.image_embeddings = self.image_embeddings / np.linalg.norm(
            self.image_embeddings, axis=1, keepdims=True
        )

    def select(self, caption: str) -> Tuple[str, float]:
        text_emb = self.model.encode([caption], convert_to_numpy=True)[0]
        text_emb = text_emb / np.linalg.norm(text_emb)
        sims = np.dot(self.image_embeddings, text_emb)
        idx = int(np.argmax(sims))
        return self.filenames[idx], float(sims[idx])


if __name__ == "__main__":
    selector = TemplateSelector()
    fname, score = selector.select("Wear a helmet, not a halo.")
    print(fname, score)
