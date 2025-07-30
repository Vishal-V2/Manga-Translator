from ultralytics import YOLO
from pipeline.core.box_data import SpeechBubble, TextCluster
import constants
from pipeline.core.detection import overlap



class TextClusterDetection:
    def __init__(self, model: YOLO):
        self.model = model
    

    def _detect_single(self, SBdata: SpeechBubble) -> list[TextCluster]:
        TCdata: list[TextCluster] = []
        SBx_min, SBy_min, _, _ = SBdata.position

        if SBdata.class_name == constants.FRAMELESS_CLASS_NAME:
            TCdata.append(TextCluster(
                position = SBdata.position,
                confidence = SBdata.confidence,
                bounding_image = SBdata.bounding_image,
                jp_text = None,
                tr_text = None
            ))

            return TCdata

        TCresult = self.model(SBdata.bounding_image)[0]

        if not TCresult.boxes:
            return TCdata
        
        for box in TCresult.boxes:
            TCconf = round(box.conf.item(), 2)
            if TCconf < constants.TEXT_CLUSTER_THRESHOLD:
                continue

            TCx_min, TCy_min, TCx_max, TCy_max = map(int, box.xyxy.tolist()[0])
            relative_pos = (
                SBx_min + TCx_min, SBy_min + TCy_min, 
                SBx_min + TCx_max, SBy_min + TCy_max 
            )

            bounding_image =  SBdata.bounding_image[TCy_min:TCy_max, TCx_min:TCx_max]

            TCdata.append(TextCluster(
                position = relative_pos,
                confidence = TCconf,
                bounding_image = bounding_image,
                jp_text = None,
                tr_text = None,
            ))
        
        return TCdata
    

    def _detect_batch(self, SBdata: list[SpeechBubble]) -> list[SpeechBubble]:
        SBupdated_data: list[SpeechBubble] = []

        for SB in SBdata:
            TCdata = self._detect_single(SB)

            if TCdata:
                SB.text_clusters = TCdata
                SBupdated_data.append(SB)
        
        SBupdated_data = overlap.overlap(SBupdated_data)
        
        return SBupdated_data


    def detect(self, SBdata: SpeechBubble | list[SpeechBubble]) -> list[TextCluster] | list[SpeechBubble]:
        if isinstance(SBdata, list):
            return self._detect_batch(SBdata)
        
        return self._detect_single(SBdata)
        
