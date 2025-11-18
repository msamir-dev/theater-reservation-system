import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Import db from models to ensure single instance
from models import db
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    
    # Database configuration
    if os.environ.get('DATABASE_URL'):
        # For production (PostgreSQL)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    else:
        # For local development (SQLite)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///theater.db')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة.'
    
    # user_loader for flask-login
    @login_manager.user_loader
    def load_user(user_id):
        from models import Admin
        return Admin.query.get(int(user_id))
    
    # Import models first to ensure they're registered with SQLAlchemy
    with app.app_context():
        # Import and register models
        from models import SeatStatus, SeatCategory, Seat, Booking, Admin
        
        # Import and register blueprints after models are loaded
        from routes.main import main_bp
        from routes.admin import admin_bp
        from routes.api import api_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(api_bp, url_prefix='/api')
        print(f'Registered blueprints: main, admin, api')
    
    # Route رئيسي مباشر
    @app.route('/')
    def home():
        return render_template('index.html')
    
    # Create tables and setup admin
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        try:
            # Define Admin model here to avoid circular imports
            class Admin(db.Model):
                __tablename__ = 'admin'
                
                id = db.Column(db.Integer, primary_key=True)
                email = db.Column(db.String(120), unique=True, nullable=False)
                password_hash = db.Column(db.String(200), nullable=False)
                
                def set_password(self, password):
                    from werkzeug.security import generate_password_hash
                    self.password_hash = generate_password_hash(password)
            
            if not Admin.query.first():
                admin = Admin(email='vipwinni@shubra.com')
                admin.set_password('vipwinni123@')
                db.session.add(admin)
                db.session.commit()
                print('✅ Admin user created successfully')
            else:
                print('✅ Admin user already exists')
        except Exception as e:
            print(f'⚠️  Could not create admin user: {e}')
            # Continue even if admin creation fails
    
    return app

if __name__ == "__main__":
    app = create_app()
