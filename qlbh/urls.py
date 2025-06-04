from django.urls import path
from . import views
from .views import NhanVienList, DoanhThuCuaHangView

urlpatterns = [
    path('index', views.index, name='index'),
    path('nhanvien', NhanVienList.as_view(), name='nhanvien'),
    path('doanh-thu/', DoanhThuCuaHangView.as_view(), name='doanh_thu_cua_hang'),
]