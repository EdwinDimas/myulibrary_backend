from datetime import datetime, timezone
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from .models import Author, Book, Genre, Request, StatusDetail, Status
from .serializers import AuthorSerializer, BookSerializer, ChangeRequestStatusSerializer, GenreSerializer, RequestSerializer, RequestSerializerList, StatusDetailSerializer
from django.contrib.auth.hashers import make_password
import cloudinary.uploader
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.db.models import Prefetch, OuterRef, Subquery
from django.contrib.auth.decorators import user_passes_test



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_books(request):
    if request.method == "POST":
        name = request.POST.get("name")
        genre = request.POST.get("genre")
        author = request.POST.get("author")
        description = request.POST.get("description")
        published_year = request.POST.get("publishedYear")
        stock = request.POST.get("stock")
        image = request.FILES.get("image")

        if not all([name, genre, author, description, published_year, stock, image]):
            return Response({"error": "Missing fields", "fields": [name, genre, author, description, published_year, stock, image]}, status=400)

        upload_result = cloudinary.uploader.upload(image)
        image_url = upload_result.get("secure_url")

        if not image_url:
            return Response({"error": "Image upload failed"}, status=400)

        book = Book.objects.create(
            name=name,
            genre= Genre.objects.filter(id=genre).first(),
            author=Author.objects.filter(id=author).first(),
            description=description,
            published_year=int(published_year),
            stock=int(stock),
            url=image_url
        )

        return Response({"message": "Book registered successfully", "book_id": book.id})
    
    return Response({"error": "Invalid request"}, status=400)

@api_view(['GET'])
def list_books(request):
    books = Book.objects.filter(stock__gte= 1)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_genres(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_authors(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

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

    filters &= Q(stock__gte=1)

    books = Book.objects.filter(filters)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_book_stock(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    stock = request.data.get('stock')

    if stock is None or not isinstance(stock, int) or stock < 0:
        return Response({"error": "Invalid stock value"}, status=status.HTTP_400_BAD_REQUEST)

    book.stock = stock
    book.save()
    return Response({"message": "Stock updated successfully", "stock": book.stock})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_request(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data  

        new_request = Request.objects.create(
            user=request.user,
            book=data['book'],
            datetime=datetime.now()
        )

        book = Book.objects.get(id=data['book'].id)
        book.stock = book.stock - 1
        book.save()

        # Fetch the initial status (assuming it always has ID = 1 -> REQUESTED)
        initial_status = Status.objects.get(pk=1)

        StatusDetail.objects.create(
            request=new_request,
            status=initial_status,
            user=request.user,
            datetime=datetime.now()
        )

        return Response({"message": "Request created successfully"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_status_detail(request):
    serializer = StatusDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    firstName = request.data.get("firstName")
    lastName = request.data.get("lastName")
    password = request.data.get("password")
    email = request.data.get("email")
    role = request.data.get("role")

    if not email or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=email).exists():
        return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
    
    group = Group.objects.filter(id=role).first()

    user = User.objects.create(username=email, email=email, first_name=firstName, last_name=lastName, password=make_password(password))

    user.groups.add(group)

    user.save()

    return Response({"message": "User created successfully", "username": user.username}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_requests(request):
    latest_statusdetail_subquery = StatusDetail.objects.filter(
        request=OuterRef('pk'),
        status__in=[1, 3]
    ).order_by('-id')  

    requests = Request.objects.annotate(
        latest_statusdetail=Subquery(latest_statusdetail_subquery.values('status')[:1])
    )

    serializer = RequestSerializerList(requests, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_request_status(request):

    serializer = ChangeRequestStatusSerializer(data=request.data)
    if serializer.is_valid():
        request_id = serializer.validated_data['request_id']
        new_status = serializer.validated_data['new_status']

        try:
            request_obj = Request.objects.get(id=request_id)

            status_obj = Status.objects.get(id=new_status.id)
            StatusDetail.objects.create(
                request=request_obj,
                status=status_obj,
                user=request.user  
            )
       
            return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)

        except Request.DoesNotExist:
            return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)
        except Status.DoesNotExist:
            return Response({"error": "Invalid status code."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def mark_as_returned(request):
    request_id = request.data.get("request_id")

    try:
        book_request = Request.objects.get(pk=request_id)
        book = book_request.book
        book.stock += 1
        book.save()

        StatusDetail.objects.create(
            request=book_request,
            status=Status.objects.get(pk=4),  #returned value
            user=request.user 
        )

        return Response({"message": "Book marked as returned successfully"}, status=status.HTTP_200_OK)

    except Request.DoesNotExist:
        return Response({"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)