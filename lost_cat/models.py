from django.db import models
from django.conf import settings

class Lostcat(models.Model):
    STATUS_CHOICES = [
        ('protected', '保護'),
        ('lost', '迷子'),
    ]
    SEX_CHOICES = [
        ('male_neutering', 'オス（去勢済）'),
        ('male_not_neutering', 'オス（去勢未）'),
        ('female_spaying', 'メス（避妊済）'),
        ('female_not_spaying', 'メス（避妊未）'),
        ('not_clear', '不明'),
    ]
    EAR_CHOICES = [
        ('not_sakura_cat', 'なし'),
        ('sakura_cat_right', 'あり（右）'),
        ('sakura_cat_left', 'あり（左）'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='lost',
    )
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='lost_cat'
    )
    name = models.CharField(max_length=8)
    lost_datetime = models.DateTimeField(null=True, blank=True)
    lost_location = models.CharField(max_length=18, blank=True, null=True)
    age_years = models.PositiveIntegerField(default=0)
    age_months = models.PositiveIntegerField(default=0)
    sex = models.CharField(
        max_length=20,
        choices=SEX_CHOICES,
        default='male_neutering',
    )
    ear_cut = models.CharField(
        max_length=20,
        choices=EAR_CHOICES,
        default='not_sakura_cat',
    )
    description1 = models.TextField(max_length=17,blank=True, null=True)
    description2 = models.TextField(max_length=17,blank=True, null=True)

    description_collar = models.TextField(max_length=7,blank=True, null=True)
    description_eye = models.TextField(max_length=6,blank=True, null=True)

    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='photos/', blank=True, null=True)
    photo3 = models.ImageField(upload_to='photos/', blank=True, null=True)

    def get_lost_datetime_display(self):
        if self.lost_datetime:
            return self.lost_datetime.strftime("%Y年%m月%d日 %H時%M分頃")
        return "未登録"

    def __str__(self):
        return self.name
    
class SightingReport(models.Model):
    lostcat = models.ForeignKey(Lostcat, on_delete=models.CASCADE, related_name="sighting_reports")
    situation = models.TextField(max_length=255, blank=True, null=True)
    lost_datetime = models.DateTimeField(null=True, blank=True)
    lost_location = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='photos/', blank=True, null=True)
    photo3 = models.ImageField(upload_to='photos/', blank=True, null=True)
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        verbose_name="電話番号",
        help_text="連絡が必要な場合に備えて、電話番号を任意で入力できます"
    )
    email = models.EmailField(
        blank=True, 
        null=True, 
        verbose_name="メールアドレス",
        help_text="連絡が必要な場合に備えて、メールアドレスを任意で入力できます"
    )

    def get_lost_datetime_display(self):
        if self.lost_datetime:
            return self.lost_datetime.strftime("%Y年%m月%d日 %H時%M分頃")
        return "未登録"
    
    def __str__(self):
        return f"目撃情報: {self.lostcat.name}"

class ResolvedLostCat(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='resolved_cats/', default='resolved_cats/no-image.jpg', blank=True)
    resolved_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.name