# Тестовое задание ПИК.ПРО

Cервис для верефикации станций метро

# Как установить


Для работы необоходим Python 3. 
Установите зависимости с помощью pip:
```bash
pip install -r requirements.txt
```
Для лучшей изоляции  рекомендуется использовать виртуальное окружение.

# Quickstart


Запуск 
```bash
$ python3 main.py
```
Сервис доступен по адресу: [localhost:8000](http://localhost:8000/)

# Как использовать

## Создать здание

### Request

`POST /api/v1/metro/verificate/`

    curl --location --request POST 'http://localhost:8000/api/v1/metro/verificate/'--header 'Content-Type: text/plain' --data-raw '["Каховская","Баррикадная", "несуществует"]'

### Response

    
    {
    "unchanged": [
        "Каховская",
        "Баррикадная"
    ],
    "update": [
        "несуществует"
    ],
    "deleted": [
        "Волгоградский проспект",
        "Бульвар Рокоссовского",
        "Калужская",
        "Международная",
        ...
    }