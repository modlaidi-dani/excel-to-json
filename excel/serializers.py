from .models import ExcelFile
from rest_framework import serializers
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExcelFile
        fields='__all__'
        