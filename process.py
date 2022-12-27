from PIL import Image
import io

class ImageProcess():
    def __init__(self, images: list[bytes]) -> None:
        self.images = []
        for image in images:
            self.images.append(Image.open(io.BytesIO(image)).convert("RGBA"))
    
    def process(self):
        return self._process(self.images)
    
    def _process(self, images: list[Image.Image]):
        w, h = images[0].size
        base = Image.new('RGBA', (w, h * len(images)), (255, 0, 0, 0))
        for i, image in enumerate(images):
            h = image.height
            base.paste(image, (0, h + h * i - h), image)
        #base.show()

        return base

