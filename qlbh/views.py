from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.utils.dateparse import parse_datetime

from .models import NhanVien

from .service.tinh_doanh_thu import tinh_doanh_thu_cua_hang

# Create your views here.

def index(request):
    return HttpResponse('Xin chào bạn đã đến app QLBH.')

@method_decorator(csrf_exempt, name='dispatch')
class NhanVienView(View):
    def get(self, request, manv = None):
        """Lấy danh sách nhân viên hoặc theo manv"""
        if manv is not None:
            nhan_vien = NhanVien.objects.get(manv=manv)
            response_data = {
                'manv': nhan_vien.manv,
                'hoten': nhan_vien.hoten,
                'ngvl': nhan_vien.ngvl,
                'sodt': nhan_vien.sodt,
            }
            return JsonResponse(response_data)
        else:
            nv_list = NhanVien.objects.all().values()
            data = list(nv_list)
            return JsonResponse(data, safe=False)

    def post(self, request):
        """Thêm nhân viên"""
        try:
            # Đọc dữ liệu JSON từ request body
            data = json.loads(request.body)


            # Tạo mới nhân viên từ dữ liệu JSON
            nhan_vien = NhanVien.objects.create(
                manv = data.get('manv'),
                hoten = data.get('hoten'),
                ngvl = data.get('ngvl'),
                sodt = data.get('sodt')
            )

            # Trả về thông tin nhân viên vừa thêm vào (nếu muốn)
            response_data = {
                'manv': nhan_vien.manv,
                'hoten': nhan_vien.hoten,
                'ngvl': nhan_vien.ngvl,
                'sodt': nhan_vien.sodt,
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request):
        """Cập nhật toàn bộ thông tin của một nhân viên"""
        try:
            data = json.loads(request.body)
            nhan_vien = NhanVien.objects.get(manv=data.get('manv'))

            # Cập nhật các trường
            nhan_vien.hoten = data.get('hoten', nhan_vien.hoten)
            nhan_vien.sodt = data.get('sodt', nhan_vien.sodt)

            ngvl_str = data.get('ngvl')
            if ngvl_str is not None:
                nhan_vien.ngvl = parse_datetime(ngvl_str)
            else:
                nhan_vien.ngvl = None  # Cho phép đặt về NULL

            nhan_vien.save()
            return JsonResponse({
                "message": "Cập nhật nhân viên thành công",
                "manv": nhan_vien.manv,
                "hoten": nhan_vien.hoten,
                "sodt": nhan_vien.sodt,
                "ngvl": nhan_vien.ngvl
            }, status=200)
        except NhanVien.DoesNotExist:
            return JsonResponse({"error": "Nhân viên không tồn tại."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dữ liệu JSON không hợp lệ."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, manv):
        """Xóa một nhân viên"""
        try:
            nhan_vien = NhanVien.objects.get(manv=manv)
            nhan_vien_hoten = nhan_vien.hoten
            nhan_vien.delete()
            return JsonResponse({"message": f"Đã xóa nhân viên: {nhan_vien_hoten} (Mã: {manv})"},
                                status=204)  # 204 No Content
        except NhanVien.DoesNotExist:
            return JsonResponse({"error": "Nhân viên không tồn tại."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class DoanhThuCuaHangView(View):
    def get(self, request):
        # Gọi hàm tính doanh thu
        doanh_thu = tinh_doanh_thu_cua_hang()

        # Trả về kết quả dưới dạng JSON
        return JsonResponse({
            'tong_doanh_thu': str(doanh_thu) # Chuyển Decimal sang string để JsonResponse xử lý
        }, status=200)

    def test(self):
        pass