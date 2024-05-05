from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import get_jwt_token, ReviewViewSet, UserViewSet, signup


v1_router = DefaultRouter()

v1_router.register(r'users', UserViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_jwt_token, name='token'),
]
