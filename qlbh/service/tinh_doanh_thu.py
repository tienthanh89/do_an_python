from decimal import Decimal
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce

from qlbh.models import HoaDon, KhachHang
# from qlbh.models import HoaDon, CuaHang


def tinh_doanh_thu_cua_hang():
    """Tính tổng doanh thu dựa trên các hóa đơn."""
    # Bắt đầu với tất cả hóa đơn
    queryset = HoaDon.objects.all()

    # Tính tổng doanh thu
    tong_doanh_thu = queryset.aggregate(Sum('trigia'))['trigia__sum']

    # Trả về 0 nếu không có hóa đơn nào hoặc tổng là None
    return tong_doanh_thu if tong_doanh_thu is not None else Decimal(0)

def tinh_doanh_so_khach_hang():
    """Tính doanh thu từng khách hàng"""
    khachhang_queryset = KhachHang.objects.all()

    # Tính doanhso
    doanh_so_khach_hang_annotated = khachhang_queryset.annotate(
        calculated_doanhso=Coalesce(
            Sum('hoadon__trigia', output_field=DecimalField()), 0.00,
            output_field=DecimalField()
        )
    )

    return doanh_so_khach_hang_annotated if doanh_so_khach_hang_annotated is not None else Decimal(0)