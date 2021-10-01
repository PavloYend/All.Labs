# Lab.4

Створено репозиторій та склоновано його

Встановлено конкретну версію Python 3.6.* за допомогою утиліти pyenv

Створене віртуальне середовище за допомогою virtualenv

Додано Flask у файл requirements.txt

Реалізовано адресу api/v1/hello-world-10, яка відповідає текстом Hello World 10

Запущено проект через WSGI сервер gunicorn

Клонуємо репозиторій та переходимо в директорію:
$ git clone https://github.com/PavloYend/Lab.4

Для створення віртуального середовища, було використано virtualenv

$ python -m pip install virtualenv

Тепер потрібно його налаштувати та активувати:

$ python -m virtualenv venv

Якщо у вас Windows, активуйте середовище

cmd.exe: venv/Scripts/activate.bat

Встановлюємо залежності:

$ pip install -r requirements.txt

Запускаємо проект:

$ cd lab_4/

$ python -m waitress --port=8000 lab_4:app

http://localhost:8000/api/v1/hello-world-10
