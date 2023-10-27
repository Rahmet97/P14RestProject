from rest_framework.serializers import Serializer, CharField, DateTimeField, IntegerField, ModelSerializer
from .models import Blog, Hashtag, Subscriber
from .tasks import send_email


class HashtagSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class BlogSerializer(ModelSerializer):
    hashtag = HashtagSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'


class BlogSerializerForPost(ModelSerializer):

    def create(self, validated_data):
        hashtags_data = validated_data.pop('hashtag')
        blog = Blog.objects.create(**validated_data)
        for hashtag_data in hashtags_data:
            hashtag, created = Hashtag.objects.get_or_create(name=hashtag_data.name)
            blog.hashtag.add(hashtag)
        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            send_email.delay(subscriber.email, validated_data['title'], validated_data['description'])
        return blog

    class Meta:
        model = Blog
        fields = '__all__'


class SubscriberSerializer(ModelSerializer):

    class Meta:
        model = Subscriber
        fields = '__all__'
