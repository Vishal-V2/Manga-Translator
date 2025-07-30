import cv2
import numpy as np
from PIL import Image
from pipeline.core.box_data import TextCluster



def apply_text_mask(inpainter: str, mask_canvas: np.ndarray, text_cluster_data: TextCluster) -> np.ndarray:
    text_cluster_image = text_cluster_data.bounding_image
    TCx_min, TCy_min, _, _ = text_cluster_data.position

    gray = cv2.cvtColor(text_cluster_image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    inverted_threshold = cv2.bitwise_not(threshold)

    kernel = np.ones((5, 5), np.uint8)
    dilated_threshold = cv2.dilate(inverted_threshold, kernel, iterations=4)
    contours, _ = cv2.findContours(dilated_threshold, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    relative_contours = []
    for contour in contours:
        relative = contour + [TCx_min, TCy_min]
        relative_contours.append(relative)

    for contour in relative_contours:
        reshaped = np.array(contour, dtype=np.int32).reshape(-1, 1, 2)
        cv2.drawContours(mask_canvas, [reshaped], -1, (0, 0, 0), thickness=cv2.FILLED)

    if inpainter == "lama":    
        mask_canvas = cv2.bitwise_not(mask_canvas)
    return mask_canvas


def batch_apply_text_mask(inpainter: str, mask_canvas: np.ndarray, text_clusters_data: list[TextCluster]) -> Image.Image:
    image_np = mask_canvas
    for text_cluster_data in text_clusters_data:
        if text_cluster_data.bounding_image is None:
            continue
        image_np = apply_text_mask(inpainter, mask_canvas, text_cluster_data)
    
    image_mask_pil = Image.fromarray(image_np)
    image_mask_pil.save("output/image_mask.png")

    return image_mask_pil