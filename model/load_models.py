from ultralytics import YOLO
from manga_ocr import MangaOcr
import constants
import logging
import warnings

try:
    from transformers.utils import logging as hf_logging
    hf_logging.set_verbosity_error()
except Exception:
    pass

logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("manga_ocr").setLevel(logging.ERROR)
logging.getLogger("manga_ocr.ocr").setLevel(logging.ERROR)

warnings.filterwarnings("ignore", category=UserWarning, message=".*unauthenticated requests to the HF Hub.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*tie.*word_embeddings.*")

try:
    from loguru import logger as _loguru_logger
    _loguru_logger.remove()
    _loguru_logger.add(lambda msg: None, level="ERROR")
except Exception:
    pass

speech_bubble_model = None
text_cluster_model = None
manga_ocr = None

def load_all_models():
    global speech_bubble_model, text_cluster_model, manga_ocr
    
    speech_bubble_model = YOLO(constants.SPEECH_BUBBLE_MODEL_PATH)
    text_cluster_model = YOLO(constants.TEXT_CLUSTER_MODEL_PATH)
    manga_ocr = MangaOcr()

    return speech_bubble_model, text_cluster_model, manga_ocr