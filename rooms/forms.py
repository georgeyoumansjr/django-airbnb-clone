from django import forms
from django.forms import ModelForm
from rooms.models import RoomType, Amenity, Facility, Room
from django_countries.fields import CountryField


class SearchForm(forms.Form):
    """Room application search form

    Inherit:
        forms.Form

    Field:
        city         : CharField
        country      : CountryField.formfield
        room_type    : ModelChoiceField (RoomType)
        price        : IntegerField
        guests       : IntegerField
        bedrooms     : IntegerField
        beds         : IntegerField
        baths        : IntegerField
        instant_book : BooleanField
        is_superhost : BooleanField
        amenities    : ModelMultipleChoiceField (Amenity)
        facilities   : ModelMultipleChoiceField (Facility)
    """

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any Kind", queryset=RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    is_superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


# class ReservationForm(ModelForm):
#     class Meta:
#         model = Room
#         fields = ["name", "check_in", "check_out", "guests"]

#     def clean(self):
#         cleaned_data = super().clean()
#         check_in = cleaned_data.get("check_in")
#         check_out = cleaned_data.get("check_out")

#         if check_in and check_out and check_out <= check_in:
#             raise forms.ValidationError("Check-out must be after check-in.")

#         return cleaned_data

