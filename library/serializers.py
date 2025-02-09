from rest_framework import serializers
from .models import Book, Request, StatusDetail, Status

class BookSerializer(serializers.ModelSerializer):
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
