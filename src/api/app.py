# src/api/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from ..caption_model.generate_caption import CaptionGenerator
from ..vision.select_template import TemplateSelector
from ..meme_renderer.render_meme import render_meme  # drake-style render

app = FastAPI(title="Gov Awareness Meme Generator (Drake Style)")

caption_gen = CaptionGenerator()
template_selector = TemplateSelector()


class MemeRequest(BaseModel):
    # For AI generation
    topic: Optional[str] = None
    tone: str = "humorous"
    campaign: str = "generic_campaign"

    # Explicit text from user (preferred if provided)
    top_text: Optional[str] = None
    bottom_text: Optional[str] = None

    # Single string format: "top || bottom"
    caption_override: Optional[str] = None


class MemeResponse(BaseModel):
    top_text: str
    bottom_text: str
    template_path: str
    meme_path: str
    similarity_score: float


def split_caption_into_two(caption: str) -> tuple[str, str]:
    """
    If caption is like 'Top || Bottom', split on '||'.
    Otherwise, split words roughly in half.
    """
    if "||" in caption:
        top, bottom = caption.split("||", 1)
        return top.strip(), bottom.strip()

    words = caption.split()
    if len(words) <= 4:
        # Too short to split
        return caption, ""

    mid = len(words) // 2
    top = " ".join(words[:mid])
    bottom = " ".join(words[mid:])
    return top, bottom


@app.post("/generate_meme", response_model=MemeResponse)
def generate_meme(req: MemeRequest):
    # ---------- 1) Decide top_text & bottom_text ----------
    if req.top_text and req.bottom_text:
        # User provided both explicitly
        top_text = req.top_text
        bottom_text = req.bottom_text

    elif req.caption_override:
        # e.g. "Doing your own research for a test || Copy and pasting from Wikipedia"
        top_text, bottom_text = split_caption_into_two(req.caption_override)

    else:
        # Use AI caption
        topic = req.topic or "generic_awareness"
        caps = caption_gen.generate(topic, req.tone, req.campaign, num_return_sequences=1)
        caption = caps[0]
        top_text, bottom_text = split_caption_into_two(caption)

    # ---------- 2) Choose template with CLIP ----------
    caption_for_clip = (top_text + " " + bottom_text).strip()
    template_path, score = template_selector.select(caption_for_clip)

    # ---------- 3) Render Drake-style meme ----------
    meme_path = render_meme(template_path, top_text, bottom_text)

    return MemeResponse(
        top_text=top_text,
        bottom_text=bottom_text,
        template_path=template_path,
        meme_path=meme_path,
        similarity_score=score,
    )
