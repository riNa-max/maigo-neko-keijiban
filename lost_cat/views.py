from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView,DetailView,TemplateView,ListView
from .models import Lostcat, SightingReport,ResolvedLostCat
from accounts.models import Account
from .forms import LostcatForm,LostSightingForm, ProtectedSightingForm
from django.views.generic.edit import UpdateView,FormView
from django.shortcuts import redirect,get_object_or_404,render
from django.http import HttpResponse
from django.views import View
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
import os
from django.conf import settings
from PIL import Image
import qrcode
from io import BytesIO
import shutil

class LostCatCreateView(LoginRequiredMixin, CreateView):
    model = Lostcat
    form_class = LostcatForm
    template_name = 'lost_cats/add_lost_cat.html'
    success_url = reverse_lazy('myaccount')

    def form_valid(self, form):
        lostcat = form.save(commit=False)
        lostcat.owner = self.request.user
        lostcat.save()
        return super().form_valid(form)
    
class LostCatDetailView(LoginRequiredMixin,DetailView):
    model = Lostcat
    template_name = 'lost_cats/lost_cat_detail.html'
    context_object_name = 'lost_cat'

    def get_queryset(self):
        return Lostcat.objects.filter(owner=self.request.user)

class LostCatUpdateView(LoginRequiredMixin, UpdateView):
    model = Lostcat
    form_class = LostcatForm
    template_name = 'lost_cats/lost_cat_edit.html'
    context_object_name = 'lost_cat'

    def get_object(self, queryset=None):
        return get_object_or_404(Lostcat, pk=self.kwargs["pk"], owner=self.request.user)

    def get_success_url(self):
        return reverse('lost_cat_detail', kwargs={'pk': self.object.pk})

