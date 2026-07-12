# Forecat - Dashboard

## Запуск

### 1. Docker
В корне проекта нужно запустить `docker compose up`. Ничего больше не потребуется. \
Доступ по пути `http://localhost`


### 2. Запуск вручную
Нужно провести все этапы по очереди.
1. Создание venv для backend:
Windows:
```sh
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Linux:
```sh
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
2. Запуск backend
```sh
cd src
uvicorn main:app
```
3. Запуск frontend
В новом терминале из корня проекта скопируйте `frontend/.env.example` в `frontend/.env`, затем:
```sh
cd frontend
npm install
npm run dev
```
После запуска frontend будет доступен по адресу `http://localhost:5173`.

## Эндпоинты

### GET /items
Query params:
```
subcategory: str
page: int = 1
page_size: int = 20
```
Список товаров с фильтром по подкатегории и пагинацией.
Пагинация работает через поле `has_next`, которое рассчитывается на backend.
Если `has_next = true`, нужно запросить следующую страницу (`page + 1`).
Если `has_next = false`, данных больше нет и подгружать дальше не нужно.
```
{
    items: [
        {
            sku: str,
            name: str,
            subcategory: str
        },
        ...
    ],
    has_next: bool
}
```

### GET /items/{sku: str}
Данные товара по SKU. Если товара с выбранным SKU нет, возвращает 404.
```
{
    sku: str,
    name: str,
    subcategory: str
}
```

### GET /items/{sku: str}/rows
Query params:
```
date_from: date
date_to: date
```
Ряды по выбранному SKU за период. Возвращает данные из daily только по выбранному SKU и периоду:
```
{
    rows: [
        {
            date: date,
            fact: float || null,
            sales: float || null,
            math: float,
            ml: float,
            ruki: float || null
        },
        ...
    ],
    metrics: {
        fa: float,
        bias: float,
        bias_direction: ENUM(up, down)
    }
}
```
