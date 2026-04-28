from PIL import Image
from simple_lama_inpainting import SimpleLama



class LamaInpainter:
    def __init__(self):
        self.model = SimpleLama()
    

    def inpaint(self, image_pil: Image.Image, image_mask: Image.Image) -> Image.Image:
        rgb_image = image_pil.convert('RGB')
        grayscale_mask = image_mask.convert('L')

        result = self.model(rgb_image, grayscale_mask)
        result.save("output/image_cleaned.png")

        return result