# goit-pythonweb-hw-08

## Встановлення та запуск

### 1. Встановіть залежності
```
poetry install
```

Активуйте віртуальне середовище
```
poetry shell
```

### 2. Налаштування змінних середовища

Створіть файл `.env` у корені проекту (можете скопіювати з `.env.example`):


### 3. Запуск PostgreSQL через Docker

```bash
docker-compose up -d
```

### 4. Застосування міграцій

```bash
alembic upgrade head
```

### 5. Заповнення бази тестовими даними

```bash
python sample_contacts.py
```

### 6. Запуск додатку

```bash
python main.py
```

Додаток буде доступний за адресою: http://localhost:8000

## API Документація

Swagger документація доступна за адресою: http://localhost:8000/docs
