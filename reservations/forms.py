from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out','guests']

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        guests = cleaned_data.get('guests')

        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Check-out must be after check-in.")

        if guests and guests <= 0:
            raise forms.ValidationError("Number of guests must be greater than zero.")

        return cleaned_data
