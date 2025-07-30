from ultralytics import YOLO
from manga_ocr import MangaOcr
import constants

speech_bubble_model = None
text_cluster_model = None
manga_ocr = None

def load_all_models():
    global speech_bubble_model, text_cluster_model, manga_ocr
    
    speech_bubble_model = YOLO(constants.SPEECH_BUBBLE_MODEL_PATH)
    text_cluster_model = YOLO(constants.TEXT_CLUSTER_MODEL_PATH)
    manga_ocr = MangaOcr()

    return speech_bubble_model, text_cluster_model, manga_ocr