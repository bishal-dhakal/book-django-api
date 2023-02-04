from django.shortcuts import render
from django.http import JsonResponse
from .models import Books
from .serializers import BooksSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['GET','POST'])
def books_list(request, format=None):
    if request.method =='GET':
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return JsonResponse({'Books':serializer.data})
    
    if request.method =='POST':
        serializer = BooksSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def books_detail(request,id,format=None):
    try:
        book= Books.objects.get(pk=id)
    except Books.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BooksSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BooksSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.Http_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)