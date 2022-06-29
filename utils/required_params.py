from typing import List

from rest_framework import status
from rest_framework.response import Response


def require_params(fields: List, key: str = "data"):
    def decorator_func(og_func, *args, **kwargs):
        def wrapper_func(request, *args, **kwargs):
            """
            Decorator to check for specific fields in the request obj
            """
            data = None
            if key == "data":
                data = request.data
            elif key == "GET":
                data = request.GET
            errors = []
            for field in fields:
                if field not in data:
                    errors.append(field)

            if len(errors):
                return Response(
                    f"{', '.join(errors)} field{'s were' if len(errors) > 1  else ' was'} not provided.",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return og_func(request, *args, **kwargs)

        return wrapper_func

    return decorator_func
