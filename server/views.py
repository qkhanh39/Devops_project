import numpy as np
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request, url_for, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import urllib.request
#
from server.model import Pyx, Pal
from skimage import io
from PIL import Image

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
            filename = secure_filename(file.filename)
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], current_user.username, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # file.save(file_path)
            image = Image.open(file)
            max_size = (512, 512)  # Define the maximum size
            image.thumbnail(max_size)
            image.save(file_path)
            flash(
                f'File uploaded successfully', category='success')
            render_template("home.html", user=current_user,
                            filename=f'uploads/{current_user.username}/{filename}')
            #run_transfer(file_path)
            # , transfer_filename='transferImages/output.png')
            return render_template("home.html", user=current_user, filename=f'uploads/{current_user.username}/{filename}')
        else:
            flash('Allowed file types are png, jpg, jpeg', category='error')
            return redirect(request.url)
    return render_template("home.html", user=current_user)


def plot(subplots=[], save_as=None, fig_h=9):
    """Plotting helper function"""
    fig, ax = plt.subplots(int(np.ceil(len(subplots) / 3)),
                           min(3, len(subplots)),
                           figsize=(18, fig_h))
    if len(subplots) == 1:
        ax = [ax]
    else:
        ax = ax.ravel()
    for i, subplot in enumerate(subplots):
        if isinstance(subplot, dict):
            ax[i].set_title(subplot["title"])
            ax[i].imshow(subplot["image"])
        else:
            ax[i].imshow(subplot)
    fig.tight_layout()
    plt.savefig(save_as)
    plt.close(fig)


def run_transfer(image_path):
    # file_path = 'server/static/transferImages/output.png'
    # image = Image.open(image_path)
    # max_size = (512, 512)  # Define the maximum size
    # image.thumbnail(max_size)
    # image.save(file_path)
    print(image_path)
    image = io.imread(image_path)
    downsample_by = 6
    palette = 7
    pyx = Pyx(factor=downsample_by, palette=palette)
    pyx.fit(image)
    new_image = pyx.transform(image)
    plot([new_image], "server/static/transferImages/output.png")
