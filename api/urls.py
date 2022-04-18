from django.urls import path
# from .views import BookReviewListAPIView, BookReviewDetailAPIView
from rest_framework.routers import DefaultRouter

from api.views import BookReviewsViewSet

app_name='api'

router = DefaultRouter()
router.register('reviews', BookReviewsViewSet, basename='review')
urlpatterns = router.urls

# urlpatterns = [
#     path('reviews/', BookReviewListAPIView.as_view(), name='list-review'),
#     path('reviews/<int:id>/', BookReviewDetailAPIView.as_view(), name='detail-review'),
# ]