﻿# API YaMDb
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нет возможности посмотреть фильм или послушать музыку.
Произведения делятся на категории, cписок которых может быть расширен. Произведению может быть присвоен жанр из списка предустановленных. 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам. Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Запуск проекта:
### 1. Клонируйте репозиторий:
- `git clone https://github.com/Banan4k2002/api_yamdb.git`
### 2. Cоздайте и активируйте виртуальное окружение:
Windows:
- `python -m venv env`
- `source venv/Scripts/activate`

Linux/Mac:
- `python3 -m venv venv`
- `source venv/bin/activate`

### 3. Установите зависимости:
`pip install -r requirements.txt`

### 4. Примените миграции:

`python manage.py migrate`

### 5. Запустите YaMDb:
`python manage.py runserver`

## Самостоятельная регистрация новых пользователей:
1. Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт `/api/v1/auth/signup/`.
Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.

2. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит JWT-токен.В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
3. После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле.

## Пользовательские роли и права доступа
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры, назначать роли пользователям.
- Суперпользователь Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперпользователя — это не лишит его прав администратора.

## Ресурсы API YaMDb
- auth: аутентификация.
- users: пользователи.
- titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
- genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

## Примеры запросов:
- Создание аккаунта:
http://127.0.0.1:8000/api/v1/auth/signup/ 

- Изменение данных своей учетной записи: http://127.0.0.1:8000/api/v1/users/me/


- Поиск по названию категории:
http://127.0.0.1:8000/api/v1/categories/

- Cписок всех отзывов:
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

- Cписок всех объектов:
http://127.0.0.1:8000/api/v1/titles/

## Документация:
http://127.0.0.1:8000/redoc/

## Использованные технологии:
- Python 3.9
- Django Rest Framework 3.12.4
- JWT Simple token
- SQLite3


## Над проектом работали:
- Алексей - https://github.com/Banan4k2002
- Виктор - https://github.com/texikator
- Анастасия - https://github.com/addamsus
