from qlbh.models import SanPham


def get_filtered_sanpham(query_masp, query_tensp, query_nuocsx):
    if query_masp:
        return SanPham.objects.get(masp=query_masp)
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
        'gia': data.gia
    }

