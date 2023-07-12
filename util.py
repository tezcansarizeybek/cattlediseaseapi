import re
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import cv2


def base64_to_pil(img_base64):
    if "base64," in str(img_base64):
        image_data = re.sub('^data:image/.+;base64,', '', img_base64)
    else:
        image_data = img_base64
    pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    return pil_image

def hist_eq(img):
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    R, G, B = cv2.split(img)
    output1_R = cv2.equalizeHist(R)
    output1_G = cv2.equalizeHist(G)
    output1_B = cv2.equalizeHist(B)
    img = cv2.merge((output1_R, output1_G, output1_B))
    color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(color_coverted)
    return img

def np_to_base64(img_np):
    img = Image.fromarray(img_np.astype('uint8'), 'RGB')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return u"data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode("ascii")