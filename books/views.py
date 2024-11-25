from lib2to3.fixes.fix_input import context

from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Book, Author, Order
from .serializers import BookSerializer,OrderSerializer, AuthorSerializers


@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True,context={'request':request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data, context={'request': request})
        author_id = request.data.get('author')
        print(author_id)
        author = get_object_or_404(Author, id=author_id)
        if serializer.is_valid():
            # author = get_object_or_404(Author, user=request.user)
            serializer.save(author=author,user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_create(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            return Response(OrderSerializer(order, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def author_detail(request, pk):
    book = get_object_or_404(Author, pk=pk)
    if request.method == 'GET':
        if book.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = AuthorSerializers(book, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if book.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        book.author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT', 'DELETE'])
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)


    if request.method == 'GET':
        serializer = AuthorSerializers(author, context={'request': request})
        return Response(serializer.data)


    # if request.method == 'PUT':
    #     if request.user != author.user:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     serializer = AuthorSerializers(author, data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #
    # if request.method == 'DELETE':
    #     if request.user != author.user:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     author.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
