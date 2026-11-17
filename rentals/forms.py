
from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle

        fields = [
            'category',
            'name',
            'brand',
            'model_year',
            'description',
            'daily_price',
            'seats',
            'transmission',
            'fuel_type',
            'main_image',
        ]

        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your vehicle...'
            }),

            'model_year': forms.NumberInput(attrs={
                'placeholder': 'e.g. 2024'
            }),

            'daily_price': forms.NumberInput(attrs={
                'placeholder': 'Price per day in NPR',
                'step': '0.01'
            }),

            'seats': forms.NumberInput(attrs={
                'placeholder': 'Number of seats'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = (
            self.fields['category'].queryset.filter(
                is_active=True
            )
        )
