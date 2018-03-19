import MySQLdb
from django.core.management.base import BaseCommand, CommandError
from core.models import *
from django.db import connection
from django.apps import apps


class Command(BaseCommand):

    content  = None
    help = 'Correct SLug'

    def saveContent(self):
        medicines = self.content.objects.all()
        for medicine in medicines:
            medicine.save()

    def handle(self, *args, **options):

        self.content = Medicine
        self.saveContent()
        self.content = Special
        self.saveContent()
        self.content = Drug
        self.saveContent()
        self.content = Disease
        self.saveContent()

        self.content = Post
        self.saveContent()

        self.content = Category
        self.saveContent()


        self.stdout.write(
            self.style.SUCCESS('Successfully imported!'))
