from django.urls import path

from . import views

urlpatterns = [
    path("register", views.register),
    path("upload-profile-img", views.upload_img),
    path("login", views.login),
]
