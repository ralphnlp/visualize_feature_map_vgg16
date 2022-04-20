from unicodedata import name
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.models import Model
import cv2
from flask import request, Flask, jsonify
from main import encoding_img, decoding_img


class Visual_VGG16:
    
    def __init__(self) -> None:
        self.vgg16 = VGG16()
        self.name_layers = [] 
        for layer in self.vgg16.layers:
            self.name_layers.append(layer.name)

    def set_layer(self, index_layer):
        self.model = Model(inputs=self.vgg16.input, outputs=self.vgg16.layers[index_layer].output)
    
    def preprocessing(self, input_image):
        input_image = cv2.resize(input_image, (224, 224))
        preprocessed_input_image = preprocess_input(input_image.reshape(1, *input_image.shape))
        return preprocessed_input_image

    def predict(self, preprocessed_input_image):
        outputs = self.model.predict(preprocessed_input_image)[0]
        return outputs


app = Flask(__name__)
@app.route('/get_name_layers', methods=['GET'])
def get_name_layers():
    name_layers = model.name_layers
    index2name = {}
    for i, name in enumerate(name_layers):
        index2name[i] = name
    return jsonify({'name_layers': index2name})


@app.route('/visual', methods=['POST'])
def visual():

    index_layer = request.form.get('index_layer')
    encoded_img = request.form.get('img')
    img = decoding_img(encoded_img)
    print
    model.set_layer(int(index_layer))
    preprocessed_input_image = model.preprocessing(img)
    outputs = model.predict(preprocessed_input_image)

    encoded_ouputs = []
    for i in range(outputs.shape[-1]):
        encoded_ouput = encoding_img(outputs[:, :, i])
        encoded_ouputs.append(encoded_ouput)
    return jsonify({'outputs': encoded_ouputs})



if __name__ == '__main__':

    model = Visual_VGG16()
    app.run(debug=True, host='127.0.0.2', port=8080)