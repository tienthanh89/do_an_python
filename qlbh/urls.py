from django.urls import path
from . import views
from .views import DoanhThuCuaHangView, NhanVienView, SanPhamView, KhachHangView, TimSanPhamView, SanPhamMuaNhieuNhatView,SanPhamMuaItNhatView


urlpatterns = [
    path('index', views.index, name='index'),
    path('nhanvien/<str:manv>', NhanVienView.as_view(), name='nhanvien'),
    path('nhanvien', NhanVienView.as_view(), name='nhanvien'),
    path('sanpham', SanPhamView.as_view(), name='nhanvien'),
    path('khachhang', KhachHangView.as_view(), name='khachhang'),
    path('doanh-thu/', DoanhThuCuaHangView.as_view(), name='doanh_thu_cua_hang'),
    path('sanpham/tim/', TimSanPhamView.as_view(), name='tim_sanpham'),
    path('sanpham/tim/nhieu-nhat/', SanPhamMuaNhieuNhatView.as_view(), name='sanpham_nhieu_nhat'),
    path('sanpham/tim/it-nhat/', SanPhamMuaItNhatView.as_view(), name='sanpham_it_nhat'),

]