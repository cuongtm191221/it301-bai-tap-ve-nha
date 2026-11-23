import pytest
from mang_dong import DynamicArray


def fill(n):
    a = DynamicArray()
    for k in range(n):
        a.append(f"GPS{k + 1}")
    return a


def test_len_la_so_phan_tu():
    assert len(fill(5)) == 5 and len(fill(0)) == 0 and len(fill(8)) == 8


def test_doc_theo_chi_so():
    a = fill(5)
    assert a[0] == "GPS1" and a[4] == "GPS5" and a[-1] == "GPS5" and a[-5] == "GPS1"


def test_chi_so_vao_o_du_phong_bao_loi():
    a = fill(6)
    for bad in (6, 7, -7):
        with pytest.raises(IndexError, match="Chỉ số ngoài phạm vi phần tử"):
            a[bad]


def test_so_lan_chep_tuyen_tinh():
    a = fill(10000)
    assert a.copies < 2 * 10000, f"10.000 lần append chép {a.copies} tham chiếu"
    assert fill(5).copies == 7 and fill(1).copies == 0
