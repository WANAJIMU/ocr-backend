import json
from pathlib import Path
import re
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


some_data = {
    "data": [
      {
        "License Number": "4000008747",
        "Name": "MREMA",
        "Date of Birth": "15/07/1995",
        "Issuing Authority": "TANZANIA",
        "Permanent Place of Residence": "123 Main St, City",
        "Categories of Vehicles": [
            "C1",
            "C2",
            "C3",
            "DE"
        ],
        "Signature": "Present"
      },
      {
        "License Number": "0987654321",
        "Name": "Jane Smith",
        "Date of Birth": "22/09/1980",
        "Issuing Authority": "CANADA",
        "Permanent Place of Residence": "456 Oak St, Town",
        "Categories of Vehicles": [
          "B",
          "C1",
          "E"
        ],
        "Signature": "Present"
      },
      {
        "License Number": "5555555555",
        "Name": "Bob Johnson",
        "Date of Birth": "10/12/1992",
        "Issuing Authority": "AUSTRALIA",
        "Permanent Place of Residence": "789 Pine St, Village",
        "Categories of Vehicles": [
          "A2",
          "C",
          "DE"
        ],
        "Signature": "Present"
      },
      {
        "License Number": "7777777777",
        "Name": "Alice Brown",
        "Date of Birth": "05/03/1985",
        "Issuing Authority": "UK",
        "Permanent Place of Residence": "101 Cedar St, Suburb",
        "Categories of Vehicles": [
          "C1",
          "D",
          "E"
        ],
        "Signature": "Present"
      },
      {
        "License Number": "4444444444",
        "Name": "Charlie Miller",
        "Date of Birth": "18/06/1990",
        "Issuing Authority": "GERMANY",
        "Permanent Place of Residence": "202 Maple St, Hamlet",
        "Categories of Vehicles": [
          "AC1",
          "C2",
          "DE"
        ],
        "Signature": "Present"
      },
      {
        "License Number": "6666666666",
        "Name": "Eva Davis",
        "Date of Birth": "28/11/1987",
        "Issuing Authority": "FRANCE",
        "Permanent Place of Residence": "303 Birch St, Outpost",
        "Categories of Vehicles": [
          "A1",
          "C",
          "E"
        ],
        "Signature": "Present"
      },
      {
        "License Number": "2222222222",
        "Name": "David Wilson",
        "Date of Birth": "14/02/1998",
        "Issuing Authority": "SPAIN",
        "Permanent Place of Residence": "404 Elm St, Settlement",
        "Categories of Vehicles": [
          "B",
          "C3",
          "DE"
        ],
        "Signature": "Present"
      },
      {
        "License Number": "9999999999",
        "Name": "Grace Taylor",
        "Date of Birth": "08/09/1983",
        "Issuing Authority": "ITALY",
        "Permanent Place of Residence": "505 Spruce St, Colony",
        "Categories of Vehicles": [
          "AC1",
          "C2",
          "E"
        ],
        "Signature": "Present"
      },
      {
        "License Number": "3333333333",
        "Name": "Frank Jones",
        "Date of Birth": "20/05/1995",
        "Issuing Authority": "JAPAN",
        "Permanent Place of Residence": "606 Fir St, Township",
        "Categories of Vehicles": [
          "A2",
          "C3",
          "DE"
        ],
        "Signature": "Present"
      },
      {
        "License Number": "8888888888",
        "Name": "Hannah Lee",
        "Date of Birth": "02/04/1988",
        "Issuing Authority": "SOUTH AFRICA",
        "Permanent Place of Residence": "707 Cedar St, Enclave",
        "Categories of Vehicles": [
          "B",
          "C",
          "E"
        ],
        "Signature": "Present"
      }
    ]
  }
  

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
            cleaned_text = re.sub(r'\s+', ' ', text).strip()
            ocr_text = cleaned_text.replace('\x0c', '')
            serializer.save(text=ocr_text)

            details = {}


            # Extract License Number
            license_number_match = re.search(r"Licence number\s+(\d+)", ocr_text)
            if license_number_match:

                license_number = license_number_match.group(1)
                details['License Number'] = license_number


                if self.is_license_number_verified(license_number, some_data):
                    details['Verification'] = 'License number verified'
                else:
                    details['Verification'] = 'License number not found, check your uploaded photo'

            # Extract Name
            name_match = re.search(r"Family name\s+con\s+(\w+)", ocr_text)
            if name_match:
                details['Name'] = name_match.group(1)

            # Extract Date of Birth
            dob_match = re.search(r"Date of birth\s+(\d{2}/\d{2}/\d{4})", ocr_text)
            if dob_match:
                details['Date of Birth'] = dob_match.group(1)

            # Extract Issuing Authority
            issuing_authority_match = re.search(r"issuing\s+%?\s+(\w+)", ocr_text)
            if issuing_authority_match:
                details['Issuing Authority'] = issuing_authority_match.group(1)

            # Extract Permanent Place of Residence
            residence_match = re.search(r"Permanent place ofresidence\s+(\w+)", ocr_text)
            if residence_match:
                details['Permanent Place of Residence'] = residence_match.group(1)

            # Extract Categories of Vehicles
            categories_match = re.search(r"Categories of Vehicles\s+([\w\s]+)", ocr_text)
            if categories_match:
                details['Categories of Vehicles'] = categories_match.group(1).split()

            # Extract Signature (if needed)
            signature_match = re.search(r"Signature", ocr_text)
            details['Signature'] = "Present" if signature_match else "Not Present"

            response_data = {
                'text': ocr_text,
                'details': details
            }


            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def extract_text_from_image(self, image):
        img = Image.open(image)
        text = pytesseract.image_to_string(img)
        return text
    
    def load_dummy_json(self):
        json_file_path = Path(__file__).resolve().parent / 'dummy.json'
        with open(json_file_path) as f:
            dummy_data = json.load(f)
        return dummy_data
    
    def is_license_number_verified(self, license_number, dummy_data):
        for item in dummy_data.get('data', []):
            if item.get('License Number') == license_number:
                return True
        return False

    

class UserDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer



class OCRAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            image = Image.open(serializer.validated_data['image'])

            text = pytesseract.image_to_string(image)


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
    