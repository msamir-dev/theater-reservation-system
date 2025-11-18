import os
from datetime import timedelta

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///theater.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # WhatsApp Business API Configuration
    WHATSAPP_ENABLED = os.environ.get('WHATSAPP_ENABLED', 'true').lower() == 'true'
    WHATSAPP_API_KEY = os.environ.get('WHATSAPP_API_KEY', '')
    WHATSAPP_API_URL = os.environ.get('WHATSAPP_API_URL', 'https://api.whatsapp.com/v1/messages')
    WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '')
    
    # CallMeBot API Configuration (Free alternative)
    CALLMEBOT_API_KEY = os.environ.get('CALLMEBOT_API_KEY', '')
    CALLMEBOT_ENABLED = os.environ.get('CALLMEBOT_ENABLED', 'true').lower() == 'true'
    
    # File upload configuration
    UPLOAD_FOLDER = 'static/temp_qr'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Application settings
    THEATER_NAME = os.environ.get('THEATER_NAME', 'مسرح المدينة')
    THEATER_ADDRESS = os.environ.get('THEATER_ADDRESS', 'القاهرة، مصر')
    THEATER_PHONE = os.environ.get('THEATER_PHONE', '01234567890')
    
    # QR Code settings
    QR_CODE_EXPIRY_HOURS = 24  # QR codes expire after 24 hours
    
    # Admin settings
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@theater.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}