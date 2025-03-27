from django.urls import path
from .views import LostCatCreateView,LostCatDetailView,LostCatUpdateView,ThankYouView,SightingListView, SightingDetailView,GenerateLostCatPosterView,LostCatPosterView,LoggedInReportSightingView,GuestReportSightingView,generate_qr_code,ReportResolvedView,ResolvedListView,ConfirmResolvedView

urlpatterns = [
    path('add/', LostCatCreateView.as_view(), name='add_lost_cat'),
    path('detail/<int:pk>/', LostCatDetailView.as_view(), name='lost_cat_detail'),
    path('edit/<int:pk>/', LostCatUpdateView.as_view(), name='lost_cat_edit'),
    path('thank-you/<int:cat_id>/   ', ThankYouView.as_view(), name='thank_you'),
    path('sightings/', SightingListView.as_view(), name='sighting_list'),
    path('sightings/<int:pk>/', SightingDetailView.as_view(), name='sighting_detail'),
    path('poster/<int:cat_id>/', GenerateLostCatPosterView.as_view(), name='generate_poster'),
    path('poster/view/<int:cat_id>/', LostCatPosterView.as_view(), name='lost_cat_poster'),
    path('sighting/<int:cat_id>/report/loggedin/', LoggedInReportSightingView.as_view(), name='report_sighting_loggedin'),
    path('sighting/<int:cat_id>/report/guest/', GuestReportSightingView.as_view(), name='report_sighting_guest'),
    path('qr/<int:lost_cat_id>/', generate_qr_code, name='generate_qr_code'),
    path('resolved/<int:cat_id>/', ReportResolvedView.as_view(), name='report_resolved'),
    path('resolved-list/', ResolvedListView.as_view(), name='resolved_list'),
    path('resolved/confirm/<int:cat_id>/', ConfirmResolvedView.as_view(), name='confirm_resolved'),
]
