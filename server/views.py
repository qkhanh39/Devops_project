import numpy as np
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request, url_for, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import urllib.request
from PIL import Image
from .model import Pyx, Pal
from datetime import datetime
from skimage import io
from PIL import Image
from .database import Images
from . import db


views = Blueprint('views', __name__, template_folder='../client/templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'{current_user.username}_{timestamp}.png' 
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], current_user.username, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            image = Image.open(file)
            max_size = (512, 512) 
            image.thumbnail(max_size)
            image.save(file_path)
            flash(f'File uploaded successfully', category='success')
            render_template("home.html", 
                            user=current_user,
                            filename=f'uploads/{current_user.username}/{filename}')
            width, height = Image.open(file_path).size
            output_path, pixel_image_name = run_transfer(file_path, current_user.username)
            new_image = Images(user_id = current_user.id, original_image=filename, pixel_image=pixel_image_name)
            db.session.add(new_image)
            db.session.commit()
            return render_template("home.html", 
                                   user=current_user, 
                                   filename=f'uploads/{current_user.username}/{filename}', 
                                   width=width, 
                                   height=height,
                                   output=output_path)
        else:
            flash('Allowed file types are png, jpg, jpeg', category='error')
            return redirect(request.url)
    return render_template("home.html", user=current_user)


def run_transfer(image_path, username):
    print(image_path)
    image = io.imread(image_path)
    downsample_by = 6
    palette = 7
    pyx = Pyx(factor=downsample_by, palette=palette)
    pyx.fit(image)
    new_image = pyx.transform(image)
    new_image = Image.fromarray(new_image)
    output_folder = os.path.join(current_app.config['OUTPUT_FOLDER'], username)
    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  
    filename = f'{username}_{timestamp}.png'  
    output_path = os.path.join(output_folder, filename)
    new_image.save(output_path)
    relative_path = f'transferImages/{username}/{filename}'
    return relative_path, filename