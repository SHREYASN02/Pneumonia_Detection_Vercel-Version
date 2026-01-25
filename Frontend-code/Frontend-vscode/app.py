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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-secret-key-that-you-should-change'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure logging
logging.basicConfig(level=logging.INFO)

# User model
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

Model_Path = 'models/pneu_cnn_model.h5'
model = load_model(Model_Path)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    if request.method == 'POST':
        logging.info("Prediction request received.")
        if 'imagefile' not in request.files:
            logging.warning("No image file in request.")
            return render_template('index.html', error='No image uploaded.')

        imagefile = request.files['imagefile']

        if imagefile.filename == '':
            logging.warning("No selected file.")
            return render_template('index.html', error='No selected file.')

        if not imagefile or not allowed_file(imagefile.filename):
            logging.warning(f"Invalid file type: {imagefile.filename}")
            return render_template('index.html', error='Please upload a valid image file (png, jpg, jpeg).')

        try:
            img = Image.open(imagefile)
            logging.info(f"Image mode: {img.mode}")
        except Exception as e:
            logging.error(f"Error opening image: {e}")
            return render_template('index.html', error='Invalid image file.')

        image_path = os.path.join('static', imagefile.filename)
        imagefile.seek(0)
        imagefile.save(image_path)

        img_for_model = load_img(image_path, target_size=(500, 500), color_mode='grayscale')
        x = img_to_array(img_for_model)
        x = x / 255.0
        x = np.expand_dims(x, axis=0)

        classes = model.predict(x)
        result1 = classes[0][0]
        prediction_percent = result1 * 100
        result2 = 'Negative'
        if result1 >= 0.5:
            result2 = 'Positive'
        
        classification = f'{result2} ({prediction_percent:.2f}%)'
        logging.info(f"Prediction: {classification}")

        insights = []
        if prediction_percent >= 20:
            insights = [
                "**Get Plenty of Rest:** Your body needs energy to fight the infection. Rest helps your immune system function effectively.",
                "**Stay Hydrated:** Drink plenty of water, clear soups, and other fluids to help loosen mucus in your lungs and prevent dehydration.",
                "**Follow Medical Advice:** If prescribed antibiotics, take the full course as directed by your doctor, even if you start to feel better.",
                "**Manage Symptoms:** Consult your doctor about using over-the-counter medications to manage fever and pain. A humidifier can also help ease breathing.",
                "**Avoid Smoking:** Smoking damages your lungs and will prolong your recovery. Seek help to quit if you are a smoker.",
                "**Eat a Nutritious Diet:** A balanced diet rich in fruits, vegetables, and lean proteins can help support your immune system."
            ]
        else:
            insights = [
                "**Practice Good Hygiene:** Wash your hands frequently with soap and water to prevent the spread of germs.",
                "**Avoid Smoking:** Smoking is a major risk factor for pneumonia. Quitting can significantly improve your lung health.",
                "**Get Vaccinated:** Talk to your doctor about getting vaccinated against pneumonia and the flu.",
                "**Maintain a Healthy Lifestyle:** A balanced diet, regular exercise, and adequate sleep are essential for a strong immune system.",
                "**Know the Symptoms:** Be aware of the symptoms of pneumonia, such as cough, fever, and difficulty breathing, and see a doctor if you are concerned."
            ]
        
        return render_template('index.html', prediction=classification, imagePath=image_path, insights=insights)

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
