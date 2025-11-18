from app import create_app, db
from models import Seat, SeatCategory, SeatStatus
from werkzeug.security import generate_password_hash

def initialize_seats():
    """تهيئة المقاعد في قاعدة البيانات"""
    app = create_app()
    
    with app.app_context():
        # إنشاء جميع الجداول
        db.create_all()
        
        # إنشاء حساب المدير الافتراضي
        from models import Admin
        if not Admin.query.first():
            admin = Admin(email='vipwinni@shubra.com')
            admin.password_hash = generate_password_hash('vipwinni123@')
            db.session.add(admin)
            print("✅ تم إنشاء حساب المدير بنجاح")
        else:
            print("✅ حساب المدير موجود بالفعل")
        
        # حذف جميع المقاعد الموجودة (لإعادة التهيئة)
        Seat.query.delete()
        
        seat_id = 1
        
        # إنشاء المقاعد للجانب الأيمن والأيسر
        for side in ['right', 'left']:
            for row in range(1, 12):  # 11 صف
                # تحديد عدد المقاعد في كل صف (66 مقعد لكل جانب)
                seats_in_row = 6  # 6 مقاعد في كل صف
                
                for seat_num in range(1, seats_in_row + 1):
                    # تحديد فئة المقعد (VIP للصف الأول)
                    category = SeatCategory.VIP if row == 1 else SeatCategory.REGULAR
                    
                    seat = Seat(
                        id=seat_id,
                        row_number=row,
                        seat_number=seat_num,
                        side=side,
                        category=category,
                        status=SeatStatus.AVAILABLE
                    )
                    
                    db.session.add(seat)
                    seat_id += 1
        
        db.session.commit()
        print(f"✅ تم إنشاء {seat_id-1} مقعد بنجاح!")

if __name__ == '__main__':
    initialize_seats()