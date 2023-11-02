from django.db import models
import uuid
import random

#linker database contains the original database found online
class Linker(models.Model):
  id = models.CharField(primary_key=True, max_length=15)
  region=models.CharField(max_length=100)
  length = models.IntegerField(default=0)
  aasequence = models.CharField(max_length=255)
  secondary_structure=models.CharField(max_length=100)
  Origin=models.CharField(max_length=225)

  def __str__(self):
    return self.id
  

class YourModel(models.Model):
    def generate_unique_6_digit_number():
      while True:
          # Generate a random 6-digit number
          unique_number = random.randint(100000, 999999)
          
          # Check if the number is already used in the database
          if not YourModel.objects.filter(id=unique_number).exists():
              return str(unique_number)
          
    id=models.CharField(primary_key=True,default=generate_unique_6_digit_number, editable=False,unique=True)
    
    aasequence = models.CharField(max_length=255)
    Origin=models.CharField(max_length=225)

    def __str__(self):
      return str(self.id)
  
#contains data from post-processing 
#containts backbone dynamic and average flexibility of linker with 5 or more amino acids
class flexibility(models.Model):
    id = models.CharField(primary_key=True, max_length=15,default='1')
    Sequence = models.CharField(max_length=100)
    backbone = models.CharField()
    average_flexibility=models.FloatField(default=0)


    def __str__(self):
        return self.id


