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

# Create your models here.


class Subject(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    name = CharField(max_length=128, blank=False, null=False)


class AnswerCategory(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    name = CharField(max_length=128, blank=False, null=False)
    subject = ForeignKey(Subject, on_delete=models.CASCADE)


class Explanation(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    content = TextField()


class Question(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    content = TextField(blank=False, null=False)
    subject = ForeignKey(Subject, on_delete=models.CASCADE)
    image = ResizedImageField(
        quality=75,
        upload_to="./static/img/question/",
        force_format="JPEG",
        keep_meta=False,
        null=True,
    )
    audio = FileField(null=True, upload_to="./static/audio/")
    explanation = ForeignKey(Explanation, on_delete=models.SET_NULL, null=True)
    year = IntegerField(null=False, blank=False)


# Answers
class AnswerTrueFalse(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    content = TextField()
    correct = BooleanField(default=False, null=False)
    points = IntegerField(default=1, null=False)


class AnswerAZ(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    button_content = CharField(max_length=256, default='["A",]')
    correct = CharField(max_length=1, default="A", null=False)
    points = IntegerField(default=1, null=False)


class AnswerWithContent(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    content = TextField()
    correct = BooleanField(default=False, null=False)
    points = IntegerField(default=1, null=False)


class AnswerAZWithContent(models.Model):
    id = AutoField(primary_key=True, unique=True, null=False, db_index=True)
    button_content = CharField(max_length=256, default='["A",]')
    content = TextField()
    correct = BooleanField(default=False, null=False)
    points = IntegerField(default=1, null=False)
