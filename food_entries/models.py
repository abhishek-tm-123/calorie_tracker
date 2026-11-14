from django.db import models

from accounts.models import User

# Create your models here.

class FoodLog(models.Model):
    title = models.CharField(max_length=20,null=True)
    
    serving_size = models.CharField(max_length=20)
    
    calorie = models.FloatField()
    
    MEAL_CHOICES = [
        ("breakfast","Breakfast"),
        ("lunch","Lunch"),
        ("snacks","Snacks"),
        ("dinner","Dinner")
    ]

    meal_type = models.CharField(max_length=20,choices=MEAL_CHOICES,default="lunch")
    
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    
    food_image = models.ImageField(upload_to="foods",null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    