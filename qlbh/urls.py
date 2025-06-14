from django.urls import path
from . import views
from .views import DoanhThuCuaHangView, NhanVienView, SanPhamView, KhachHangView, DoanhSoKhachHangView,TimHoaDonMaxMinView, SanPhamMuaNhieuNhatView, SanPhamMuaItNhatView
urlpatterns = [
    path('index', views.index, name='index'),

    path('nhanvien/<str:manv>', NhanVienView.as_view(), name='nhanvien_manv'),
    path('nhanvien', NhanVienView.as_view(), name='nhanvien'),

    path('sanpham', SanPhamView.as_view(), name='sanpham'),
    path('sanpham/<str:masp>', SanPhamView.as_view(), name='sanpham_masp'),

    path('khachhang', KhachHangView.as_view(), name='khachhang'),
    path('khachhang/<str:makh>', KhachHangView.as_view(), name='khachhang_makh'),

    path('doanh-so-khach-hang', DoanhSoKhachHangView.as_view(), name='doanh-so-khach-hang'),
    path('doanh-thu/', DoanhThuCuaHangView.as_view(), name='doanh_thu_cua_hang'),

    path('hoa-don-max-min/', TimHoaDonMaxMinView.as_view(), name='hoa_don_max_min'),
    path('tim-kiem/san-pham/nhieu-nhat/', SanPhamMuaNhieuNhatView.as_view(), name='sp_mua_nhieu_nhat'),
    path('tim-kiem/san-pham/it-nhat/', SanPhamMuaItNhatView.as_view(), name='sp_mua_it_nhat'),
]