from django import forms
from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "title",
            "director",
            "genre",
            "release_date",
        ]

        widgets = {
            "release_date": forms.DateInput(
                attrs={"type": "date"}
            )
        }