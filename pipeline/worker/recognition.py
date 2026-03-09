from PySide6.QtCore import (
    QObject, Signal, Slot
)

from pipeline.core.recognition.manga_ocr import TextRecognition
from pipeline.core.recognition.easyocr_recognition import EasyOcrRecognition
from pipeline.core.box_data import SpeechBubble



class RecognitionWorker(QObject):
    finished = Signal(list)

    def __init__(self, ocr_engine, speech_bubbles_data: list[SpeechBubble]):
        super().__init__()
        # ocr_engine is either a MangaOcr instance or an EasyOcrRecognition instance
        if isinstance(ocr_engine, EasyOcrRecognition):
            self.text_recognition_engine = ocr_engine
        else:
            self.text_recognition_engine = TextRecognition(ocr_engine)
        self.speech_bubbles_data = speech_bubbles_data
    

    @Slot()
    def run(self):
        self._text_recognition()
        
        self.finished.emit(self.speech_bubbles_data)
    

    def _text_recognition(self):
        self.speech_bubbles_data = self.text_recognition_engine.text_recognition(self.speech_bubbles_data)
