from models import db, Seat, SeatCategory, SeatStatus

def initialize_seats(app):
    with app.app_context():
        Seat.query.delete()
        db.session.commit()

        created = 0
        for row in range(1, 12):
            for side in ['right', 'left']:
                for seat_num in range(1, 7):
                    category = SeatCategory.VIP if row == 1 else SeatCategory.REGULAR

                    seat = Seat(
                        row_number=row,
                        seat_number=seat_num,
                        side=side,
                        category=category,
                        status=SeatStatus.AVAILABLE
                    )

                    db.session.add(seat)
                    created += 1

        db.session.commit()
        print(f"✅ Created {created} seats (132 expected)")
