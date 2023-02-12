from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from .models import Blog



class PublicBlog(APIView):

### GET function to view the blog (without being authenticated)

   def get(self, request):
      try:

### to get the random blogs om page with every refresh

         blogs = Blog.objects.all().order_by('?')

### Pagination of following app:
  
         page_number = request.GET.get('page', '1')
         paginator = Paginator(blogs, 10)

         serializer = BlogSerializers(paginator.page(page_number), many=True)

         return Response({
            'data':serializer.data,
            'message': 'blog fetched sucessfully'
         }, status=status.HTTP_201_CREATED)
      
      except Exception as e:
         print(e)

         return Response({
               'data' : {},
               'messeage': 'something went wrong'
         }, status=status.HTTP_400_BAD_REQUEST)


class BlogView(APIView):
   permission_classes = [IsAuthenticated]
   authentication_classes = [JWTAuthentication]


### GET function to view the blog!!

   def get(self, request):
      try:
         blogs = Blog.objects.filter(user=request.user)

         serializer = BlogSerializers(blogs, many=True)

         return Response({
            'data':serializer.data,
            'message': 'blog fetched sucessfully'
         }, status=status.HTTP_201_CREATED)
      
      except Exception as e:
         print(e)

         return Response({
               'data' : {},
               'messeage': 'something went wrong or invalid page'
         }, status=status.HTTP_400_BAD_REQUEST)


### POST function to create the blog!!

   def post(self, request):
      try:
         data=request.data
         data["user"] = request.user.id

         serializer = BlogSerializers(data=data)

         if not serializer.is_valid():
            return Response({
               'data' : serializer.errors,
               'messeage': 'something went wrong'
         }, status=status.HTTP_400_BAD_REQUEST)
         serializer.save()

         return Response({
            'data':serializer.data,
            'message': 'blog created sucessfully'
         }, status=status.HTTP_201_CREATED)

      except Exception as e:
         print(e)
         return Response({
               'data' : {},
               'messeage': 'something went wrong'
         }, status=status.HTTP_400_BAD_REQUEST)


### PATCH function to perform edit in blog!!!

   def patch(self, request):
      try:
         data = request.data
         
         blog = Blog.objects.filter(uid=data.get('uid'))

         if not blog.exists():
            return Response({
               'data':{},
               'message': 'invalid blog uid'
         }, status=status.HTTP_400_BAD_REQUEST)

         if request.user != blog[0].user:
            return Response({
            'data': {},
            'message': 'you are not authorized to do this'
         }, status=status.HTTP_400_BAD_REQUEST)

         serializer = BlogSerializers(blog[0], data =data, partial=True)

         if not serializer.is_valid():
            return Response({
               'data' : serializer.errors,
               'messeage': 'something went wrong'
         }, status=status.HTTP_400_BAD_REQUEST)
         serializer.save()

         return Response({
            'data':serializer.data,
            'message': 'blog updated sucessfully'
         }, status=status.HTTP_201_CREATED)

      except Exception as e:
         print(e)
         return Response({
               'data' : {},
               'messeage': 'something went wrong'
         }, status=status.HTTP_400_BAD_REQUEST)


### DELETE function to perform delete in blog!!!

   def delete(self, request):
         try:
            data = request.data
            
            blog = Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
               return Response({
                  'data':{},
                  'message': 'invalid blog uid'
            }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
               return Response({
               'data': {},
               'message': 'you are not authorized to do this'
            }, status=status.HTTP_400_BAD_REQUEST)

            blog[0].delete()

            return Response({
               'data':{},
               'message': 'blog deleted sucessfully'
            }, status=status.HTTP_201_CREATED)

         
         except Exception as e:
            print(e)
            return Response({
                  'data' : {},
                  'messeage': 'something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
         

         