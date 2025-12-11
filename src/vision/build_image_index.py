# src/vision/build_image_index.py

import os
import pickle
from PIL import Image
import numpy as np
from sentence_transformers import SentenceTransformer

# Compute absolute paths based on this file location
THIS_DIR = os.path.dirname(__file__)                     # ...\src\vision
BASE_DIR = os.path.dirname(os.path.dirname(THIS_DIR))    # ...\ (CaptionAI root)

TEMPLATES_DIR = os.path.join(BASE_DIR, "data", "templates")
INDEX_PATH = os.path.join(BASE_DIR, "models", "clip_image_index.pkl")
MODEL_NAME = "clip-ViT-B-32"

ALLOWED_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".jfif")


def load_images():
    images = []
    filenames = []

    if not os.path.isdir(TEMPLATES_DIR):
        print(f"[build_image_index] Templates directory does NOT exist: {TEMPLATES_DIR}")
        return images, filenames

    print(f"[build_image_index] Loading templates from: {TEMPLATES_DIR}")

    for fname in os.listdir(TEMPLATES_DIR):
        if not fname.lower().endswith(ALLOWED_EXTS):
            continue

        path = os.path.join(TEMPLATES_DIR, fname)
        try:
            img = Image.open(path).convert("RGB")
            images.append(img)
            filenames.append(path)
            print(f"[build_image_index] Loaded: {path}")
        except Exception as e:
            print(f"[build_image_index] Error loading {path}: {e}")

    print(f"[build_image_index] Total loaded templates: {len(images)}")
    return images, filenames


def build_index():
    images, filenames = load_images()

    if len(images) == 0:
        print(
            "[build_image_index] ERROR: No valid images loaded.\n"
            f"Ensure you have at least one image in: {TEMPLATES_DIR}\n"
            f"Extensions allowed: {ALLOWED_EXTS}"
        )
        return

    print(f"[build_image_index] Encoding {len(images)} images with CLIP model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)

    image_embeddings = model.encode(
        images,
        batch_size=8,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    index = {
        "filenames": filenames,
        "embeddings": image_embeddings,
        "model_name": MODEL_NAME,
    }

    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    with open(INDEX_PATH, "wb") as f:
        pickle.dump(index, f)

    print(f"[build_image_index] Saved index to: {INDEX_PATH}")


if __name__ == "__main__":
    build_index()
