import csv
import sqlite3
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

DB_PATH = BASE_DIR.joinpath('db.sqlite3')
STATIC_DIR = BASE_DIR.joinpath('static', 'data')

USER_FILE = 'users.csv'
USER_PASSEWORD = 'qwerty1'

DATA_SOURCES = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}

# Маппинг заголовков в csv файлах и полей в таблицах.
DATA_MAPPING = {
    Title: {
        'id': 'id',
        'name': 'name',
        'year': 'year',
        'category': 'category_id',
        'description': 'description',
    },
    Category: {
        'id': 'id',
        'name': 'name',
        'slug': 'slug',
    },
    Genre: {'id': 'id', 'name': 'name', 'slug': 'slug'},
    GenreTitle: {'id': 'id', 'title_id': 'title_id', 'genre_id': 'genre_id'},
    Comment: {
        'id': 'id',
        'review_id': 'review_id',
        'text': 'text',
        'author': 'author_id',
        'pub_date': 'pub_date',
    },
    Review: {
        'id': 'id',
        'text': 'text',
        'title_id': 'title_id',
        'author': 'author_id',
        'score': 'score',
        'pub_date': 'pub_date',
    },
}


class Command(BaseCommand):
    help = 'Импорт данных.'

    def get_data(self, model_name, file_name):
        """Импорт данных для заданной модели из файла *.csv
        с полной очисткой таблицы"""

        file_path = STATIC_DIR.joinpath(file_name)
        mapping = DATA_MAPPING[model_name]
        parsed_data = []

        with open(file_path, encoding='utf8', mode='r') as f_n:

            null_fields = {}
            reader = csv.reader(f_n)
            headers = next(reader)

            # Заменяем заголовки столбцов в файле на имена столбцов в DB.
            mapped_fields = [mapping.get(item) for item in headers]
            table_name = model_name._meta.db_table

            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()

            # Очищаем таблицу
            sql_delete_string = f'DELETE FROM {table_name}'
            cursor.execute(sql_delete_string)

            # Получаем имена столбцов целевой таблицы
            column_list = cursor.execute(
                'PRAGMA table_info("' + table_name + '")'
            )
            column_list = [item[1] for item in column_list.fetchall()]

            # Поля, которые не заданы в файлах
            null_fields = {
                key: None for key in column_list if key not in mapped_fields
            }

            fields = ', '.join(f':{item}' for item in column_list)
            sql_insert_string = (
                f'INSERT INTO {table_name} VALUES ' f'({fields});'
            )
            for row in reader:
                row_result = {}

                # Приводим числовые значения к int.
                cleaned_row = [
                    int(item) if item.isnumeric() else item for item in row
                ]

                row_result = dict(zip(mapped_fields, cleaned_row))
                row_result.update(null_fields)
                parsed_data.append(row_result)

            cursor.executemany(sql_insert_string, parsed_data)
            connection.commit()
            connection.close()

    def create_users(self):
        model_name = User
        file_path = STATIC_DIR.joinpath(USER_FILE)

        model_name.objects.all().delete()
        with open(file_path, encoding='utf8', mode='r', newline='') as f_n:

            reader = csv.DictReader(f_n)
            for row in reader:
                User.objects.create_user(
                    id=row.get('id'),
                    username=row.get('username'),
                    email=row.get('email'),
                    password=USER_PASSEWORD,
                    role=row.get('role'),
                    bio=row.get('bio'),
                    first_name=row.get('first_name'),
                    last_name=row.get('last_name'),
                )

    def handle(self, *args, **kwargs):
        self.create_users()
        for key, value in DATA_SOURCES.items():
            self.get_data(key, value)
