from qlbh.models import KhachHang


def get_filtered_khachhang(query_makh, query_hoten, query_sodt):
    if query_makh:
        return KhachHang.objects.get(manv=query_makh)
    elif query_hoten:
        return KhachHang.objects.filter(hoten__icontains=query_hoten)
    elif query_sodt:
        return KhachHang.objects.get(sodt=query_sodt)
    else:
        return KhachHang.objects.all()

def khachhang_to_dict(data):
    return {
        'makh': data.makh,
        'hoten': data.hoten,
        'dchi': data.dchi,
        'sodt': data.sodt,
        'ngsinh': data.ngsinh,
        'ngdk': data.ngdk,
        'doanhso': data.doanhso
    }

