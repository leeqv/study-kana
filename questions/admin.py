from django.contrib import admin
from .models import HiraganaQuestion, HiraganaAnswer, KatakanaQuestion, KatakanaAnswer

# Register your models here.

class HiraganaAnswerInLine(admin.TabularInline):
    model = HiraganaAnswer

class HiraganaQuestionAdmin(admin.ModelAdmin):
    inlines = [HiraganaAnswerInLine]

class KatakanaAnswerInLine(admin.TabularInline):
    model = KatakanaAnswer

class KatakanaQuestionAdmin(admin.ModelAdmin):
    inlines = [KatakanaAnswerInLine]

admin.site.register(HiraganaQuestion, HiraganaQuestionAdmin)
admin.site.register(HiraganaAnswer)
admin.site.register(KatakanaQuestion, KatakanaQuestionAdmin)
admin.site.register(KatakanaAnswer)
