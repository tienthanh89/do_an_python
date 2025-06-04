from django.core.management.base import BaseCommand
from datetime import datetime
from decimal import Decimal
from qlbh.models import KhachHang, NhanVien, SanPham, HoaDon, CTHD

class Command(BaseCommand):
    help = 'Populates the database with initial sample data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Bắt đầu thêm dữ liệu...'))

        # --- Thêm dữ liệu NHANVIEN ---
        nhan_vien_data = [
            ('NV01', 'Nguyen Nhu Nhut', '0927345678', '13/4/2006'),
            ('NV02', 'Le Thi Phi Yen', '0987567390', '21/4/2006'),
            ('NV03', 'Nguyen Van B', '0997047382', '27/4/2006'),
            ('NV04', 'Ngo Thanh Tuan', '0913758498', '24/6/2006'),
            ('NV05', 'Nguyen Thi Truc Thanh', '0918590387', '20/7/2006'),
        ]

        for manv, hoten, sodt, ngvl_str in nhan_vien_data:
            ngvl = datetime.strptime(ngvl_str, '%d/%m/%Y')
            NhanVien.objects.get_or_create(
                manv=manv,
                defaults={
                    'hoten': hoten,
                    'sodt': sodt,
                    'ngvl': ngvl
                }
            )
        self.stdout.write(self.style.SUCCESS('Đã thêm dữ liệu NhanVien.'))

        # --- Thêm dữ liệu KHACHHANG ---
        khach_hang_data = [
            ('KH01', 'Nguyen Van A', '731, Tran Hung Dao, Q5, TPHCM', '08823451', '22/10/1960', 13060000, '22/07/2006'),
            ('KH02', 'Tran Ngoc Han', '23/5 Nguyen Trai, Q5, TpHCM', '0908256478', '03/04/1974', 280000, '30/07/2006'),
            ('KH03', 'Tran Ngoc Linh', '45 Nguyen Canh Chan, Q1, TpHCM', '0938776266', '12/06/1980', 3860000, '05/08/2006'),
            ('KH04', 'Tran Minh Long', '50/34 Le Dai hanh, Q10, TpHCM', '0917325476', '09/03/1965', 250000, '02/10/2006'),
            ('KH05', 'Le Nhat Minh', '34 Truong Dinh, Q3, TPHCM', '08246108', '10/03/1960', 21000, '28/10/2006'),
            ('KH06', 'Le Hoai Thuong', '227 Nguyen Van Cu, Q5, TpHCM', '08631738', '31/12/1981', 915000, '24/11/2006'),
            ('KH07', 'Nguyen Van Tam', '32/3 Tran Binh Trong, Q5, TpHCM', '0916783565', '06/04/1971', 12500, '01/12/2006'),
            ('KH08', 'Phan Thi Thanh', '45/2 An Duong Vuong, Q5, TPHCM', '0938435756', '10/01/1971', 365000, '13/12/2006'),
            ('KH09', 'Le Ha Vinh', '873 Le Hong Phong, Q5, TPHCM', '08654763', '03/09/1979', 70000, '14/01/2007'),
            ('KH10', 'Ha Duy Lap', '34/34B Nguyen Trai, Q1, TPHCM', '08768904', '02/05/1963', 67500, '16/01/2007'),
        ]

        for makh, hoten, dchi, sodt, ngsinh_str, doanhso, ngdk_str in khach_hang_data:
            ngsinh = datetime.strptime(ngsinh_str, '%d/%m/%Y') if ngsinh_str else None
            ngdk = datetime.strptime(ngdk_str, '%d/%m/%Y') if ngdk_str else None
            KhachHang.objects.get_or_create(
                makh=makh,
                defaults={
                    'hoten': hoten,
                    'dchi': dchi,
                    'sodt': sodt,
                    'ngsinh': ngsinh,
                    'doanhso': Decimal(doanhso),
                    'ngdk': ngdk
                }
            )
        self.stdout.write(self.style.SUCCESS('Đã thêm dữ liệu KhachHang.'))

        # --- Thêm dữ liệu SANPHAM ---
        san_pham_data = [
            ('BC01', 'But Chi', 'cay', 'Singapore', 3000),
            ('BC02', 'But Chi', 'cay', 'Singapore', 5000),
            ('BC03', 'But Chi', 'cay', 'Viet Nam', 3500),
            ('BC04', 'But Chi', 'hop', 'Viet Nam', 30000),
            ('BB01', 'But bi', 'cay', 'Viet Nam', 5000),
            ('BB02', 'But bi', 'cay', 'Trung Quoc', 7000),
            ('BB03', 'But bi', 'hop', 'Thai Lan', 100000),
            ('TV01', 'Tap 100 giay mong', 'quyen', 'Trung Quoc', 2500),
            ('TV02', 'Tap 200 giay mong', 'quyen', 'Trung Quoc', 4500),
            ('TV03', 'Tap 100 giay tot', 'quyen', 'Viet Nam', 3000),
            ('TV04', 'Tap 200 giay tot', 'quyen', 'Viet Nam', 5500),
            ('TV05', 'Tap 100 trang', 'chuc', 'Viet Nam', 23000),
            ('TV06', 'Tap 200 trang', 'chuc', 'Viet Nam', 53000),
            ('TV07', 'Tap 100 trang', 'chuc', 'Trung Quoc', 34000),
            ('ST01', 'So tay 500 trang', 'quyen', 'Trung Quoc', 40000),
            ('ST02', 'So tay loai 1', 'quyen', 'Viet Nam', 55000),
            ('ST03', 'So tay loai 2', 'quyen', 'Viet Nam', 51000),
            ('ST04', 'So tay', 'quyen', 'Thai Lan', 55000),
            ('ST05', 'So tay mong', 'quyen', 'Thai Lan', 20000),
            ('ST06', 'Phan viet bang', 'hop', 'Viet Nam', 5000),
            ('ST07', 'Phan khong bui', 'hop', 'Viet Nam', 5000),
            ('ST08', 'Bong bang', 'cai', 'Viet Nam', 1000),
            ('ST09', 'But long', 'cay', 'Viet Nam', 5000),
            ('ST10', 'But long', 'cay', 'Trung Quoc', 7000),
        ]

        for masp, tensp, dvt, nuocsx, gia in san_pham_data:
            SanPham.objects.get_or_create(
                masp=masp,
                defaults={
                    'tensp': tensp,
                    'dvt': dvt,
                    'nuocsx': nuocsx,
                    'gia': Decimal(gia)
                }
            )
        self.stdout.write(self.style.SUCCESS('Đã thêm dữ liệu SanPham.'))

        # --- Thêm dữ liệu HOADON ---
        hoa_don_data = [
            (1001, '23/07/2006', 'KH01', 'NV01', 100000),
            (1002, '12/08/2006', 'KH01', 'NV02', 840000),
            (1003, '23/06/2006', 'KH02', 'NV01', 100000),
            (1004, '01/09/2006', 'KH02', 'NV01', 180000),
            (1005, '20/10/2006', 'KH01', 'NV02', 3800000),
            (1006, '16/10/2006', 'KH01', 'NV03', 2430000),
            (1007, '28/10/2006', 'KH03', 'NV03', 510000),
            (1008, '28/10/2006', 'KH01', 'NV03', 440000),
            (1009, '28/10/2006', 'KH03', 'NV04', 320000),
            (1010, '01/11/2006', 'KH01', 'NV01', 5200000),
            (1011, '04/11/2006', 'KH04', 'NV03', 250000),
            (1012, '30/11/2006', 'KH05', 'NV03', 21000),
            (1013, '12/12/2006', 'KH06', 'NV01', 5000),
            (1014, '31/12/2006', 'KH03', 'NV02', 3150000),
            (1015, '01/01/2007', 'KH06', 'NV01', 910000),
            (1016, '01/01/2007', 'KH07', 'NV02', 12500),
            (1017, '02/01/2007', 'KH08', 'NV03', 35000),
            (1018, '13/01/2007', 'KH08', 'NV03', 330000),
            (1019, '13/01/2007', 'KH01', 'NV03', 30000),
            (1020, '14/01/2007', 'KH09', 'NV04', 70000),
            (1021, '16/01/2007', 'KH10', 'NV04', 67500),
            (1022, '16/01/2007', None, 'NV03', 7000),
            (1023, '17/01/2007', None, 'NV01', 330000),
        ]

        for sohd, nghd_str, makh, manv, trigia in hoa_don_data:
            nghd = datetime.strptime(nghd_str, '%d/%m/%Y')
            khach_hang = KhachHang.objects.get(makh=makh) if makh else None
            nhan_vien = NhanVien.objects.get(manv=manv)
            HoaDon.objects.get_or_create(
                sohd=sohd,
                defaults={
                    'nghd': nghd,
                    'makh': khach_hang,
                    'manv': nhan_vien,
                    'trigia': Decimal(trigia)
                }
            )
        self.stdout.write(self.style.SUCCESS('Đã thêm dữ liệu HoaDon.'))

        # --- Thêm dữ liệu CTHD ---
        cthd_data = [
            (1001, 'TV02', 10), (1001, 'ST01', 5), (1001, 'BC01', 5), (1001, 'BC02', 10), (1001, 'ST08', 10),
            (1002, 'BC04', 20), (1002, 'BB01', 20), (1002, 'BB02', 20),
            (1003, 'BB03', 10),
            (1004, 'TV01', 20), (1004, 'TV02', 10), (1004, 'TV03', 10), (1004, 'TV04', 10),
            (1005, 'TV05', 50), (1005, 'TV06', 50),
            (1006, 'TV07', 20), (1006, 'ST01', 30), (1006, 'ST02', 10),
            (1007, 'ST03', 10),
            (1008, 'ST04', 8),
            (1009, 'ST05', 10),
            (1010, 'TV07', 50), (1010, 'ST07', 50), (1010, 'ST08', 100), (1010, 'ST04', 50), (1010, 'TV03', 100),
            (1011, 'ST06', 50),
            (1012, 'ST07', 3),
            (1013, 'ST08', 5),
            (1014, 'BC02', 80), (1014, 'BB02', 100), (1014, 'BC04', 60), (1014, 'BB01', 50),
            (1015, 'BB02', 30), (1015, 'BB03', 7),
            (1016, 'TV01', 5),
            (1017, 'TV02', 1), (1017, 'TV03', 1), (1017, 'TV04', 5),
            (1018, 'ST04', 6),
            (1019, 'ST05', 1), (1019, 'ST06', 2),
            (1020, 'ST07', 10),
            (1021, 'ST08', 5), (1021, 'TV01', 7), (1021, 'TV02', 10),
            (1022, 'ST07', 1),
            (1023, 'ST04', 6),
        ]

        for sohd_val, masp_val, sl_val in cthd_data:
            hoa_don = HoaDon.objects.get(sohd=sohd_val)
            san_pham = SanPham.objects.get(masp=masp_val)
            CTHD.objects.get_or_create(
                sohd=hoa_don,
                masp=san_pham,
                defaults={'sl': sl_val}
            )
        self.stdout.write(self.style.SUCCESS('Đã thêm dữ liệu CTHD.'))

        self.stdout.write(self.style.SUCCESS('Quá trình thêm dữ liệu hoàn tất.'))