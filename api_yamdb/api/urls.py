from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CategoryViewset, GenreViewSet, TitleViewSet


v1_router = DefaultRouter()

v1_router.register('categories', CategoryViewset, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(v1_router.urls))
]
