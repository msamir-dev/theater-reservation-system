from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from models import db, Seat, Booking, Admin, SeatStatus
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import os
import uuid
import base64
import traceback

# --- 1. الاستيراد الصحيح والمباشر (تم إزالة الـ try/except المكرر) ---
# لازم الملف whatsapp_production.py يكون موجود جنبه
from whatsapp_production import send_whatsapp_notification
WHATSAPP_AVAILABLE = True

# استيراد مكتبات الصور
import qrcode
from PIL import Image, ImageDraw, ImageFont

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(email=email).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            session["msg"] = "تم تسجيل الدخول بنجاح!"
            session["type"] = "success"
            return redirect(url_for('admin.dashboard'))
        else:
            session["msg"] = "البريد الإلكتروني أو كلمة المرور غير صحيحة"
            session["type"] = "error"
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session["msg"] = "تم تسجيل الخروج بنجاح"
    session["type"] = "success"
    return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total': Seat.query.count(),
        'available': Seat.query.filter_by(status=SeatStatus.AVAILABLE).count(),
        'reserved': Seat.query.filter_by(status=SeatStatus.RESERVED).count(),
        'booked': Seat.query.filter_by(status=SeatStatus.BOOKED).count()
    }
    
    pending_bookings = Booking.query.join(Seat).filter(
        Seat.status == SeatStatus.RESERVED
    ).order_by(Booking.booking_time.desc()).all()
    
    confirmed_bookings = Booking.query.join(Seat).filter(
        Seat.status == SeatStatus.BOOKED
    ).order_by(Booking.confirmation_time.desc()).all()
    
    all_seats = Seat.query.order_by(Seat.side, Seat.row_number, Seat.seat_number).all()
    
    return render_template('admin/dashboard.html',
                           stats=stats,
                           pending_bookings=pending_bookings,
                           confirmed_bookings=confirmed_bookings,
                           all_seats=all_seats)

