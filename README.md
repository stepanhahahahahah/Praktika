# Фитнес-клуб практика
## Выполнили студенты гр. Ис-61 Морозов С. и Игошева П.

## Запуск
Для запуска нужно ввести последовательность команд
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask run --debug
```

## Обновление базы данных
```bash
flask db init
flask db migrate -m "Add table"
flask db upgrade
```
