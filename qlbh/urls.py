from django.urls import path
from . import views
from .views import DoanhThuCuaHangView, NhanVienView, SanPhamView, KhachHangView, DoanhSoKhachHangView

urlpatterns = [
    path('index', views.index, name='index'),
    path('nhanvien/<str:manv>', NhanVienView.as_view(), name='nhanvien'),
    path('nhanvien', NhanVienView.as_view(), name='nhanvien'),
    path('sanpham', SanPhamView.as_view(), name='nhanvien'),
    path('khachhang', KhachHangView.as_view(), name='khachhang'),
    path('doanh-so-khach-hang', DoanhSoKhachHangView.as_view(), name='doanh-so-khach-hang'),
    path('doanh-thu/', DoanhThuCuaHangView.as_view(), name='doanh_thu_cua_hang'),
]