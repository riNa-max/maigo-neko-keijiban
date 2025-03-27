from django import forms
from .models import Lostcat,SightingReport
from .widgets import DateTimeMultiWidget

class LostcatForm(forms.ModelForm):
    class Meta:
        model = Lostcat
        fields = ['name', 'description1', 'description2', 'description_collar', 'description_eye', 'status', 'sex', 'age_years', 'age_months', 'lost_datetime', 'photo', 'photo2', 'photo3', 'lost_location',]
        widgets = {
            'status': forms.RadioSelect,
            'age_years': forms.Select(choices=[(i, f"{i}歳") for i in range(21)]),
            'age_months': forms.Select(choices=[(i, f"{i}ヶ月") for i in range(12)]),
            'lost_datetime': DateTimeMultiWidget(),
            "lost_location": forms.TextInput(attrs={
                "placeholder": "大阪府大阪市淀川区三国本町１丁目"
            })
        }

    def clean_lost_datetime(self):
        data = self.cleaned_data.get('lost_datetime')
        if data is None: 
            return None
        return data

class LostSightingForm(forms.ModelForm):
    lost_datetime = forms.DateTimeField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        label="目撃日時"
    )
    
    class Meta:
        model = SightingReport
        fields = ['situation', 'lost_datetime', 'lost_location', 'photo', 'photo2', 'photo3', 'phone_number', 'email']

class ProtectedSightingForm(LostSightingForm):
    pass