@admin_bp.route('/api/confirm-booking/<int:booking_id>', methods=['POST'])
@login_required
def confirm_booking(booking_id):
    try:
        booking = Booking.query.get_or_404(booking_id)
        seat = booking.seat
        
        if seat.status != SeatStatus.RESERVED:
            return jsonify({'success': False, 'message': 'هذا الحجز غير صالح للتأكيد'})
        
        # تحديث حالة المقعد والحجز
        seat.status = SeatStatus.BOOKED
        booking.confirmation_time = datetime.utcnow()
        booking.confirmed_by = current_user.id
        
        # إنشاء رمز QR والحصول على المسار النسبي
        qr_code_path = generate_qr_code(booking)
        booking.qr_code_path = qr_code_path 
        
        db.session.commit()
        
        # --- 2. إرسال الواتساب بالاستدعاء الصحيح ---
        try:
            if WHATSAPP_AVAILABLE:
                # إرسال رقم الهاتف أولاً، ثم المسار، ثم الأوبجكت
                print(f"[INFO] Attempting to send WhatsApp to {booking.customer_phone}...")
                success = send_whatsapp_notification(booking.customer_phone, qr_code_path, booking=booking)
                
                if success:
                    print(f"[SUCCESS] WhatsApp sent to {booking.customer_phone}")
                else:
                    print(f"[WARNING] Failed sending WhatsApp to {booking.customer_phone}")
            else:
                print("[INFO] WhatsApp service unavailable flag is False")
                
        except Exception as e:
            print(f"[ERROR] WhatsApp Exception: {e}")
            traceback.print_exc()
        
        return jsonify({'success': True, 'message': 'تم تأكيد الحجز بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        print(f"[FATAL ERROR] {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@admin_bp.route('/api/delete-booking/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    try:
        booking = Booking.query.get_or_404(booking_id)
        seat = booking.seat
        
        if seat.status != SeatStatus.BOOKED:
            return jsonify({'success': False, 'message': 'لا يمكن حذف هذا الحجز - الحالة غير صالحة'})
        
        seat.status = SeatStatus.AVAILABLE
        
        # حذف الملف الفعلي باستخدام المسار المطلق
        if booking.qr_code_path:
            full_path = os.path.join(os.getcwd(), booking.qr_code_path)
            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except Exception as e:
                    print(f"[WARNING] Failed removing QR file: {e}")
        
        db.session.delete(booking)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم حذف الحجز بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@admin_bp.route('/api/reject-booking/<int:booking_id>', methods=['POST'])
@login_required
def reject_booking(booking_id):
    try:
        booking = Booking.query.get_or_404(booking_id)
        seat = booking.seat
        
        if seat.status != SeatStatus.RESERVED:
            return jsonify({'success': False, 'message': 'هذا الحجز غير صالح للرفض'})
        
        seat.status = SeatStatus.AVAILABLE
        
        db.session.delete(booking)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم رفض الحجز بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

def generate_qr_code(booking):
    """Generate ticket image. ASCII only to avoid Linux font issues."""
    
    # QR content
    qr_data = f"""
    Theater Ticket - Confirmation
    Booking ID: {booking.id}
    Name: {booking.customer_name}
    Phone: {booking.customer_phone}
    Seat: {booking.seat.side} - Row {booking.seat.row_number} - Seat {booking.seat.seat_number}
    """
    
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=15,
        border=6,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="#2C3E50", back_color="#ECF0F1").convert('RGB')
    
    canvas_width = 750
    canvas_height = 950
    canvas = Image.new('RGB', (canvas_width, canvas_height), "#F8F9FA")
    draw = ImageDraw.Draw(canvas)
    
    try:
        # Use basic fonts to ensure compatibility
        title_font = ImageFont.truetype("arial.ttf", 40)
        header_font = ImageFont.truetype("arial.ttf", 28)
        text_font = ImageFont.truetype("arial.ttf", 22)
        small_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Background
    for y in range(canvas_height):
        blue_intensity = int(240 - (y / canvas_height) * 60)
        draw.line([(0, y), (canvas_width, y)], fill=(blue_intensity, blue_intensity, 255))
    
    overlay = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 40))
    canvas.paste(overlay, (0, 0), overlay)
    
    # Header
    header_height = 160
    for y in range(header_height):
        blue_intensity = int(44 + (y / header_height) * 30)
        draw.line([(0, y), (canvas_width, y)], fill=(blue_intensity, 62, 80))
    
    draw.text((canvas_width//2, 60), "THEATER TICKET", font=title_font, fill="#ECF0F1", anchor="mm")
    draw.text((canvas_width//2, 110), "OFFICIAL CONFIRMATION", font=header_font, fill="#BDC3C7", anchor="mm")
    
    border_color = "#F39C12"
    draw.rectangle([25, 25, canvas_width-25, canvas_height-25], outline=border_color, width=4)
    draw.rectangle([30, 30, canvas_width-30, canvas_height-30], outline=border_color, width=2)
    
    info_y_start = 200
    info_height = 280
    
    # Draw Shadow FIRST (Layer Fix)
    shadow_offset = 4
    draw.rectangle([50+shadow_offset, info_y_start+shadow_offset, canvas_width-50+shadow_offset, info_y_start+info_height+shadow_offset], 
                   fill="#D3D3D3")

    # Draw Box SECOND
    draw.rectangle([50, info_y_start, canvas_width-50, info_y_start+info_height], 
                   fill="#FFFFFF", outline="#3498DB", width=3)
    
    draw.text((canvas_width//2, info_y_start+40), "BOOKING DETAILS", font=header_font, fill="#2C3E50", anchor="mm")
    
    draw.line([100, info_y_start+80, canvas_width-100, info_y_start+80], fill="#3498DB", width=3)
    
    details_start_y = info_y_start + 120
    line_height = 45
    
    # Safe text drawing (No Emojis)
    draw.text((80, details_start_y), f"Booking ID: #{booking.id}", font=text_font, fill="#2C3E50")
    
    # Sanitize name
    safe_name = booking.customer_name.encode('ascii', 'ignore').decode('ascii')
    draw.text((80, details_start_y + line_height), f"Customer: {safe_name}", font=text_font, fill="#2C3E50")
    draw.text((80, details_start_y + line_height*2), f"Phone: {booking.customer_phone}", font=text_font, fill="#2C3E50")
    draw.text((80, details_start_y + line_height*3), f"Seat: {booking.seat.side} - R:{booking.seat.row_number} - S:{booking.seat.seat_number}", font=text_font, fill="#2C3E50")
    
    confirmation_time = booking.confirmation_time.strftime('%Y-%m-%d %H:%M') if hasattr(booking, 'confirmation_time') else datetime.now().strftime('%Y-%m-%d %H:%M')
    draw.text((80, details_start_y + line_height*4), f"Date: {confirmation_time}", font=text_font, fill="#2C3E50")
    
    qr_size = 250
    qr_x = (canvas_width - qr_size) // 2
    qr_y = info_y_start + info_height + 80
    
    border_size = qr_size + 50
    draw.rectangle([qr_x-25, qr_y-25, qr_x+border_size-25, qr_y+border_size-25], 
                   fill="#FFFFFF", outline="#3498DB", width=4)
    
    # Corners
    corner_size = 20
    corner_color = "#E74C3C"
    draw.polygon([(qr_x-25, qr_y-25), (qr_x-25+corner_size, qr_y-25), (qr_x-25, qr_y-25+corner_size)], fill=corner_color)
    draw.polygon([(qr_x+border_size-25, qr_y-25), (qr_x+border_size-25-corner_size, qr_y-25), (qr_x+border_size-25, qr_y-25+corner_size)], fill=corner_color)
    draw.polygon([(qr_x-25, qr_y+border_size-25), (qr_x-25+corner_size, qr_y+border_size-25), (qr_x-25, qr_y+border_size-25-corner_size)], fill=corner_color)
    draw.polygon([(qr_x+border_size-25, qr_y+border_size-25), (qr_x+border_size-25-corner_size, qr_y+border_size-25), (qr_x+border_size-25, qr_y+border_size-25-corner_size)], fill=corner_color)
    
    qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    canvas.paste(qr_resized, (qr_x, qr_y))
    
    instructions_y = qr_y + border_size - 25 + 50
    draw.text((canvas_width//2, instructions_y), "SCAN QR CODE AT ENTRANCE", font=text_font, fill="#2C3E50", anchor="mm")
    draw.text((canvas_width//2, instructions_y+40), "KEEP THIS TICKET FOR ENTRY", font=text_font, fill="#E74C3C", anchor="mm")
    
    # Stars (ASCII)
    star_color = "#F39C12"
    star_positions = [(120, 120), (canvas_width-120, 120), (180, canvas_height-180), (canvas_width-180, canvas_height-180)]
    for x, y in star_positions:
        draw.text((x, y), "*", font=header_font, fill=star_color, anchor="mm")
    
    footer_height = 100
    footer_y = canvas_height - footer_height
    draw.rectangle([0, footer_y, canvas_width, canvas_height], fill="#2C3E50")
    
    footer_text = "OFFICIAL THEATER TICKET - NOT TRANSFERABLE"
    draw.text((canvas_width//2, footer_y+35), footer_text, font=text_font, fill="#ECF0F1", anchor="mm")
    
    serial_text = f"SERIAL: {booking.id:06d}"
    draw.text((canvas_width//2, footer_y+65), serial_text, font=small_font, fill="#BDC3C7", anchor="mm")
    
    # File Saving
    filename = f"ticket_{booking.id}_{uuid.uuid4().hex[:8]}.png"
    relative_path = os.path.join('static', 'temp_qr', filename)
    full_path = os.path.join(os.getcwd(), relative_path)
    
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    canvas.save(full_path, 'PNG', quality=100, optimize=True)
    
    print(f"[SUCCESS] Ticket created: {relative_path}")
    return relative_path
