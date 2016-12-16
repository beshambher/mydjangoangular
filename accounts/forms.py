from django.contrib.auth import authenticate, get_user_model, login, logout

from django import forms
from .models import Profile

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("This user does not exist.")
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect Password.")
        if not user.is_active:
            raise forms.ValidationError("This user is no longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_qs = User.objects.filter(email=email)

        if email_qs.exists():
            raise forms.ValidationError("This Email is already been registered.")

        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords Do not match.")

        return confirm_password


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'content'
        ]




