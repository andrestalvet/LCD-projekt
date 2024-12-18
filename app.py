from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
from luma.core.interface.serial import spi
from luma.lcd.device import ili9341

app = Flask(__name__)

# Kaust, kuhu pildid laaditakse
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy kasutaja andmed
USERNAME = 'admin'
PASSWORD = 'password'

# Lubatud faililaiendid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']

# Initsialiseerime LCD ekraani
serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
lcd = ili9341(serial, width=320, height=240)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('change_image'))
        else:
            error = 'Vale kasutajanimi või parool'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/change_image', methods=['GET', 'POST'])
def change_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'Pilt puudub', 400
        file = request.files['image']
        if file.filename == '':
            return 'Pilt puudub', 400
        if file and allowed_file(file.filename):
            # Salvestame üleslaetud pildi
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Kuvame pildi LCD ekraanil
            display_image_on_lcd(filepath)

            return render_template('change_image.html', image_url=url_for('static', filename='uploads/' + file.filename))

    # Vaikepilt, kui midagi pole üles laetud
    return render_template('change_image.html', image_url=url_for('static', filename='default_image.jpg'))

def display_image_on_lcd(image_path):
    """Kuvab pildi LCD ekraanil"""
    with Image.open(image_path) as img:
        # Muudame pildi suuruseks 320x240
        img = img.resize((320, 240)).convert("RGB")
        # Kuvame pildi LCD ekraanil
        lcd.display(img)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
