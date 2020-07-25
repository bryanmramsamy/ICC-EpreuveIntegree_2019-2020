# SERINA-Project

**S**uperintent app for **E**ducational **R**esources, **I**nsciptions a**N**d **A**dministration

Épreuve intégrée de la section: Bachelier en informatique de gestion

Bryan M. Ramsamy 2019-2020 - Institut des Carrières Commerciales 2019-2020

## Commands

```bash
# makemigrations
docker-compose run --rm dill python3 manage.py makemigrations
```

```bash
# migrate
docker-compose run --rm dill python3 manage.py migrate
```

```bash
# undo migrate
docker-compose run --rm dill python3 manage.py migrate <app> <migration_to_undo^1>
```

```bash
# undo all migrates
docker-compose run --rm dill python3 manage.py migrate <app> zero
```