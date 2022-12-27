import sys
import json
import os
import io
import configparser

from tkinter.filedialog import askopenfilenames

import numpy
from PIL import Image

from image import image_to_byte_array
from video import all_frames_to_byte_list, color_to_alpha, auto_alpha
from process import ImageProcess
from utils import mcmeta_file, properties_file

def get_images_from_dir(dirname):
    paths = []
    print(allow_image_extensions)
    for file in os.listdir(dirname):
        if os.path.isfile(os.path.join(dirname, file)):
            print(os.path.splitext(file)[1].replace(".", ""))
            if os.path.splitext(file)[1].replace(".", "") in allow_image_extensions:
                paths.append(file)
    return paths

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(sys.argv[0]), "config.ini"), encoding='utf-8')

    allow_image_extensions = json.loads(config.get("GENERAL","allow_image_extensions"))
    allow_video_extensions = json.loads(config.get("GENERAL","allow_video_extensions"))

    specific_color_to_alpha = config.get("VIDEO","specific_color_to_alpha")
    auto_detect_specific_color = config.get("VIDEO","auto_detect_specific_color")
    specific_color = tuple(int(i) for i in json.loads(config.get("VIDEO","specific_color")))

    create_mcmeta = config.get("FILE","create_mcmeta")
    create_properties = config.get("FILE","create_properties")

    reverse_animation = config.get("OPTIONAL","reverse_animation")
    skip_frame = int(config.get("OPTIONAL","skip_frame"))

    paths = sys.argv.copy()
    paths.pop(0)

    is_image = False
    is_video = False

    result_paths = []

    if len(paths) == 0:
        paths = askopenfilenames(title="Select Video or Images")
        
    if len(paths) == 1:
        path = paths[0]
        if os.path.isfile(path) == True:
            extension = os.path.splitext(path)[1].replace(".", "")
            if extension in allow_image_extensions:
                is_image = True
                dirname = os.path.dirname(path)
                result_paths = get_images_from_dir(dirname)
            if extension in allow_video_extensions:
                result_paths.append(path)
                is_video = True
        
        if os.path.isdir(path) == True:
            print("yes")
            result_paths = get_images_from_dir(path)
            is_image = True
            input("a")
        #os.listdir(path)
    
    if len(paths) > 1:
        result_paths = paths
        is_image = True
    dirname = os.path.dirname(paths[0])
    result_paths = [os.path.join(dirname, path) for path in result_paths]
    print(result_paths)
    image_byte_list = []
    if is_video == True:
        image_byte_list = all_frames_to_byte_list(result_paths[0])
        print("VIDEO")
    elif is_image == True:
        if skip_frame != 0:
            file_number = 0
            use_files = []
            for num in range(len(result_paths)):
                if len(result_paths) - 1 <= file_number:
                    use_files.append(result_paths[len(result_paths) - 1])
                    break
                print("Added " + str(result_paths[file_number]))
                use_files.append(result_paths[file_number])
                file_number = file_number + 1 + skip_frame
        else:
            use_files = result_paths.copy()
        image_byte_list = [image_to_byte_array(path) for path in use_files]
    else:
        input("ERROR (unknown file extension)")
    image_process = ImageProcess(image_byte_list)
    image = image_process.process()
    if is_video == True:
        if specific_color_to_alpha == "yes":
            if auto_detect_specific_color == "yes":
                image = auto_alpha(image)
            else:
                ndarray = color_to_alpha(numpy.array(image), specific_color)
                image = Image.fromarray(ndarray)
    result_folder = os.path.join(dirname, "results")
    os.makedirs(result_folder, exist_ok=True)
    result_texture_path = os.path.join(result_folder, "texture.png")
    image.save(result_texture_path)
    if create_mcmeta == "yes":
        reverse = True if reverse_animation == "yes" else False
        mcmeta_file(result_texture_path, len(image_byte_list), reverse)
    if create_properties == "yes":
        w, h = Image.open(io.BytesIO(image_byte_list[0])).convert("RGBA").size
        properties_file(result_texture_path, w, h)