from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('reviews', views.ReviewViewSet, basename='history-viewsets')

urlpatterns = [
    path('', include(router.urls))
]
