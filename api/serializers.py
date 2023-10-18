from rest_framework.serializers import Serializer, CharField, DateTimeField, IntegerField, ModelSerializer
from .models import Blog, Hashtag


class HashtagSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class BlogSerializer(ModelSerializer):
    hashtag = HashtagSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'
        # exclude = ('hashtag',)
