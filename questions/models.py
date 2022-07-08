from django.db import models
from quizzes.models import HiraganaQuiz, KatakanaQuiz
from lessons.models import HiraganaLetter, KatakanaLetter

# Create your models here.

class HiraganaQuestion(models.Model):
    text = models.ForeignKey(HiraganaLetter, on_delete=models.CASCADE)
    quiz = models.ForeignKey(HiraganaQuiz, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.hiraganaanswer_set.all()
    
    def get_correct_answer(self):
        return self.hiraganaanswer_set.get(correct=True)

class HiraganaAnswer(models.Model):
    text = models.ForeignKey(HiraganaLetter, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(HiraganaQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

class KatakanaQuestion(models.Model):
    text = models.ForeignKey(KatakanaLetter, on_delete=models.CASCADE)
    quiz = models.ForeignKey(KatakanaQuiz, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.katakanaanswer_set.all()

    def get_correct_answer(self):
        return self.katakanaanswer_set.get(correct=True)

class KatakanaAnswer(models.Model):
    text = models.ForeignKey(KatakanaLetter, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(KatakanaQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

