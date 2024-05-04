from django.contrib import admin

from reviews.models import Category, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'score', 'author', 'title', 'pub_date')
