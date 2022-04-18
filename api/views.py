from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView

from api.serializers import BookReviewSerializer
from books.models import BookReview

class BookReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all().order_by('created_at')
    lookup_field = 'id'

# class BookReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BookReviewSerializer
#     queryset = BookReview.objects.all
#     lookup_field = 'id'
#
# class BookReviewListAPIView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BookReviewSerializer
#     queryset = BookReview.objects.all().order_by('-created_at')