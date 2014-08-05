from django.contrib.auth.forms import UserCreationForm as UCF
from captcha.fields import CaptchaField

class UserCreationForm(UCF):
    captcha = CaptchaField()
