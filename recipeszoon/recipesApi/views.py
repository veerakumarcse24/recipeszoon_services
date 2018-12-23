# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.shortcuts import render

#from hrmsv2.settings import FRONT_URL

from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.signing import Signer
# from rest_framework.test import APIRequestFactory
from django.core.files import uploadedfile
from django.core.files import uploadhandler
from rest_framework import generics
from datetime import datetime
#from hrmsv2.settings import MEDIA_URL
from django.db.models import Q
from django.db.models import Sum
import dateutil.parser
import os
# import datetime
import json
import base64

from recipesApi.models import *
from recipesApi.serializers import *
from recipesApi.constant import *


from django.utils.crypto import get_random_string


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def creatRecipe(request): #save Recipe
    if request.method == "POST":
        data=json.loads(request.POST.get('data'))
        model = Recipes()
        model.recipe_name = data.get('recipe_name')
        model.recipe_due = data.get('recipe_due')
        model.recipe_description = data.get('recipe_description')
        model.save()
        imageUpload(request, model.id)
        data = {'Status': 'success', 'message': 'Recipe created successfully.'}
    else:
        data = {'Status': 'failed', 'message': 'Invalid'}
    return JSONResponse(data)

@csrf_exempt
def getRecipes(request): #save users ratings
    if request.method == "GET":
        getAllRecipes = Recipes.objects.filter(is_delete=0)
        getAllRecipesImages = RecipesImages.objects.all()
        recipes_serializer = RecipesSerializer(getAllRecipes, many=True)
        recipes_image_serializer = RecipesImagesSerializer(getAllRecipesImages, many=True)
        recipesListdata  = recipes_serializer.data
        for recipe in recipesListdata:
            recipe['image_urls'] = [];
        for recipe in recipesListdata:
            recipe['image_urls'] = list(img_url['image_url'] for img_url in recipes_image_serializer.data if (img_url['recipe_id'] == recipe['id']))
        data = {'Status': 'success', 'data': recipesListdata, 'message': 'Success'}
    else:
        data = {'Status': 'failed', 'message': 'Invalid'}
    return JSONResponse(data)

@csrf_exempt
def imageUpload(request, id, format=None):
    if request.method == "POST":
        recipe_name = json.loads(request.POST.get('data')).get('recipe_name')
        index = 1
        for single_file in request.FILES:
            file_data = request.FILES.get(single_file)
            filename,extension = os.path.splitext(file_data.name)
            final_file_name = 'image_'+str(index)+extension
            img_url = handle_uploaded_file(request.FILES[single_file],final_file_name, id)
            model = RecipesImages()
            model.image_url = img_url
            model.recipe_id_id = id
            model.save()
            index = index + 1
        data = {'Status': 'success', 'message': 'Images uploated successfully.'}
    else:
        data = {'Status': 'failed', 'message': 'Invalid'}
    return JSONResponse(data)


def handle_uploaded_file(f,file_name, id):
    id = str(id)
    BASE = os.path.dirname(os.path.abspath(__file__))
    dir_name = os.path.join(BASE + '/static/'+id+'/')
    if not os.path.isdir(dir_name):
        os.mkdir(os.path.join(BASE + '/static', id))
   # return dir_name;
    with open(dir_name + file_name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    return (backendurl+'/static/'+id+'/'+ file_name)

@csrf_exempt
def deleteRecipe(request): #save users ratings
    if request.method == "POST":
        data=json.loads(request.body)
        try:
            model = Recipes.objects.get(id = data.get('recipe_id'))
            model.is_delete = 1
            model.save()
            data = {'Status': 'success', 'message': 'successfully deleted recipe.'}
        except Recipes.DoesNotExist:
            data = {'Status': 'failed', 'message': 'Invalid'}
    else:
        data = {'Status': 'failed', 'message': 'Invalid'}
    return JSONResponse(data)




