# backend/main.py
import os
import base64
import json
from io import BytesIO
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google.genai import types
import google.generativeai as genai

from google import genai
from google.genai.types import GenerateContentConfig


# -------------------------
# CONFIG — YOUR API KEY
# ------------------------- 
API_KEY = "AIzaSyAXwrziKIk_SVGj2rm5joNbK9GXSTuxGNk"
MODEL_NAME = "gemini-3-pro-image-preview"

client = genai.Client(api_key=API_KEY)

app = FastAPI(title="Meme Generator (Gemini)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    topic: str
    top_text: Optional[str] = None
    bottom_text: Optional[str] = None


@app.post("/generate")
async def generate(req: GenerateRequest):
    topic = req.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")


    prompt = prompt = f"""
        You are a creative meme generator.

        The user will provide a GOVERNMENT RULE or NEW POLICY.
        Your task:

        1. Create a FUNNY MEME ABOUT THE RULE.
        2. You decide the meme style (reaction meme, character meme, relatable meme, sarcastic, etc.)
        3. You decide the visual (cartoon, real photo style, exaggerated expression, template-like pose, etc.)
        4. You decide the top and bottom caption text.

        RETURN TWO PARTS:

        PART 1 — TEXT (JSON ONLY):
        {{
        "top_text": "<top line of meme>",
        "bottom_text": "<bottom line of meme>",
        "caption": "<combined caption or explanation>"
        }}

        PART 2 — IMAGE:
        Generate a meme-style image that visually represents the rule in a humorous or exaggerated way.
        The image should match the caption’s meaning.

        IMPORTANT RULES:
        - JSON must contain only valid JSON (no extra text).
        - Be creative — every rule should produce a different style of meme.
        - The visual should be funny or exaggerated.
        - If the rule is serious, still make the meme humorous but not offensive.

        USER RULE:
        "{topic}"
        """


    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini request failed: {e}")

    # ------------------------------
    # EXTRACT JSON + IMAGE (WORKING)
    # ------------------------------
    caption = None
    image_b64 = None

    try:
        for cand in response.candidates:
            parts = cand.content.parts

            for part in parts:
                # TEXT PART
                if hasattr(part, "text") and part.text:
                    txt = part.text.strip()
                    try:
                        json_obj = json.loads(txt)
                        caption = json_obj.get("caption")
                    except:
                        pass

                # IMAGE PART
                if hasattr(part, "inline_data") and part.inline_data:
                    raw = part.inline_data.data  # RAW IMAGE BYTES
                    if raw:
                        image_b64 = base64.b64encode(raw).decode("utf-8")

            if image_b64:
                break

        if not image_b64:
            raise RuntimeError("Gemini did not return inline_data image")

        if not caption:
            caption = f"Meme about {topic}"

        return {
            "caption": caption,
            "image_b64": image_b64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse Gemini response: {e}")
