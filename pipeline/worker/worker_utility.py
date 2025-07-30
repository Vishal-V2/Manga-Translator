from PySide6.QtCore import QThread



def run_in_thread(worker_class, *args, on_finished=None, **kwargs):
    thread = QThread()
    worker = worker_class(*args, **kwargs)

    worker.moveToThread(thread)

    thread.started.connect(worker.run)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)

    if on_finished is not None:
        worker.finished.connect(on_finished)

    thread.start()

    return worker, thread
