import random, time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import View, ListView
from django.db.models import Min

from profiles.models import Profile, StimmtHistory
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
        history_words = StimmtHistory.objects.filter(user=profile)
        weights = weight_list_generator(all_words=all_words, history=history_words)
        random_word = get_object_or_404(Substantiv, pk=random.choices(population=all_words, weights=weights)[0])
        
        # TESTING RANDOMNESS
        # tic = time.perf_counter()
        # for n in range(1000000):
        #     weights = weight_list_generator(all_words=all_words, history=history_words)
        # toc = time.perf_counter()
        # print('TIME MEASURED:', toc - tic)
        
        # def generator(bar):
        #     for k in range(bar):
        #         yield k
        # test_bar = generator(1000)
        # test_result = dict()
        # list_gened = weight_list_generator(all_words=all_words, history=history_words)
        #
        # for n in range(8):
        #     t = list_gened.__next__()
        #     print(Substantiv.objects.get(pk=t[0]), t[1])
        #
        # print('---------------------')
        # for n in test_bar:
        #     w = weight_list_generator(all_words=all_words, history=history_words)
        #     r = random.choices(population=all_words, weights=w)
        #     random_word = get_object_or_404(Substantiv, pk=r[0])
        #     # random = weight_list_generator(all_words=all_words, history=history_words)
        #     test_result[random_word] = test_result.get(random_word, 0) + 1
        # test_result = dict(sorted(test_result.items(), key=lambda item: item[1], reverse=True))
        # for wrd, rnd in test_result.items():
        #     print(wrd, rnd/1000)
        
        context = {
            'random_word': random_word,
            'history_words': history_words,
        }
        return render(request, template_name=self.template_name, context=context)


def weight_list_generator(all_words, history=None):
    base = 1.0
    adjust = 0
    history_word_list = history.values_list('wort', flat=True)
    if len(all_words) == len(history_word_list):
        try:
            min_mal = history.order_by('mal').first().mal
            adjust = min_mal
        except AttributeError:
            pass
    for word_id in all_words:
        probability = base
        if word_id in history_word_list:
            probability = probability / (history.get(wort_id=word_id).mal - adjust + 1)
        yield probability


# def weight_list_generator(all_words, history=None):
#     base = 1
#     for history_word in history:
#         occ = history_word.mal
#         base = base + occ
#     weight_list = []
#     for word_id in all_words:
#         probability = base
#         if word_id in history.values_list('wort', flat=True):
#             probability = base - history.get(wort_id=word_id).mal
#         weight_list.append(probability)
#     min_weight = min(weight_list) - 1
#     weight_list = [weight-min_weight for weight in weight_list]
#     return weight_list
