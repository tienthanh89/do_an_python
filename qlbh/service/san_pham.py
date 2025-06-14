from qlbh.models import SanPham, CTHD
from django.db.models import Sum

def get_filtered_sanpham(query_masp, query_tensp, query_nuocsx):
    if query_masp:
        return SanPham.objects.filter(masp__iexact=query_masp)
    elif query_tensp:
        return SanPham.objects.filter(tensp__icontains=query_tensp)
    elif query_nuocsx:
        return SanPham.objects.filter(nuocsx__icontains=query_nuocsx)
    else:
        return SanPham.objects.all()

def sanpham_to_dict(data):
    return {
        'masp': data.masp,
        'tensp': data.tensp,
        'dvt': data.dvt,
        'nuocsx': data.nuocsx,
        'gia': float(data.gia)
    }

def get_top_sanpham_mua_nhieu(limit=3):
    return (
        CTHD.objects.values('masp__masp', 'masp__tensp')
        .annotate(tong_sl=Sum('sl'))
        .order_by('-tong_sl')[:limit]
    )

def get_top_sanpham_mua_it(limit=3):
    return (
        CTHD.objects.values('masp__masp', 'masp__tensp')
        .annotate(tong_sl=Sum('sl'))
        .order_by('tong_sl')[:limit]
    )