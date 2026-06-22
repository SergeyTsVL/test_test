#  Тестовое задание "ООО НЛ Континент" 


# Установка виртуального окружения
pip freeze > requirements.txt
pip install -r requirements.txt
pip install django-two-factor-auth[phonenumbers,totp]
pip install django-otp
pip install django-two-factor-auth
pip install psycopg2-binary


# Создание миграций
python manage.py makemigrations
python manage.py migrate






daphne -b 127.0.0.1 -p 8000 project.asgi:application
daphne -b 192.168.0.19 -p 8000 project.asgi:application
"C:\caddy\caddy_windows_amd64.exe" run --config C:\caddy\Caddyfile
+ запустить докер


http://192.168.10.1/cgi-bin/luci/


# Создание учетной записи администратора
python manage.py createsuperuser
Например:
Username (leave blank to use 'tsars'): tsars
Email address: test@example.com
Password: 123456789

# Установите свою базу данных PostgreSQL 



как востановить образ https://yandex.ru/video/preview/13959145096990315866








# Запуск всех тестов
python manage.py test --keepdb
python manage.py test --verbosity 2


