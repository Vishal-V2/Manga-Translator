from PySide6.QtCore import (
    Signal, QObject
)

from pipeline.worker.worker_utility import run_in_thread
from pipeline.worker.recognition import RecognitionWorker
from pipeline.core.box_data import SpeechBubble, TranslationPage



class RecognitionManager(QObject):
    data = Signal(list)

    def __init__(self, ocr_engine):
        super().__init__()
        self.ocr_engine = ocr_engine


    def start(self, page_data: TranslationPage):
        speech_bubbles_data = page_data.speech_bubbles
        
        self.worker, self.run_in_thread = run_in_thread(
            RecognitionWorker,
            self.ocr_engine,
            speech_bubbles_data,
            on_finished=self._complete
        )
    

    def _complete(self, speech_bubbles_data: list[SpeechBubble]):
        self.data.emit(speech_bubbles_data)