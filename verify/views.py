from rest_framework import generics
from .models import UserData
from .serializers import UserDataSerializer
from rest_framework.permissions import IsAuthenticated

class UserDataListCreateView(generics.ListCreateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer

