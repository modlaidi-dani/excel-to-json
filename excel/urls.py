from django.urls import path, include
from .views import FileViewSet, ExcelToJson
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('excelfile-to-json', FileViewSet, basename='excelfile')

urlpatterns = [
    path('', include(router.urls)),
    path('excel-to-json/', ExcelToJson.as_view())
]