import csv
from pathlib import Path
import sqlite3

from django.core.management.base import BaseCommand

from titles.models import Category, Genre, GenreTitle, Title

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

DB_PATH = BASE_DIR.joinpath('db.sqlite3')
STATIC_DIR = BASE_DIR.joinpath('static').joinpath('data')

DATA_SOURCES = {

    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    # Users: 'users.csv',
    # Review: 'review.csv',
    # Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Импорт данных.'

    def get_data(self, model_name, file_name):
        """Импорт данных для заданной модели из файла *.csv
         с полной очисткой таблицы"""

        file_path = STATIC_DIR.joinpath(file_name)
        parsed_data = []   

        with open(file_path, encoding='utf8', mode='r') as f_n:
            
            reader = csv.reader(f_n)
            headers = next(reader)
            table_name = model_name._meta.db_table

            sql_delete_string = f'DELETE FROM {table_name}'

            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()

            cursor.execute(sql_delete_string) 

            fields_placeholder = ', '.join(('?' for i in range(len(headers))))
            sql_insert_string = (f'INSERT INTO {table_name} VALUES '
                                 f'({fields_placeholder});')
            
            for row in reader:
                cleaned_row = tuple(int(item) if item.isnumeric()
                                    else item for item in row)
                parsed_data.append(cleaned_row)

            cursor.executemany(sql_insert_string, parsed_data)
            connection.commit()
            connection.close()

    def handle(self, *args, **kwargs):
        for key, value in DATA_SOURCES.items():
            self.get_data(key, value)


    
