from rest_framework.urlpatterns import format_suffix_patterns

from django.conf.urls import include, url
from django.conf import settings

from .views import *


urlpatterns = [
    url(r'^creatRecipe/', creatRecipe),
    url(r'^getRecipes/', getRecipes),
    url(r'^deleteRecipe/', deleteRecipe)

]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
