from flask import Blueprint, jsonify, request
from models import db, Seat, Booking, SeatStatus, SeatCategory
from datetime import datetime
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/seats')
def get_seats():
    print('API /seats endpoint called')  # Debug output
    """الحصول على جميع المقاعد"""
    try:
        seats = Seat.query.order_by(Seat.side, Seat.row_number, Seat.seat_number).all()
        
        seats_data = []
        for seat in seats:
            seats_data.append({
                'id': seat.id,
                'side': seat.side,
                'row_number': seat.row_number,
                'seat_number': seat.seat_number,
                'category': seat.category.value,
                'status': seat.status.value,
                'booking_id': seat.booking.id if seat.booking else None
            })
        
        return jsonify({
            'success': True,
            'seats': seats_data
        })
    except Exception as e:
        print(f'Error in get_seats: {e}')
        return jsonify({
            'success': False,
            'message': str(e),
            'seats': []
        })

@api_bp.route('/book-seat', methods=['POST'])
def book_seat():
    """حجز مقعد"""
    try:
        data = request.get_json()
        seat_id = data.get('seat_id')
        customer_name = data.get('customer_name')
        customer_phone = data.get('customer_phone')
        
        if not all([seat_id, customer_name, customer_phone]):
            return jsonify({'success': False, 'message': 'جميع الحقول مطلوبة'})
        
        # التحقق من صحة رقم الهاتف المصري
        import re
        egyptian_phone_regex = r'^01[0125][0-9]{8}$'
        if not re.match(egyptian_phone_regex, customer_phone):
            return jsonify({'success': False, 'message': 'يرجى إدخال رقم مصري صحيح (مثال: 01020158805)'})
        
        # التحقق من المقعد
        seat = Seat.query.get(seat_id)
        if not seat:
            return jsonify({'success': False, 'message': 'المقعد غير موجود'})
        
        if seat.status != SeatStatus.AVAILABLE:
            return jsonify({'success': False, 'message': 'المقعد غير متاح'})
        
        # إنشاء حجز جديد
        booking = Booking(
            seat_id=seat_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            booking_time=datetime.utcnow()
        )
        
        # تحديث حالة المقعد
        seat.status = SeatStatus.RESERVED
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم حجز المقعد بنجاح، سيتم التواصل معك قريباً لتأكيد الحجز',
            'booking_id': booking.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'حدث خطأ: {str(e)}'})

@api_bp.route('/booking-status/<int:booking_id>')
def booking_status(booking_id):
    """التحقق من حالة الحجز"""
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'exists': False})
    
    return jsonify({
        'exists': True,
        'status': booking.seat.status.value,
        'seat_info': str(booking.seat)
    })