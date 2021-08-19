from django.urls import path
from profiles.views import (
    AddStimmt,
    AddFalsch,
)

app_name = 'profiles'
urlpatterns = [
    path('add-stimmt/', AddStimmt.as_view(), name='add-stimmt'),
    path('add-falsch/', AddFalsch.as_view(), name='add-falsch'),
]
