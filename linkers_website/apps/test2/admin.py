from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import testdata

#resources function allows the id in the json file to be recognized as id for the database in Django
class ProductAdminResource(resources.ModelResource):
    class Meta:
         model = testdata
         import_id_fields = ['id']

@admin.register(testdata)
class ProductAdminView(ImportExportModelAdmin):
    resource_class = ProductAdminResource
