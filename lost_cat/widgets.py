from django import forms
import datetime

class DateTimeMultiWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.Select(choices=[(year, f"{year}年") for year in range(2010, datetime.datetime.now().year + 1)]),
            forms.Select(choices=[(month, f"{month}月") for month in range(1, 13)]),
            forms.Select(choices=[(day, f"{day}日") for day in range(1, 32)]),
            forms.Select(choices=[(hour, f"{hour}時") for hour in range(0, 24)]),
            forms.Select(choices=[(minute, f"{minute}分") for minute in range(0, 60, 5)]),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [
                value.year,
                value.month,
                value.day,
                value.hour,
                value.minute,
            ]
        return [None, None, None, None, None]

    def value_from_datadict(self, data, files, name):
        try:
            year = int(data.get(f"{name}_0"))
            month = int(data.get(f"{name}_1"))
            day = int(data.get(f"{name}_2"))
            hour = int(data.get(f"{name}_3"))
            minute = int(data.get(f"{name}_4"))
            return datetime.datetime(year, month, day, hour, minute)
        except (ValueError, TypeError):
            return None
