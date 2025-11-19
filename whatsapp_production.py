import requests
import os
import time
from datetime import datetime
import base64


def send_whatsapp_notification(booking, qr_code_path=None):
    """ إرسال إشعار واتساب عند تأكيد الحجز """
    print(f"🚀 بدء إرسال إشعار واتساب...")
    
    # التعامل مع booking كـ dictionary أو كائن قاعدة بيانات
    if hasattr(booking, 'get'):
        # booking هو dictionary
        customer_name = booking.get('customer_name', '')
        phone = booking.get('phone', '')
        event_title = booking.get('event_title', '')
        event_date = booking.get('event_date', '')
        event_time = booking.get('event_time', '')
        seats = booking.get('seats', '')
        total_price = booking.get('total_price', '')
    else:
        # booking هو كائن قاعدة بيانات
        customer_name = getattr(booking, 'customer_name', '')
        phone = getattr(booking, 'customer_phone', '')
        event_title = "مسرحية غنوة تيتا"  # قيمة افتراضية
        event_date = booking.confirmation_time.strftime('%Y-%m-%d') if hasattr(booking, 'confirmation_time') else ''
        event_time = booking.confirmation_time.strftime('%H:%M') if hasattr(booking, 'confirmation_time') else ''
        seats = f"{booking.seat.side} - صف {booking.seat.row_number} - مقعد {booking.seat.seat_number}" if hasattr(booking, 'seat') else ''
        total_price = "تم الدفع"  # قيمة افتراضية
    
    print(f"📋 بيانات الحجز: {customer_name}")
    print(f"📱 رقم الهاتف: {phone}")
    print(f"🖼️ مسار QR Code: {qr_code_path}")
    
    try:
        # نحصل على المتغيرات من البيئة
        ultramsg_token = os.getenv("ULTRAMSG_TOKEN", os.getenv("WHATSAPP_API_KEY", ""))
        ultramsg_instance = os.getenv("ULTRAMSG_INSTANCE", os.getenv("ULTRAMSG_INSTANCE_ID", ""))

        
        print(f"🔑 Token موجود: {bool(ultramsg_token)}")
        print(f"🏢 Instance موجود: {bool(ultramsg_instance)}")
        
        if not ultramsg_token or not ultramsg_instance:
            print("❌ خطأ: معلومات UltraMsg غير مكتملة")
            print(f"🔍 بحثنا عن: ULTRAMSG_TOKEN أو WHATSAPP_API_KEY")
            print(f"🔍 بحثنا عن: ULTRAMSG_INSTANCE أو ULTRAMSG_INSTANCE_ID")
            return False
        
        print(f"✅ معلومات UltraMsg مكتملة")
        print(f"🔑 Instance ID: {ultramsg_instance}")
        print(f"📱 Token: {ultramsg_token[:10]}...")
        
        # تنظيف رقم الهاتف
        phone = str(phone)
        phone = phone.replace('+', '').replace(' ', '').replace('-', '')
        if not phone.startswith('2'):
            phone = '2' + phone
        
        print(f"📞 رقم الهاتف بعد التنظيف: {phone}")
        
        # إعداد رسالة التأكيد بالعربي مع جميع تفاصيل الحجز
        message = f"""🎭 تم تأكيد حجزك بنجاح 🎭

👤 الاسم: {customer_name}
📱 رقم الهاتف: {phone}
🎪 العرض: {event_title}
📅 التاريخ: {event_date}
🕐 الوقت: {event_time}
💺 المقعد: {seats}
💰 الإجمالي: {total_price} ج.م

📱 استخدم كود QR المرفق للدخول إلى المسرح
🎟️ احتفظ بتذكرتك الإلكترونية بأمان

شكراً لاختيارك مسرحنا! 🎪"""
        
        print(f"💬 نص الرسالة: {message[:100]}...")
        
        # إرسال الرسالة النصية
        print(f"📤 نرسل الرسالة النصية...")
        text_success = send_text_message(phone, message, ultramsg_token, ultramsg_instance)
        print(f"✅ نجاح الرسالة النصية: {text_success}")
        
        # إرسال صورة QR Code
        image_success = False
        if qr_code_path:
            print(f"🔍 البحث عن ملف QR Code: {qr_code_path}")
            
            # نجرب مسارات مختلفة
            possible_paths = [
                qr_code_path,  # المسار الأصلي
                os.path.join(os.getcwd(), qr_code_path),  # المسار الكامل
                os.path.join('static', qr_code_path.replace('static/', '')),  # مسار static
                os.path.join(os.getcwd(), 'static', qr_code_path.replace('static/', '')),  # مسار static الكامل
                os.path.join('static', 'temp_qr', os.path.basename(qr_code_path)),  # مسار temp_qr
                os.path.join(os.getcwd(), 'static', 'temp_qr', os.path.basename(qr_code_path)),  # مسار temp_qr الكامل
            ]
            
            # نحذف التكرارات ونتحقق
            checked_paths = list(set(possible_paths))
            
            for path in checked_paths:
                print(f"🔍 نجرب المسار: {path}")
                if os.path.exists(path):
                    print(f"✅ تم العثور على الملف: {path}")
                    print(f"📊 حجم الملف: {os.path.getsize(path)} بايت")
                    
                    # نجرب إرسال الصورة مع النص في نفس الوقت
                    print("🎯 نجرب إرسال الصورة مع النص معاً...")
                    image_success = send_image_with_text(phone, path, message, ultramsg_token, ultramsg_instance)
                    
                    # لو فشلت الطريقة الجديدة، نحاول الطرق القديمة
                    if not image_success:
                        print("⚠️ فشل إرسال الصورة مع النص، نحاول طرق بديلة...")
                        image_success = send_image_message(phone, path, ultramsg_token, ultramsg_instance)
                        if not image_success:
                            print("⚠️ فشل إرسال الصورة كملف، نحاول كـ base64...")
                            image_success = send_image_as_base64(phone, path, ultramsg_token, ultramsg_instance)
                    
                    break
                else:
                    print(f"❌ الملف غير موجود: {path}")
            
            if not image_success:
                print(f"⚠️ لم يتم العثور على ملف QR Code في أي مسار")
                print(f"📁 المسارات التي تم التحقق منها: {checked_paths}")
        else:
            print("⚠️ لم يتم توفير مسار QR Code")
        
        print(f"📊 نتائج الإرسال:")
        print(f" ✅ رسالة نصية: {text_success}")
        print(f" ✅ صورة QR: {image_success}")
        
        return text_success or image_success
        
    except Exception as e:
        print(f"❌ خطأ عام في إرسال إشعار واتساب: {e}")
        import traceback
        traceback.print_exc()
        return False

