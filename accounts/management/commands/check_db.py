"""Check database connection. Usage: python manage.py check_db"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Check that database connection succeeds'

    def handle(self, *args, **options):
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS('Database connection successful.'))
            with connection.cursor() as cursor:
                cursor.execute('SELECT sqlite_version();')
                version = cursor.fetchone()[0]
                self.stdout.write(f'SQLite version: {version}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database connection failed: {e}'))
