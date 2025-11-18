@echo off
echo Starting Theater Server with UltraMsg WhatsApp Integration...
echo.

REM Set environment variables
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=True

REM Display current settings
echo WhatsApp Configuration:
echo WHATSAPP_ENABLED=%WHATSAPP_ENABLED%
echo ULTRAMSG_INSTANCE_ID=%ULTRAMSG_INSTANCE_ID%
echo ULTRAMSG_TOKEN=%ULTRAMSG_TOKEN%
echo.

REM Start the server
echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
pause