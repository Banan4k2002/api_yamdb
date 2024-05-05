from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin)

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from reviews.constants import NAME_MAX_LENGTH, SLUG_MAX_LENGTH
from reviews.models import Category, Genre, Review,Title
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (AdminPermission)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    RegistrationSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleCreteUpdateSerializer,
    TokenSerializer,
    UserSerializer,
)

User =  get_user_model()


class DictViewMixin(CreateModelMixin,
                    DestroyModelMixin,
                    ListModelMixin,
                    GenericViewSet):
    """Михин для жанров и категорий"""
    pass


class CategoryViewset(DictViewMixin):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(DictViewMixin):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.all()
    filter_backends = (SearchFilter,)
    # serializer_class = TitleSerializer
    search_fields = ('name', 'year', 'description',
                     'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreteUpdateSerializer
        return TitleSerializer

    def handle_create_update(self, serializer):
        """Обработка сохранения данных с переключением сериализатора."""
        if serializer.is_valid():

            obj = serializer.save()
            serializer = TitleSerializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        return self.handle_create_update(serializer)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        return self.handle_create_update(serializer)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup(request):
    if not User.objects.filter(username=request.data.get('username', None),
                               email=request.data.get('email', None)).first():
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    user = get_object_or_404(
        User,
        username=request.data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="Registration",
        message=f"Verification code: {confirmation_code}",
        from_email=None,
        recipient_list=[user.email],
    )
    return Response(data=request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )

    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    # pagination_class = PageNumberPagination

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    @action(
        methods=[
            'post',
        ],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, AdminPermission],
    )
    def create_user(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=[
            'delete',
        ],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def delete_user(self, request):
        user = request.user
        if request.method == "DELETE":
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=[
            'post',
            'get',
            'patch',
        ],
        detail=False,

        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            if 'role' not in request.data:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "POST":
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        search_term = request.query_params.get('search')
        if search_term:
            queryset = queryset.filter(username__icontains=search_term)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data})


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title())  # , author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review())  # , author=self.request.user)
