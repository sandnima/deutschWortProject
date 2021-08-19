from django.contrib import admin

from profiles.models import Profile, StimmtHistory, FalschHistory


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(StimmtHistory)
class StimmtHistoryAdmin(admin.ModelAdmin):
    pass


@admin.register(FalschHistory)
class FalschHistoryAdmin(admin.ModelAdmin):
    pass
