from django.urls import path
from . import views
from .views import  DoanhThuCuaHangView, NhanVienService

urlpatterns = [
    path('index', views.index, name='index'),
    path('nhanvien/<str:manv>', NhanVienService.as_view(), name='nhanvien'),
    path('nhanvien', NhanVienService.as_view(), name='nhanvien'),
    path('doanh-thu/', DoanhThuCuaHangView.as_view(), name='doanh_thu_cua_hang'),
]