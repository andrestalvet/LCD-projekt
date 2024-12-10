from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
import os

app = Flask(__name__)

# Pildi üleslaadimise kaust
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy kasutajanimi ja parool
USERNAME = 'admin'
PASSWORD = 'password'

# TFT ekraani seadistamine
serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
device = ili9341(serial)

# Lubatud faililaiendid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']

# Pildi suuruse muutmine
def resize_image(image_path, width, height):
    img = Image.open(image_path)
    img_resized = img.resize((width, height))
    return img_resized

# Kuvame pildi ekraanil
def display_image(image_path):
    img = Image.open(image_path).convert("RGB")  # LCD jaoks teisendame RGB-ks
    device.display(img)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kontrollime, kas sisestatud andmed on õiged
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('change_image'))  # Kui on õiged, liigume pildi vahetamise juurde
        else:
            error = 'Vale kasutajanimi või parool'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/change_image', methods=['GET', 'POST'])
def change_image():
    if request.method == 'POST':
        # Kontrollime, kas pilt on üles laaditud
        if 'image' not in request.files:
            return 'Pilt puudub', 400
        file = request.files['image']

        # Kontrollime faili nime ja laiendit
        if file.filename == '':
            return 'Pilt puudub', 400
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Muudame pildi suurust 320x240 ekraanile sobivaks
            resized_image = resize_image(filepath, 320, 240)
            resized_image.save(filepath)  # Asendame originaali suurusega versiooni

            # Kuvame pildi ekraanil
            display_image(filepath)

            return render_template('change_image.html', image_url=filepath)

    return render_template('change_image.html', image_url=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)