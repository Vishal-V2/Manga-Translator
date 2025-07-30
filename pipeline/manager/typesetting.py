from PySide6.QtCore import Signal, QObject

from pipeline.worker.worker_utility import run_in_thread
from pipeline.worker.typesetting import TypesettingWorker
from pipeline.core.box_data import TranslationBatch



class TypesettingManager(QObject):
    data = Signal()

    def __init__(self):
        super().__init__()


    def start(self, batch_data: TranslationBatch):
        self.worker, self.run_in_thread = run_in_thread(
            TypesettingWorker,
            batch_data,
            on_finished=self._complete
        )
    

    def _complete(self):
        self.data.emit()