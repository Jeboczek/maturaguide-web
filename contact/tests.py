from django.test import TestCase, RequestFactory
from contact.models import Message, MessageReason
from .forms import MessageForm
from captcha.client import RecaptchaResponse
from unittest.mock import patch



class ContactTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.test_reason = MessageReason(name="test").save()

    def response_validator(self, response, invalid = False):
        self.assertEqual(response.status_code, 200)
        if(invalid):
            self.assertEqual(len(response.redirect_chain), 0)
        else:
            self.assertGreater(len(response.redirect_chain), 0)
            self.assertEqual(response.redirect_chain[-1][0].replace("/", ""), "kontaktsuccess")


    @patch("captcha.fields.client.submit")
    def test_valid_message_form(self, mocked_submit):
        mocked_submit.resturn_value = RecaptchaResponse(is_valid=True)
        response = self.client.post(
            "/kontakt/",
            {
                "firstname": "user",
                "email": "user@example.com",
                "phonenumber": "543213432",
                "reason": "1",
                "content": "TEST",
                "g-recaptcha-response": "PASSED",
            },
            follow=True,
        )

        self.response_validator(response)

    @patch("captcha.fields.client.submit")
    def test_empty_number(self, mocked_submit):
        mocked_submit.resturn_value = RecaptchaResponse(is_valid=True)
        response = self.client.post(
            "/kontakt/",
            {
                "firstname": "user",
                "email": "user@example.com",
                "phonenumber": "",
                "reason": "1",
                "content": "TEST",
                "g-recaptcha-response": "PASSED",
            },
            follow=True,
        )

        self.response_validator(response)


    @patch("captcha.fields.client.submit")
    def test_invalid_number(self, mocked_submit):
        mocked_submit.resturn_value = RecaptchaResponse(is_valid=True)
        response = self.client.post(
            "/kontakt/",
            {
                "firstname": "user",
                "email": "user@example.com",
                "phonenumber": "gfdsafews",
                "reason": "1",
                "content": "TEST",
                "g-recaptcha-response": "PASSED",
            },
            follow=True,
        )
        self.response_validator(response, invalid=True)

    @patch("captcha.fields.client.submit")
    def test_phone_unformating(self, mocked_submit):
        mocked_submit.resturn_value = RecaptchaResponse(is_valid=True)
        response = self.client.post(
            "/kontakt/",
            {
                "firstname": "user",
                "email": "user@example.com",
                "phonenumber": "+48666666666",
                "reason": "1",
                "content": "TEST",
                "g-recaptcha-response": "PASSED",
            },
            follow=True,
        )
        self.response_validator(response)
    
    @patch("captcha.fields.client.submit")
    def test_unicode(self, mocked_submit):
        mocked_submit.resturn_value = RecaptchaResponse(is_valid=True)
        response = self.client.post(
            "/kontakt/",
            {
                "firstname": "żółć",
                "email": "user@example.com",
                "phonenumber": "+48666666666",
                "reason": "1",
                "content": "TEST",
                "g-recaptcha-response": "PASSED",
            },
            follow=True,
        )
        self.response_validator(response)
        self.assertEqual(Message.objects.last().firstname, "żółć")

