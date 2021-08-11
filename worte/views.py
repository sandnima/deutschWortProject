from django.shortcuts import render
from django.views.generic import View, ListView

from worte.models import Substantiv, Adjektiv


class WorteView(View):
    template_name = 'worte/worte_list.html'
    
    def get(self, request):
        substantiv = Substantiv.objects.all().order_by('-updated_at')[:10]
        adjektiv = Adjektiv.objects.all().order_by('-updated_at')[:10]
        context = {
            'substantiv_list': substantiv,
            'adjektiv_list': adjektiv,
        }
        return render(request, template_name=self.template_name, context=context)


class SubstantivView(ListView):
    model = Substantiv
    
    def get_ordering(self):
        return '-updated_at'


class AdjektivView(ListView):
    model = Adjektiv
    
    def get_ordering(self):
        return '-updated_at'
