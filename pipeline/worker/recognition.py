from PySide6.QtCore import (
    QObject, Signal, Slot
)
from manga_ocr import MangaOcr

from pipeline.core.recognition.manga_ocr import TextRecognition
from pipeline.core.box_data import SpeechBubble



class RecognitionWorker(QObject):
    finished = Signal(list)

    def __init__(self, manga_ocr: MangaOcr, speech_bubbles_data: list[SpeechBubble]):
        super().__init__()
        self.text_recogntion = TextRecognition(manga_ocr)
        self.speech_bubbles_data = speech_bubbles_data
    

    @Slot()
    def run(self):
        self._text_recognition()
        
        self.finished.emit(self.speech_bubbles_data)
    

    def _text_recognition(self):
        self.speech_bubbles_data = self.text_recogntion.text_recognition(self.speech_bubbles_data)
