from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from photos import views

urlpatterns = [
    path('api/v1/photo/', views.PhotoList.as_view()),
    path('api/v1/photo/<int:pk>/', views.PhotoDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)