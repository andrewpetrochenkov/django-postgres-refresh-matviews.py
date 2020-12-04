from datetime import datetime
from django.db import connection

from .models import Matview, Log

SQL = """
SELECT format('%s.%s',schemaname,matviewname)
FROM pg_matviews
ORDER BY format('%s.%s',schemaname,matviewname)
"""


def get_pg_matviews():
    cursor = connection.cursor()
    cursor.execute(SQL)
    return list(map(lambda r: r[0], cursor.fetchall()))


def refresh_pg_matviews():
    cursor = connection.cursor()
    full_names = get_pg_matviews()
    for full_name in full_names:
        schemaname, matviewname = full_name.split('.')
        sql = 'REFRESH MATERIALIZED VIEW "%s"."%s";' % (
            schemaname, matviewname)
        log = Log.objects.create(
            schemaname=schemaname,
            matviewname=matviewname
        )
        cursor.execute(sql)
        Log.objects.filter(pk=log.pk).update(completed_at=datetime.now())


def init_matviews():
    full_names = get_pg_matviews()
    for full_name in full_names:
        schemaname, matviewname = full_name.split('.')
        Matview.objects.get_or_create(
            schemaname=schemaname, matviewname=matviewname)
    for m in Matview.objects.all():
        full_name = '%s.%s' % (m.schemaname, m.matviewname)
        if full_name not in full_names:
            m.delete()


def refresh_pending_matviews():
    for m in Matview.objects.exclude(is_disabled=True).order_by('-priority'):
        if m.is_pending or not m.completed_at or datetime.now() >= m.expired_at:
            m.refresh()
