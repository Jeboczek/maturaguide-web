from django import forms
from django.core.exceptions import ValidationError
from .models import MessageReason, Message
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

import re
from string import digits

class MessageForm(forms.Form):
    firstname = forms.CharField(max_length=128, required=True, label="Twoje imie", widget=forms.TextInput(attrs={"placeholder": "Jakub"}))
    email = forms.EmailField(required=True, label="Adres e-mail", widget=forms.EmailInput(attrs={"placeholder": "jakub@example.com"}))
    phonenumber = forms.CharField(required=False, label="Numer telefonu (opcjonalnie)", widget=forms.TextInput(attrs={"placeholder": "666666666"}))
    reason = forms.ModelChoiceField(queryset=MessageReason.objects.all(), required=True, label="Przyczyna ")
    content = forms.CharField(max_length=1024, required=True, label="Wiadomość", widget=forms.Textarea(attrs={"placeholder": "Treść wiadomości..."}))
    captcha = ReCaptchaField(label="Captcha", widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Message
        fields = [
            "firstname",
            "email",
            "phonenumber",
            "reason"
        ]
    
    def clean_phonenumber(self, *args, **kwargs):
        ph = self.cleaned_data.get("phonenumber")
        if ph is None:
            return None
        else:
            ph = ph.replace(" ", "")
            ph = re.sub(r"^(\+48)", "", ph)
            if (len(ph) != 9 or any([digits.find(ph_number) == -1 for ph_number in ph])):
                raise forms.ValidationError("Niepoprawny numer telefonu, upewnij się że ma 9 liczb.")
            else:
                return ph

    def clean_content(self, *args, **kwargs):
        content = self.cleaned_data.get("content")
        if (len(content) > 1024):
            raise forms.ValidationError("Wiadomość nie może być dłuższa niż 1024 znaki.")
        else:
            return content
    
    def save(self, commit=True, *args, **kwargs) -> Message:
        message = Message()
        
        message.firstname = self.cleaned_data.get("firstname")
        message.email = self.cleaned_data.get("email")
        message.phonenumber = self.cleaned_data.get("phonenumber")
        message.reason = self.cleaned_data.get("reason")
        message.content = self.cleaned_data.get("content")

        if commit:
            message.save()

        return message