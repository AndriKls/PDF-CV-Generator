from django.urls import path
from . import views

urlpatterns = [
    path('', views.AcceptView.as_view(), name='accept'),
    path ('success/', views.SuccessView.as_view(), name='success'),
    path('cv/<int:id>/', views.CVView.as_view(), name='cv')
]
