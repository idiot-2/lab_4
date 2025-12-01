from flask import Blueprint, render_template, current_app, send_from_directory
import os

# Now the image will live inside the merged project. We serve it from the app root.
IMG_FILENAME = '393326927f757e07d786936ad5d1f35e.jpg'

dot_bp = Blueprint('dot', __name__)


@dot_bp.route('/dot')
def dot():
    return render_template('dot.html')


@dot_bp.route('/dot/image')
def dot_image():
    # Serve the JPG from the merged project's root directory (next to app.py)
    root = current_app.root_path
    return send_from_directory(root, IMG_FILENAME)
