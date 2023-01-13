from django.contrib import admin
from .models import MLModel


class MLModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "uploaded_by",
        "uploaded_on",
        "model_file",
        "train_file",
        "test_file",
    )
    search_fields = ["name", "model_file"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(MLModel, MLModelAdmin)
