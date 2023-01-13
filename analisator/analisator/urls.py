"""analisator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from analisator import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.ModelsList.as_view(), name="home"),
    path("", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("upload/", views.upload_files, name="upload"),
    path("<slug:slug>/", views.ml_model_detail, name="ml_model_detail"),
    path("<slug:slug>/pdf", views.generate_pdf, name="generate-pdf"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