def send_text_message(phone, message, token, instance):
    """إرسال رسالة النصية"""
    try:
        # تأكيد UTF-8
        message = message.encode('utf-8').decode('utf-8')

        if not message:
            message = "🎭 تم تأكيد حجزك بنجاح! برجاء إحضار صورة QR Code عند الحضور."
        
        reference_id = f"theater_booking_{int(datetime.now().timestamp())}"

        url = f"https://api.ultramsg.com/{instance}/messages/chat"

        payload = {
            "token": token,
            "to": phone,
            "body": message,
            "priority": 10,
            "referenceId": reference_id
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        response = requests.post(url, data=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if result.get('sent') == 'true':
                print("✅ تم إرسال رسالة النصية بنجاح")
                return True
            else:
                print(f"⚠️ فشل إرسال الرسالة النصية: {result}")
                return False
        else:
            print(f"⚠️ فشل إرسال الرسالة النصية - رمز الحالة: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ خطأ في إرسال الرسالة النصية: {e}")
        return False


def send_image_message(phone, image_path, token, instance):
    """إرسال صورة QR Code مع تصميج احترافي"""
    try:
        # التأكد من المسار الكامل
        full_path = os.path.join(os.getcwd(), image_path) if not os.path.isabs(image_path) else image_path
        
        if not os.path.exists(full_path):
            print(f"⚠️ ملف الصورة غير موجود: {full_path}")
            # نحاول المسار الأصلي كمان
            if os.path.exists(image_path):
                full_path = image_path
            else:
                print(f"❌ ملف الصورة غير موجود في أي مسار: {image_path}")
                return False
        
        print(f"📤 جاري إرسال الصورة: {full_path}")
        print(f"📊 حجم الملف: {os.path.getsize(full_path)} بايت")
        
        # التحقق من حجم الملف (ما يتعداش 5 ميجا)
        file_size = os.path.getsize(full_path)
        if file_size > 5 * 1024 * 1024:  # 5 MB
            print(f"⚠️ حجم الملف كبير جداً: {file_size} بايت")
            return False
        
        # نحاول أكثر من طريقة
        # الطريقة 1: إرسال كملف مرفق
        try:
            upload_url = f"https://api.ultramsg.com/{instance}/messages/image"
            with open(full_path, 'rb') as image_file:
                filename = os.path.basename(full_path)
                files = {'file': (filename, image_file, 'image/png')}
                data = {
                    'token': token,
                    'to': phone,
                    'caption': '🎫 *تذكرتك الإلكترونية* 🎫\n\n✅ تم تأكيد حجزك بنجاح!\n📱 برجاء إظهار هذه الصورة عند البوابة\n🎭 شكراً لاختياركم مسرح المدينة',
                    'referenceId': f"qr_code_{int(datetime.now().timestamp())}"
                }
                
                print(f"📤 إرسال صورة إلى UltraMsg API...")
                print(f"📤 الرابط: {upload_url}")
                print(f"📤 الهاتف: {phone}")
                print(f"📤 الملف: {filename}")
                
                response = requests.post(upload_url, files=files, data=data, timeout=30)
                
                print(f"📨 رمز الاستجابة: {response.status_code}")
                print(f"📨 نص الاستجابة: {response.text[:500]}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"📨 نتيجة الاستجابة: {result}")
                    if result.get('sent') == 'true':
                        print("✅ تم إرسال صورة QR Code بنجاح")
                        return True
                    elif result.get('error'):
                        print(f"⚠️ فشل إرسال الصورة بسبب خطأ: {result.get('error')}")
                    else:
                        print(f"⚠️ فشل إرسال الصورة: {result}")
                else:
                    print(f"⚠️ فشل إرسال الصورة - رمز الحالة: {response.status_code}")
                    print(f"📨 الرد الكامل: {response.text}")
        
        except Exception as method1_error:
            print(f"❌ خطأ في الطريقة 1: {method1_error}")
            # لو فشلت الطريقة الأولى، نجرب طريقة تانية
            print("🔄 نحاول طريقة تانية...")
            return send_image_as_url(phone, full_path, token, instance)
    
    except Exception as e:
        print(f"❌ خطأ في إرسال الصورة: {e}")
        import traceback
        traceback.print_exc()
        return False

def send_image_as_url(phone, image_path, token, instance):
    """طريقة بديلة لإرسال الصورة كرابط أو base64"""
    try:
        # نحاول أكثر من طريقة
        # الطريقة 1: إرسال كرابط
        try:
            upload_url = f"https://api.ultramsg.com/{instance}/messages/image"
            # نبعت الصورة كرابط من السيرفر المحلي
            server_url = f"http://localhost:5000/{image_path.replace('static/', '')}"
            # لو الصورة في static folder نستخدم المسار الصحيح
            if 'static' in image_path:
                server_url = f"http://localhost:5000/{image_path}"
            
            print(f"📡 جاري إرسال الصورة كرابط: {server_url}")
            
            data = {
                'token': token,
                'to': phone,
                'image': server_url,
                'caption': '🎫 *تذكرتك الإلكترونية* 🎫\n\n✅ تم تأكيد حجزك بنجاح!',
                'referenceId': f"qr_code_url_{int(datetime.now().timestamp())}"
            }
            
            response = requests.post(upload_url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('sent') == 'true':
                    print("✅ تم إرسال صورة QR Code بالرابط بنجاح")
                    return True
                else:
                    print(f"⚠️ فشل إرسال الصورة بالرابط: {result}")
            else:
                print(f"⚠️ فشل إرسال الصورة بالرابط - رمز الحالة: {response.status_code}")
        
        except Exception as url_error:
            print(f"❌ خطأ في إرسال الرابط: {url_error}")
        
        # الطريقة 2: إرسال كملف base64
        print("🔄 نحاول إرسال كملف base64...")
        return send_image_as_base64(phone, image_path, token, instance)
    
    except Exception as e:
        print(f"❌ خطأ في إرسال الصورة بالرابط: {e}")
        return False

def send_image_as_base64(phone, image_path, token, instance):
    """إرسال الصورة كملف base64"""
    try:
        import base64
        
        # قراءة الصورة وتحويلها لـ base64
        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        upload_url = f"https://api.ultramsg.com/{instance}/messages/image"
        
        data = {
            'token': token,
            'to': phone,
            'image': f"data:image/png;base64,{encoded_image}",
            'caption': '🎫 *تذكرتك الإلكترونية* 🎫\n\n✅ تم تأكيد حجزك بنجاح!',
            'referenceId': f"qr_code_base64_{int(datetime.now().timestamp())}"
        }
        
        print(f"📡 جاري إرسال الصورة كـ base64...")
        response = requests.post(upload_url, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('sent') == 'true':
                print("✅ تم إرسال صورة QR Code كـ base64 بنجاح")
                return True
            else:
                print(f"⚠️ فشل إرسال الصورة كـ base64: {result}")
                return False
        else:
            print(f"⚠️ فشل إرسال الصورة كـ base64 - رمز الحالة: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ خطأ في إرسال الصورة كـ base64: {e}")
        return False

def send_image_with_text(phone, image_path, text, ultramsg_token, ultramsg_instance):
    """إرسال صورة مع نص في نفس الرسالة"""
    try:
        print(f"📤 إرسال صورة مع نص...")
        
        # نقرأ الصورة ونحولها لـ base64
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # نحول الصورة لـ base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # نحصل على نوع الصورة
        image_type = 'image/png' if image_path.endswith('.png') else 'image/jpeg'
        
        # نجهز البيانات للإرسال
        url = f"https://api.ultramsg.com/{ultramsg_instance}/messages/image"
        data = {
            "token": ultramsg_token,
            "to": phone,
            "image": f"data:{image_type};base64,{image_base64}",
            "caption": text,
            "priority": 10,
            "referenceId": ""
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        print(f"📡 إرسال إلى: {url}")
        response = requests.post(url, json=data, headers=headers)
        
        print(f"📊 رمز الحالة: {response.status_code}")
        print(f"📄 الرد: {response.text[:200]}")
        
        if response.status_code == 200:
            response_data = response.json()
            if 'sent' in str(response_data).lower():
                print("✅ تم إرسال الصورة مع النص بنجاح!")
                return True
            else:
                print(f"⚠️ لم يتم إرسال الرسالة: {response_data}")
                return False
        else:
            print(f"❌ فشل الإرسال، رمز الحالة: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ خطأ في إرسال الصورة مع النص: {e}")
        return False

# اختبار الوظيفة
if __name__ == "__main__":
    # اختبار بسيط
    print("🧪 اختبار نظام UltraMsg...")
    
    # قراءة الإعدادات
    token = "dptyizexv2v66opm"
    instance = "instance150426"

    
    if token and instance:
        print(f"✅ تم العثور على الإعدادات: Instance={instance}")
        print("يمكنك الآن اختبار الإرسال من لوحة التحكم الإدارية")
    else:
        print("❌ لم يتم العثور على إعدادات UltraMsg في ملف .env")
