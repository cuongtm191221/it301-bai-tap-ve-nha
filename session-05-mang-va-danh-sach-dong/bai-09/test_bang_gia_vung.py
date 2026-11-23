import pytest
from bang_gia_vung import ZoneFares, report


def make():
    return ZoneFares([25000, 32000, 41000])


def test_get_set_size():
    b = make()
    assert b.size() == 3 and b.get(0) == 25000 and b.get(-1) == 41000
    b.set(1, 33000)
    assert [b.get(i) for i in range(3)] == [25000, 33000, 41000] and b.size() == 3


def test_chi_so_ngoai_pham_vi():
    b = make()
    for bad in (3, -4, 99):
        with pytest.raises(IndexError, match="Chỉ số ngoài phạm vi bảng giá"):
            b.get(bad)


def test_chi_so_khong_phai_so_nguyen():
    b = make()
    for bad in ("1", 1.0, True, None):
        with pytest.raises(TypeError, match="Chỉ số phải là số nguyên"):
            b.get(bad)


def test_gia_khong_hop_le():
    for bad in ([25000, 0], [-1000], [12000.5], ["12000"], [True]):
        with pytest.raises(ValueError, match="Giá phải là số nguyên dương"):
            ZoneFares(bad)
    b = make()
    with pytest.raises(ValueError):
        b.set(0, -5)
    assert b.get(0) == 25000


def test_ban_sao_dau_vao():
    fares = [25000, 32000]
    b = ZoneFares(fares)
    fares[0] = 1
    assert b.get(0) == 25000


def test_surge_khong_sua_bang_goc():
    b = make()
    s = b.surge(15)
    assert [s.get(i) for i in range(3)] == [28000, 36000, 47000]
    assert [b.get(i) for i in range(3)] == [25000, 32000, 41000]
    assert [b.surge(0).get(i) for i in range(3)] == [25000, 32000, 41000]
    for bad in (-1, 101, 1.5):
        with pytest.raises(ValueError, match="Mức tăng phải từ 0 đến 100"):
            b.surge(bad)


def test_report():
    assert report(make()) == "Vùng 1: 25.000đ | Vùng 2: 32.000đ | Vùng 3: 41.000đ"
    assert report(ZoneFares([])) == "Chưa có vùng nào."


def test_report_chi_dung_thao_tac_adt():
    class Fake:
        def size(self):
            return 2

        def get(self, i):
            return [5000, 7000][i]
    assert report(Fake()) == "Vùng 1: 5.000đ | Vùng 2: 7.000đ"
