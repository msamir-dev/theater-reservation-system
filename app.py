import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

from models import db, Admin, Seat

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # --------------------
    # Config
    # --------------------
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')

    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///theater.db"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --------------------
    # Init extensions
    # --------------------
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "admin.login"

    @login_manager.user_loader
    def load_user(uid):
        return Admin.query.get(int(uid))

    # --------------------
    # Register Blueprints
    # --------------------
    with app.app_context():
        from routes.main import main_bp
        from routes.admin import admin_bp
        from routes.api import api_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp, url_prefix="/admin")
        app.register_blueprint(api_bp, url_prefix="/api")

        db.create_all()

    # --------------------
    # HOME
    # --------------------
    @app.route("/")
    def home():
        return render_template("index.html")

    # --------------------
    # INIT SEATS (WORKS NOW)
    # --------------------
    from init_db import initialize_seats

    @app.route('/init-seats')
    def init_seats_route():
        secret = request.args.get("secret")
        if secret != "vipinit2024":
            return "Unauthorized", 403

        initialize_seats(app)
        return "Seats initialized successfully!"

    # --------------------
    # DEBUG COUNT
    # --------------------
    @app.route('/debug/count-seats')
    def debug_count_seats():
        return str(Seat.query.count())

    return app
