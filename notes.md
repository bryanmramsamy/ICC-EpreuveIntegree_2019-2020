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

#### deployment docker commands

sudo ls
    2  ls
    3  ll
    4  deluser brya
    5  sudo deluser brya
    6  groups
    7  cd ..
    8  ls
    9  sudo rm -r brya
   10  ls
   11  exit
   12  su
   13  exit
   14  ls
   15  ll
   16  mkdir -p ~/.ssh/authorized_keys
   17  ls
   18  ll
   19  cd .ssh/
   20  ls
   21  cd authorized_keys/
   22  cd ..
   23  rmdir authorized_keys/
   24  vi authorized_keys
   25  exit
   26  ls
   27  exit
   28  ls
   29  l
   30  ll
   31  exit
   32  ls
   33  cd ICC-EpreuveIntegree_2019-2020/
   34  ls
   35  docker-compose -f docker-compose.prod.yml up --build
   36  sudo apt-get remove docker-compose
   37  sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   38  sudo chmod +x /usr/local/bin/docker-compose
   39  docker-compose --version
   40  sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
   41  docker-compose --version
   42  docker-compose -f docker-compose.prod.yml up --build
   43  chmod +x serina-project/entrypoint.*
   44  docker-compose -f docker-compose.prod.yml up --build
   45  git pull
   46  docker-compose -f docker-compose.prod.yml up --build
   47  history

scp .env* bryan@78.46.198.120:~/ICC-EpreuveIntegree_2019-2020

docker-compose up
docker-compose down -v


docker-compose -f docker-compose.prod.yml down -v

docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear

#343a40
