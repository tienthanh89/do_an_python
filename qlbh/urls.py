from django.urls import path
from . import views
from .views import DoanhThuCuaHangView, NhanVienView, SanPhamView, KhachHangView, TimSanPhamTheoMaView, TimSanPhamTheoTenView, TimSanPhamTheoNuocSXView, SanPhamMuaNhieuNhatView, SanPhamMuaItNhatView

urlpatterns = [
    path('index', views.index, name='index'),
    path('nhanvien/<str:manv>', NhanVienView.as_view(), name='nhanvien'),
    path('nhanvien', NhanVienView.as_view(), name='nhanvien'),
    path('sanpham', SanPhamView.as_view(), name='nhanvien'),
    path('khachhang', KhachHangView.as_view(), name='khachhang'),
    path('doanh-thu/', DoanhThuCuaHangView.as_view(), name='doanh_thu_cua_hang'),
    path('tim-kiem/san-pham/ma/', TimSanPhamTheoMaView.as_view(), name='tim_san_pham_ma'),
    path('tim-kiem/san-pham/ten/', TimSanPhamTheoTenView.as_view(), name='tim_san_pham_ten'),
    path('tim-kiem/san-pham/nuoc/', TimSanPhamTheoNuocSXView.as_view(), name='tim_san_pham_nuoc'),
    path('tim-kiem/san-pham/nhieu-nhat/', SanPhamMuaNhieuNhatView.as_view(), name='sp_mua_nhieu_nhat'),
    path('tim-kiem/san-pham/it-nhat/', SanPhamMuaItNhatView.as_view(), name='sp_mua_it_nhat'),



]