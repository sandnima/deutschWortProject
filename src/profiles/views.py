from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from profiles.models import Profile, StimmtHistory
from worte.models import Substantiv


@method_decorator(csrf_exempt, name='dispatch')
class AddStimmt(LoginRequiredMixin, View):
    def post(self, request):
        wort_pk = request.POST.get("pk")
        wort_obj = get_object_or_404(Substantiv, pk=wort_pk)
        stimmt_obj = StimmtHistory.objects.get_or_create(wort=wort_obj)[0]
        stimmt_obj.mal += 1
        stimmt_obj.save()
        return HttpResponse('successful')


@method_decorator(csrf_exempt, name='dispatch')
class AddFalsch(LoginRequiredMixin, View):
    def post(self, request, wort_id):
        pass
