from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Book, Request, StatusDetail, Status
from .serializers import BookSerializer, RequestSerializer, StatusDetailSerializer
from django.contrib.auth.hashers import make_password

# Crear uno o más libros
@api_view(['POST'])
def create_books(request):
    if isinstance(request.data, list):  # Si se envía una lista de libros
        serializer = BookSerializer(data=request.data, many=True)
    else:
        serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Listar todos los libros
@api_view(['GET'])
def list_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

# Buscar libros por nombre, género y/o autor
@api_view(['GET'])
def find_books(request):
    name = request.GET.get('name', "").strip()
    genre = request.GET.getlist('genre', None)
    author = request.GET.getlist('author', None)

    filters = Q()
    if name:
        filters &= Q(name__icontains=name)
    if genre:
        filters &= Q(genre__in=genre)
    if author:
        filters &= Q(author__in=author)

    books = Book.objects.filter(filters)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

# Actualizar el stock de un libro
@api_view(['PATCH'])
def update_book_stock(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    stock = request.data.get('stock')

    if stock is None or not isinstance(stock, int) or stock < 0:
        return Response({"error": "Invalid stock value"}, status=status.HTTP_400_BAD_REQUEST)

    book.stock = stock
    book.save()
    return Response({"message": "Stock updated successfully", "stock": book.stock})

# Crear una solicitud de libro
@api_view(['POST'])
def make_request(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Crear un detalle de estado para una solicitud
@api_view(['POST'])
def create_status_detail(request):
    serializer = StatusDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Crear un nuevo usuario
@api_view(['POST'])
def create_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(username=username, email=email, password=make_password(password))
    return Response({"message": "User created successfully", "username": user.username}, status=status.HTTP_201_CREATED)
