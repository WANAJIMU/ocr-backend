from PIL import Image
import pytesseract
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Check, UserData
from .serializers import CheckSerializer, UserDataSerializer, ImageUploadSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OCRData
from .serializers import OCRDataSerializer
from .validators import validate_name, validate_address

class UserDataListCreateView(generics.ListCreateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer


class CheckImageCreateView(generics.ListCreateAPIView):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    def get(self, request, format=None):
        ocr_data = OCRData.objects.all()
        serializer = OCRDataSerializer(ocr_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OCRDataSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            text = self.extract_text_from_image(image)
            serializer.save(text=text)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def extract_text_from_image(self, image):
        img = Image.open(image)
        text = pytesseract.image_to_string(img)
        return text

    

class UserDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer



class OCRAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            # Open the uploaded image using Pillow
            image = Image.open(serializer.validated_data['image'])

            # Perform OCR using Pytesseract
            text = pytesseract.image_to_string(image)

            # Do something with the extracted text, e.g., save it to a model

            return Response({'text': text}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class OCRDataListCreateView(APIView):
    def get(self, request, format=None):
        ocr_data = OCRData.objects.all()
        serializer = OCRDataSerializer(ocr_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OCRDataSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            text = self.extract_text_from_image(image)

            name_valid = validate_name(serializer.validated_data.get('name'))
            address_valid = validate_address(serializer.validated_data.get('address'))

            serializer.save(text=text)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def extract_text_from_image(self, image):
        img = Image.open(image)
        text = pytesseract.image_to_string(img)
        return text

from rest_framework.parsers import MultiPartParser

class CheckImage_CreateView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        if 'image' not in request.FILES:
            return Response({"error": "no image uploaded"})
        image = request.FILES['image']
        image_data = image.read()

        with open('my_image.jpg', 'wb') as f:
            f.write(image_data)
        return Response({'message': 'successful'})
    