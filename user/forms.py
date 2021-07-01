from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user.models import Account


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'email', ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('email') is None:
            self._errors['email'] = self._errors.get('email', [])
            self._errors['email'].append('Please Enter Your Email Address')
        return cleaned_data


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'phone', 'birthday', 'gender', 'avatar']
