from django.db.models import Q
from rest_framework import generics, viewsets, status
from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Genre, Movie
from main.serializers import GenreSerializer, MovieSerializer
from .permissions import MoviePermissions

# @api_view(['GET'])
# def genres(request):
#     if request.method == 'GET':
#         genres = Genre.objects.all()
#         serializer = GenreSerializer(genres, many=True)
#         return Response(serializer.data)
#
#
# class MovieListView(APIView):
#     def get(self, request):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         movie = request.data.get('movie')
#         serializer = MovieSerializer(data=movie)
#         if serializer.is_valid(raise_exception=True):
#             movie_saved = serializer.save()
#         return Response({'message': 'safasfa'})


# class MovieView(generics.ListCreateAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#
#
# class MovieDetailView(generics.RetrieveAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#
#
# class MovieUpdateView(generics.UpdateAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#
#
# class MovieDeleteView(generics.DestroyAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer

class MyPaginationClass(PageNumberPagination):
    page_size = 4

    def get_paginated_response(self, data):
        for i in range(self.page_size):
            text = data[i]['description']
            data[i]['description'] = text[:65] + '...'
        return super().get_paginated_response(data)


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny, ]


class MoviesViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = MyPaginationClass

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [MoviePermissions, ]
        else:
            permissions = [IsAdminUser, ]
        return [permission() for permission in permissions]

    # @action(detail=False, methods=['get'])
    # def own(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(director=director)
    #

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(name__icontains=q) |
                                   Q(description__icontains=q))
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
