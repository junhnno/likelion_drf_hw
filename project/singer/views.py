from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Singer, Song
from .serializers import SingerSerializer, SongSerializers

from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
def singer_list_create(request):
    if request.method == 'GET':
        singers = Singer.objects.all()
        serializer =  SingerSerializer(singers, many = True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = SingerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
@api_view(['GET', 'PATCH', "DELETE"])
def singer_detail_update_delete(request, singer_id):
    singer = get_object_or_404(Singer, id=singer_id)

    if request.method == 'GET':
        serializer = SingerSerializer(singer)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = SingerSerializer(instance=singer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        singer.delete()
        data = {
            'deleted_singer':singer_id
        }
        return Response(data)

@api_view(['GET', 'POST'])
def song_read_create(request, singer_id):
    singer = get_object_or_404(Singer, id=singer_id)

    if request.method == 'GET':
        songs = Song.objects.filter(singer=singer)
        serializer = SongSerializers(songs, many=True)
        return Response(data=serializer.data)
    
    if request.method == 'POST':
        serializer = SongSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(singer=singer)
        return Response(serializer.data)   

