from PySide6.QtCore import (
    QObject, Signal, Slot
)

from pipeline.core.typesetting.typesetting import TypesettingProcess
from pipeline.core.box_data import TranslationBatch



class TypesettingWorker(QObject):
    finished = Signal()

    def __init__(self, batch_data: TranslationBatch):
        super().__init__()
        self.typesetting_process = TypesettingProcess()
        self.batch_data = batch_data


    @Slot()
    def run(self):
        self._start_text_typesetting()

        self.finished.emit()
    

    def _start_text_typesetting(self):
        for pages in self.batch_data.pages:
            image_qt = self.typesetting_process.convert_image(pages.cleaned_image)
            self.typesetting_process.set_image(image_qt)

            self.typesetting_process.load_font()
            self.typesetting_process.batch_text_typesetting(pages.speech_bubbles, pages.index)