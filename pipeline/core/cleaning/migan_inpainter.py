import numpy as np
from PIL import Image
import onnxruntime
import constants



class MiganInpainter:
    def __init__(self):
        self.model = onnxruntime.InferenceSession(constants.MIGAN_MODEL_PATH)


    def inpaint(self, image_pil: Image.Image, image_mask: Image.Image) -> Image.Image:
        rgb_image = image_pil.convert('RGB')
        grayscale_mask = image_mask.convert('L')

        image_np = np.array(rgb_image).astype(np.uint8)
        image_np = np.transpose(image_np, (2, 0, 1))[np.newaxis, ...]

        mask_np = np.array(grayscale_mask).astype(np.uint8)
        binary_mask = np.where(mask_np > 127, 255, 0).astype(np.uint8)
        binary_mask = binary_mask[np.newaxis, np.newaxis, ...]

        input = {
            self.model.get_inputs()[0].name: image_np, 
            self.model.get_inputs()[1].name: binary_mask
        }

        output = self.model.run(None, input)[0]
        image_cleaned_np = np.transpose(output[0], (1, 2, 0)).astype(np.uint8)

        image_cleaned_pil = Image.fromarray(image_cleaned_np)
        image_cleaned_pil.save("output/image_cleaned.png")

        return image_cleaned_pil