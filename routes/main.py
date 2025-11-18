from flask import Blueprint, render_template
from models import Seat, Booking
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')