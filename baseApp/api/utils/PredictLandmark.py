import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import os
import matplotlib.pyplot as plt
import requests



class imglandmark:
    def __init__(self,img_path):
        # Load the trained model
        self.model = load_model('ImgProcessingModel.keras')
        self.image_path=img_path
        # Get the class names (landmark names)
        self.dataset_path = './myds/'  # Use the same path you used for training
        self.class_names = sorted(os.listdir(self.dataset_path))
        
    def predict_landmark(self):
        # Load and preprocess the image
        img = image.load_img(self.image_path, target_size=(224, 224,3))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Make prediction
        preds = self.model.predict(x)
        
        # Get top 5 predictions
        top_5_indices = preds[0].argsort()[-5:][::-1]
        top_5_predictions = [(self.class_names[i], preds[0][i]) for i in top_5_indices]
        self.predictions=top_5_predictions
        return top_5_predictions


    def plot_predictions(self):
        # Create a figure with two subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot the image
        img = image.load_img(self.image_path)
        ax1.imshow(img)
        ax1.axis('off')
        ax1.set_title('Input Image')
        
        # Plot the predictions
        landmarks, confidences = zip(*self.predictions)
        y_pos = range(len(landmarks))
        
        ax2.barh(y_pos, confidences, align='center')
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(landmarks)
        ax2.invert_yaxis()  # Labels read top-to-bottom
        ax2.set_xlabel('Confidence')
        ax2.set_title('Top 5 Predictions')
        
        # Adjust layout and display the plot
        plt.tight_layout()
        plt.show()

    def get_osm_details(self,landmark_name):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": landmark_name,
            "format": "json"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json()
            if results:
                return results[0]  # Return the first result
            else:
                return None
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_wikidata_details(self,landmark_name):
        #print(f"========================================={landmark_name}")
        # last_space_index = landmark_name.strip().rfind('_')
        # print(last_space_index)
        # place_name=landmark_name[:last_space_index] if last_space_index != -1 else landmark_name
        # print(f"{last_space_index}=============={place_name}")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{landmark_name}"# "https://www.wikidata.org/w/api.php"
        print(f"=============={url}")
        params = {
            "action": "wbsearchentities",
            "search": landmark_name,
            "language": "en",
            "format": "json"
        }

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            results = response.json()#.get('search')
            #print(results)
            if results:
                return {
                    'title': results.get('title'),
                    'description': results.get('description'),
                    'extract': results.get('extract'),
                    'thumbnail': results.get('thumbnail', {}).get('source'),
                }
            else:
                return None
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

# # Example usage
# image_path = 'path/to/your/test/image.jpg'  # Replace with the path to your test image
# predictions = predict_landmark(image_path)

# print(f"Predictions for image: {image_path}")
# for landmark, confidence in predictions:
#     print(f"{landmark}: {confidence:.2f}")

# # Plot the predictions
# plot_predictions(image_path, predictions)

# If you want to predict and plot for multiple images in a directory
# test_dir = '.'
# for image_name in os.listdir(test_dir):
#     if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
#         image_path = os.path.join(test_dir, image_name)
#         predictions = predict_landmark(image_path)
        
#         if(predictions):
#             print(f"{predictions}")
#             #predictions.sort()
#             mostSutableLandmark=predictions[0][0]
#             mostSutableLandmark=mostSutableLandmark.replace(' ','_')
#             details=get_wikidata_details(mostSutableLandmark)
#             #print(f"================={mostSutableLandmark} details=================\n{details}")
#         print(f"\nPredictions for image: {image_name}")
#         for landmark, confidence in predictions:
#             print(f"{landmark}: {confidence:.2f}")
            
            
        
        # Plot the predictions
        #plot_predictions(image_path, predictions)
