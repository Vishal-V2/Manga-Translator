from manga_ocr import MangaOcr
from PIL import Image
import cv2
import numpy as np

from pipeline.core.box_data import SpeechBubble, TextCluster
from pipeline.core.utility import convert_image



class TextRecognition:
    def __init__(self, manga_ocr: MangaOcr):
        self.manga_ocr = manga_ocr
    

    def _text_recognition_single(self, text_cluster_data: TextCluster) -> str:
        text_cluster_image = text_cluster_data.bounding_image
        text_cluster_image_pil = convert_image.cv2_to_pil(text_cluster_image)

        ocr_results = self.manga_ocr(text_cluster_image_pil)
        print("OCR: ", ocr_results)
        return ocr_results

    
    def _text_recognition_batch(self, speech_bubbles_data: list[SpeechBubble]) -> list[SpeechBubble]:
        for speech_bubble_data in speech_bubbles_data:
            if speech_bubble_data.bounding_image is None:
                continue
            
            text_clusters_data = speech_bubble_data.text_clusters
            
            for text_cluster_data in text_clusters_data:
                if text_cluster_data.bounding_image is None:
                    continue
                jp_text = self._text_recognition_single(text_cluster_data)
                text_cluster_data.jp_text = jp_text
        
        return speech_bubbles_data
    

    def text_recognition(self, data: TextCluster | list[SpeechBubble]) -> str | list[SpeechBubble]:
        if isinstance(data, TextCluster):
            return self._text_recognition_single(data)
        elif isinstance(data, list):
            return self._text_recognition_batch(data)