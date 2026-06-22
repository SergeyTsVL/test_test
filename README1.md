cd /mnt/c/Users/tsars/PycharmProjects/chat

curl -4 ifconfig.me
91.149.114.55

sudo apt update
tsars
Qazwsxedc123
sudo apt install -y python3.12 python3.12-venv python3-pip nginx redis-server ufw

sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
sudo ufw status

pip freeze > requirements.txt
pip install -r requirements.txt
pip install "django>=5.0" channels channels_redis daphne
django-admin startproject config .
python manage.py startapp chat

python manage.py migrate
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
python manage.py runserver 127.0.0.1:8000
http://127.0.0.1:8000/room/test/
https://test-dns.ru/admin/
daphne -b 127.0.0.1 -p 8000 config.asgi:application

python -m daphne -b 127.0.0.1 -p 8000 config.asgi:application

python -m daphne -b 0.0.0.0 -p 8000 config.asgi:application


python -m daphne -b 127.0.0.1 -p 8000 project.asgi:application 

http://test-dns.ru/ws/room/test/
adminadmin
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d test-dns.ru -d www.test-dns.ru

sudo ss -ltnp | grep ':80'

tsarskiytsarskiy@mail.ru
91.105.181.47 - дом
91.149.114.55 - работа

https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/
brew install cloudflared
winget install --id Cloudflare.cloudflared
Get-ChildItem C:\ -Filter cloudflared.exe -Recurse -ErrorAction SilentlyContinue
$pathToAdd = "C:\Program Files (x86)\cloudflared"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$pathToAdd", "User")
cloudflared --version
where.exe cloudflared

curl.exe -I http://127.0.0.1
curl.exe -I www.test-dns.ru
cloudflared tunnel login
cloudflared tunnel create test-dns

cloudflared tunnel route dns test-dns test-dns.ru
cloudflared tunnel route dns test-dns www.test-dns.ru

cloudflared tunnel run --url http://127.0.0.1:80 test-dns


cloudflared tunnel --protocol http2 run --url http://127.0.0.1:8000 test-dns
cloudflared tunnel --config "C:\Users\tsars\.cloudflared\config.yml" run


cloudflared tunnel --config "C:\Users\tsars\.cloudflared\config.yml" run test-dns --protocol1 http2





cloudflared tunnel --config "C:\Users\tsars\.cloudflared\config.yml" run --protocol http2 cdd645a3-ccfd-4ca8-a195-6a63ae59c7ae

cloudflared tunnel --config "C:\Users\tsars\.cloudflared\config.yml" --protocol quic run
cloudflared tunnel --config "C:\Users\tsars\.cloudflared\config.yml" run test-dns








daphne -b 127.0.0.1 -p 8000 config.asgi:application
















sudo nano /etc/nginx/sites-available/test-dns.ru
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 80;
    server_name test-dns.ru www.test-dns.ru;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $remote_addr;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
    }
Сохранить: нажмите
Ctrl + O
(Write Out)
Он покажет строку “File Name to Write …” (как у вас на скрине) → просто нажмите Enter для подтверждения имени файла
Выйти: нажмите
Ctrl + X
Активируйте:
sudo ln -s /etc/nginx/sites-available/test-dns.ru /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d test-dns.ru -d www.test-dns.ru

dns_cloudflare_api_token = oCUl1t7DW8-YN-MeIfmyqfnFdYq_DgrFZYG0lCZZ

curl "https://api.cloudflare.com/client/v4/user/tokens/verify" \
-H "Authorization: Bearer oCUl1t7DW8-YN-MeIfmyqfnFdYq_DgrFZYG0lCZZ"
sudo mkdir -p /root/.secrets/certbot
dns_cloudflare_api_token = oCUl1t7DW8-YN-MeIfmyqfnFdYq_DgrFZYG0lCZZ
sudo cat /root/.secrets/certbot/cloudflare.ini

sudo apt update
sudo apt install -y certbot python3-certbot-dns-cloudflare

sudo certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials /root/.secrets/certbot/cloudflare.ini \
  --dns-cloudflare-propagation-seconds 60 \
  -d test-dns.ru -d www.test-dns.ru

sudo chown root:root /root/.secrets/certbot/cloudflare.ini
sudo chmod 600 /root/.secrets/certbot/cloudflare.ini
sudo chmod 700 /root/.secrets/certbot
sudo chmod 700 /root/.secrets

sudo ls -ld /root/.secrets /root/.secrets/certbot
sudo ls -l /root/.secrets/certbot/cloudflare.ini




 













