# init_db.py
from app import create_app
from models import db, Seat, SeatCategory, SeatStatus, Admin
from werkzeug.security import generate_password_hash

def initialize_seats():
    """Initialize seats using the same Flask app & DB config as the running app."""
    app = create_app()

    with app.app_context():
        # Ensure tables exist
        db.create_all()

        # Create default admin if not exists
        if not Admin.query.filter_by(email="vipwinni@shubra.com").first():
            admin = Admin(email='vipwinni@shubra.com')
            admin.set_password('vipwinni123@')
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin created")
        else:
            print("✅ Admin already exists")

        # Remove existing seats (optional - reinitialize)
        Seat.query.delete()
        db.session.commit()

        # Create seats: 11 rows, each side (left/right) with 6 seats -> total 11*2*6 = 132
        created = 0
        for row in range(1, 12):        # rows 1..11
            for side in ['right', 'left']:
                for seat_num in range(1, 7):    # 1..6
                    category = SeatCategory.VIP if row == 1 else SeatCategory.REGULAR
                    s = Seat(
                        row_number=row,
                        seat_number=seat_num,
                        side=side,
                        category=category,
                        status=SeatStatus.AVAILABLE
                    )
                    db.session.add(s)
                    created += 1

        db.session.commit()
        print(f"✅ Created {created} seats (should be 132)")
        # show count
        print("DB seat count:", Seat.query.count())

if __name__ == "__main__":
    initialize_seats()
