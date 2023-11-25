from django.urls import path
from .views import CheckImageCreateView, OCRAPIView, OCRDataListCreateView, UserDataListCreateView, UserDataRetrieveUpdateDestroyView

urlpatterns = [
    path('apply/', UserDataListCreateView.as_view(), name='loan-list-create'),
    path('apply/<int:pk>/', UserDataRetrieveUpdateDestroyView.as_view(), name='loan-retrieve-update-destroy'),
    path('api/ocr/', OCRAPIView.as_view(), name='ocr_api'),
    path('upload-now/ocrdata/', OCRDataListCreateView.as_view(), name='ocrdata-list-create'),
    path('doc-create/', CheckImageCreateView.as_view(), name='okay')
]
