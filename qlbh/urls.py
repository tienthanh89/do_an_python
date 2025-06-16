from django.urls import path
from . import views
from .views import  DoanhThuCuaHangView, NhanVienView
from .service import views_auth

urlpatterns = [
    path('index', views.index, name='index'),
    path('nhanvien/<str:manv>', NhanVienView.as_view(), name='nhanvien'),
    path('nhanvien', NhanVienView.as_view(), name='nhanvien'),
    path('doanh-thu/', DoanhThuCuaHangView.as_view(), name='doanh_thu_cua_hang'),
    path('register/', views_auth.register_view),
    path('login/', views_auth.login_view),
    path('forgot-password/', views_auth.forgot_password_view),
]