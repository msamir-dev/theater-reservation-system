from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import enum

# Import db from app to avoid circular imports
try:
    from app import db
except ImportError:
    # Fallback for when app is not available yet
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()
    print('Using fallback SQLAlchemy instance')

class SeatStatus(enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    BOOKED = "booked"

class SeatCategory(enum.Enum):
    VIP = "vip"
    REGULAR = "regular"

class Seat(db.Model):
    __tablename__ = 'seats'
    
    id = db.Column(db.Integer, primary_key=True)
    row_number = db.Column(db.Integer, nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    side = db.Column(db.String(10), nullable=False)  # 'left' or 'right'
    category = db.Column(db.Enum(SeatCategory), default=SeatCategory.REGULAR)
    status = db.Column(db.Enum(SeatStatus), default=SeatStatus.AVAILABLE)
    
    # Relationship
    booking = db.relationship('Booking', backref='seat', uselist=False)
    
    def __repr__(self):
        return f"<Seat {self.side.upper()[0]}{self.row_number}-{self.seat_number}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'row': self.row_number,
            'number': self.seat_number,
            'side': self.side,
            'category': self.category.value,
            'status': self.status.value,
            'label': f"{self.side.upper()[0]}{self.row_number}-{self.seat_number}"
        }

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    seat_id = db.Column(db.Integer, db.ForeignKey('seats.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_by = db.Column(db.Integer, db.ForeignKey('admin.id'))
    confirmation_time = db.Column(db.DateTime)
    qr_code_path = db.Column(db.String(200))
    
    def __repr__(self):
        return f"<Booking {self.customer_name} - {self.seat}>"

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<Admin {self.email}>"