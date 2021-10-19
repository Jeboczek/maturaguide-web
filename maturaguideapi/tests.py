from django.test import TestCase, RequestFactory
from .views import MaturaGuideAPIViews
from .models import Subject

import json

# Create your tests here.

class TestGenerateQuiz(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.subject = Subject(name="test_subject")
        self.subject.save()
    
    def test_generate_quiz_without_subject_id(self):
        request = self.factory.get("/api/generate_quiz")
        resp = MaturaGuideAPIViews.generate_quiz(request)
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content.decode("utf-8"))
        self.assertEqual(content["error"], 1)

    def test_generate_quiz_with_bad_subject_id(self):
        request = self.factory.get("/api/generate_quiz?subject_id=1000")
        resp = MaturaGuideAPIViews.generate_quiz(request)
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content.decode("utf-8"))
        self.assertEqual(content["error"], 1)

    def test_generate_quiz_with_success(self):
        request = self.factory.get(f"/api/generate_quiz?subject_id={self.subject.id}")
        resp = MaturaGuideAPIViews.generate_quiz(request)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content.decode("utf-8"))
        self.assertEqual(type(content), list)

class TestSubjectApi(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    def test_subject_api_without_subjects(self):
        # Delete old subjects
        [ subject.delete() for subject in Subject.objects.all() ]
        request = self.factory.get("/api/get_subjects/")
        response = MaturaGuideAPIViews.get_subjects(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), "[]")
    def test_subject_api_with_one_subject(self):
        sub = Subject(name="TEST", subject_type="R")
        sub.save()
        # Get an ID from the newly created Subject. Because the DBMS may allocate a number other than 1.
        id = sub.id
        self.assertEqual(Subject.objects.count(), 1)

        request = self.factory.get("/api/get_subjects/")
        response = MaturaGuideAPIViews.get_subjects(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), json.dumps([{"id": id, "name": "TEST", "type": "R"}]))

