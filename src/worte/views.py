import random, time
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import View, ListView

from profiles.models import Profile, StimmtHistory, FalschHistory
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


class RandomChooseView(LoginRequiredMixin, View):
    template_name = 'worte/random.html'
    
    def get(self, request):
        all_words = Substantiv.objects.all().values_list('id', flat=True)
        profile = Profile.objects.get(user=request.user)
        stimmt_history_words = StimmtHistory.objects.filter(user=profile)
        falsch_history_words = FalschHistory.objects.filter(user=profile)
        weights = weight_list_generator(all_words=all_words,
                                        stimmt_history=stimmt_history_words,
                                        falsch_history=falsch_history_words)
        word_pk = random.choices(population=all_words, weights=weights)[0]
        random_word = get_object_or_404(Substantiv, pk=word_pk)

        context = {
            'random_word': random_word,
            'stimmt_history_words': stimmt_history_words,
            'falsch_history_words': falsch_history_words,
        }
        return render(request, template_name=self.template_name, context=context)


def weight_list_generator(all_words, stimmt_history=None, falsch_history=None):
    base = 1.0
    s_adjust = 0
    f_adjust = 0
    stimmt_history_word_list = stimmt_history.values_list('wort', flat=True)
    falsch_history_word_list = falsch_history.values_list('wort', flat=True)
    if len(all_words) == len(stimmt_history_word_list):
        try:
            s_min_mal = stimmt_history.order_by('mal').first().mal
            s_adjust = s_min_mal
        except AttributeError:
            pass
    if len(all_words) == len(falsch_history_word_list):
        try:
            f_min_mal = stimmt_history.order_by('mal').first().mal
            f_adjust = f_min_mal
        except AttributeError:
            pass
    for word_id in all_words:
        probability = base
        if word_id in stimmt_history_word_list:
            probability = probability / (stimmt_history.get(wort_id=word_id).mal - s_adjust + 1)
        elif word_id in falsch_history_word_list:
            probability = probability * (falsch_history.get(wort_id=word_id).mal - f_adjust + 1)
        yield probability
