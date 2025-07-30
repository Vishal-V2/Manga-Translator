from dataclasses import dataclass, field
import numpy as np
from PIL import Image

@dataclass
class TextCluster:
    position: tuple[int, int, int, int]
    confidence: float
    bounding_image: np.ndarray | None = None
    jp_text: str | None = None
    tr_text: str | None = None
    area: float | None = None


@dataclass
class SpeechBubble:
    position: tuple[int, int, int, int]
    confidence: float
    class_name: str
    bounding_image: np.ndarray | None = None
    text_clusters: list[TextCluster] = field(default_factory=list)


@dataclass
class TranslationPage:
    index: int
    file_name: str
    image_cv2: np.ndarray
    image_pil: Image.Image
    cleaned_image: Image.Image
    speech_bubbles: list[SpeechBubble] = field(default_factory=list)



@dataclass
class TranslationBatch:
    pages: list[TranslationPage] = field(default_factory=list)