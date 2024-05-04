from rest_framework.serializers import ModelSerializer

from reviews.models import Comment, Review


class ReviewSerializer(ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('id', 'author', 'pub_date')
