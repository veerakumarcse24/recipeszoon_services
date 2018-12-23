from rest_framework import serializers
from datetime import datetime
from recipesApi.models import *

class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = '__all__'

class RecipesImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipesImages
        fields = '__all__'
