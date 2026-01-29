from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, flash
from tensorflow.keras.utils import load_img
from keras_preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import logging
import os
import math
import requests
import base64

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- ML Model and Helpers ---
Model_Path = 'models/pneu_cnn_model.h5'
model = load_model(Model_Path)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Geolocation Helpers ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) * math.sin(dLon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def find_nearby_places(user_lat, user_lon, amenity):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node(around:20000,{user_lat},{user_lon})["amenity"="{amenity}"];
      way(around:20000,{user_lat},{user_lon})["amenity"="{amenity}"];
      relation(around:20000,{user_lat},{user_lon})["amenity"="{amenity}"];
    );
    out center;
    """
    try:
        response = requests.post(overpass_url, data={'data': overpass_query})
        response.raise_for_status()
        data = response.json()
        
        places = {} # Use a dict to handle duplicates
        for element in data['elements']:
            if 'tags' in element and 'name' in element['tags']:
                name = element['tags']['name']
                if name not in places:
                    lat = element.get('lat') or element.get('center', {}).get('lat')
                    lon = element.get('lon') or element.get('center', {}).get('lon')
                    if lat and lon:
                        distance = haversine(user_lat, user_lon, lat, lon)
                        address_tags = element.get('tags', {})
                        address_parts = [
                            address_tags.get('addr:housenumber'),
                            address_tags.get('addr:street'),
                            address_tags.get('addr:city')
                        ]
                        address = ", ".join(filter(None, address_parts))
                        if not address:
                            address = f"{lat:.4f}, {lon:.4f}"
                        
                        maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                        
                        places[name] = {
                            'name': name, 
                            'distance': distance,
                            'address': address,
                            'maps_link': maps_link
                        }
        
        places_list = list(places.values())
        return sorted(places_list, key=lambda x: x['distance'])[:5]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error querying Overpass API for {amenity}: {e}")
        return []

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    logging.info("Prediction request received.")
    if 'imagefile' not in request.files:
        return render_template('index.html', error='No image uploaded.')

    imagefile = request.files['imagefile']

    if imagefile.filename == '':
        return render_template('index.html', error='No selected file.')

    if not allowed_file(imagefile.filename):
        return render_template('index.html', error='Please upload a valid image file.')

    temp_image_path = os.path.join('/tmp', imagefile.filename)
    try:
        # Save the image temporarily to check its mode
        imagefile.seek(0)
        imagefile.save(temp_image_path)
        
        img_check = Image.open(temp_image_path)
        if img_check.mode != 'L':
            return render_template('index.html', error='Warning: This does not appear to be a grayscale X-ray image. Please upload a valid X-ray.')
        
        img = load_img(temp_image_path, target_size=(500, 500), color_mode='grayscale')
        x = img_to_array(img)
        x /= 255.0
        x = np.expand_dims(x, axis=0)

        prediction = model.predict(x)[0][0]
        prediction_percent = prediction * 100
        classification = f"Positive ({prediction_percent:.2f}%)" if prediction >= 0.5 else f"Negative ({prediction_percent:.2f}%)"

        # Encode the image to base64 to display it on the webpage
        with open(temp_image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        image_data_url = f"data:image/jpeg;base64,{encoded_string}"


        insights = []
        hospitals = {}
        if prediction_percent >= 20:
            insights = [
                "**Get Plenty of Rest:** Your body needs energy to fight infection.",
                "**Stay Hydrated:** Fluids help loosen mucus and prevent dehydration.",
                "**Follow Medical Advice:** Take all medications as prescribed by your doctor.",
                "**Manage Symptoms:** Consult a doctor about over-the-counter symptom relief.",
            ]
            # user_lat = request.form.get('latitude')
            # user_lon = request.form.get('longitude')
            # if user_lat and user_lon:
            #     user_lat, user_lon = float(user_lat), float(user_lon)
            #     hospitals = {
            #         "multi_specialty": find_nearby_places(user_lat, user_lon, "hospital"),
            #         "specialized": find_nearby_places(user_lat, user_lon, "clinic"),
            #         "nursing_home": find_nearby_places(user_lat, user_lon, "nursing_home"),
            #     }
        else:
            insights = [
                "**Practice Good Hygiene:** Wash hands frequently.",
                "**Avoid Smoking:** Smoking damages your lungs.",
                "**Get Vaccinated:** Ask your doctor about pneumonia and flu vaccines.",
                "**Maintain a Healthy Lifestyle:** A balanced diet and exercise boost your immune system.",
            ]

        return render_template('index.html', prediction=classification, imagePath=image_data_url, insights=insights, hospitals=hospitals)

    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return render_template('index.html', error='Invalid image file or error processing image.')
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)


