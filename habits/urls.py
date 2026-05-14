from rest_framework.routers import DefaultRouter
from habits.views import HabitViewSet, PublicHabitListAPIView
from django.urls import path, include

router = DefaultRouter()
router.register(r'', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('public/', PublicHabitListAPIView.as_view(), name='public-habits'),
]
