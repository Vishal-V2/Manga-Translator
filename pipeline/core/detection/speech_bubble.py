from ultralytics import YOLO
import numpy as np

from pipeline.core.box_data import SpeechBubble
import constants


class SpeechBubbleDetection:
    def __init__(self, model: YOLO):
        self.model = model
    

    def detect(self, image: np.ndarray) -> list[SpeechBubble]:
        SBdata: list[SpeechBubble] = []
        SBresult = self.model(image)[0]

        if not SBresult.boxes:
            return SBdata
        
        for box in SBresult.boxes:
            SBconf = round(box.conf.item(), 2)
            if SBconf < constants.SPEECH_BUBBLE_THRESHOLD:
                continue
            
            SBx_min, SBy_min, SBx_max, SBy_max = map(int, box.xyxy.tolist()[0])
            
            class_id = int(box.cls.item())
            class_name = self.model.names[class_id]

            bounding_image = image[SBy_min:SBy_max, SBx_min:SBx_max]

            SBdata.append(SpeechBubble(
                position=(SBx_min, SBy_min, SBx_max, SBy_max),
                confidence=SBconf,
                class_name=class_name,
                bounding_image=bounding_image,
                text_clusters=None
            ))
        
        return SBdata