cd PycharmProjects\chat
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=80 connectaddress=192.168.38.23 connectport=80

PS C:\Users\tsars> cd PycharmProjects\chat
PS C:\Users\tsars\PycharmProjects\chat> netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=80 connectaddress=192.168.38.23 connectport=80

PS C:\Users\tsars\PycharmProjects\chat> netsh interface portproxy show v4tov4

Listen on ipv4:             Connect to ipv4:

Address         Port        Address         Port
--------------- ----------  --------------- ----------
0.0.0.0         80          192.168.38.23   80


PS C:\Users\tsars\PycharmProjects\chat> netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=80 connectaddress=192.168.38.23 connectport=80

PS C:\Users\tsars\PycharmProjects\chat> netsh interface portproxy show v4tov4

Listen on ipv4:             Connect to ipv4:

Address         Port        Address         Port
--------------- ----------  --------------- ----------
0.0.0.0         80          192.168.38.23   80



sudo -u www-data venv/bin/ pip install daphne

описать подробно как на python 3.12 в django  сделать сайт для общения в формате видео чата мой DNS test-DNS.ru

Ниже — подробная, практичная инструкция как на Python 3.12 + Django поднять видео-чат (WebRTC) и привязать домен test-DNS.ru. 
Я опишу рабочий вариант 1-на-1 (P2P) с Django Channels (WebSocket-сигналинг), STUN/TURN, HTTPS, деплоем на Linux + Nginx. Э
то базис; после него можно расширять до комнат и групповых звонков (через SFU).

sudo systemctl status certbot.timer




8) HTTPS (Let’s Encrypt)

Самый простой путь — certbot:
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d test-dns.ru -d www.test-dns.ru

После этого certbot автоматически включит 443 и редирект с 80 на 443 (если выберете redirect).
Проверка:
https://test-dns.ru/room/test/

9) TURN (coturn) — чтобы работало “везде”

9.1 Установка coturn

sudo apt install -y coturn

9.2 Настройка 
/etc/turnserver.conf

Минимальный пример (упрощённо):
listening-port=3478
fingerprint
lt-cred-mech
realm=test-dns.ru

user=webrtcuser:webrtcpass

# Важно: внешний IP сервера
external-ip=ВАШ_ПУБЛИЧНЫЙ_IP

# (рекомендуется) ограничить диапазон UDP портов
min-port=49160
max-port=49200

Включите сервис:
sudo sed -i 's/#TURNSERVER_ENABLED=0/TURNSERVER_ENABLED=1/' /etc/default/coturn
sudo systemctl enable --now coturn

Откройте firewall (если есть):

3478 tcp/udp
49160-49200 udp (или ваш диапазон)

9.3 Добавьте TURN в 
iceServers
 (в шаблоне JS)

const iceServers = [
  { urls: "stun:stun.l.google.com:19302" },
  { urls: "turn:turn.test-dns.ru:3478", username: "webrtcuser", credential: "webrtcpass" }
];

TURN лучше держать на отдельном VPS, если домашний NAT/роутер “капризный”, но технически можно и на том же сервере.
10) Запуск как сервис (systemd), чтобы работало постоянно

Создайте 
/etc/systemd/system/webrtcchat.service
:
[Unit]
Description=WebRTC Django (Daphne)
After=network.target

[Service]
User=www-data
WorkingDirectory=/srv/webrtcchat
Environment="DJANGO_SETTINGS_MODULE=config.settings"
ExecStart=/srv/webrtcchat/venv/bin/daphne -b 127.0.0.1 -p 8000 config.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
формат ini

Права на папку:
sudo chown -R www-data:www-data /srv/webrtcchat

Запуск:
sudo systemctl daemon-reload
sudo systemctl enable --now webrtcchat
sudo systemctl status webrtcchat



Что дальше можно улучшить (когда базис заработает)

Авторизация пользователей (логин), список “онлайн”, кнопка “позвонить”
Комнаты по приглашению (одноразовые ссылки)
Ограничение комнаты до 2 участников
Запись звонка (тут может пригодиться aiortc на сервере)
Групповые звонки (нужен SFU: mediasoup/janus/ion-sfu и т.п.)


Уточнения, чтобы привязать именно к вашей ситуации

Вы хотите хостить это на домашнем Windows ПК или на Linux/VPS?


Если на Windows/дома — напишите:

какой у вас роутер (модель) и есть ли проброс 80/443
какой процесс будет использоваться: Nginx (Windows) или хотите всё же Caddy
— и я адаптирую “деплой” шаги под Windows 11, включая сертификаты и службу.
