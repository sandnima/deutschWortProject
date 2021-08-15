from django.shortcuts import render
from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404

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


class RandomChooseView(View):
    template_name = 'worte/random.html'
    
    def get(self, request):
        words = Substantiv.objects.all().values_list('id', flat=True)
        random = get_object_or_404(Substantiv, pk=weighted_choice(words, history={}))
        
        context = {
            'random_word': random,
        }
        return render(request, template_name=self.template_name, context=context)


def weight_list_generator(words, history):
    base = 1
    for word, occ in history.items():
        base = base + occ
    for word in words:
        probability = base
        if word in history:
            probability = base - history[word]
        yield word, probability


def weighted_choice(words, history=()):
    import random
    
    total = 1
    for occ in history.values():
        total = total + occ
    total = total * len(words) - (total - 1)
    
    for word, probability in weight_list_generator(words, history):
        rand = random.random()
        prob = 1 / total * probability
        total = total - probability
        if rand < prob:
            return word
