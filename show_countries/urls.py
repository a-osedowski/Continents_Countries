from django.urls import path
from . import views
#
# from show_countries.views import PostContinentFromUser

urlpatterns = [
    path('', views.home, name='continent-post')
]