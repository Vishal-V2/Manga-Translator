import easyocr
import cv2
import numpy as np

from pipeline.core.box_data import SpeechBubble, TextCluster



class EasyOcrRecognition:
    # Map config language names to EasyOCR language codes
    LANG_MAP = {
        "japanese": ["ja", "en"],
        "chinese_simplified": ["ch_sim", "en"],
        "chinese_traditional": ["ch_tra", "en"],
        "korean": ["ko", "en"],
    }

    def __init__(self, language: str = "japanese"):
        lang_codes = self.LANG_MAP.get(language, ["ja", "en"])
        self.reader = easyocr.Reader(lang_codes, gpu=True)
        self.language = language
        print(f"EasyOCR initialized for language: {language} ({lang_codes})")


    def _text_recognition_single(self, text_cluster_data: TextCluster) -> str:
        text_cluster_image = text_cluster_data.bounding_image
        if text_cluster_image is None:
            return ""

        results = self.reader.readtext(text_cluster_image, detail=0)
        ocr_text = " ".join(results).strip()
        print("OCR: ", ocr_text)
        return ocr_text


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
