from flask import Blueprint, render_template, request, url_for, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import urllib.request

from .model import Pyx, Pal

from skimage import io

views = Blueprint('views', __name__, template_folder='../client/templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method =='POST':
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            flash('File uploaded successfully', category='success')
            return render_template("home.html", user=current_user, filename=filename)
        else:
            flash('Allowed file types are png, jpg, jpeg', category='error')
            return redirect(request.url)
    return render_template("home.html", user=current_user)


# @views.route('/<username>', methods=['POST'])
# @login_required
# def upload_image(username):
#     if 'file' not in request.files:
#         flash('No file part', category='error')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No selected file', category='error')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], username, filename)
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)
#         file.save(file_path)
#         flash('File uploaded successfully', category='success')
#         return render_template("home.html", user=current_user, filename=filename)
#     else:
#         flash('Allowed file types are png, jpg, jpeg', category='error')
#         return redirect(request.url)
    

# def run_transfer(image_path):
#     image = io.imread(image_path)
#     downsample_by = 14
#     palette = 8
#     pyx = Pyx(factor=downsample_by, palette=palette)
#     pyx.fit(image)
#     new_image = pyx.transform(image)
#     SAVE_PATH = "./static/transferImages/"
#     io.imsave(SAVE_PATH + "output.png", new_image)
