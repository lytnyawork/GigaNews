from django import forms
from django.core.validators import validate_integer

class ReactionForm(forms.Form):
    article_id = forms.IntegerField(
        validators=[validate_integer],
        widget=forms.HiddenInput()
    )
    reaction_type_id = forms.IntegerField(
        validators=[validate_integer],
        widget=forms.HiddenInput()
    )