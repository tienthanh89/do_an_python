from django.urls import path
from . import views
from .views import  DoanhThuCuaHangView, NhanVienView

urlpatterns = [
    path('index', views.index, name='index'),
    path('nhanvien/<str:manv>', NhanVienView.as_view(), name='nhanvien'),
    path('nhanvien', NhanVienView.as_view(), name='nhanvien'),
    path('doanh-thu/', DoanhThuCuaHangView.as_view(), name='doanh_thu_cua_hang'),
]