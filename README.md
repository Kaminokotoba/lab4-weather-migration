# Лаб 4. Міграція БД

Полєжаєв Єгор, КМ-41, №15 (варіант 3 — опади)

## Що зроблено

- Layered Architecture (domain / repositories / services / cli)
- ORM на SQLAlchemy
- Alembic: створення схеми + винесення опадів в окрему таблицю без втрати даних
- Колонка is_worth_going_outside + проста формула
- Завантаження з CSV
- Консольний запит по країні і даті
- Перенесення на MySQL

## Запуск

```bash
pip install -r requirements.txt
cp .env
alembic upgrade head
python scripts/load_data.py --limit 2000
python -m app.cli.main
```

## Формула

- опади ≥ 2 мм → ні
- вологість ≥ 90% і є опади → ні
- вітер ≥ 40 км/год → ні
- інакше → так
