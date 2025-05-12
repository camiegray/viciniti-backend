# import Home view from the views file
from .views import Home
from django.urls import path

urlpatterns = [
    path('', Home.as_view(), name='home'),
]