import MySQLdb
from django.core.management.base import BaseCommand, CommandError
from core.models import *
from django.db import connection
from django.apps import apps

class Command(BaseCommand):
    help = 'Transfer data from old database to'

    def add_arguments(self, parser):
        parser.add_argument('table', nargs='+', type=str)

    def handle(self, *args, **options):

        for table in options['table']:

            if table == 'districts' or table == 'provinces':
                db_name = 'static'
            else:
                db_name = 'cagaileo'

            conn = MySQLdb.connect(host="42.112.31.173",    # your host, usually localhost
                                   user="tieungao",         # your username
                                   passwd="tieungao123",  # your password
                                   db=db_name, charset='utf8mb4')        # name of the data base
            try:
                connection.cursor().execute("set FOREIGN_KEY_CHECKS = 0")
                connection.cursor().execute("TRUNCATE TABLE %s" % table)

                cursor = conn.cursor(MySQLdb.cursors.DictCursor)

                if table == 'product_tag':
                    cursor.execute("select * from %s" % table)
                    for row in cursor.fetchall():
                        connection.cursor().execute("insert into %s (product_id, tag_id)  VALUES(%s, %s)" % (table, row['product_id'], row['tag_id']))
                elif table == 'post_tag':
                    cursor.execute("select * from %s" % table)
                    for row in cursor.fetchall():
                        connection.cursor().execute("insert into %s (post_id, tag_id)  VALUES(%s, %s)" % (table, row['post_id'], row['tag_id']))
                elif table == 'modules':
                    cursor.execute("select * from %s" % table)
                    for row in cursor.fetchall():
                        obj, created = Module.objects.update_or_create(**{ 'name' : row['type'] })
                        model_name = next((m for m in apps.get_models() if m._meta.db_table==row['content']), None)
                        main_obj = model_name.objects.get(pk=row['value'])
                        main_obj.module.add(obj)
                        main_obj.save()
                else:
                    model_name = next((m for m in apps.get_models() if m._meta.db_table==table), None)
                    if model_name is not None:
                        cursor.execute("select * from %s" % table)
                        model_name.objects.bulk_create([model_name(**row) for row in cursor.fetchall()])

                connection.cursor().execute("set FOREIGN_KEY_CHECKS = 1")
            finally:
                conn.close()

            self.stdout.write(self.style.SUCCESS('Successfully imported "%s"' % table))