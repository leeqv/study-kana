from django.contrib import admin
from .models import HiraganaLesson, HiraganaLetter, KatakanaLesson, KatakanaLetter

# Register your models here.

class HiraganaLetterInLine(admin.TabularInline):
    model = HiraganaLetter

class HiraganaLessonAdmin(admin.ModelAdmin):
    inlines = [HiraganaLetterInLine]

class KatakanaLetterInLine(admin.TabularInline):
    model = KatakanaLetter

class KatakanaLessonAdmin(admin.ModelAdmin):
    inlines = [KatakanaLetterInLine]

admin.site.register(HiraganaLesson, HiraganaLessonAdmin)
admin.site.register(HiraganaLetter)
admin.site.register(KatakanaLesson, KatakanaLessonAdmin)
admin.site.register(KatakanaLetter)