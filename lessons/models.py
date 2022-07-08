from django.db import models

# Create your models here.

class HiraganaLesson(models.Model):
    code = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=60, unique=True)
    order = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Hiragana Lesson {self.code}: {self.name}"

    def get_letters(self):
        return self.letters.all().order_by("order")

class HiraganaLetter(models.Model):
    kana = models.CharField(max_length=20)
    romaji = models.CharField(max_length=20)
    ex_kana = models.CharField(max_length=30)
    ex_romaji = models.CharField(max_length=30)
    ex_english = models.CharField(max_length=30)
    ex_emoji = models.CharField(max_length=20)
    strokeorder_img = models.FileField(upload_to='images/lessons/hiragana_stroke_order',null=True, blank=True)
    kana_img = models.FileField(upload_to='images/lessons/hiragana_kana',null=True, blank=True)
    lesson = models.ForeignKey(HiraganaLesson, related_name="letters", on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kana} ({self.romaji})"

class KatakanaLesson(models.Model):
    code = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=60, unique=True)
    order = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Katakana Lesson {self.code}: {self.name}"

    def get_letters(self):
        return self.letters.all().order_by("order")

class KatakanaLetter(models.Model):
    kana = models.CharField(max_length=20)
    romaji = models.CharField(max_length=20)
    ex_kana = models.CharField(max_length=30)
    ex_romaji = models.CharField(max_length=30)
    ex_english = models.CharField(max_length=30)
    ex_emoji = models.CharField(max_length=20)
    strokeorder_img = models.FileField(upload_to='images/lessons/katakana_stroke_order',null=True, blank=True)
    kana_img = models.FileField(upload_to='images/lessons/katakana_kana',null=True, blank=True)
    lesson = models.ForeignKey(KatakanaLesson, related_name="letters", on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kana} ({self.romaji})"