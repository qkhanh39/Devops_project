from flask import Blueprint, render_template, request, url_for, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import urllib.request
views = Blueprint('views', __name__, template_folder='../client/templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/<username>')
@login_required
def home(username):
    return render_template("home.html", user=current_user)

@views.route('/<username>', methods=['POST'])
@login_required
def upload_image(username):
    if 'file' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], username, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        flash('File uploaded successfully', category = 'success')
        return render_template("home.html", user=current_user, filename=filename)
    else:
        flash('Allowed file types are png, jpg, jpeg', category='error')
        return redirect(request.url)