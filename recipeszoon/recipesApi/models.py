from django.db import models

# Create your models here.
class Recipes(models.Model):
    recipe_name = models.CharField(max_length=100)
    recipe_description = models.CharField(max_length=500)
    recipe_due = models.CharField(max_length=100)
    is_delete = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RecipesImages(models.Model):
    recipe_id = models.ForeignKey(Recipes)
    image_url = models.CharField(max_length=250, default='null')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
