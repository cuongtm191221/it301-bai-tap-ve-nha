import inspect

from lien_ket import make_list
import bai_s1


def test_vi_du_trong_de():
    q = make_list(["S1", "S1", "S2", "S2", "S2", "S3"])
    assert bai_s1.dedupe_adjacent(q) == 3
    assert q.to_text() == "S1 -> S2 -> S3 -> None"
    assert q.tail.value == "S3"


def test_tu_kiem_tra_va_giai_thich():
    assert inspect.getsource(bai_s1.tu_kiem_tra).count("assert ") >= 3, "tu_kiem_tra() cần ít nhất 3 lệnh assert"
    bai_s1.tu_kiem_tra()
    assert len(bai_s1.GIAI_THICH.split()) >= 8, "cần ghi giải thích cách làm và Big-O"
