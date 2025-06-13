from qlbh.models import NhanVien


def get_filtered_nhanvien(query_manv, query_hoten, query_sodt):
    if query_manv:
        return NhanVien.objects.get(manv=query_manv)
    elif query_hoten:
        return NhanVien.objects.filter(hoten__icontains=query_hoten)
    elif query_sodt:
        return NhanVien.objects.get(sodt=query_sodt)
    else:
        return NhanVien.objects.all()

def nhanvien_to_dict(data):
    return {
        'manv': data.manv,
        'hoten': data.hoten,
        'ngvl': data.ngvl,
        'sodt': data.sodt,
    }

