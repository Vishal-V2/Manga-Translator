from PySide6.QtCore import (
    Signal, QObject
)

from pipeline.worker.worker_utility import run_in_thread
from pipeline.worker.translation import TranslationWorker



class TranslationManager(QObject):
    data = Signal(dict)

    def __init__(self, api_config: dict, translation_config: dict):
        super().__init__()
        self.api_config = api_config
        self.translation_config = translation_config


    def start(self, texts_data: dict):
        self.worker, self.run_in_thread = run_in_thread(
            TranslationWorker,
            self.api_config,
            self.translation_config,
            texts_data,
            on_finished=self._complete
        )
    

    def _complete(self, translated_texts_data: dict):
        self.data.emit(translated_texts_data)