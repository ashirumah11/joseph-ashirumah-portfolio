from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Bot honeypot field (hidden from real users via CSS & widget)
    confirm_website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'tabindex': '-1',
            'aria-hidden': 'true',
            'class': 'd-none',
        })
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Your Full Name',
                'autocomplete': 'name',
                'id': 'id_contact_name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'your.email@example.com',
                'autocomplete': 'email',
                'id': 'id_contact_email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Project inquiry, engineering role, or collaboration',
                'id': 'id_contact_subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Tell me about the software challenge, system requirements, or role...',
                'rows': 5,
                'id': 'id_contact_message',
            }),
        }

    def clean_confirm_website(self):
        # Honeypot validation
        honeypot = self.cleaned_data.get('confirm_website')
        if honeypot:
            raise forms.ValidationError("Spam detected.")
        return honeypot

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please provide your name (at least 2 characters).")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError("Please write a meaningful message (at least 10 characters).")
        return message
