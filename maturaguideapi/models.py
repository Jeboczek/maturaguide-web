from django.db import models
from django.db.models.fields import (
    AutoField,
    BooleanField,
    CharField,
    IntegerField,
    TextField,
)
from django.db.models.fields.files import FileField
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey
from django_resized import ResizedImageField


class Subject(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    name = CharField(max_length=128, blank=False, null=False, help_text="Nazwa przedmiotu np. Matematyka")


# QuestionCategory will allow us to organize questions by type.
class QuestionCategory(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    name = CharField(max_length=128, blank=False, null=False, help_text="Nazwa kategori np. Słuchanie")
    subject = ForeignKey(Subject, on_delete=models.CASCADE, help_text="Przedmiot")


# QuestionTag will allow us to organize the affiliation of the question to the materials
class QuestionTag(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    name = CharField(max_length=255, null=False, blank=False, help_text="Nazwa tagu np. Jedzenie słownictwo")
    subject = ForeignKey(Subject, on_delete=models.CASCADE, null=False, blank=False, help_text="Przedmiot")


class Explanation(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    content = JSONField(null=False, blank=False, default=list, help_text="Wyjasnienia do zadań w postaci listy.")


class Question(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    header = TextField(blank=False, null=False, help_text="Poczatek zadania który będzie wyświetlony grubą czcionką.")
    content = TextField(blank=False, null=False, help_text="Zawartość zadania.")
    subject = ForeignKey(Subject, on_delete=models.CASCADE, help_text="Przedmiot")
    image = ResizedImageField(
        quality=75,
        upload_to="./static/img/question/",
        force_format="JPEG",
        keep_meta=False,
        null=True,
        help_text = "Dodatkowy obrazek do zadania, jeżeli null to pytanie nie będzie miało obrazu."
    )
    audio = FileField(null=True, upload_to="./static/audio/", help_text="Plik dźwiękowy do zadania, jeżeli null to pytanie nie będzie miało nagrania.")
    explanation = ForeignKey(Explanation, on_delete=models.SET_NULL, null=True, help_text="Połączenie z wyjaśnieniami.")
    year = IntegerField(null=False, blank=False, help_text="Rok w którym pytanie pojawiło się na egzaminie maturalnym.")


# ANSWERS

# Simple True/False answer (type 1)
class AnswerTrueFalse(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    content = TextField(help_text="Zawartość pytania.")
    correct = BooleanField(default=False, null=False, help_text="Ktore pytanie jest poprawne? Jeżeli checkbox jest zaznaczony to prawidłowa jest prawda.")
    points = IntegerField(default=1, null=False, help_text="Punkty które użytkownik dostaje za poprawną odpowiedź.")
    question = ForeignKey(Question, on_delete=models.CASCADE, null=True, help_text="Połączenie z pytaniem.")


# Answer with a choice of A to Z (type 2)
class AnswerAZ(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    button_content = JSONField(max_length=256, default=list, help_text="Zawartość przycisków w JSON.")
    correct = CharField(max_length=1, default="A", null=False, help_text="Zawartość prawidłowego buttona.")
    points = IntegerField(default=1, null=False, help_text="Punkty które użytkownik dostaje za poprawną odpowiedź.")
    question = ForeignKey(Question, on_delete=models.CASCADE, null=True, help_text="Połączenie z pytaniem.")


# Answer with content in buttons (type 3)
class AnswerWithContent(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    content = TextField()
    buttons_content = JSONField(null=False, blank=False, default=list, help_text="Teksty które będą pojawiały się koło przycisków.")
    correct = IntegerField(default=False, null=False, help_text="Indeks poprawnej odpowiedzi.")
    points = IntegerField(default=1, null=False, help_text="Punkty które użytkownik dostaje za poprawną odpowiedź.")
    question = ForeignKey(Question, on_delete=models.CASCADE, null=True, help_text="Połączenie z pytaniem.")


# Answer with a choice of A to Z and content (type 4)
class AnswerAZWithContent(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    button_content = JSONField(max_length=256, default=list, help_text="Zawartość przycisków w JSON.")
    content = TextField(help_text="Zawartość pytania.")
    correct = CharField(max_length=1, default="A", null=False, help_text="Zawartość prawidłowego buttona.")
    points = IntegerField(default=1, null=False, help_text="Punkty które użytkownik dostaje za poprawną odpowiedź.")
    question = ForeignKey(Question, on_delete=models.CASCADE, null=True, help_text="Połączenie z pytaniem.")
