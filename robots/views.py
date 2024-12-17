import json
from datetime import datetime
from io import StringIO

import xlsxwriter

from django.db.models.aggregates import Count
from django.db.models.functions import TruncWeek
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings

from robots.models import Robot
from robots.forms import GetStatisticsForm


def write_to_exel(file_name: str, write_data: QuerySet):
    workbook = xlsxwriter.Workbook(f"{settings.MEDIA_ROOT}/{file_name}")
    output = StringIO()

    all_models = set(write_data.values_list("model", flat=True))
    for model in all_models:
        robots_data = write_data.filter(model=model)
        versions_robot = set(robots_data.values_list("version", flat=True))
        worksheet = workbook.add_worksheet(name=model)
        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', "Модель", bold)
        worksheet.write('B1', "Версия", bold)
        worksheet.write('C1', "Количество за неделю", bold)
        row = 1
        col = 0

        for version in versions_robot:
            current_robot = robots_data.filter(version=version)
            robot_info = current_robot.annotate(week=TruncWeek("created")).values("version").annotate(count=Count("week")).order_by("-week")
            count = robot_info[0].get("count")
            worksheet.write(row, col, model)
            worksheet.write(row, col + 1, version)
            worksheet.write(row, col + 2, count)
            row += 1

    workbook.close()

    xlsx_data = output.getvalue()
    return xlsx_data


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


def get_statistics(request):
    rodots_data = Robot.objects.all()
    data = write_to_exel("weekly_report.xlsx", rodots_data)
    if request.POST:
        with open(f"{settings.MEDIA_ROOT}/weekly_report.xlsx", "rb") as f:
            response = HttpResponse(f.read(), content_type="application/vnd.ms-exel")
            response["Content-Disposition"] = f"attachment; filename=weekly_report.xlsx"
            response.write(data)
            return response
    form = GetStatisticsForm()
    return render(request, "robots/download_statistics.html", context={"form": form})
