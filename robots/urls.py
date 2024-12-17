from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from robots.views import add_robots, get_statistics

urlpatterns = [
    path('add_robot/', add_robots),
    path("get_statistics/", get_statistics),
]