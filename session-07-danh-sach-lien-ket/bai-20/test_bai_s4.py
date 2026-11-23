import inspect

from lien_ket import make_list
import bai_s4


def test_vi_du_trong_de():
    s = make_list([3, 5, 9])
    bai_s4.insert_sorted(s, 7)
    assert s.to_text() == "3 -> 5 -> 7 -> 9 -> None"
    bai_s4.insert_sorted(s, 1)
    assert s.head.value == 1
    bai_s4.insert_sorted(s, 10)
    assert s.tail.value == 10


def test_tu_kiem_tra_va_giai_thich():
    assert inspect.getsource(bai_s4.tu_kiem_tra).count("assert ") >= 3, "tu_kiem_tra() cần ít nhất 3 lệnh assert"
    bai_s4.tu_kiem_tra()
    assert len(bai_s4.GIAI_THICH.split()) >= 8, "cần ghi giải thích cách làm và Big-O"
