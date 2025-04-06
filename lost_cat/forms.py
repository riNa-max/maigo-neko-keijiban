from django import forms
from .models import Lostcat,SightingReport
from .widgets import DateTimeMultiWidget
import re

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
                "placeholder": "例）大阪府大阪市淀川区三国本町１丁目（最大18文字）",
                "maxlength": "18"
            }),
            "description_collar": forms.TextInput(attrs={
                "placeholder": "例）青い魚柄（最大7文字）",
                "maxlength": "7"
            }),
            "description_eye": forms.TextInput(attrs={
                "placeholder": "例）緑色（最大6文字）",
                "maxlength": "6"    
            }),
            "description1": forms.TextInput(attrs={
                "placeholder": "例）フワフワした鍵しっぽ（最大17文字）",
                "maxlength": "17"
            }),
            "description2": forms.TextInput(attrs={
                "placeholder": "例）非常にビビりで、家族以外近づかない（最大17文字）",
                "maxlength": "17"
            }),
            "name": forms.TextInput(attrs={
                "placeholder": "例）ジジ（最大8文字）",
                "maxlength": "8"
            }),
        }

class LostSightingForm(forms.ModelForm):
    lost_datetime = forms.DateTimeField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        label="目撃日時"
    )

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '')
        if phone:
            pattern = r'^\d{2,4}-?\d{2,4}-?\d{4}$'
            if not re.match(pattern, phone):
                raise forms.ValidationError("※電話番号の形式が正しくありません。")
        return phone
    class Meta:
        model = SightingReport
        fields = ['situation', 'lost_datetime', 'lost_location', 'photo', 'photo2', 'photo3', 'phone_number', 'email']
        widgets = {
            "lost_location": forms.TextInput(attrs={
                "placeholder": "例）〇〇さんの家の裏庭の塀の上"
            }),
            "situation": forms.TextInput(attrs={
                "placeholder": "例）怪我はなく、〇〇さんの軒下の隠れていった"
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '000-0000-0000'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'example@example.com'
            }),
        }

class ProtectedSightingForm(LostSightingForm):
    pass