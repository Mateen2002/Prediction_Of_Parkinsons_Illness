from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address= models.CharField(max_length=3000)
    gender= models.CharField(max_length=30)

class predict_parkinsons_illness(models.Model):

    RID= models.CharField(max_length=3000)
    name= models.CharField(max_length=3000)
    MDVP_Fo_Hz= models.CharField(max_length=3000)
    MDVP_Fhi_Hz= models.CharField(max_length=3000)
    MDVP_Flo_Hz= models.CharField(max_length=3000)
    MDVP_Jitter= models.CharField(max_length=3000)
    MDVP_Jitter_Abs= models.CharField(max_length=3000)
    MDVP_RAP= models.CharField(max_length=3000)
    MDVP_PPQ= models.CharField(max_length=3000)
    Jitter_DDP= models.CharField(max_length=3000)
    MDVP_Shimmer= models.CharField(max_length=3000)
    MDVP_Shimmer_dB= models.CharField(max_length=3000)
    Shimmer_APQ3= models.CharField(max_length=3000)
    Shimmer_APQ5= models.CharField(max_length=3000)
    MDVP_APQ= models.CharField(max_length=3000)
    Shimmer_DDA= models.CharField(max_length=3000)
    NHR= models.CharField(max_length=3000)
    HNR= models.CharField(max_length=3000)
    RPDE= models.CharField(max_length=3000)
    DFA= models.CharField(max_length=3000)
    spread1= models.CharField(max_length=3000)
    spread2= models.CharField(max_length=3000)
    D2= models.CharField(max_length=3000)
    PPE= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



