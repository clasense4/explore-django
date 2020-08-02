from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from photos.models import Photo
from photos.serializers import PhotoSerializer
from rest_framework import permissions
from photos.permissions import IsOwner
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone


class PhotoList(APIView):
    """
    List all photos, or create a new photo.
    """
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner
    ]

    def get(self, request, format=None):
        # Filter by query params | ?status=p
        photo_status = request.query_params.get('status', None)
        if photo_status:
            photos = Photo.objects.filter(user=request.user.id, status=photo_status)
        else:
            photos = Photo.objects.filter(user=request.user.id)

        # Filter by query params | ?sort=asc/desc
        allowed_sort = ['asc', 'desc']
        sort = request.query_params.get('sort', None)
        if sort in allowed_sort:
            column = 'published_at' if sort == 'asc' else '-published_at'
            photos = photos.order_by(column)

        photo_serializer = PhotoSerializer(photos, many=True, context={'request': request})
        return Response(photo_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        photo_serializer = PhotoSerializer(data=request.data, context={'request': request})

        if photo_serializer.is_valid():
            # Add published_at if status=p
            if request.data['status'] == 'p':
                photo_serializer.save(
                    user=self.request.user, published_at=timezone.now()
                )
            else:
                photo_serializer.save(user=self.request.user)
            return Response(photo_serializer.data, status=status.HTTP_201_CREATED)
        return Response(photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoDetail(APIView):
    """
    Retrieve, update or delete a photo instance.
    """
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner
    ]

    def get_object(self, pk):
        try:
            obj = get_object_or_404(Photo, pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Photo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            # Only allow update captions and status from draft to publish
            if 'captions' in request.data:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif 'status' in request.data:
                if request.data['status'] == 'p':
                    serializer.save(published_at=timezone.now())
                else:
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'only allow captions and status'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Photo = self.get_object(pk)
        Photo.delete()
        # Delete media?
        return Response(status=status.HTTP_204_NO_CONTENT)
