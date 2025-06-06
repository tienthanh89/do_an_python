from django.db.models import QuerySet
from django.db.models.expressions import result
from django.db.models.fields import return_None
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.utils.dateparse import parse_datetime

from .models import NhanVien, SanPham

from .service.tinh_doanh_thu import tinh_doanh_thu_cua_hang
from .service.nhan_vien import get_filtered_nhanvien, nhanvien_to_dict
from .service.san_pham import get_filtered_sanpham, sanpham_to_dict

# Create your views here.

def index(request):
    return HttpResponse('Xin chào bạn đã đến app QLBH.')

@method_decorator(csrf_exempt, name='dispatch')
class NhanVienView(View):
    def get(self, request):
        """Lấy danh sách nhân viên, tìm kiếm theo manv, họ tên, số điện thoại"""
        query_manv = request.GET.get('manv')
        query_hoten = request.GET.get('hoten')
        query_sodt = request.GET.get('sodt')

        try:
            data = get_filtered_nhanvien(query_manv, query_hoten, query_sodt)

            if isinstance(data, NhanVien):
                return JsonResponse(nhanvien_to_dict(data))
            else:
                return JsonResponse([nhanvien_to_dict(nv) for nv in data], safe=False)

        except NhanVien.DoesNotExist:
            return JsonResponse({"error": "Không tìm thấy nhân viên theo thông tin cung cấp."})
        except Exception as e:
            print(f"Lỗi không xác định trong GET NhanVien: {e}")
            return JsonResponse({"error": f"Đã xảy ra lỗi: {str(e)}"}, status=500)

    def post(self, request):
        """Thêm nhân viên"""
        try:
            # Đọc dữ liệu JSON từ request body
            data = json.loads(request.body)

            # Tạo mới nhân viên từ dữ liệu JSON
            data = NhanVien.objects.create(
                manv = data.get('manv'),
                hoten = data.get('hoten'),
                ngvl = data.get('ngvl'),
                sodt = data.get('sodt')
            )

            # Trả về thông tin nhân viên vừa thêm vào
            return JsonResponse(nhanvien_to_dict(data), status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request):
        """Cập nhật toàn bộ thông tin của một nhân viên"""
        try:
            # Đọc dữ liệu JSON từ request body
            data = json.loads(request.body)
            # Tìm nhân viên
            nhan_vien = NhanVien.objects.get(manv=data.get('manv'))

            # Cập nhật các trường
            nhan_vien.hoten = data.get('hoten', nhan_vien.hoten)
            nhan_vien.sodt = data.get('sodt', nhan_vien.sodt)
            ngvl_str = data.get('ngvl')
            if ngvl_str:
                nhan_vien.ngvl = parse_datetime(ngvl_str)

            nhan_vien.save()

            return JsonResponse([
                {"message": "Cập nhật nhân viên thành công"},
                nhanvien_to_dict(nhan_vien)
            ], safe=False, status=200)
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

# --- Lớp SanPhamView ---
@method_decorator(csrf_exempt, name='dispatch')
class SanPhamView(View):
    def get(self, request):  # Không còn tham số masp_path
        """Lấy danh sách sản phẩm hoặc tìm kiếm theo masp, tensp, nuocsx từ query string."""
        query_masp = request.GET.get('masp')
        query_tensp = request.GET.get('tensp')
        query_nuocsx = request.GET.get('nuocsx')

        try:
            data = get_filtered_sanpham(query_masp, query_tensp, query_nuocsx)

            if isinstance(data, SanPham):
                return JsonResponse(sanpham_to_dict(data), status=200)
            else:
                return JsonResponse([sanpham_to_dict(sp) for sp in data], safe=False, status=200)

        except SanPham.DoesNotExist:
            return JsonResponse({"error": "Không tìm thấy sản phẩm theo thông tin cung cấu."})
        except Exception as e:
            print(f"Lỗi không xác định trong GET SanPham: {e}")
            return JsonResponse({"error": f"Đã xảy ra lỗi: {str(e)}"}, status=500)


    def post(self, request):
        """Thêm một sản phẩm mới. Dữ liệu (bao gồm masp) được gửi trong request body."""
        try:
            data = json.loads(request.body)

            # Kiểm tra trường masp bắt buộc
            if not data.get('masp'):
                return JsonResponse({"error": "Mã sản phẩm (masp) là bắt buộc để thêm."}, status=400)

            # Kiểm tra xem masp đã tồn tại chưa
            if SanPham.objects.filter(masp=data['masp']).exists():
                return JsonResponse({"error": f"Mã sản phẩm '{data['masp']}' đã tồn tại."}, status=409)  # 409 Conflict

            san_pham = SanPham.objects.create(
                masp=data['masp'],  # masp là bắt buộc
                tensp=data.get('tensp'),
                dvt=data.get('dvt'),
                nuocsx=data.get('nuocsx'),
                gia=data.get('gia')
            )
            return JsonResponse(sanpham_to_dict(san_pham), status=201)  # 201 Created
        except KeyError as e:
            return JsonResponse({"error": f"Thiếu trường bắt buộc: {e}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dữ liệu JSON không hợp lệ."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request, *args, **kwargs):
        """
        Cập nhật toàn bộ thông tin của một sản phẩm.
        Mã sản phẩm (masp) để xác định sản phẩm cần cập nhật phải được gửi trong request body.
        """
        try:
            data = json.loads(request.body)

            target_masp = data.get('masp')  # Lấy masp từ request body

            if not target_masp:
                return JsonResponse({"error": "Mã sản phẩm (masp) là bắt buộc trong body để cập nhật."}, status=400)

            san_pham = SanPham.objects.get(masp=target_masp)

            # Cập nhật các trường. Dùng .get(key, old_value) để giữ giá trị cũ nếu không có trong request
            san_pham.tensp = data.get('tensp', san_pham.tensp)
            san_pham.dvt = data.get('dvt', san_pham.dvt)
            san_pham.nuocsx = data.get('nuocsx', san_pham.nuocsx)
            san_pham.gia = data.get('gia', san_pham.gia)

            san_pham.save()

            return JsonResponse(sanpham_to_dict(san_pham), status=200)  # 200 OK
        except SanPham.DoesNotExist:
            return JsonResponse({"error": "Sản phẩm không tồn tại để cập nhật."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dữ liệu JSON không hợp lệ."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, *args, **kwargs):
        """
        Xóa một sản phẩm.
        Mã sản phẩm (masp) để xác định sản phẩm cần xóa phải được gửi trong request body.
        """
        try:
            data = json.loads(request.body)
            target_masp = data.get('masp')  # Lấy masp từ request body

            if not target_masp:
                return JsonResponse({"error": "Mã sản phẩm (masp) là bắt buộc trong body để xóa."}, status=400)

            san_pham = SanPham.objects.get(masp=target_masp)
            tensp = san_pham.tensp
            san_pham.delete()
            return JsonResponse({"message": f"Đã xóa sản phẩm: {tensp} (Mã: {target_masp})"},
                                status=204)  # 204 No Content
        except SanPham.DoesNotExist:
            return JsonResponse({"error": "Sản phẩm không tồn tại để xóa."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dữ liệu JSON không hợp lệ."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)