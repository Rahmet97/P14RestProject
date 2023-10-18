from .models import Blog, Hashtag
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BlogSerializer


@api_view(['GET'])
def hello(request):
    return Response({'message': 'Hello World!'})


class BlogAPIView(APIView):

    def get(self, request):
        blogs = Blog.objects.all().order_by('-created_at')
        blog_serializer = BlogSerializer(blogs, many=True)
        # blogs_data = []
        # for blog in blogs:
        #     blog_dict = {
        #         'ID': blog.id,
        #         'title': blog.title,
        #         'description': blog.description,
        #         'created_at': blog.created_at
        #     }
        #     blogs_data.append(blog_dict)
        return Response(blog_serializer.data)
