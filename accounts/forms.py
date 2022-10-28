from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django import forms
from accounts.models import Profile

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

class UpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')
        labels = {
            'email' : '이메일',
            'first_name' : '이름',
            'last_name' : '성'
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'status_message']
        labels = {
            'image' : '프로필 이미지',
            'status_message' : '상태메시지',
        }