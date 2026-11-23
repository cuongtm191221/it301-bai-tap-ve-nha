import pytest
from gio_mon import Basket


def test_pop_cuoi_va_dau():
    b = Basket(["A", "B", "C"])
    assert b.pop() == "C" and b.items() == ["A", "B"] and len(b) == 2
    assert b.pop(0) == "A" and b.items() == ["B"]


def test_pop_bo_tham_chieu_thua():
    b = Basket(["A", "B", "C"])
    b.pop(0)
    assert b._data[len(b)] is None, "ô vừa bỏ trống phải về None"
    b.pop()
    b.pop()
    with pytest.raises(IndexError):
        b.pop()


def test_remove_chi_xoa_lan_dau():
    b = Basket(["Phở", "Trà", "Trà", "Chè"])
    b.remove("Trà")
    assert b.items() == ["Phở", "Trà", "Chè"]
    assert b.checks == 2, "dừng ngay sau lần khớp đầu"


def test_remove_khong_co():
    b = Basket(["Phở"])
    with pytest.raises(ValueError, match="không tìm thấy món"):
        b.remove("Cơm")
    assert b.items() == ["Phở"]
