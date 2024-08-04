from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('Score', index),
     path('callback', index),
     #path('user_metrics', index)
]