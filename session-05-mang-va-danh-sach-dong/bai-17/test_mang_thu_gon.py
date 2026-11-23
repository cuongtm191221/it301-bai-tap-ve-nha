import pytest
from mang_thu_gon import ShrinkArray


def fill(n):
    a = ShrinkArray()
    for k in range(n):
        a.append(k)
    return a


def test_append_get():
    a = fill(9)
    assert a.size() == 9 and a.capacity() == 16
    assert a.get(0) == 0 and a.get(-1) == 8 and a.items() == list(range(9))


def test_get_sai():
    a = fill(3)
    with pytest.raises(IndexError, match="Chỉ số ngoài phạm vi phần tử"):
        a.get(3)
    with pytest.raises(TypeError):
        a.get("1")


def test_pop_thu_gon():
    a = fill(9)
    assert [a.pop() for _ in range(7)] == [8, 7, 6, 5, 4, 3, 2]
    assert a.items() == [0, 1] and a.capacity() == 4
    a.pop()
    assert a.capacity() == 2
    a.pop()
    assert a.size() == 0 and a.capacity() == 1


def test_pop_rong():
    with pytest.raises(IndexError, match="Mảng rỗng"):
        ShrinkArray().pop()


def test_khong_doi_vung_lien_tuc_o_nguong():
    a = fill(8)
    before = a.copies
    for _ in range(1000):
        a.append("x")
        a.pop()
    assert a.copies - before <= 32, f"thêm rồi lấy 1.000 lần chép {a.copies - before} tham chiếu"


def test_khong_giu_tham_chieu_thua():
    a = fill(5)
    a.pop()
    assert all(v is None for v in a._data[a.size():])


def test_chi_phi_tuyen_tinh():
    a = fill(100000)
    for _ in range(100000):
        a.pop()
    assert a.copies <= 4 * 100000 and a.capacity() == 1
