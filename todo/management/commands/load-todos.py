import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from todo.models import Todo


class Command(BaseCommand):
    help = "For loading some test todos"

    def handle(self, *args, **kwargs):
        user = User.objects.get(is_superuser=True)

        for i in range(1, 50):
            Todo.objects.create(
                user=user,
                name=f"Do something {i}",
                stage=random.choice([0, 1, 2, 3]),
                priority=random.choice(['HIGH', 'LOW', 'MEDIUM']),
            )

            print(f"created item {i}")
