import uuid
from django.db import models
from django.conf import settings

class UserData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(upload_to="uploads/")
    current_occupation = models.CharField(max_length=255)
    address = models.TextField()
    loan_amount = models.PositiveIntegerField()
    purpose = models.TextField()
    date_of_application = models.DateTimeField(auto_now=True)
    organization_working_under = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # is_verified = models.BooleanField(default=False)

    # def verify_loan(self):
    #     self.is_verified==True


    
class Check(models.Model):
    image_1 = models.ImageField(upload_to='check_images/')


class OCRData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='ocr_images/')
    text = models.TextField(blank=True)

    # also each should be associated with a user




    # ID_NO = 
    # employers_details = a bunch of details
    # ID_TYPE = 




# Please attach: ID card (e.g National ID, Voters reg. No, Driving license, Passport, Ward ID, Others), Three Recent Salary slips, Two Recent Photographs, Employment Contract, Introduction letter, Passport (if any), Valuation report (if security is landed property), Working and Residence permit (if non citizen) and Others as may be advised by Bank official.



