from app import create_app
from models import db, Seat, SeatCategory, SeatStatus, Admin
from werkzeug.security import generate_password_hash

def initialize_seats():
    """تهيئة المقاعد في قاعدة البيانات"""
    app = create_app()
    
    with app.app_context():
        
        # إنشاء الجداول
        db.create_all()

        # إنشاء حساب المدير الافتراضي
        if not Admin.query.first():
            admin = Admin(email='vipwinni@shubra.com')
            admin.password_hash = generate_password_hash('vipwinni123@')
            db.session.add(admin)
            print("✅ تم إنشاء حساب المدير")
        else:
            print("⚠️ حساب المدير موجود بالفعل")

        # مسح المقاعد القديمة
        Seat.query.delete()
        db.session.commit()

        seats = []
        
        # 11 صف × 6 يمين × 6 شمال = 132 مقعد
        for side in ['right', 'left']:
            for row in range(1, 12):
                for seat_num in range(1, 7):

                    category = (
                        SeatCategory.VIP if row == 1 else SeatCategory.REGULAR
                    )

                    seats.append(
                        Seat(
                            row_number=row,
                            seat_number=seat_num,
                            side=side,
                            category=category,
                            status=SeatStatus.AVAILABLE
                        )
                    )

        db.session.bulk_save_objects(seats)
        db.session.commit()

        print(f"🎉 تم إنشاء {len(seats)} مقعد بنجاح!")

if __name__ == '__main__':
    initialize_seats()
