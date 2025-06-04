from django.db import models

class KhachHang(models.Model):
    makh = models.CharField(primary_key=True, max_length=4)
    hoten = models.CharField(max_length=50)
    dchi = models.CharField(max_length=50, null=True, blank=True)
    sodt = models.CharField(max_length=15, null=True, blank=True)
    ngsinh = models.DateTimeField(null=True, blank=True)
    ngdk = models.DateTimeField(null=True, blank=True)
    doanhso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.hoten

class NhanVien(models.Model):
    manv = models.CharField(primary_key=True, max_length=4)
    hoten = models.CharField(max_length=50)
    sodt = models.CharField(max_length=15, null=True, blank=True)
    ngvl = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.hoten

class SanPham(models.Model):
    masp = models.CharField(primary_key=True, max_length=4)
    tensp = models.CharField(max_length=40)
    dvt = models.CharField(max_length=20, null=True, blank=True)
    nuocsx = models.CharField(max_length=40, null=True, blank=True)
    gia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.tensp

class HoaDon(models.Model):
    sohd = models.IntegerField(primary_key=True)
    nghd = models.DateTimeField(null=True, blank=True)
    trigia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Quan hệ 1-N: Một khách hàng có nhiều hóa đơn
    makh = models.ForeignKey(KhachHang, on_delete=models.SET_NULL, null=True, blank=True) # Foreign Key to KhachHang
    # Quan hệ 1-N: Một nhân viên lập nhiều hóa đơn
    manv = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, blank=True) # Foreign Key to NhanVien

    # Quan hệ N-N với SanPham thông qua CTHD (bảng trung gian cthd)
    san_phams = models.ManyToManyField(SanPham, through='CTHD')

    def __str__(self):
        return f"HD{self.sohd}"

class CTHD(models.Model):
    sohd = models.ForeignKey(HoaDon, on_delete=models.CASCADE) # Foreign Key to HoaDon
    masp = models.ForeignKey(SanPham, on_delete=models.CASCADE) # Foreign Key to SanPham
    sl = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('sohd', 'masp'),) # Defines the composite primary key

    def __str__(self):
        return f"CTHD - HD:{self.sohd}, SP:{self.masp}"






