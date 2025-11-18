@echo off
echo 🚀 تشغيل تطبيق مسرحية غنوة تيتا
echo.

REM طباعة معلومات البيئة
echo 🔍 متغيرات البيئة:
echo ULTRAMSG_TOKEN: %ULTRAMSG_TOKEN%
echo ULTRAMSG_INSTANCE: %ULTRAMSG_INSTANCE%
echo WHATSAPP_API_KEY: %WHATSAPP_API_KEY%
echo ULTRAMSG_INSTANCE_ID: %ULTRAMSG_INSTANCE_ID%
echo.

REM محاولة تشغيل التطبيق
echo 🎯 تشغيل التطبيق...
echo.

REM استخدام Python المتاح
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ تم العثور على Python
    echo.
    python -c "import sys; print('Python version:', sys.version)"
    echo.
    echo 🚀 تشغيل التطبيق...
    python app.py
) else (
    echo ❌ لم يتم العثور على Python
    echo 📥 يرجى تثبيت Python أو التحقق من PATH
)

echo.
echo 🏁 انتهى التشغيل
pause