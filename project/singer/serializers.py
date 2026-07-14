from rest_framework import serializers
from .models import *

class SingerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True) # 사실 상 무의미한 코드
    songs = serializers.SerializerMethodField(read_only=True) 
    # songs는 역참조 관계라 fields = '__all__'로는 아예 노출되지 않음
    # → 명시적으로 필드를 선언해서 중첩된 노래 정보를 내려줌
    tags = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(use_url=True, required=False)

    def get_songs(self, instance):
        serializer = SongSerializers(instance.songs, many=True)
        return serializer.data
    
    def get_tags(self, instance):
        tags = instance.tags.all()
        return [tag.name for tag in tags]

    class Meta:
        model = Singer
        fields = ['id', 'name', 'content', 'debut','songs', 'tags', 'image']

class SongSerializers(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
        read_only_fields = ['singer']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
