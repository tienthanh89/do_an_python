from django.urls import path
from . import views
from .views import DoanhThuCuaHangView, NhanVienView, SanPhamView, KhachHangView, DoanhSoKhachHangView,TimHoaDonMaxMin, SanPhamMuaNhieuNhatView, SanPhamMuaItNhatView
urlpatterns = [
    path('index', views.index, name='index'),
    path('nhanvien/<str:manv>', NhanVienView.as_view(), name='nhanvien'),
    path('nhanvien', NhanVienView.as_view(), name='nhanvien'),
    path('sanpham', SanPhamView.as_view(), name='nhanvien'),
    path('khachhang', KhachHangView.as_view(), name='khachhang'),
    path('doanh-so-khach-hang', DoanhSoKhachHangView.as_view(), name='doanh-so-khach-hang'),
    path('doanh-thu/', DoanhThuCuaHangView.as_view(), name='doanh_thu_cua_hang'),

  path('hoa-don-max-min/', TimHoaDonMaxMin.as_view(), name='hoa_don_max_min'),
  path('tim-kiem/san-pham/nhieu-nhat/', SanPhamMuaNhieuNhatView.as_view(), name='sp_mua_nhieu_nhat'),
  path('tim-kiem/san-pham/it-nhat/', SanPhamMuaItNhatView.as_view(), name='sp_mua_it_nhat'),
]