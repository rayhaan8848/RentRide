
from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'pickup_date',
            'return_date',
            'customer_note',
        ]

        widgets = {
            'pickup_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),

            'return_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),

            'customer_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests? (Optional)',
            }),
        }
