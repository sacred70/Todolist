# Todolist
Планировщик задач 
Cтек

python3.10
Django 4.1
Postgres 15.0
Docker
poetry
DRF 3.14
Pydentic 1.1
Docker-compose
В данном проекте реализован планировщик задач на Django с использованием DRF. Список не обходимых переменных окружения находится в .env.dist

Ознакомиться с версией проекта можно по ссылке http://51.250.16.249 Установка:

Клонируйте репозиторий с github на локальный компьютер
Создайте виртуальное окружение
установите poetry командой pip install poetry
установите зависимости командой poetry install
Создайте в корне проекта файл в .env и заполните
Соберите и поднимите docker-контейнер командой docker compose up -d --build
Список приложений проекта и их реализация:

core
    Регистрация пользователя
    Login и Logout
    Обновление данных о пользователе и пароля
goals

Создание новой доски
Получение списка досок пользователя
Редактирование и удаление досок пользователя
Создание новой категории
Получение списка категорий где текущий user является участником
Создание цели у категории
Получение списка целей
Редактирование и удаление целей
Создание, редактирование и удаление комментариев у цели
bot

Реализованна аутентификация через telegram
С помощью telegram-bot можно получить список целей
С помощью telegram-bot можно создать новую цель
