from django.db import models
import random

# Create your models here.


class Linker(models.Model):
    def generate_unique_6_digit_number():
      while True:
          # Generate a random 6-digit number
          unique_number = random.randint(100000, 999999)
          
          # Check if the number is already used in the database
          if not Linker.objects.filter(id=unique_number).exists():
              return str(unique_number)
    id = models.CharField(primary_key=True, max_length=15,default=generate_unique_6_digit_number) #random generated id 
    pdb_id=models.CharField(max_length=15,default='N/A') #pdb id if there is one
    length = models.IntegerField(default=0) #length of the amino acid sequence
    aasequence = models.CharField(max_length=255) #amino acid sequence
    Source=models.CharField(max_length=350,default='NA') #description of where it is from like which protein it is from and etc. 
    Reference=models.CharField(max_length=400,default='N/A') #reference paper or literature website 

    def __str__(self):
        return self.id
    
class flexibility(models.Model):
    def generate_unique_6_digit_number():
      while True:
          # Generate a random 6-digit number
          unique_number = random.randint(100000, 999999)
          
          # Check if the number is already used in the database
          if not Linker.objects.filter(id=unique_number).exists():
              return str(unique_number)
    id = models.CharField(primary_key=True, max_length=15,default=generate_unique_6_digit_number)
    Sequence = models.CharField(max_length=100)
    backbone = models.CharField(default='NA')
    average_flexibility=models.FloatField(default=0)
    #pdb_id=models.CharField(max_length=15,default='N/A')
    type=models.CharField(max_length=100,default='Unknown')


    def __str__(self):
        return self.id

class Hydrophobicity(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    sequence = models.CharField(max_length=100)
    
    # Acidic environment hydrophobicity percentages
    acidic_very_hydrophobic = models.FloatField(default=0)
    acidic_hydrophobic = models.FloatField(default=0)
    acidic_neutral = models.FloatField(default=0)
    acidic_hydrophilic = models.FloatField(default=0)
    
    # Neutral environment hydrophobicity percentages
    neutral_very_hydrophobic = models.FloatField(default=0)
    neutral_hydrophobic = models.FloatField(default=0)
    neutral_neutral = models.FloatField(default=0)
    neutral_hydrophilic = models.FloatField(default=0)
    
    # GRAVY score
    gravy_score = models.FloatField(default=0)
    
    # Base64-encoded image data for both environments
    acidic_img_data = models.TextField()
    neutral_img_data = models.TextField()

    def __str__(self):
        return self.id

  