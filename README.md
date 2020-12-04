<!--
https://readme42.com
-->


[![](https://img.shields.io/pypi/v/django-postgres-refresh-matviews.svg?maxAge=3600)](https://pypi.org/project/django-postgres-refresh-matviews/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![](https://github.com/andrewp-as-is/django-postgres-refresh-matviews.py/workflows/tests42/badge.svg)](https://github.com/andrewp-as-is/django-postgres-refresh-matviews.py/actions)

### Installation
```bash
$ [sudo] pip install django-postgres-refresh-matviews
```

#### How it works
1. `refresh_pg_matviews` - refresh all `pg_matviews` matviews
2. `refresh_pending_matviews` - refresh `Matview` model matviews:
    +   `repeat_seconds` - seconds interval to refresh matview
    +   `is_pending` - set `True` to force refresh

##### `settings.py`
```python
INSTALLED_APPS+=['django_postgres_refresh_matviews']
```

##### migrate
```bash
$ python manage.py migrate
```

#### Examples
```python
from django_postgres_refresh_matviews.utils import refresh_pg_matviews

refresh_pg_matviews()
```

```python
from django_postgres_refresh_matviews.models import Matview
from django_postgres_refresh_matviews.utils import refresh_pending_matviews

Matview.objects.get_or_create(schemaname='public',matviewname='matview1')

refresh_pending_matviews()

Matview.objects.filter(schemaname='public').update(is_pending=False)
```

Log
```python
from django_postgres_refresh_matviews.models import Log

for l in Log.objects.filter(schemaname='public',matviewname='matview1'):
    l.started_at, l.completed_at
```

cli
```bash
$ python manage.py clear_matviews   # clear matviews
$ python manage.py init_matviews    # init postgres matviews
$ python manage.py refresh_pg_matviews # refresh pg_matviews
$ python manage.py refresh_pending_matviews # refresh pending Matview matviews
```

raw sql
```sql
INSERT INTO refresh_matview(schemaname,matviewname)
SELECT schemaname,matviewname
FROM pg_matviews
ON CONFLICT (schemaname,matviewname) DO NOTHING;

UPDATE refresh_matview SET is_pending=true
WHERE schemaname='public' AND matviewname='matview1';
```

<p align="center">
    <a href="https://readme42.com/">readme42.com</a>
</p>
