from datetime import datetime

from dateutil import parser
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.required_params import require_params

from todo.constants import BACKLOG_ID, DONE_ID, ONGOING_ID, TODO_ID
from todo.models import Todo
from todo.serializers import TodoSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_kanban(request):
    user_todos = request.user.todos.all()
    to_return = {}

    to_return[BACKLOG_ID] = TodoSerializer(user_todos.filter(stage=0), many=True).data
    to_return[TODO_ID] = TodoSerializer(user_todos.filter(stage=1), many=True).data
    to_return[ONGOING_ID] = TodoSerializer(user_todos.filter(stage=2), many=True).data
    to_return[DONE_ID] = TodoSerializer(user_todos.filter(stage=3), many=True).data

    return Response(to_return)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@require_params(["to", "id"])
def move_kanban(request):
    data = request.data
    user = request.user
    to = data["to"]
    if to == BACKLOG_ID:
        to = 0
    elif to == TODO_ID:
        to = 1
    elif to == ONGOING_ID:
        to = 2
    elif to == DONE_ID:
        to = 3

    task = Todo.objects.filter(id=data["id"], user=user)
    if not task.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    task = task[0]
    task.stage = to
    task.save()

    return Response()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@require_params(["taskName", "priority", "deadLine"])
def new_todo(request):
    data = request.data

    todo_obj = Todo.objects.create(
        name=data["taskName"],
        user=request.user,
        stage=0,
        priority=data["priority"],
        # 30th June, 2022
        # 24-6-2022
        deadline=datetime.strptime(data["deadLine"], "%d-%m-%Y").date(),
    )

    return Response(TodoSerializer(todo_obj).data)


# deadline: "9 Aug, 22"
# id: 238
# name: "do instantly"
# priority: "LOW"
# stage: 0
# user: 4
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def edit_todo(request):
    data = request.data
    todo_obj = Todo.objects.get(id=data["id"])

    todo_obj.name = data["taskName"]
    todo_obj.priority = data["priority"]
    todo_obj.deadline = datetime.strptime(data["deadLine"], "%d-%m-%Y").date()
    todo_obj.save()

    return Response(TodoSerializer(todo_obj).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@require_params(["id"])
def delete_kanban(request):
    id = request.data["id"]
    Todo.objects.get(id=id).delete()
    return Response()
