from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    year = NumberFilter(field_name='year')
    description = CharFilter(field_name='description')

    class Meta:
        model = Title
        fields = [
            'genre__slug',
            'name',
            'year',
            'description',
            'category__slug',
        ]
