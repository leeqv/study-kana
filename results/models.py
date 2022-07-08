from django.db import models
from django.contrib.auth.models import User
from quizzes.models import HiraganaQuiz, KatakanaQuiz
from lessons.models import HiraganaLesson, HiraganaLetter, KatakanaLesson, KatakanaLetter
from questions.models import HiraganaQuestion, KatakanaQuestion

# Create your models here.

class HiraganaResult(models.Model):
    quiz = models.ForeignKey(HiraganaQuiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(help_text="score in %")

    def __str__(self):
        return f"{self.user} scored {self.score}% in {self.quiz}"

class KatakanaResult(models.Model):
    quiz = models.ForeignKey(KatakanaQuiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(help_text="score in %")

    def __str__(self):
        return f"{self.user} scored {self.score}% in {self.quiz}"

class Trophy(models.Model):
    code = models.CharField(max_length=120, null=True, blank=True)
    name = models.CharField(max_length=120)
    desc = models.CharField(max_length=250)

    def __str__(self):
       return f'{self.code}: "{self.name}" trophy'

    class Meta:
        verbose_name_plural = 'Trophies'
        ordering = ('code',)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    trophies = models.ManyToManyField(Trophy, blank=True)
    
    current_H_lesson = models.ForeignKey(HiraganaLesson, related_name="current_users", on_delete=models.SET_NULL, null=True, blank=True)
    finished_H_lessons = models.ManyToManyField(HiraganaLesson, blank=True) 
    hiragana_watchlist = models.ManyToManyField(HiraganaLetter, blank=True)
    failed_H_questions = models.ManyToManyField(HiraganaQuestion, blank=True)

    current_K_lesson = models.ForeignKey(KatakanaLesson, related_name="current_users", on_delete=models.SET_NULL, null=True, blank=True)
    finished_K_lessons = models.ManyToManyField(KatakanaLesson, blank=True)
    katakana_watchlist = models.ManyToManyField(KatakanaLetter, blank=True)
    failed_K_questions = models.ManyToManyField(KatakanaQuestion, blank=True)

    def __str__(self):
       return f'User profile of "{self.user}"'

    def get_H_results(self):
        return self.hiraganaresult_set.all()

    def get_K_results(self):
        return self.katakanaresult_set.all()