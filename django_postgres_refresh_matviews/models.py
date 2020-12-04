from datetime import datetime, timedelta

from django.db import connection, models


class Matview(models.Model):
    schemaname = models.TextField(default='public')
    matviewname = models.TextField()
    is_disabled = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    repeat_seconds = models.IntegerField(null=True)
    started_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'refresh_matview'
        indexes = [
            models.Index(fields=["is_disabled"],),
            models.Index(fields=["is_pending"],),
            models.Index(fields=["is_running"],),
            models.Index(fields=["-priority"],),
        ]
        unique_together = ['schemaname', 'matviewname']

    def refresh(self):
        cursor = connection.cursor()
        sql = 'REFRESH MATERIALIZED VIEW "%s"."%s";' % (
            self.schemaname, self.matviewname)
        started_at = datetime.now()
        type(self).objects.filter(pk=self.pk).update(
            started_at=started_at,
            is_running=True
        )
        log = Log.objects.create(
            schemaname=self.schemaname,
            matviewname=self.matviewname
        )
        cursor.execute(sql)
        completed_at = datetime.now()
        type(self).objects.filter(pk=self.pk).update(
            completed_at=completed_at,
            is_pending=False,
            is_running=False
        )
        Log.objects.filter(pk=log.pk).update(completed_at=completed_at)

    @property
    def expired_at(self):
        if not self.repeat_seconds or self.repeat_seconds <= 0:
            return
        if self.completed_at:
            return self.completed_at + timedelta(seconds=self.repeat_seconds)
        return datetime.now()


class Log(models.Model):
    schemaname = models.TextField(default='public')
    matviewname = models.TextField()
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'refresh_matview_log'
        indexes = [
            models.Index(fields=["schemaname", "matviewname"],),
            models.Index(fields=["-completed_at"],),
        ]
