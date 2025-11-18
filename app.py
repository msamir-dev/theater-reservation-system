import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

# Import db from models (single instance only)
from models import db, Admin, Seat, SeatStatus, SeatCategory, Booking

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # ======================
    # Flask Configuration
    # ======================
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

    # Database (PostgreSQL on Railway or SQLite locally)
    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///theater.db"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ======================
    # Initialize Extensions
    # ======================
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'


    # ======================
    # User Loader
    # ======================
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))


    # ======================
    # Register Blueprints
    # ======================
    with app.app_context():
        from routes.main import main_bp
        from routes.admin import admin_bp
        from routes.api import api_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp, url_prefix="/admin")
        app.register_blueprint(api_bp, url_prefix="/api")


    # ======================
    # Home Route
    # ======================
    @app.route("/")
    def home():
        return render_template("index.html")


    # ======================
    # Create Tables + Default Admin
    # ======================
    with app.app_context():
        db.create_all()

        try:
            if not Admin.query.filter_by(email="vipwinni@shubra.com").first():
                admin = Admin(email='vipwinni@shubra.com')
                admin.set_password('vipwinni123@')
                db.session.add(admin)
                db.session.commit()
                print("✔ Default admin created")
            else:
                print("✔ Admin already exists")
        except Exception as e:
            print(f"⚠ Failed to create admin: {e}")


    return app


# IMPORTANT FOR RAILWAY (Gunicorn)
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
