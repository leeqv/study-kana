from django.db import models
from lessons.models import HiraganaLesson, KatakanaLesson

# Create your models here.

class HiraganaQuiz(models.Model):
    code = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=120, unique=True)
    lesson = models.ForeignKey(HiraganaLesson, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"Quiz {self.code}: {self.name}"

    def get_questions(self):
        return self.hiraganaquestion_set.all()

    class Meta:
        verbose_name_plural = 'Hiragana quizzes'

class KatakanaQuiz(models.Model):
    code = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=120, unique=True)
    lesson = models.ForeignKey(KatakanaLesson, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"Quiz {self.code}: {self.name}"

    def get_questions(self):
        return self.katakanaquestion_set.all()

    class Meta:
        verbose_name_plural = 'Katakana quizzes'