from decimal import Decimal
from django.db.models import Sum

from qlbh.models import HoaDon
# from qlbh.models import HoaDon, CuaHang


def tinh_doanh_thu_cua_hang():
    """Tính tổng doanh thu dựa trên các hóa đơn."""
    # Bắt đầu với tất cả hóa đơn
    queryset = HoaDon.objects.all()

    # Tính tổng doanh thu
    tong_doanh_thu = queryset.aggregate(Sum('trigia'))['trigia__sum']

    # Trả về 0 nếu không có hóa đơn nào hoặc tổng là None
    return tong_doanh_thu if tong_doanh_thu is not None else Decimal(0)