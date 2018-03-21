import MySQLdb
from django.core.management.base import BaseCommand, CommandError
from taggit.models import Tag

from core.models import *
from django.db import connection
from django.apps import apps


class Command(BaseCommand):
    help = 'Transfer data from old database to'

    def save_post(self, cursor):
        # fill to ban-tin-duoc-lieu
        category1 = Category.objects.filter(slug__exact='ban-tin-duoc-lieu').first()
        # fill to thong-tin-khoa-hoc
        category2 = Category.objects.filter(slug__exact='thong-tin-khoa-hoc').first()
        Post.objects.filter(category__in=[category1, category2]).delete()

        cursor.execute("select * from posts where category_id in (select id from categories where parent_id=4 )")
        rows = cursor.fetchall()
        for row in rows:
            post1 = Post.objects.create(
                name=row['title'],
                slug=row['slug'],
                desc=row['desc'],
                seo_name=row['seo_title'],
                seo_desc=row['desc'],
                content=row['content'],
                views=row['views'],
                category=category1,
                image=row['image']
            )
            # tags
            cursor.execute(
                "select t3.* from posts t1 left join post_tag t2 on t1.id=t2.post_id left join tags t3 on t2.tag_id=t3.id where t1.id=%s" %
                row['id'])
            for tag in cursor.fetchall():
                post1.tags.add(str(tag['title']))
            post1.save()

        cursor.execute("select * from posts where category_id in (select id from categories where parent_id=9)")
        rows = cursor.fetchall()
        for row in rows:
            post2 = Post.objects.create(
                name=row['title'],
                slug=row['slug'],
                desc=row['desc'],
                seo_name=row['seo_title'],
                seo_desc=row['desc'],
                content=row['content'],
                views=row['views'],
                category=category2,
                image=row['image']
            )
            # tags
            cursor.execute(
                "select t3.* from posts t1 left join post_tag t2 on t1.id=t2.post_id left join tags t3 on t2.tag_id=t3.id where t1.id=%s" %
                row['id'])
            for tag in cursor.fetchall():
                post2.tags.add(str(tag['title']))

            post2.save()

    def save_special(self, cursor):
        category = Category.objects.filter(slug__exact='tra-cuu-danh-luc').first()
        if category:
            cursor.execute("select * from posts where category_id=13")
            rows = cursor.fetchall()
            for row in rows:
                special_medicine = Post.objects.create(
                    name=row['title'],
                    slug=row['slug'],
                    s_name=row['s_name'],
                    desc=row['desc'],
                    seo_name=row['seo_title'],
                    category=category,
                    seo_desc=row['desc'],
                    content=row['content'],
                    views=row['views'],
                    image=row['image']
                )

                # tags
                cursor.execute(
                    "select t3.* from posts t1 left join post_tag t2 on t1.id=t2.post_id left join tags t3 on t2.tag_id=t3.id where t1.id=%s" %
                    row['id'])
                for tag in cursor.fetchall():
                    special_medicine.tags.add(str(tag['title']))

                special_medicine.save()

    def save_medicine(self, cursor):
        category = Category.objects.filter(slug__exact='tra-cuu-duoc-lieu').first()

        if category:
            cursor.execute("select * from posts where category_id=2")
            rows = cursor.fetchall()
            for row in rows:
                medicine = Post.objects.create(
                    name=row['title'],
                    slug=row['slug'],
                    s_name=row['s_name'],
                    desc=row['desc'],
                    category=category,
                    seo_name=row['seo_title'],
                    seo_desc=row['desc'],
                    content=row['content'],
                    views=row['views'],
                    image=row['image']
                )

                # tags
                cursor.execute(
                    "select t3.* from posts t1 left join post_tag t2 on t1.id=t2.post_id left join tags t3 on t2.tag_id=t3.id where t1.id=%s" %
                    row['id'])
                for tag in cursor.fetchall():
                    medicine.tags.add(str(tag['title']))

                medicine.save()

    def save_disease(self, cursor):
        category = Category.objects.filter(slug__exact='tra-cuu-theo-benh').first()

        if category:
            cursor.execute("select * from posts where category_id=3")
            rows = cursor.fetchall()
            for row in rows:
                disease = Post.objects.create(
                    name=row['title'],
                    slug=row['slug'],
                    s_name=row['s_name'],
                    category=category,
                    desc=row['desc'],
                    seo_name=row['seo_title'],
                    seo_desc=row['desc'],
                    content=row['content'],
                    views=row['views'],
                    image=row['image']
                )

                # tags
                cursor.execute(
                    "select t3.* from posts t1 left join post_tag t2 on t1.id=t2.post_id left join tags t3 on t2.tag_id=t3.id where t1.id=%s" %
                    row['id'])
                for tag in cursor.fetchall():
                    disease.tags.add(str(tag['title']))

                disease.save()

    def save_drug(self, cursor):

        category = Category.objects.filter(slug__exact='tra-cuu-bai-thuoc').first()

        if category:
            cursor.execute("select * from posts where category_id=14")
            rows = cursor.fetchall()
            for row in rows:
                drug = Post.objects.create(
                    name=row['title'],
                    slug=row['slug'],
                    s_name=row['s_name'],
                    desc=row['desc'],
                    category=category,
                    seo_name=row['seo_title'],
                    seo_desc=row['desc'],
                    content=row['content'],
                    views=row['views'],
                    image=row['image']
                )

                # tags
                cursor.execute(
                    "select t3.* from posts t1 left join post_tag t2 on t1.id=t2.post_id left join tags t3 on t2.tag_id=t3.id where t1.id=%s" %
                    row['id'])
                for tag in cursor.fetchall():
                    drug.tags.add(str(tag['title']))

                drug.save()

    def handle(self, *args, **options):

        conn = MySQLdb.connect(host="42.112.31.173",  # your host, usually localhost
                               user="tieungao",  # your username
                               passwd="tieungao123",  # your password
                               db="duoclieu", charset='utf8mb4')  # name of the data base



        Post.objects.all().delete()
        Tag.objects.all().delete()
        SiteSlug.objects.all().delete()

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        self.save_post(cursor)
        self.save_medicine(cursor)
        self.save_special(cursor)
        self.save_drug(cursor)
        self.save_disease(cursor)

        self.stdout.write(
            self.style.SUCCESS('Successfully imported !'))
