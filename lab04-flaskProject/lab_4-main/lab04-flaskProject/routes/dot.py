from flask import Blueprint, render_template, current_app, send_from_directory

dot_bp = Blueprint('dot', __name__)


@dot_bp.route('/dot')
def dot():
    return render_template('dot.html')


@dot_bp.route('/dot/image')
def dot_image():
    # Serve the uploaded JPG that lives in the project folder
    return send_from_directory(current_app.root_path, '393326927f757e07d786936ad5d1f35e.jpg')
