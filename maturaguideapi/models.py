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
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django_resized import ResizedImageField




class Subject(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    name = CharField(
        max_length=128,
        blank=False,
        null=False,
        help_text="Nazwa przedmiotu np. Matematyka",
    )

    def __str__(self) -> str:
        return self.name

    def count_questions(self):
        return Question.objects.filter(subject=self).count()


# QuestionCategory will allow us to organize questions by type.
class QuestionCategory(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    name = CharField(
        max_length=128,
        blank=False,
        null=False,
        help_text="Nazwa kategori np. Słuchanie",
    )
    subject = ForeignKey(Subject, on_delete=models.CASCADE, help_text="Przedmiot")

    def __str__(self) -> str:
        return f"[{self.subject.name}] {self.name}"

    def count_questions(self) -> int:
        return Question.objects.filter(question_category = self).count()

# QuestionTag will allow us to organize the affiliation of the question to the materials
class QuestionTag(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    name = CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text="Nazwa tagu np. Jedzenie słownictwo",
    )
    subject = ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        help_text="Przedmiot",
    )
    def __str__(self) -> str:
        return f"[{self.subject.name}] {self.name}"

class Explanation(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    content = JSONField(
        null=False,
        blank=False,
        default=list,
        help_text="Wyjasnienia do zadań w postaci listy.",
    )


class Question(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    header = TextField(
        blank=False,
        null=False,
        help_text="Poczatek zadania który będzie wyświetlony grubą czcionką.",
    )
    content = TextField(blank=False, null=False, help_text="Zawartość zadania.")
    subject = ForeignKey(Subject, on_delete=models.CASCADE, help_text="Przedmiot")
    question_category = ForeignKey(QuestionCategory, on_delete=models.SET_NULL, null=True, help_text="Kategoria pytania.")
    question_tags = ManyToManyField(QuestionTag, help_text="Tagi pytania.")
    image = ResizedImageField(
        quality=75,
        upload_to="./static/img/question/",
        force_format="JPEG",
        keep_meta=False,
        null=True,
        blank=True,
        help_text="Dodatkowy obrazek do zadania, jeżeli null to pytanie nie będzie miało obrazu.",
    )
    audio = FileField(
        null=True,
        blank=True,
        upload_to="./static/audio/",
        help_text="Plik dźwiękowy do zadania, jeżeli null to pytanie nie będzie miało nagrania.",
    )
    year = IntegerField(
        null=False,
        blank=False,
        help_text="Rok w którym pytanie pojawiło się na egzaminie maturalnym.",
    )
    cke_order = IntegerField(
        null=True,
        blank=True,
        help_text="Numer zadania w arkuszu cke (jeżeli null to znaczy że zadanie nie pochodzi z arkusza CKE)"
    )
    def __str__(self) -> str:
        return f"[{self.id}] {self.subject} ({self.year}) - f{self.header[:30]}"

    def get_as_object(self) -> dict:
        audio_url = None if self.audio.name == "" else self.audio.url
        img_url = None if self.image.name == "" else self.image.url

        return {
            "id": self.id,
            "category": self.question_category.name,
            "content_img": img_url,
            "audio_url": audio_url,
            "answers": [answer.get_as_object() for answer in get_all_answers_for_question(self)],
            "have_explanations": self.have_explanations()
        }
    
    def get_list_of_all_answers(self) -> list:
        return get_all_answers_for_question(self)

    def have_explanations(self) -> bool:
        return any([answer.explanation is not None for answer in get_all_answers_for_question(self)])

# ANSWERS

# Simple True/False answer (type 1)
class AnswerTrueFalse(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    content = TextField(help_text="Zawartość pytania.")
    correct = BooleanField(
        default=False,
        null=False,
        help_text="Ktore pytanie jest poprawne? Jeżeli checkbox jest zaznaczony to prawidłowa jest prawda.",
    )
    points = IntegerField(
        default=1,
        null=False,
        help_text="Punkty które użytkownik dostaje za poprawną odpowiedź.",
    )
    question = ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        help_text="Połączenie z pytaniem.",
    )
    explanation = TextField(null=True, blank=True, help_text="Wyjaśnienie do pytania")

    def __str__(self) -> str:
        return f"[{self.id}] {self.content}"

    def get_as_object(self) -> dict:
        return {
            "type": 1,
            "answer_id": self.id,
            "content": self.content,
            "correct": self.correct,
            "points": self.points, 
        } 


# Answer with a choice of A to Z (type 2)
class AnswerAZ(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    buttons_content = JSONField(
        max_length=256, default=list, help_text="Zawartość przycisków w JSON."
    )
    correct = CharField(
        max_length=1,
        default="A",
        null=False,
        help_text="Zawartość prawidłowego buttona.",
    )
    points = IntegerField(
        default=1,
        null=False,
        help_text="Punkty które użytkownik dostaje za poprawną odpowiedź.",
    )
    question = ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        help_text="Połączenie z pytaniem.",
    )
    explanation = TextField(null=True, blank=True, help_text="Wyjaśnienie do pytania")

    def __str__(self) -> str:
        return f"[{self.id}] " + " ".join(self.buttons_content)

    def get_as_object(self) -> dict:
        return {
            "type": 2,
            "answer_id": self.id,
            "buttons_content": self.buttons_content,
            "correct": self.correct,
            "points": self.points, 
        } 

# Answer with content in buttons (type 3)
class AnswerWithContent(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    content = TextField()
    buttons_content = JSONField(
        null=False,
        blank=False,
        default=list,
        help_text="Teksty które będą pojawiały się koło przycisków.",
    )
    correct = IntegerField(
        default=False, null=False, help_text="Indeks poprawnej odpowiedzi."
    )
    points = IntegerField(
        default=1,
        null=False,
        help_text="Punkty które użytkownik dostaje za poprawną odpowiedź.",
    )
    question = ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        help_text="Połączenie z pytaniem.",
    )
    explanation = TextField(null=True, blank=True, help_text="Wyjaśnienie do pytania")

    def __str__(self) -> str:
        return f"[{self.id}] " + " ".join(self.buttons_content)

    def get_as_object(self) -> dict:
        return {
            "type": 3,
            "answer_id": self.id,
            "buttons_content": self.buttons_content,
            "correct": self.correct,
            "points": self.points, 
        } 

# Answer with a choice of A to Z and content (type 4)
class AnswerAZWithContent(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    buttons_content = JSONField(
        max_length=256, default=list, help_text="Zawartość przycisków w JSON."
    )
    content = TextField(help_text="Zawartość pytania.")
    correct = CharField(
        max_length=1,
        default="A",
        null=False,
        help_text="Zawartość prawidłowego buttona.",
    )
    points = IntegerField(
        default=1,
        null=False,
        help_text="Punkty które użytkownik dostaje za poprawną odpowiedź.",
    )
    question = ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        help_text="Połączenie z pytaniem.",
    )
    explanation = TextField(null=True, blank=True, help_text="Wyjaśnienie do pytania")

    def __str__(self) -> str:
        return f"[{self.id}] {self.content[:20]} " + " ".join(self.buttons_content)

    def get_as_object(self) -> dict:
        return {
            "type": 4,
            "answer_id": self.id,
            "content": self.content,
            "buttons_content": self.buttons_content,
            "correct": self.correct,
            "points": self.points,
        } 

def get_all_answers_for_question(question : Question) -> list:
    answers = []
    for AnswerClass in (AnswerTrueFalse, AnswerAZ, AnswerAZWithContent, AnswerWithContent):
        answers += AnswerClass.objects.filter(question=question)
    return answers