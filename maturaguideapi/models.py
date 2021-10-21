from typing import List
import re
from django.db import models
from django.db.models.fields import (
    AutoField,
    CharField,
    SmallIntegerField,
    TextField,
)
from django.db.models.fields.files import FileField
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django_resized import ResizedImageField


class Subject(models.Model):
    BASIC = "P"
    EXTENDED = "R"
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    name = CharField(
        max_length=128,
        blank=False,
        null=False,
        help_text="Nazwa przedmiotu np. Matematyka",
    )
    subject_type = CharField(
        max_length=1,
        choices=[(BASIC, "Podstawowy"), (EXTENDED, "Rozserzony")],
        blank=False,
        null=False,
        help_text="Typ przedmiotu rozserzony, podstawowy",
    )

    def get_as_object(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.subject_type,
        }

    def get_categories(self) -> list:
        return QuestionCategory.objects.filter(subject=self)

    def __str__(self) -> str:
        return f"[{self.id}] {self.subject_type}{self.name}"


class QuestionCategory(models.Model):
    id = AutoField(primary_key=True, null=False, blank=False)
    name = CharField(max_length=128, null=False, blank=False)
    subject = ManyToManyField(Subject)

    def __str__(self) -> str:
        return f"[{self.id}] - {self.name}"


class Excercise(models.Model):
    id = AutoField(primary_key=True, null=False, blank=False)
    audio = FileField(
        null=True,
        blank=True,
        upload_to="./static/audio/",
        help_text="Plik dźwiękowy do zadania, jeżeli null to pytanie nie będzie miało nagrania.",
    )
    image = ResizedImageField(
        quality=75,
        upload_to="./static/img/question/",
        force_format="JPEG",
        keep_meta=False,
        null=True,
        blank=True,
        help_text="Dodatkowy obrazek do zadania, jeżeli null to pytanie nie będzie miało obrazu.",
    )
    header = TextField(default=None, null=True, blank=True)
    content = TextField(default=None, null=True, blank=True)
    footer = TextField(default=None, null=True, blank=True)
    more_text = TextField(default=None, null=True, blank=True)

    def _delete_newline_from_content(self, content) -> str:
        return content.replace("\n", "").replace("\r", "")

    def _format_content(self, content, question_nr) -> str:
        splitted = re.split(r"\d\.\d\. _{5}", content)
        if len(splitted) > 1:
            content = ""
            for i, o in enumerate(splitted):
                content += o
                if i >= 0 and i < len(splitted)-1:
                    content += f" {question_nr}.{i+1}. _____ "
        return content

    def __str__(self) -> str:
        return f"[{self.id}] {self.header[:50]}"

    def get_as_object(self, question_nr) -> dict:
        return {
            "id": self.id,
            "header": self.header,
            "content": self._format_content(self._delete_newline_from_content(self.content), question_nr),
            "footer": self.footer,
            "more_text": self.more_text,
            "audio": None if self.audio.name == "" else self.audio.url,
            "img": None if self.image.name == "" else self.image.url,
            "excercise_contents": [
                answer.get_as_object(f"{question_nr}.{x}")
                for x, answer in enumerate(Answer.objects.filter(excercise=self), 1)
            ],
        }


class Question(models.Model):
    id = AutoField(primary_key=True, null=False, blank=False)
    subject = ForeignKey(Subject, on_delete=models.CASCADE)
    category = ForeignKey(QuestionCategory, on_delete=models.CASCADE)
    content = TextField()
    cke_year = SmallIntegerField(null=True, blank=True)
    cke_order = SmallIntegerField(null=True, blank=True)
    excercise = ForeignKey(Excercise, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"[{self.id}] {self.content[:50]}"

    def get_as_object(self, question_nr="") -> dict:
        return {
            "id": self.id,
            "category": self.category.name,
            "title": f"Zadanie {question_nr}",
            "content": self.content,
            "excercise": self.excercise.get_as_object(question_nr),
        }


class Explanation(models.Model):
    id = AutoField(primary_key=True, null=False, blank=False)
    content = TextField()

    def __str__(self) -> str:
        return f"[{self.id}] {self.content[:20]}"

    def get_as_object(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
        }


class Answer(models.Model):
    TRUEFALSE = 1
    AZ = 2
    BUTTONCONTENT = 3
    TEXTANDAZ = 4

    id = AutoField(primary_key=True, null=False, blank=False)
    question_type = models.SmallIntegerField(
        choices=[
            (TRUEFALSE, "Prawda, fałsz"),
            (AZ, "Przyciski od A - Z"),
            (BUTTONCONTENT, "Przyciski z zawartością"),
            (TEXTANDAZ, "Tekst z przyciskami A - Z"),
        ]
    )
    button_content = JSONField(null=True, blank=True, default=list)
    content = CharField(max_length=512, null=True, blank=True)
    to_button = CharField(max_length=1, default="Z", null=True, blank=True)
    excercise = ForeignKey(Excercise, on_delete=models.CASCADE, null=False, blank=False)
    explanation = ForeignKey(
        Explanation, on_delete=models.CASCADE, blank=True, null=True
    )
    correct = CharField(max_length=1, blank=False, null=False)


    def __str__(self):
        return f"[{self.id}] - type {self.question_type} | {self.excercise}"

    def _get_content(self, answer_nr="") -> str:
        return answer_nr if self.content is None else f"{answer_nr} {self.content}"

    def _get_answers(self) -> list:
        if self.question_type == 1:
            return [{"index": "T", "content": None}, {"index": "F", "content": None}]
        elif self.question_type == 2:
            return [
                {"index": chr(x), "content": None}
                for x in range(ord("A"), ord(self.to_button) + 1)
            ]
        elif self.question_type == 3:
            return [
                {"index": chr(x), "content": content}
                for x, content in zip(
                    range(ord("A"), ord(self.to_button) + 1), self.button_content
                )
            ]
        elif self.question_type == 4:
            return [
                {
                    "index": chr(x),
                    "title": title,
                    "header": header,
                    "footer": footer,
                    "content": content
                }
                for x, title, header, footer, content in zip(
                    range(ord("A"), ord(self.to_button) + 1),
                    self.title,
                    self.button_content,
                    self.header,
                    self.footer,
                    self.content
                )
            ]

    def get_as_object(self, answer_nr="") -> dict:
        return {
            "id": self.id,
            "type": self.question_type,
            "content": self._get_content(answer_nr),
            "answers": self._get_answers(),
            "explanation": None
            if self.explanation is None
            else self.explanation.get_as_object(),
            "correct": self.correct,
        }


class StudySource(models.Model):
    id = AutoField(primary_key=True, null=False, blank=False)
    header = CharField(max_length=255)
    title = CharField(max_length=255)
    link = CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
