from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdminPermission
from .models import Blog, Hashtag
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BlogSerializer, BlogSerializerForPost


@api_view(['GET'])
def hello(request):
    return Response({'message': 'Hello World!'})


class BlogAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        blogs = Blog.objects.all().order_by('-created_at')
        blog_serializer = BlogSerializer(blogs, many=True)
        return Response(blog_serializer.data)


class AddBlogAPIView(APIView):
    permission_classes = (IsAdminPermission,)

    def post(self, request):
        request.data._mutable = True
        data = request.data
        data['user_id'] = request.user.id
        blog_serializer = BlogSerializerForPost(data=data)
        blog_serializer.is_valid(raise_exception=True)
        blog_serializer.save()
        return Response(blog_serializer.data)
