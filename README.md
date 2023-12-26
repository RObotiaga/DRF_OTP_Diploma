# Аутентификационный Страж
### Проект "Аутентификационный Страж" предназначен для создания безопасной системы аутентификации пользователей. Включает в себя функционал регистрации, подтверждения по коду, управления пригласительными кодами и безопасного обновления паролей.

# Установка
### Клонируйте репозиторий на свой локальный компьютер:
`git clone https://github.com/RObotiaga/DRF_OTP_Diploma.git`

### Перейдите в каталог проекта:
`cd DRF_OTP_Diploma`

### Установите зависимости, используя poetry:
`poetry install`

# Настройка
Для работы сервиса необходимо настроить некоторые параметры, такие как база данных и настройки email-отправки. Вам потребуются следующие параметры, которые вы можете установить в файле .env:
```
DEBUG=True

DB_NAME=
DB_USER=postgres
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432

ACCESS_TOKEN_LIFETIME=1500
REFRESH_TOKEN_LIFETIME=15

#Также требуется регистрация в сервисе https://www.twilio.com/
TWILIO_SID=
TWILIO_TOKEN=
NUMBER=
```
# Запуск
### Запустите сервер 
`python manage.py runserver`
# Docker
* Создайте файл .env и установите необходимые переменные окружения:
* Запустите проект с помощью Docker Compose:
`docker-compose up -d`

# Postman
Импортировать коллекцию запросов postman
`https://api.postman.com/collections/30740427-8f1b58ab-7c84-4562-ae6f-976bb814328e?access_key=PMAT-01HJKC8A5PK9R2SJJQDXZRFMP5`
# PythonAnywhere
`http://aptemond.pythonanywhere.com/`
