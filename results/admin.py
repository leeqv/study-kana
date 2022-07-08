from django.contrib import admin
from .models import UserProfile, Trophy, HiraganaResult, KatakanaResult

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Trophy)
admin.site.register(HiraganaResult)
admin.site.register(KatakanaResult)


