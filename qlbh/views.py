from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import NhanVien

from .tinh_doanh_thu.tinh_doanh_thu import tinh_doanh_thu_cua_hang

# Create your views here.

def index(request):
    return HttpResponse('Xin chào bạn đã đến app QLBH.')

@method_decorator(csrf_exempt, name='dispatch')
class NhanVienList(View):
    def get(self, request):
        nv_list = NhanVien.objects.all().values()
        data = list(nv_list)
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            # Đọc dữ liệu JSON từ request body
            data = json.loads(request.body)


            # Tạo mới nhân viên từ dữ liệu JSON
            nhan_vien = NhanVien.objects.create(
                manv = data.get('manv'),
                hoten = data.get('hoten'),
                ngvl = data.get('ngvl'),
                sodt = data.get('sodt'),
                ch_id = data.get('ch')
            )

            # Trả về thông tin nhân viên vừa thêm vào (nếu muốn)
            response_data = {
                'manv': nhan_vien.manv,
                'hoten': nhan_vien.hoten,
                'ngvl': nhan_vien.ngvl,
                'sodt': nhan_vien.sodt,
                'mach': nhan_vien.ch.mach
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class DoanhThuCuaHangView(View):
    def get(self, request):
        # Gọi hàm tính doanh thu
        doanh_thu = tinh_doanh_thu_cua_hang()

        # Trả về kết quả dưới dạng JSON
        return JsonResponse({
            'tong_doanh_thu': str(doanh_thu) # Chuyển Decimal sang string để JsonResponse xử lý
        }, status=200)
