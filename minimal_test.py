#!/usr/bin/env python3
"""
تطبيق بسيط للاختبار
"""

from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>🎭 مسرحية غنوة تيتا</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 40px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            h1 { font-size: 3em; margin-bottom: 20px; }
            .button {
                background: #ff6b6b;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 1.2em;
                cursor: pointer;
                margin: 10px;
                transition: transform 0.3s;
            }
            .button:hover { transform: scale(1.05); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 مسرحية غنوة تيتا</h1>
            <h2>نظام حجز المقاعد</h2>
            <p>✅ تم تشغيل الموقع بنجاح!</p>
            <p>🌐 الموقع يعمل على: <strong>http://localhost:5000</strong></p>
            <br>
            <button class="button" onclick="alert('تم تحديث رسائل الواتساب بنجاح!')">
                اختبار نظام الواتساب
            </button>
            <button class="button" onclick="alert('نظام الحجز جاهز!')">
                اختبار نظام الحجز
            </button>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    print('🎭 تم تشغيل مسرحية غنوة تيتا بنجاح!')
    print('🌐 فتح المتصفح على: http://localhost:5000')
    print('✅ اضغط Ctrl+C لايقاف الخادم')
    app.run(debug=True, host='0.0.0.0', port=5000)