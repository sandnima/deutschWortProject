from django.urls import path
from worte.views import (
    WorteView,
    SubstantivView,
    AdjektivView,
)

app_name = 'worte'
urlpatterns = [
    path('', WorteView.as_view(), name='worte-list'),
    path('substantiv/', SubstantivView.as_view(), name='substantiv-list'),
    path('adjektiv/', AdjektivView.as_view(), name='adjektiv-list'),
]
