# init_db.py

from flask import Flask
from models import db, Seat, SeatCategory, SeatStatus, Admin

def initialize_seats(app):
    with app.app_context():
        # إزالة المقاعد القديمة
        Seat.query.delete()
        db.session.commit()

        # إنشاء المقاعد
        created = 0
        for row in range(1, 12):  # الصفوف 1..11
            for side in ['right', 'left']:
                for seat_num in range(1, 7):  # 1..6 لكل صف
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

if __name__ == "__main__":
    # تشغيل بفصل يدوي عند الحاجة فقط
    from app import create_app
    app = create_app()
    initialize_seats(app)
    print("Seats initialized successfully!")
