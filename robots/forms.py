import os

from django import forms
from django.conf import settings


class GetStatisticsForm(forms.Form): ...
    # link = forms.FilePathField(path=os.path.abspath(settings.MEDIA_ROOT), label="Файл")