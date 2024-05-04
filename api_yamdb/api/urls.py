from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
