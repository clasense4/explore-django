from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from photos import views

urlpatterns = [
    path('api/v1/photos', views.PhotoList.as_view()),
    path('api/v1/photo/<int:pk>', views.PhotoDetail.as_view()),
    path('api/v1/user/<str:username>', views.UserList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)