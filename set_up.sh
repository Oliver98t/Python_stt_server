python stt_server/manage.py makemigrations 
python stt_server/manage.py migrate
#python stt_server/manage.py runserver 0.0.0.0:8000
cd stt_server
gunicorn stt_server.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --log-level debug --access-logfile - --error-logfile -