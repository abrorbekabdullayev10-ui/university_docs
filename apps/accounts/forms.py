from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Role
from apps.groups.models import Group


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    full_name = forms.CharField(max_length=150, required=True, label="Ism Familiya")
    role = forms.ChoiceField(choices=Role.choices, label="Rol")
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), 
        required=False, 
        label="Guruh (Faqat o'quvchilar uchun)",
        empty_label="Guruhni tanlang"
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'role', 'group', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Login"
        self.fields['password1'].label = "Parol"
        self.fields['password2'].label = "Parolni tasdiqlash"


class TeacherAddStudentForm(forms.ModelForm):
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'group']
        labels = {
            'username': "Login",
            'full_name': "Ism Familiya",
            'email': "Email",
            'group': "Guruhga biriktirish"
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'student'
        if commit:
            user.save()
        return user