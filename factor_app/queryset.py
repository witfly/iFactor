import datetime
from django.utils.timezone import now
from django.db import connection
from django.db.models import Q
from django.db.models.query import QuerySet

class InvoiceQuerySet(QuerySet):
    def overdue(self):
        return self.unpaid() \
            .filter(date_due__lt=datetime.datetime.combine(now().date(), datetime.time.max)) \
            .exclude(type=self.model.InvoiceStatus.HELD_FOR_CREDIT)
    def lock(self):
        """ Lock table.
        Read more: https://www.postgresql.org/docs/9.4/static/sql-lock.html
        """
        cursor = connection.cursor()
        table = self.model._meta.db_table
        cursor.execute("LOCK TABLE %s" % table)


class ItemQuerySet(QuerySet):
    def with_tag(self, tag):
        return self.filter(tag=tag)