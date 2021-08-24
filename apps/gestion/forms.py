# Third party integration
from django_select2 import forms as s2forms
from django import forms


class NAPFormAdmin(forms.ModelForm):
     widgets = {
            "Spliiter_principal": s2forms.ModelSelect2Widget(
                model="gestion.Spliiter_principal",
                search_fields=[
                    "Numero_Puerto__icontains",
                ],
                dependent_fields={"subprogram": "subprograms"},
                max_results=100,
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
            }