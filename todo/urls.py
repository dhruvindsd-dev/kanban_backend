from django.urls import path

from . import views

urlpatterns = [
    path("new", views.new_todo),
    path("edit", views.edit_todo),
    path("kanban", views.get_kanban),
    path("kanban/move", views.move_kanban),
    path("kanban/delete", views.delete_kanban),
]
