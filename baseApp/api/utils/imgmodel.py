import numpy as np
import tensorflow_datasets as tfds
#pip install tensorflow-datasets
import tensorflow as tf
# Load the Open Images dataset
# dataset, info = tfds.load('open_images_v6', with_info=True, as_supervised=True)
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input,decode_predictions

class imgProcessingModel:
    def __init__(self,image_path):
        # Load the pre-trained ResNet model
        self.model = ResNet50(weights='imagenet', include_top=True)#, pooling='avg')
        self.img_path=image_path
        self.dataset, self.info = tfds.load('open_images_v6', with_info=True, as_supervised=True)
        (self.train_dataset, self.test_dataset), self.info = tfds.load(
            'open_images_v6',
            split=['train', 'validation'],
            with_info=True,
            as_supervised=True
        )
        # # Load the Open Images dataset
        # dataset, info = tfds.load('open_images_v6', with_info=True, as_supervised=True)
        self.train_dataset = self.train_dataset.map(self.recognize_place()).batch(32).prefetch(tf.data.AUTOTUNE)

    def preprocess_image(image, label):
        image = tf.image.resize(image, (224, 224))  # Resize for your model
        image = image / 255.0  # Normalize to [0, 1]
        return image, label

    # Load and preprocess the image
    def load_and_preprocess_image(self):
        img = image.load_img(self.img_path, target_size=(224, 224))  # ResNet50 input size
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)  # Preprocess for ResNet
        return img_array

    # Predict the place
    def recognize_place(self):
        img_array = self.load_and_preprocess_image()
        features = self.model.predict(img_array)  # Extract features
        decoded_predictions = decode_predictions(features, top=5)[0]
        for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
            print(f"print lines {i + 1}: {label} ({score:.2f})")
        # Here, you can use the features for further classification, e.g., with a separate classifier
        return features
