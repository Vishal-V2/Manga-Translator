from PySide6.QtCore import (
    Signal, QObject
)

from pipeline.manager.detection import DetectionManager
from pipeline.manager.cleaning import CleaningManager
from pipeline.manager.recognition import RecognitionManager
from pipeline.manager.translation import TranslationManager
from pipeline.manager.typesetting import TypesettingManager

from pipeline.core.box_data import TranslationBatch, TranslationPage, SpeechBubble

from pipeline.core.utility import convert_image
import numpy as np
from PIL import Image
from config.base import ConfigBase



class PageJob:
    def __init__(self, index: int, file_path: str):
        self.page = TranslationPage(
            index=index,
            file_name=file_path,
            image_cv2=None,
            image_pil=None,
            cleaned_image=None
        )
        self.status = "pending"



class AutomaticTranslationBase(QObject):
    receive_selected_files = Signal(list)

    def __init__(self, speech_bubble_model, text_cluster_model, manga_ocr):
        super().__init__()
        self.load_config()

        self.detection_manager = DetectionManager(self.detection_config, speech_bubble_model, text_cluster_model)
        self.cleaning_manager = CleaningManager(self.cleaning_config)
        self.recognition_manager = RecognitionManager(manga_ocr)
        self.translation_manager = TranslationManager(self.api_config, self.translation_config)
        self.typesetting_manager = TypesettingManager()

        self._connect_signals()
    

    def load_config(self):
        self.config = ConfigBase()
        self.api_config = self.config.api_config
        self.detection_config = self.config.detection_config
        self.cleaning_config = self.config.cleaning_config
        self.translation_config = self.config.translation_config


    def _connect_signals(self):
        self.receive_selected_files.connect(self._images_path_received)
        self.detection_manager.data.connect(self._handle_detection_data)
        self.cleaning_manager.data.connect(self._handle_cleaning_data)
        self.recognition_manager.data.connect(self._handle_recognition_data)
        self.translation_manager.data.connect(self._handle_translation_data)
        self.typesetting_manager.data.connect(self._handle_typesetting_data)
    

    def _images_path_received(self, images_path):
        self.batch = TranslationBatch()
        self.jobs = [PageJob(idx, path) for idx, path in enumerate(images_path)]

        self._process_next_job()


    def _process_next_job(self):
        if not self.jobs:
            self._translation_setup()
            return
        
        self.current_job = self.jobs.pop(0)
        self.current_job.status = "processing"
        print(f"Processing page: {self.current_job.page.index}")

        self.current_job.page.image_cv2 = convert_image.to_cv2(self.current_job.page.file_name)
        self.current_job.page.image_pil = convert_image.to_pil(self.current_job.page.file_name)

        self.detection_manager.start(self.current_job.page.image_cv2)
    

    def _translation_setup(self):
        translation_data = {}

        for page in self.batch.pages:
            bubble_data = {}
            for bubble_idx, bubble in enumerate(page.speech_bubbles):
                cluster_data = {
                    cluster_idx: {
                        "jp_text": cluster.jp_text,
                        "tr_text": ""
                    }
                    for cluster_idx, cluster in enumerate(bubble.text_clusters)
                }
                bubble_data[bubble_idx] = cluster_data
            translation_data[page.index] = bubble_data

        self.translation_manager.start(translation_data)
    

    def _handle_detection_data(self, speech_bubbles_data: SpeechBubble):
        job = self.current_job
        job.page.speech_bubbles = speech_bubbles_data
        print(speech_bubbles_data)
        print("FILE: ", job.page.file_name)
        self.cleaning_manager.start(job.page)

    
    def _handle_cleaning_data(self, cleaned_image):
        job = self.current_job
        job.page.cleaned_image = cleaned_image
        self.recognition_manager.start(job.page)
    

    def _handle_recognition_data(self, speech_bubbles_data):
        job = self.current_job
        job.page.speech_bubbles = speech_bubbles_data
        job.status = "done"
        self.batch.pages.append(job.page)

        self._process_next_job()
    

    def _handle_translation_data(self, translated_dict):
        self.translated_dict = translated_dict

        for page in self.batch.pages:
            page_idx = page.index
            page_translations = self.translated_dict.get(str(page_idx), {})

            for bubble_idx, bubble in enumerate(page.speech_bubbles):
                bubble_translations = page_translations.get(str(bubble_idx), {})

                for cluster_idx, cluster in enumerate(bubble.text_clusters):
                    cluster_trans = bubble_translations.get(str(cluster_idx), {})

                    translated_text = cluster_trans.get("tr_text", "")
                    cluster.tr_text = translated_text

                    print("JP:", cluster.jp_text)
                    print("EN:", translated_text)
    
        self.typesetting_manager.start(self.batch)
    

    def _handle_typesetting_data(self):
        print("DONE ALL BATCH")
