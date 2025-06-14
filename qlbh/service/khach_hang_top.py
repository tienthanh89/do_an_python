from qlbh.models import KhachHang

def lay_khach_hang_doanh_so_cao_nhat():
    khach_hang = KhachHang.objects.order_by('-doanhso').first()
    if khach_hang:
        return {
            'makh': khach_hang.makh,
            'hoten': khach_hang.hoten,
            'doanhso': float(khach_hang.doanhso),
        }
    return khach_hang