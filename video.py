from collections import Counter
import math
import cv2
import numpy as np
from PIL import Image
from utils import create_coord_list

def all_frames_to_byte_list(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    image_byte_list = []
    while True:
        ret, frame = cap.read()
        if ret:
            #cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
            #n += 1
            image_byte_list.append(cv2.imencode(f".png", frame)[1].tobytes())
            #print(type(bytes))
            #image = Image.open(io.BytesIO(image_bytes))
            #image.show()
            
        else:
            #ImageProcess(image_byte_list)
            return image_byte_list

def color_to_alpha(im, alpha_color):
    alpha = np.max(
        [
            np.abs(im[..., 0] - alpha_color[0]),
            np.abs(im[..., 1] - alpha_color[1]),
            np.abs(im[..., 2] - alpha_color[2]),
        ],
        axis=0,
    )
    ny, nx, _ = im.shape
    im_rgba = np.zeros((ny, nx, 4), dtype=im.dtype)
    for i in range(3):
        im_rgba[..., i] = im[..., i]
    im_rgba[..., 3] = alpha
    return im_rgba

def auto_alpha(image: Image.Image):
    w, h = image.size
    around = math.ceil(w/10)
    colors = []
    for x, y in create_coord_list(0,0, around, around):
        colors.append(image.getpixel((x,y)))
    for x, y in create_coord_list(w - around, 0, w, 0 + around):
        colors.append(image.getpixel((x,y)))
    for x, y in create_coord_list(w - around, h - around, w, h):
        colors.append(image.getpixel((x,y)))
    for x, y in create_coord_list(0, h - around, 0 + around, h):
        colors.append(image.getpixel((x,y)))
    
    r, g, b, _ = Counter(colors).most_common()[0][0]
    target_color = (r, g, b)
    img_ndarray = np.asarray(image)
    alpha_img_ndarray = color_to_alpha(img_ndarray, target_color)
    return Image.fromarray(alpha_img_ndarray)
    

#remove_background_color("./sample.png")
#im = np.array(Image.open('sample.png'))
#for i in range(10):
#    target_color = (3 + i, 2 + i, 244 + i)
    #im = Image.open("./texture.png", mode='r')
#    im = color_to_alpha(im, target_color)

    #target_color = (3 - i, 2 - i, 244 - i)
    #im = color_to_alpha(im, target_color)
#target_color = (3, 2, 244)
#im = Image.open("./texture.png", mode='r')
#im = color_to_alpha(im, target_color)
#Image.fromarray(im).show()
#rc("sample.png")

#https://stackoverflow.com/questions/765736/how-to-use-pil-to-make-all-white-pixels-transparent