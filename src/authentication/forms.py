from django import forms
from django.contrib.auth.forms import AuthenticationForm

from authentication.models import User, UserProfile
from django.contrib.auth.models import Group


class LoginForm(AuthenticationForm):
    error_css_class = 'is-invalid'

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter your email'}
    ), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter your password'}
    ), required=True)


class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'minlength': 8
        }
    ))
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput(
            attrs={
                'minlength': 8
            }
        ))

    email = forms.EmailField(required=True, max_length=100, widget=forms.TextInput())
    first_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput())
    last_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput())
    company_name = forms.CharField(max_length=100, widget=forms.TextInput())
    phone = forms.CharField(max_length=100, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', "first_name", "last_name", "company_name", "phone")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        group = Group.objects.filter(name='customer').first()
        user.is_active = False
        if commit:
            user.save()
        group.user_set.add(user)
        return user


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['company_name', 'phone', 'first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserProfile
        fields = '__all__'
