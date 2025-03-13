from django import forms

class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=255, required=False)

class ExampleForm(forms.Form):
    """
    ExampleForm: A sample form to demonstrate Django's built-in form validation.
    """
    name = forms.CharField(max_length=100, required=True, help_text="Enter your name")
    email = forms.EmailField(required=True, help_text="Enter a valid email")
    message = forms.CharField(widget=forms.Textarea, required=True, help_text="Enter your message")
