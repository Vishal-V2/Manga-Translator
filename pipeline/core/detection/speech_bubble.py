from ultralytics import YOLO
import numpy as np
import cv2

from pipeline.core.box_data import SpeechBubble
import constants


def _iou(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    if inter_x2 <= inter_x1 or inter_y2 <= inter_y1:
        return 0.0
    inter = (inter_x2 - inter_x1) * (inter_y2 - inter_y1)
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    union = max(area_a + area_b - inter, 1)
    return inter / union


class SpeechBubbleDetection:
    def __init__(self, model: YOLO, threshold: float | None = None):
        self.model = model
        self.threshold = threshold if threshold is not None else constants.SPEECH_BUBBLE_THRESHOLD
    

    def detect(self, image: np.ndarray) -> list[SpeechBubble]:
        SBdata: list[SpeechBubble] = []
        SBresult = self.model(image)[0]

        if not SBresult.boxes:
            pass
        
        if SBresult.boxes:
            for box in SBresult.boxes:
                SBconf = round(box.conf.item(), 2)
                if SBconf < self.threshold:
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

        # Always run classical-vision fallback to supplement missing bubbles
        h, w = image.shape[:2]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # Otsu threshold; bubbles are typically bright inside
        _, bin_img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((7, 7), np.uint8)
        closed = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel, iterations=2)
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, ww, hh = cv2.boundingRect(cnt)
            area = ww * hh
            if area <= 0:
                continue
            ratio = area / float(w * h)
            # relax thresholds to catch tall/skinny bubbles too
            if ratio < 0.005 or ratio > 0.60:
                continue
            if ww < 24 or hh < 48:
                continue
            aspect = ww / float(hh)
            if aspect < 0.15 or aspect > 6.0:
                continue
            roi_mean = np.mean(gray[max(0, y):min(h, y + hh), max(0, x):min(w, x + ww)])
            if roi_mean < 160:  # bubbles tend to be light
                continue
            candidate = (x, y, x + ww, y + hh)
            # only add if not overlapping with existing YOLO bubbles too much
            if any(_iou(candidate, sb.position) > 0.30 for sb in SBdata):
                continue
            bounding_image = image[y:y + hh, x:x + ww]
            SBdata.append(SpeechBubble(
                position=candidate,
                confidence=0.30,
                class_name="standard",
                bounding_image=bounding_image,
                text_clusters=None
            ))

        return SBdata
