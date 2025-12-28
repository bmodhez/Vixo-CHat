from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'displayname', 'info']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-gray-700 file:text-white hover:file:bg-gray-600',
            }),
            'displayname': forms.TextInput(attrs={
                'placeholder': 'Add display name',
                'class': 'w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-4 py-3 outline-none focus:border-emerald-500',
            }),
            'info': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add information',
                'class': 'w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-4 py-3 outline-none focus:border-emerald-500',
            })
        }