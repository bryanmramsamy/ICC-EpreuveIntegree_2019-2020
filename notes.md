# Notes

## Date

```python
import datetime


datetime.date.today()
# datetime.date(2020, 7, 14)
```

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
