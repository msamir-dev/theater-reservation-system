import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

# Import db + models
from models import db, Admin, Seat, SeatStatus, SeatCategory, Booking

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # ======================
    # Config
    # ======================
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///theater.db"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ======================
    # Init Extensions
    # ======================
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'

    # ======================
    # Login Loader
    # ======================
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # ======================
    # Blueprints
    # ======================
    with app.app_context():
        from routes.main import main_bp
        from routes.admin import admin_bp
        from routes.api import api_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp, url_prefix="/admin")
        app.register_blueprint(api_bp, url_prefix="/api")

    # ======================
    # Routes
    # ======================
    @app.route("/")
    def home():
        return render_template("index.html")

    # ======================
    # Create Tables + Default Admin
    # ======================
    with app.app_context():
        db.create_all()

        if not Admin.query.filter_by(email="vipwinni@shubra.com").first():
            admin = Admin(email='vipwinni@shubra.com')
            admin.set_password('vipwinni123@')
            db.session.add(admin)
            db.session.commit()
            print("✔ Default admin created")
        else:
            print("✔ Admin already exists")

    # ======================
    # TEMP INIT SEATS ROUTE ⚠️
    # ======================
    @app.route('/init-seats')
    def init_seats_route():
        secret = request.args.get("secret")
        if secret != "vipinit2024":
            return "Unauthorized", 403

        from init_db import initialize_seats
        initialize_seats()
        return "Seats initialized successfully!"

    # ======================
    # Debug seat count
    # ======================
    @app.route('/debug/count-seats')
    def debug_count_seats():
        return str(Seat.query.count())

    return app


# For Gunicorn
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
