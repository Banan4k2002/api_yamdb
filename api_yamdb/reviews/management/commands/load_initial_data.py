import csv
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

DB_PATH = BASE_DIR.joinpath('db.sqlite3')
STATIC_DIR = BASE_DIR.joinpath('static', 'data')

USER_FILE = 'users.csv'
DEFAULT_USER_PASSWORD = 'qwerty1'

DATA_SOURCES = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}

GENRE_TITLE_FILE = 'genre_title.csv'

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
                    password=DEFAULT_USER_PASSWORD,
                    role=row.get('role'),
                    bio=row.get('bio'),
                    first_name=row.get('first_name'),
                    last_name=row.get('last_name'),
                )

    def genre_title_matching(self):
        title_id = 'title_id'
        genre_id = 'genre_id'

        file_path = STATIC_DIR.joinpath(GENRE_TITLE_FILE)
        with open(file_path, encoding='utf8', mode='r') as f_n:
            reader = csv.DictReader(f_n)

            for row in reader:
                title = Title.objects.get(pk=row.get(title_id))
                genre = Genre.objects.get(pk=row.get(genre_id))
                title.genre.add(genre)

    def handle(self, *args, **kwargs):
        self.create_users()
        for model, file_name in DATA_SOURCES.items():

            file_path = STATIC_DIR.joinpath(file_name)
            with open(file_path, encoding='utf8', mode='r') as f_n:

                headers_str = f_n.readline().rstrip('\n')
                headers_list = headers_str.split(',')
                field_names = [DATA_MAPPING[model][item]
                               for item in headers_list]

                reader = csv.DictReader(f_n, fieldnames=field_names)
                model.objects.all().delete()
                data = [model(**row) for row in reader]

                model.objects.bulk_create(data)

        self.genre_title_matching()
        self.genre_title_matching()
