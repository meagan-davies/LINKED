from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Linker,flexibility,YourModel
import json
#register the models/databases
@admin.register(Linker)
@admin.register(flexibility)
@admin.register(YourModel)
class LinkerResource(ImportExportModelAdmin):
    pass


