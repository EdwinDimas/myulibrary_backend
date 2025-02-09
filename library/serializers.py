from rest_framework import serializers
from .models import Author, Book, Genre, Request, StatusDetail, Status


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=False, read_only=True)
    author = AuthorSerializer(many=False, read_only=True)
    class Meta:
        model = Book
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

class StatusDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusDetail
        fields = '__all__'
