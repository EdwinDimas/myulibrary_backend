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
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Request
        fields = ['book']


class StatusDetailSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()  # Show the status as a string
    user = serializers.StringRelatedField()  # Show the user who updated the status

    class Meta:
        model = StatusDetail
        fields = ('status', 'user', 'datetime')


class RequestSerializerList(serializers.ModelSerializer):
    book = serializers.StringRelatedField()  # Display book title (or any field)
    status_details = StatusDetailSerializer(many=True, source='statusdetail_set')  # Use the correct reverse relation

    class Meta:
        model = Request
        fields = '__all__'

class ChangeRequestStatusSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()
    new_status = serializers.IntegerField()

    def validate_new_status(self, value):
        try:
            status = Status.objects.get(id=value)
        except Status.DoesNotExist:
            raise serializers.ValidationError("Invalid status code.")
        return status