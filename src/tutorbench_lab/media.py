"""Image loading helpers for multimodal model calls."""

from __future__ import annotations

import base64
import mimetypes
from dataclasses import dataclass
from pathlib import Path

import httpx

from tutorbench_lab.schemas import ImageRef


@dataclass(frozen=True)
class EncodedImage:
    data: bytes
    media_type: str

    @property
    def data_base64(self) -> str:
        return base64.b64encode(self.data).decode("ascii")

    @property
    def data_url(self) -> str:
        return f"data:{self.media_type};base64,{self.data_base64}"


def load_image(ref: ImageRef, *, timeout_s: float = 30.0) -> EncodedImage | None:
    """Load an ImageRef as base64. Returns None for text-only rows."""

    if ref.path:
        path = Path(ref.path)
        data = path.read_bytes()
        media_type = mimetypes.guess_type(path.name)[0] or ref.media_type
        return EncodedImage(data, media_type)

    if ref.url:
        with httpx.Client(timeout=timeout_s, follow_redirects=True) as client:
            response = client.get(ref.url)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").split(";", 1)[0]
            media_type = content_type or mimetypes.guess_type(ref.url)[0] or ref.media_type
            return EncodedImage(response.content, media_type)

    return None
