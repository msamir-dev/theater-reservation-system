@echo off
echo 🎭 بدء إعداد نظام حجز مقاعد المسرح...
echo.

REM التحقق من تثبيت Python
"C:\Program Files\Python312\python.exe" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت أو غير متاح في PATH
    echo 📥 يرجى تثبيت Python أولاً من:
    echo    https://www.python.org/downloads/
    echo.
    echo تأكد من اختيار "Add Python to PATH" أثناء التثبيت
    pause
    exit /b 1
)

echo ✅ Python موجود
"C:\Program Files\Python312\python.exe" --version
echo.

REM تثبيت المتطلبات
echo 📦 تثبيت المتطلبات...
"C:\Program Files\Python312\python.exe" -m pip install --upgrade pip
"C:\Program Files\Python312\python.exe" -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ فشل تثبيت المتطلبات
    pause
    exit /b 1
)

echo ✅ تم تثبيت المتطلبات بنجاح
echo.

REM تهيئة قاعدة البيانات
echo 🗄️ تهيئة قاعدة البيانات...
"C:\Program Files\Python312\python.exe" init_db.py

if %errorlevel% neq 0 (
    echo ❌ فشل تهيئة قاعدة البيانات
    pause
    exit /b 1
)

echo ✅ تم تهيئة قاعدة البيانات
echo.

REM تشغيل التطبيق
echo 🚀 تشغيل تطبيق المسرحية...
echo.
echo 📱 سيتم فتح الموقع تلقائياً...
echo 🔑 بيانات تسجيل الدخول الإدارية:
echo    البريد: vipwinni@shubra.com
 echo   الباسوورد: vipwinni123@
echo.
echo ⚠️ لا تغلق هذه النافذة أثناء تشغيل الموقع
echo.

REM فتح المتصفح
start http://localhost:5000

REM تشغيل التطبيق
"C:\Program Files\Python312\python.exe" app.py

if %errorlevel% neq 0 (
    echo ❌ فشل تشغيل التطبيق
    echo تأكد من أن المنفذ 5000 متاح
    pause
    exit /b 1
)

echo ✅ تم إيقاف التشغيل بنجاح
pause