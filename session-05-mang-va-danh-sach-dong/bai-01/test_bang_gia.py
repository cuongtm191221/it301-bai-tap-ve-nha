import pytest
from bang_gia import FareTable


def make():
    return FareTable([12000, 10000, 9000, 8000])


def test_get_size_last():
    t = make()
    assert t.get(0) == 12000 and t.size() == 4
    assert t.last() == 8000


def test_set_chi_thay_gia():
    t = make()
    t.set(1, 11000)
    assert [t.get(i) for i in range(t.size())] == [12000, 11000, 9000, 8000]
    assert t.size() == 4


def test_chi_so_bang_size_bao_dung_loi():
    t = make()
    with pytest.raises(IndexError, match="Chỉ số ngoài phạm vi bảng giá"):
        t.get(4)
    with pytest.raises(IndexError, match="Chỉ số ngoài phạm vi bảng giá"):
        t.set(4, 1000)


def test_chi_so_am_va_mot_muc():
    with pytest.raises(IndexError):
        make().get(-1)
    one = FareTable([15000])
    assert one.last() == 15000 and one.size() == 1
