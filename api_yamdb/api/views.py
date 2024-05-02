from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from api.serializers import ReviewSerializer
from reviews.models import Title


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title())  # , author=self.request.user)
