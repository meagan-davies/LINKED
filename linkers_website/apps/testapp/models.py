from django.db import models
import uuid
import random

#linker database contains the original database found online
#contains general information of linker

#generating id 
def id_generator():
  while True:
    # Generate a random 6-digit number
    unique_number = random.randint(100000, 999999)
          
    # Check if the number is already used in the database
    if not YourModel.objects.filter(id=unique_number).exists():
      return str(unique_number)

#contains general information of linker
class Linker(models.Model):
  id = models.CharField(primary_key=True, max_length=15,default=id_generator,editable=False,unique=True) #random generated id 
  pdb_id=models.CharField(max_length=15,default=None) #pdb id if there is one
  length = models.IntegerField(default=0) #length of the amino acid sequence
  aasequence = models.CharField(max_length=255) #amino acid sequence
  Source=models.CharField(max_length=350) #description of where it is from like which protein it is from and etc. 
  Reference=models.CharField(max_length=400,default=None) #reference paper or literature website 

  def __str__(self):
    return self.id


class YourModel(models.Model):

          
    id=models.CharField(primary_key=True,default=id_generator, editable=False,unique=True)
    
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