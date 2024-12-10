from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Pildi üleslaadimise kaust
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy kasutajanimi ja parool
USERNAME = 'admin'
PASSWORD = 'password'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/greet/<name>')
def greet(name):
    return render_template('greet.html',name=name)

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
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return render_template('change_image.html', image_url=filename)

    return render_template('change_image.html', image_url='static/default_image.jpg')

def allowed_file(filename):
    # Lubatud faililaiendid (nt .jpg, .png)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']

if __name__ == '__main__':
    app.run(debug=True)
