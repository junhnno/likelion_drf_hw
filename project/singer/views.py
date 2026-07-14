from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Singer, Song, Tag
from .serializers import SingerSerializer, SongSerializers

from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
def singer_list_create(request):
    if request.method == 'GET':
        singers = Singer.objects.all()
        serializer =  SingerSerializer(singers, many = True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = SingerSerializer(data=request.data)  # 1. Json -> 파이썬 dict
        if serializer.is_valid(raise_exception=True):     # 2. 필드 타입에 맞는 지 검증(name, content, debut)
            singer = serializer.save()                    # 3. 실제 DB에 저장
            # 여기서 왜 {singer =}이 필요한가?
            # serializer.save()만 작성해도 DB에는 잘 저장됨
            # 하지만 밑에서 [방금 저장한 객체 바로 그거!] 를 사용하기 위해 {singer =}로 저장 

            content = request.data['content']
            tags = [word[1:] for word in content.split(' ') if word.startswith('#')]
            for t in tags:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                singer.tags.add(tag)
                # tags = models.ManyToManyField(Tag, blank=True) 을 통해 M2M table이 이미 만들어져있음
                # singer.tags : 둘의 M2M 테이블에 접근
                # add() : Django ORM의 메서드 -> 테이블에 row 추가

            singer.save()
            return Response(data=SingerSerializer(singer).data)
        
@api_view(['GET', 'PATCH', "DELETE"])
def singer_detail_update_delete(request, singer_id):
    singer = get_object_or_404(Singer, id=singer_id)

    if request.method == 'GET':
        serializer = SingerSerializer(singer)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = SingerSerializer(instance=singer, data=request.data)
        if serializer.is_valid():
            singer = serializer.save()

            singer.tags.clear()
            content = request.data.get("content")
            tags = [word[1:] for word in content.split(' ') if word.startswith('#')]
            for t in tags:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                singer.tags.add(tag)

            singer.save()
            return Response(data=SingerSerializer(singer).data)
        
    
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
    
@api_view(['GET'])
def find_tag(request, tags_name):
    tags = get_object_or_404(Tag, name=tags_name)

    if request.method == 'GET':
        singers = Singer.objects.filter(tags__in=[tags])   # ORM의 필드명__룩업이름 
        serializer = SingerSerializer(singers, many=True)
        return Response(data=serializer.data)

