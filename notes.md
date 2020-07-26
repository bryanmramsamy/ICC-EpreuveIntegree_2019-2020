# Notes

## Raw memento

### Commands

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


### Syntax and semantics

#### datetime

```python
import datetime


datetime.date.today()
# datetime.date(2020, 7, 14)
```

#### Create object in shell

Example: `UserProfile` instantiation

```python
up = UserProfile(
    pk=1,
    user=bryan,
    birthday=datetime.date(1995, 1, 24),
    nationality="Belgian",
    address="Raccoon City 1998",
    postalCode="666",
    postalLocality="Raccoon"
)

# or

up = UserProfile(
    bryan,
    1,
    datetime.date(1995, 1, 24),
    "Belgian",
    "Raccoon City 1998",
    "666",
    "Raccoon"
)
```

#### related_name

Get the first module

```python
module = Module.objects.all()[0]
```

Get all the Users from it's eligible_teachers field

```python
module.can_be_teached_by.all()
```

Result:

```python
class Module(Resource):
    eligible_teachers = models.ManyToManyField(
        User,
        blank=True,
        related_name="can_be_teached_by",
        verbose_name=_("Eligible teachers")
    )
```