class LoggedInReportSightingView(LoginRequiredMixin, FormView):
    template_name = 'lost_cats/report_sighting_loggedin.html'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        self.cat = get_object_or_404(Lostcat, id=self.kwargs['cat_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return LostSightingForm if self.cat.status == 'lost' else ProtectedSightingForm

    def form_valid(self, form):
        sighting = form.save(commit=False)
        sighting.lostcat = self.cat
        sighting.reporter = self.request.user
        sighting.phone_number = form.cleaned_data.get('phone_number')
        sighting.email = form.cleaned_data.get('email')
        sighting.save()
        return redirect(reverse('sighting_list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lost_cat'] = self.cat
        return context

class GuestReportSightingView(FormView):
    template_name = 'lost_cats/report_sighting_guest.html'

    def dispatch(self, request, *args, **kwargs):
        self.cat = get_object_or_404(Lostcat, id=self.kwargs['cat_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return LostSightingForm if self.cat.status == 'lost' else ProtectedSightingForm

    def form_valid(self, form):
        sighting = form.save(commit=False)
        sighting.lostcat = self.cat
        sighting.phone_number = form.cleaned_data.get('phone_number')
        sighting.email = form.cleaned_data.get('email')
        sighting.save()
        return redirect(reverse('thank_you', kwargs={'cat_id': self.cat.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lost_cat'] = self.cat
        return context

class ThankYouView(TemplateView):
    template_name = 'lost_cats/thank_you.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = Lostcat.objects.get(id=self.kwargs['cat_id'])
        return context

class SightingListView(LoginRequiredMixin, ListView):
    model = SightingReport
    template_name = 'lost_cats/sighting_list.html'
    context_object_name = 'sightings'
    login_url = '/login/'

    def get_queryset(self):
        return SightingReport.objects.filter(lostcat__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lost_cats'] = Lostcat.objects.filter(owner=self.request.user)
        return context
    
    def get_queryset(self):
        return SightingReport.objects.order_by('-lost_datetime')           


class SightingDetailView(LoginRequiredMixin, DetailView):
    model = SightingReport
    template_name = 'lost_cats/sighting_detail.html'
    context_object_name = 'sighting'
    login_url = '/login/'

    def get_queryset(self):
        return SightingReport.objects.filter(lostcat__owner=self.request.user)

# フォントファイルの絶対パス
FONT_PATH = os.path.join(settings.BASE_DIR, "static/fonts/MEIRYO.TTC")
FONT_PATH_BOLD = os.path.join(settings.BASE_DIR, "static/fonts/MEIRYOB.TTC")

# フォントの登録
pdfmetrics.registerFont(TTFont("Meiryo", FONT_PATH, subfontIndex=0))
pdfmetrics.registerFont(TTFont("Meiryo-Bold", FONT_PATH_BOLD, subfontIndex=0))

NO_IMAGE_PATH = os.path.join(settings.BASE_DIR, "static/images/no-image.jpg")

def draw_image_or_placeholder(p, image_path, x, y, width, height):
    if image_path and os.path.exists(image_path):
        img = ImageReader(image_path)
    else:
        img = ImageReader(NO_IMAGE_PATH)

    p.drawImage(img, x, y, width=width, height=height, preserveAspectRatio=True)

def draw_image_with_crop(p, image_path, x, y, target_width, target_height):
    if image_path and os.path.exists(image_path):
        with Image.open(image_path) as img:
            img_width, img_height = img.size

            if img.mode == "RGBA":
                img = img.convert("RGB")

            img_aspect = img_width / img_height
            target_aspect = target_width / target_height

            if img_aspect > target_aspect:
                new_width = int(img_height * target_aspect)
                new_height = img_height
                left = (img_width - new_width) // 2
                upper = 0
            else:
                new_width = img_width
                new_height = int(img_width / target_aspect)
                left = 0
                upper = (img_height - new_height) // 2

            img = img.crop((left, upper, left + new_width, upper + new_height))

            ext = image_path.split(".")[-1].lower()
            temp_path = f"temp_cropped.{ext}"

            img.save(temp_path, format="PNG" if ext == "png" else "JPEG")

            img_reader = ImageReader(temp_path)
            p.drawImage(img_reader, x, y, width=target_width, height=target_height, preserveAspectRatio=False)

            os.remove(temp_path)
    else:
        p.drawImage(ImageReader(NO_IMAGE_PATH), x, y, width=target_width, height=target_height, preserveAspectRatio=False)

class GenerateLostCatPosterView(View):
    def get(self, request, cat_id, *args, **kwargs):
        lost_cat = get_object_or_404(Lostcat, id=cat_id)
        user = request.user

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="nyan_cheese_poster_{lost_cat.id}.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # QRコードのURLを生成
        qr_url = f"http://{request.get_host()}/lost-cat/sighting/{lost_cat.id}/report/guest/"
        
        # QRコードを生成
        qr = qrcode.make(qr_url)

        # メモリ上にQRコード画像を保存
        qr_buffer = BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        # タイトル‐背景色
        p.setFillColorRGB(0.984, 0.867, 0.247)
        p.rect(0, height - 180, width, 180, fill=True, stroke=False)

        # タイトル‐「猫」
        p.setFillColorRGB(1, 0.2196, 0.2196) 
        p.setFont("Meiryo", 123) 
        p.drawString(40, height - 140, "猫") 

        # タイトル‐名前プレート
        p.setFillColorRGB(1, 1, 1)
        p.roundRect(170, height - 95, 384, 65, 3, fill=True, stroke=False)

        # タイトル‐「を探しています」
        p.setFillColorRGB(1, 0.219607843, 0.219607843)
        p.setFont("Meiryo-Bold", 50)
        p.drawString(170, height - 150, "を探しています")

        # タイトル‐「名前1」
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Meiryo", 12)
        p.drawString(183, height - 58, "名")

        # タイトル‐「名前2」
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Meiryo", 12)
        p.drawString(183.5, height - 78, "前")

        # タイトル-名前
        p.setFillColorRGB(0, 0, 0) 
        p.setFont("Meiryo-Bold", 40)
        p.drawString(208, height - 80, f"{lost_cat.name}")

        # 画像
        image1_path = lost_cat.photo.path if lost_cat.photo else None
        image2_path = lost_cat.photo2.path if lost_cat.photo2 else None
        image3_path = lost_cat.photo3.path if lost_cat.photo3 else None

        draw_image_with_crop(p, image1_path, 41, height - 501, 300, 300)
        draw_image_with_crop(p, image2_path, 363, height - 340, 191, 140)
        draw_image_with_crop(p, image3_path, 363, height - 501, 191, 140)

        # **アイコン画像のパス**
        icon_location = os.path.join(settings.BASE_DIR, "static/images/map.png")
        icon_clock = os.path.join(settings.BASE_DIR, "static/images/clock.png")

        # **迷子になった場所**
        if os.path.exists(icon_location):
            img = ImageReader(icon_location)
            p.drawImage(img, 270, height - 540, width=16.27, height=18, mask="auto")
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Meiryo", 14)
        p.drawString(292, height - 537, f"{lost_cat.lost_location}")

        # **迷子になった日時**
        lost_datetime_str = lost_cat.lost_datetime.strftime("%Y年%m月%d日 %H時%M分頃")
        if os.path.exists(icon_clock):
            img = ImageReader(icon_clock)
            p.drawImage(img, 41, height - 540, width=16.27, height=18, mask="auto")
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Meiryo", 14)
        p.drawString(63, height - 537, f"{lost_datetime_str}")

        # 性別
        p.setFillColorRGB(0.984, 0.867, 0.247)
        p.roundRect(41, height - 598, 90, 40, 20, fill=True, stroke=False)

        p.setFillColorRGB(0, 0, 0) 
        p.setFont("Meiryo", 20)
        p.drawString(66, height - 586, "性別")

        sex_display = lost_cat.get_sex_display()
        p.setFillColorRGB(0, 0, 0) 
        p.setFont("Meiryo-Bold", 20)
        p.drawString(143, height - 586, f"{sex_display}")

        # 年齢
        p.setFillColorRGB(0.984, 0.867, 0.247)
        p.roundRect(312, height - 598, 90, 40, 20, fill=True, stroke=False)

        p.setFillColorRGB(0, 0, 0) 
        p.setFont("Meiryo", 20)
        p.drawString(337, height - 586, "年齢")

        p.setFillColorRGB(0, 0, 0) 
        p.setFont("Meiryo-Bold", 20)
        p.drawString(414, height - 586, f"{ lost_cat.age_years }歳{ lost_cat.age_months }か月")

        # 特徴
        p.setFillColorRGB(0.984, 0.867, 0.247)
        p.roundRect(41, height - 649, 90, 40, 20, fill=True, stroke=False)

        p.setFillColorRGB(0, 0, 0) 
        p.setFont("Meiryo", 20)
        p.drawString(66, height - 637, "特徴")

        p.setFont("Meiryo-Bold", 20)
        p.drawString(143, height - 640, f"・{lost_cat.description1}")
        p.drawString(143, height - 663, f"・{lost_cat.description2}")
        p.drawString(143, height - 686, f"・{lost_cat.description_collar}")
        p.drawString(143, height - 709, f"・{lost_cat.description_eye}")

        # 注意書き
        p.setFillColorRGB(1, 0.219607843, 0.219607843)
        p.rect(0, height - 756, width, 27, fill=True, stroke=False)

        p.setFillColorRGB(1, 1, 1)
        p.setFont("Meiryo", 12)
        p.drawString(76, height - 747, "情報提供のご協力よろしくお願いいたします※無理な捕獲・追走はご遠慮ください")

        # アカウント情報
        p.setFillColorRGB(0.984, 0.867, 0.247)
        p.rect(0, height - 842, width, 86, fill=True, stroke=False)

        p.setFillColorRGB(1, 0.219607843, 0.219607843)
        p.setFont("Meiryo-Bold", 20)
        p.drawString(27, height - 806, "連絡先")

        p.setFillColorRGB(0, 0, 0)
        p.setFont("Meiryo-Bold", 14)
        p.drawString(100, height - 789, f"{user.username}")
        p.drawString(100, height - 807, f"{user.phone_number}")
        p.drawString(100, height - 823, f"{user.email}")

        # QRコード
        qr_image = ImageReader(qr_buffer)
        qr_x = width - 110
        qr_y = 10
        qr_size = 65
        p.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size, mask="auto")

        p.setFillColorRGB(0, 0, 0)
        p.setFont("Meiryo", 13)
        p.drawString(325, height - 784, "QRコードから登録不要で")   

        p.setFillColorRGB(0, 0, 0)
        p.setFont("Meiryo", 13)
        p.drawString(325, height - 802, "情報提供いただけます")

        p.showPage()    
        p.save()

        return response 
    
class LostCatPosterView(View):
    def get(self, request, cat_id, *args, **kwargs):
        lost_cat = get_object_or_404(Lostcat, id=cat_id)
        return render(request, 'lost_cats/lost_cat_poster.html', {'lost_cat': lost_cat})

def generate_qr_code(request, lost_cat_id):
    """
    迷子猫ごとの目撃情報入力フォームのQRコードを生成するビュー
    """
    url = f"http://{request.get_host()}/lost-cat/sighting/{lost_cat_id}/report/guest/"
    qr = qrcode.make(url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")

class ReportResolvedView(View):
    def post(self, request, cat_id):
        lost_cat = get_object_or_404(Lostcat, id=cat_id)

        if lost_cat.photo:  
            old_photo_path = lost_cat.photo.path
            new_photo_path = os.path.join(settings.MEDIA_ROOT, 'resolved_cats', os.path.basename(old_photo_path))
            shutil.move(old_photo_path, new_photo_path)
            new_photo_name = f'resolved_cats/{os.path.basename(new_photo_path)}'
        else:
            new_photo_name = 'resolved_cats/no-image.jpg'

        for extra_photo in [lost_cat.photo2, lost_cat.photo3]:
            if extra_photo:
                extra_photo_path = extra_photo.path
                if os.path.exists(extra_photo_path):
                    os.remove(extra_photo_path)

        ResolvedLostCat.objects.create(
            name=lost_cat.name,
            photo=new_photo_name
        )

        owner = lost_cat.owner 

        lost_cat.delete()

        if owner:
            owner.delete()

        return redirect('resolved_list')
    
class ResolvedListView(ListView):
    model = ResolvedLostCat
    template_name = 'lost_cats/resolved_list.html'
    context_object_name = 'resolved_cats'

class ConfirmResolvedView(View):
    def get(self, request, cat_id):
        lost_cat = get_object_or_404(Lostcat, id=cat_id)
        return render(request, 'lost_cats/confirm_resolved.html', {'lost_cat': lost_cat})