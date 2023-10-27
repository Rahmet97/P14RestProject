from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdminPermission
from .models import Blog, Hashtag
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, GenericAPIView

from .serializers import BlogSerializer, BlogSerializerForPost, SubscriberSerializer


@api_view(['GET'])
def hello(request):
    return Response({'message': 'Hello World!'})


# class BlogAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         blogs = Blog.objects.all().order_by('-created_at')
#         blog_serializer = BlogSerializer(blogs, many=True)
#         return Response(blog_serializer.data)
#
#
# class AddBlogAPIView(APIView):
#     permission_classes = (IsAdminPermission,)
#
#     def post(self, request):
#         request.data._mutable = True
#         data = request.data
#         data['user_id'] = request.user.id
#         blog_serializer = BlogSerializerForPost(data=data)
#         blog_serializer.is_valid(raise_exception=True)
#         blog_serializer.save()
#         return Response(blog_serializer.data)


# class UpdateDestroyAPIView(APIView):
#     permission_classes = (IsAdminPermission,)
#
#     def get_object(self, pk):
#         return Blog.objects.get(pk=pk)
#
#     def put(self, request, pk):
#         try:
#             blog = self.get_object(pk)
#             data = BlogSerializerForPost(blog, data=request.data)
#             data.is_valid(raise_exception=True)
#             data.save()
#         except Exception as e:
#             return Response({'success': False, 'message': e}, status=400)
#         return Response({'success': True})
#
#     def patch(self, request, pk):
#         try:
#             blog = self.get_object(pk)
#             data = BlogSerializerForPost(blog, data=request.data, partial=True)
#             data.is_valid(raise_exception=True)
#             data.save()
#         except Exception as e:
#             return Response({'success': False, 'message': e}, status=400)
#         return Response({'success': True})
#
#     def delete(self, request, pk):
#         self.get_object(pk).delete()
#         return Response(status=204)
class UpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializerForPost
    permission_classes = (IsAdminPermission,)


class AddBlogAPIView(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializerForPost
    permission_classes = (IsAdminPermission,)


class BlogAPIView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)


class SubscriberAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = SubscriberSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
