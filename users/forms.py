from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'loginUsername'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'loginPassword'
        })
    )

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'loginUsername'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'registerEmail'
        }),
        required=True
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'registerPassword'}),
        help_text='Минимум 8 символов'
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'registerConfirmPassword'})
    )

    terms_accepted = forms.BooleanField(
        label='Принимаю условия',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'termsCheck'
        }),
        required=True,
        error_messages={
            'required': 'Вы должны принять условия использования'
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
       

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже используется")
        return email
    


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'full_name', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({'id': 'id_avatar'})


class CustomPasswordChangeForm(PasswordChangeForm):
    error_css_class = 'is-invalid'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'id': 'currentPasswordInput',
            'placeholder': 'Введите текущий пароль'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'newPasswordInput',
            'placeholder': 'Введите новый пароль'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'confirmPasswordInput',
            'placeholder': 'Повторите новый пароль'
        })