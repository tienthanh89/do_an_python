from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Sum

import json
from django.utils.dateparse import parse_datetime

from .models import NhanVien, SanPham, KhachHang, CTHD

from .service.tinh_doanh_thu import tinh_doanh_thu_cua_hang, tinh_doanh_so_khach_hang
from .service.nhan_vien import get_filtered_nhanvien, nhanvien_to_dict
from .service.san_pham import get_filtered_sanpham, sanpham_to_dict
from .service.khach_hang import get_filtered_khachhang, khachhang_to_dict
from .service.tri_gia_max_min import tri_gia_max_min

# Create your views here.

def index(request):
    return HttpResponse('Xin chào bạn đã đến app QLBH.')

# --- NhanVienView ---
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

            # Kiểm tra manv
            if not data.get('manv'):
                return JsonResponse({"error": "Mã nhân viên (manv) là bắt buộc để thêm."}, status=400)
            if NhanVien.objects.filter(manv=data['manv']).exists():
                return JsonResponse({"error": f"Mã nhân viên '{data['manv']}' đã tồn tại."}, status=409)

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
            manv = data.get('manv')
            if not manv:
                return JsonResponse({"error": "Mã nhân viên (manv) là bắt buộc."}, status=400)

            # Tìm nhân viên
            nhan_vien = NhanVien.objects.get(manv=manv)

            # Cập nhật các trường
            nhan_vien.hoten = data.get('hoten', nhan_vien.hoten)
            nhan_vien.sodt = data.get('sodt', nhan_vien.sodt)
            ngvl_str = data.get('ngvl')
            if ngvl_str:
                nhan_vien.ngvl = parse_datetime(ngvl_str)

            nhan_vien.save()

            return JsonResponse({
                "message": "Cập nhật nhân viên thành công",
                "nhan_vien_moi": nhanvien_to_dict(nhan_vien)}
            , safe=False, status=200)
        except NhanVien.DoesNotExist:
            return JsonResponse({"error": "Nhân viên không tồn tại."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request):
        """Xóa một nhân viên"""
        try:
            data = json.loads(request.body)
            manv = data.get('manv')
            if not manv:
                return JsonResponse({"error": "Mã sản phẩm (masp) là bắt buộc."}, status=400)

            nhan_vien = NhanVien.objects.get(manv=manv)
            hoten = nhan_vien.hoten
            nhan_vien.delete()
            return JsonResponse({"message": f"Đã xóa nhân viên: {hoten} (Mã: {manv})"},
                                status=204)

        except NhanVien.DoesNotExist:
            return JsonResponse({"error": "Nhân viên không tồn tại."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# --- SanPhamView ---
@method_decorator(csrf_exempt, name='dispatch')
class SanPhamView(View):
    def get(self, request):
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
                masp=data['masp'],
                tensp=data.get('tensp'),
                dvt=data.get('dvt'),
                nuocsx=data.get('nuocsx'),
                gia=data.get('gia')
            )
            return JsonResponse(sanpham_to_dict(san_pham), status=201)  # 201 Created

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request):
        """Cập nhật thông tin của một sản phẩm."""
        try:
            data = json.loads(request.body)
            masp = data.get('masp')
            if not masp:
                return JsonResponse({"error": "Mã sản phẩm (masp) là bắt buộc."}, status=400)

            san_pham = SanPham.objects.get(masp=masp)

            # Cập nhật các trường
            san_pham.tensp = data.get('tensp', san_pham.tensp)
            san_pham.dvt = data.get('dvt', san_pham.dvt)
            san_pham.nuocsx = data.get('nuocsx', san_pham.nuocsx)
            san_pham.gia = data.get('gia', san_pham.gia)

            san_pham.save()

            return JsonResponse(sanpham_to_dict(san_pham), status=200)

        except SanPham.DoesNotExist:
            return JsonResponse({"error": "Sản phẩm không tồn tại."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request):
        """
        Xóa một sản phẩm.
        """
        try:
            data = json.loads(request.body)
            masp = data.get('masp')  # Lấy masp từ request body

            if not masp:
                return JsonResponse({"error": "Mã sản phẩm (masp) là bắt buộc."}, status=400)

            san_pham = SanPham.objects.get(masp=masp)
            tensp = san_pham.tensp
            san_pham.delete()

            return JsonResponse({"message": f"Đã xóa sản phẩm: {tensp} (Mã: {masp})"},
                                status=204)

        except SanPham.DoesNotExist:
            return JsonResponse({"error": "Sản phẩm không tồn tại."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# --- KhachHangView Class ---
@method_decorator(csrf_exempt, name='dispatch')
class KhachHangView(View):
    def get(self, request):
        """Lấy danh sách khách hàng hoặc tìm kiếm theo makh, hoten, sodt từ query string."""
        query_makh = request.GET.get('makh')
        query_hoten = request.GET.get('hoten')
        query_sodt = request.GET.get('sodt')

        try:
            data = get_filtered_khachhang(query_makh, query_hoten, query_sodt)

            if isinstance(data, KhachHang):
                return JsonResponse(khachhang_to_dict(data))
            else:
                return JsonResponse([khachhang_to_dict(kh) for kh in data], safe=False)


        except KhachHang.DoesNotExist:
            return JsonResponse({"error": "Không tìm thấy nhân viên theo thông tin cung cấp."})
        except Exception as e:
            print(f"Lỗi không xác định trong GET NhanVien: {e}")
            return JsonResponse({"error": f"Đã xảy ra lỗi: {str(e)}"}, status=500)

    def post(self, request):
        """Thêm khách hàng"""
        try:
            data = json.loads(request.body)
            if not data.get('makh'):
                return JsonResponse({"error": "Mã khách hàng (makh) là bắt buộc để thêm."}, status=400)

            # Kiểm tra xem makh đã tồn tại chưa
            if KhachHang.objects.filter(makh=data['makh']).exists():
                return JsonResponse({"error": f"Mã khách hàng '{data['makh']}' đã tồn tại."}, status=409)

            data = KhachHang.objects.create(
                makh=data.get('makh'),
                hoten=data.get('hoten'),
                dchi=data.get('dchi'),
                sodt=data.get('sodt'),
                ngsinh=data.get('ngsinh'),
                ngdk=data.get('ngdk'),
                doanhso=data.get('doanhso')
            )
            return JsonResponse(khachhang_to_dict(data), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request):
        """Cập nhật thông tin khách hàng"""
        try:
            data = json.loads(request.body)

            makh = data.get('makh')

            if not makh:
                return JsonResponse({"error": "Không tìm thấy mã khách hàng (makh)."}, status=400)

            khach_hang = KhachHang.objects.get(makh=makh)

            # Cập nhật các trường
            khach_hang.hoten = data.get('hoten', khach_hang.hoten)
            khach_hang.dchi = data.get('dchi', khach_hang.dchi)
            khach_hang.sodt = data.get('sodt', khach_hang.sodt)
            khach_hang.ngsinh = data.get('ngsinh', khach_hang.ngsinh)
            khach_hang.ngdk = data.get('ngdk', khach_hang.ngdk)
            khach_hang.doanhso = data.get('doanhso', khach_hang.doanhso)
            khach_hang.save()

            return JsonResponse({
                "message": "Cập nhật khách hàng thành công",
                "khach_hang_moi": khachhang_to_dict(khach_hang)}
            , safe=False, status=200)

        except KhachHang.DoesNotExist:
            return JsonResponse({"error": "Khách hàng không tồn tại."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request):
        """
        Xóa khách hàng
        """
        try:
            data = json.loads(request.body)
            makh = data.get('makh')
            if not makh:
                return JsonResponse({"error": "Mã khách hàng (makh) là bắt buộc."}, status=400)

            khach_hang = KhachHang.objects.get(makh=makh)
            hoten = khach_hang.hoten  # Save name before deleting
            khach_hang.delete()
            return JsonResponse({"message": f"Đã xóa khách hàng: {hoten} (ID: {makh})"},
                                status=204)

        except KhachHang.DoesNotExist:
            return JsonResponse({"error": "Khách hàng không tồn tại."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# --- SanPhamMuaNhieuNhatView ---
@method_decorator(csrf_exempt, name='dispatch')
class SanPhamMuaNhieuNhatView(View):
    """Tim top 3 san pham mua nhieu"""
    def get(self, request):
        ket_qua = (
            CTHD.objects.values('masp__masp', 'masp__tensp')
            .annotate(tong_sl=Sum('sl'))
            .order_by('-tong_sl')[:3]
        )

        if ket_qua:
            return JsonResponse({
                "message": "Top 3 sản phẩm được mua nhiều nhất",
                "data": list(ket_qua)
            })
        else:
            return JsonResponse({
                "error": "Không có dữ liệu mua hàng."
            }, status=404)

# --- SanPhamMuaItNhatView ---
@method_decorator(csrf_exempt, name='dispatch')
class SanPhamMuaItNhatView(View):
    """Tim top 3 san pham mua it"""
    def get(self, request):
        ket_qua = (
            CTHD.objects.values('masp__masp', 'masp__tensp')
            .annotate(tong_sl=Sum('sl'))
            .order_by('tong_sl')[:3]
        )

        if ket_qua:
            return JsonResponse({
                "message": "Top 3 sản phẩm được mua ít nhất",
                "data": list(ket_qua)
            })
        else:
            return JsonResponse({
                "error": "Không có dữ liệu mua hàng."
            }, status=404)

# --- DoanhSoKhachHangView ---
@method_decorator(csrf_exempt, name='dispatch')
class DoanhSoKhachHangView(View):
    def get(self, request):
        """
        Tính toán và trả về doanh số của từng khách hàng.
        """
        try:
            # Tính doanhso
            doanh_so_khach_hang_annotated = tinh_doanh_so_khach_hang()

            response_data = []
            for khach_hang in doanh_so_khach_hang_annotated:
                # Cập nhật
                khach_hang.doanhso = khach_hang.calculated_doanhso
                khach_hang.save()

                # Thông tin trả về
                response_data.append({
                    'makh': khach_hang.makh,
                    'hoten': khach_hang.hoten,
                    'doanhso_cap_nhat': float(khach_hang.doanhso)
                })

            return JsonResponse(response_data, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Đã xảy ra lỗi khi tính doanh số: {str(e)}"}, status=500)

# --- DoanhThuCuaHangView ---
@method_decorator(csrf_exempt, name='dispatch')
class DoanhThuCuaHangView(View):
    def get(self, request):
        # Gọi hàm tính doanh thu
        doanh_thu = tinh_doanh_thu_cua_hang()

        # Trả về kết quả dưới dạng JSON
        return JsonResponse({
            'tong_doanh_thu': str(doanh_thu)
        }, status=200)

# --- TimHoaDonMaxMinView ---
@method_decorator(csrf_exempt, name='dispatch')
class TimHoaDonMaxMinView(View):
    def get(self, request):
        data = tri_gia_max_min()
        return data

#--- TimKhachHangCoDoanhSoCaoNhat ---
@method_decorator(csrf_exempt, name='dispatch')
class TimKhachHangCoDoanhSoCaoNhat(View):
    def get(self, request):
        try:
            khach_hang = KhachHang.objects.order_by('-doanhso').first()
            if khach_hang:
                data = {
                    'makh': khach_hang.makh,
                    'hoten': khach_hang.hoten,
                    'doanhso': float(khach_hang.doanhso),
                }
                return JsonResponse(data, status=200)
            else:
                return JsonResponse({"error": "Không có dữ liệu khách hàng."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Lỗi khi truy vấn: {str(e)}"}, status=500)