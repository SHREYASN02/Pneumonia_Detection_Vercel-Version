from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, flash
from tensorflow.keras.utils import load_img
from keras_preprocessing.image import img_to_array
from keras.models import load_model
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import numpy as np
import logging
import os
import math
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-secret-key-that-you-should-change'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- Database Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
@login_required
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    logging.info("Prediction request received.")
    if 'imagefile' not in request.files:
        return render_template('index.html', error='No image uploaded.')

    imagefile = request.files['imagefile']

    if imagefile.filename == '':
        return render_template('index.html', error='No selected file.')

    if not allowed_file(imagefile.filename):
        return render_template('index.html', error='Please upload a valid image file.')

    image_path = os.path.join('static', imagefile.filename)
    imagefile.seek(0)
    imagefile.save(image_path)

    img = load_img(image_path, target_size=(500, 500), color_mode='grayscale')
    x = img_to_array(img)
    x /= 255.0
    x = np.expand_dims(x, axis=0)

    prediction = model.predict(x)[0][0]
    prediction_percent = prediction * 100
    classification = f"Positive ({prediction_percent:.2f}%)" if prediction >= 0.5 else f"Negative ({prediction_percent:.2f}%)"

    insights = []
    hospitals = {}
    if prediction_percent >= 20:
        insights = [
            "**Get Plenty of Rest:** Your body needs energy to fight infection.",
            "**Stay Hydrated:** Fluids help loosen mucus and prevent dehydration.",
            "**Follow Medical Advice:** Take all medications as prescribed by your doctor.",
            "**Manage Symptoms:** Consult a doctor about over-the-counter symptom relief.",
        ]
        user_lat = request.form.get('latitude')
        user_lon = request.form.get('longitude')
        if user_lat and user_lon:
            user_lat, user_lon = float(user_lat), float(user_lon)
            hospitals = {
                "multi_specialty": find_nearby_places(user_lat, user_lon, "hospital"),
                "specialized": find_nearby_places(user_lat, user_lon, "clinic"),
                "nursing_home": find_nearby_places(user_lat, user_lon, "nursing_home"),
            }
    else:
        insights = [
            "**Practice Good Hygiene:** Wash hands frequently.",
            "**Avoid Smoking:** Smoking damages your lungs.",
            "**Get Vaccinated:** Ask your doctor about pneumonia and flu vaccines.",
            "**Maintain a Healthy Lifestyle:** A balanced diet and exercise boost your immune system.",
        ]

    return render_template('index.html', prediction=classification, imagePath=image_path, insights=insights, hospitals=hospitals)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(username=request.form['username'])
        new_user.set_password(request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('secret')
            db.session.add(admin)
            db.session.commit()
            logging.info("Admin user created.")

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)