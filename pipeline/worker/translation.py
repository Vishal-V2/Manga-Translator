from PySide6.QtCore import (
    QObject, Signal, Slot
)

from pipeline.core.translation.base import TranslationBase



class TranslationWorker(QObject):
    finished = Signal(dict)

    def __init__(self, api_config: dict, translation_config: dict, batch_dict: dict):
        super().__init__()
        self.batch_dict = batch_dict
        self.api_config = api_config
        self.translation_config = translation_config
        self.translation_process = TranslationBase(self.api_config, self.translation_config)
    

    @Slot()
    def run(self):
        self._start_text_translation()

        self.finished.emit(self.batch_dict)
    

    def _start_text_translation(self):
        self.batch_dict = self.translation_process.batch_translation(self.batch_dict)