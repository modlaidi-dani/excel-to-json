import pytest
from excel.models import *
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
@pytest.mark.django_db
def excel_to_json_without_saving(): 
    client=APIClient()
    file_content = b"col1,col2\n1,2\n3,4\n"
    file = SimpleUploadedFile("test.xlsx", file_content)

    response = client.post('/api/excel-to-json/', {'file': file.file}) 
    assert response.status_code == 200
    assert 'col1' in response.data
    assert 'col2' in response.data
    assert response.data['col1'][0]==1
    assert response.data['col1'][1]==3
    assert response.data['col2'][0]==2
    assert response.data['col2'][1]==4
    
    
    