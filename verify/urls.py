from django.urls import path
from .views import UserDataListCreateView, UserDataRetrieveUpdateDestroyView

urlpatterns = [
    path('apply/', UserDataListCreateView.as_view(), name='loan-list-create'),
    path('apply/<int:pk>/', UserDataRetrieveUpdateDestroyView.as_view(), name='loan-retrieve-update-destroy'),
]
