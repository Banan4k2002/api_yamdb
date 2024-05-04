from rest_framework.serializers import ModelSerializer

from reviews.models import Review


class ReviewSerializer(ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('id', 'author', 'pub_date')
