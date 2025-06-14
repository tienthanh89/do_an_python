from django.http import JsonResponse
from qlbh.models import HoaDon

def tri_gia_max_min():
    #Lấy hóa đơn có giá trị cao nhất
    hoa_don_max = HoaDon.objects.order_by('-trigia').first()

    # Lấy hóa đơn có giá trị nhỏ nhất
    hoa_don_min = HoaDon.objects.order_by('trigia').first()

    data = {}
    #Gán thông tin hóa đơn lớn nhất nếu có
    if hoa_don_max is not None:
        data['hoa_don_tri_gia_lon_nhat'] = {
            'sohd': hoa_don_max.sohd ,
            'nghd': hoa_don_max.nghd,
            'trigia': float(hoa_don_max.trigia),    #Ép kiểu về float để đảm bảo dữ liệu JSON đúng chuẩn
        }
    else:
        data['hoa_don_tri_gia_lon_nhat'] = None

    #Gán thông tin hóa đơn nhỏ nhất nếu có
    if hoa_don_min is not None:
        data['hoa_don_tri_gia_nho_nhat'] = {
            'sohd': hoa_don_min.sohd,
            'nghd': hoa_don_min.nghd,
            'trigia': float(hoa_don_min.trigia),    #Ép kiểu về float để đảm bảo dữ liệu JSON đúng chuẩn
        }
    else:
        data['hoa_don_tri_gia_nho_nhat'] = None

    return JsonResponse(data)