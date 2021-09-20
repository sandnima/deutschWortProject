from django.contrib import admin
from django.contrib.auth import get_user_model

from worte.models import Stufe, Substantiv, Adjektiv


class AutoAutor(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'autor':
            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['autor'].initial = request.user
        return form
    
    
@admin.register(Stufe)
class SubstantivAdmin(admin.ModelAdmin):
    pass


@admin.register(Substantiv)
class SubstantivAdmin(AutoAutor):
    list_display = ('__str__', 'stufe')
    list_editable = ('stufe',)
    list_filter = ('stufe',)


@admin.register(Adjektiv)
class AdjektivAdmin(AutoAutor):
    list_display = ('__str__', 'stufe')
    list_editable = ('stufe',)
    list_filter = ('stufe',)
