import pandas as pd
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ExcelFile
from .serializers import FileSerializer
from django.http import FileResponse
class ExcelToJson(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        if file:
            try:
                data = pd.read_excel(file)
                return Response(data.to_json(), status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

class FileViewSet(viewsets.ModelViewSet):
    queryset = ExcelFile.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser]

    def get_json_excel_data(self, request, *args, **kwargs):
        file_id = kwargs.get('pk')
        if file_id:
            try:
                excel_file = ExcelFile.objects.get(id=file_id).file
                data = pd.read_excel(excel_file)
                return Response(data.to_json(), status=status.HTTP_200_OK)
            except ExcelFile.DoesNotExist:
                return Response({'Error': 'The file does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Error': 'No file ID provided'}, status=status.HTTP_400_BAD_REQUEST)

    def download_file(self, request, *args, **kwargs):
        file_id = kwargs.get('pk')
        if file_id:
            try:
                excel_file = ExcelFile.objects.get(id=file_id).file
                response = FileResponse(open(excel_file.path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')                
                response['Content-Disposition'] = f'attachment; filename="{excel_file.name}"'
                return response
            except ExcelFile.DoesNotExist:
                return Response({'Error': 'The file does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Error': 'No file ID provided'}, status=status.HTTP_400_BAD_REQUEST)
