import streamlit as st
import requests
from PIL import Image
import numpy as np
import base64
import cv2


def encoding_img(img):
    _, im_arr = cv2.imencode('.jpg', img)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64.decode('utf-8')


def decoding_img(im_b64, gray_flag = False):
    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    if gray_flag == False:
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    else:
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_GRAYSCALE)
    return img


if __name__ == '__main__':

    file = st.file_uploader('')
    name_layers = requests.get('http://127.0.0.2:8080/get_name_layers').json()['name_layers']
    st.write(str(name_layers))
    index_layer_input = st.text_input(label='index_layer')

    if file != None:
        img = Image.open(file).convert('RGB')
        st.image(img, width=128)
        img = np.array(img) 
        encoded_img = encoding_img(img)

        reponse = requests.post('http://127.0.0.2:8080/visual', data={'index_layer': int(index_layer_input), 'img': encoded_img}).json()
        outputs = reponse['outputs']
        decoded_imgs = []
        for output in outputs:
            decoded_img = decoding_img(output, gray_flag=True)
            decoded_imgs.append(decoded_img)
        st.image(decoded_imgs, width=96)

