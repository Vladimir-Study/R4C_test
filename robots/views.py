import json
from datetime import datetime

from django.http import JsonResponse
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt

from robots.models import Robot


@csrf_exempt
def add_robots(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            keys = list(data.keys())
            if len(data) != 3 or (
                "model" not in keys or "version" not in keys or "created" not in keys
            ):
                response = {
                        "status": "error",
                        "message": "Bad request"
                    }
                return JsonResponse(response, status=400)
            created = datetime.strptime(data["created"], "%Y-%m-%d %H:%M:%S")
            Robot.objects.create(model=data["model"], version=data["version"], created=make_aware(created))
            response = {
                "status": "success",
                "message": "Robot added",
            }
            return JsonResponse(response, status=201)
        except json.decoder.JSONDecodeError:
            response = {
                "status": "error",
                "message": "Invalid JSON",
            }
            return JsonResponse(response, status=400)
    else:
        response = {
            "status": "error",
            "message": "Only POST requests are allowed",
        }
        return JsonResponse(response, status=400)
