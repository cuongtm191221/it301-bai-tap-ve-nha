import inspect

from lien_ket import make_list
import bai_s2


def test_vi_du_trong_de():
    scores = make_list([7, 4, 9, 5, 3])
    passed, failed = bai_s2.split_by_score(scores, 5)
    assert passed.to_text() == "7 -> 9 -> 5 -> None"
    assert failed.to_text() == "4 -> 3 -> None"
    assert scores.to_text() == "7 -> 4 -> 9 -> 5 -> 3 -> None"


def test_tu_kiem_tra_va_giai_thich():
    assert inspect.getsource(bai_s2.tu_kiem_tra).count("assert ") >= 3, "tu_kiem_tra() cần ít nhất 3 lệnh assert"
    bai_s2.tu_kiem_tra()
    assert len(bai_s2.GIAI_THICH.split()) >= 8, "cần ghi giải thích cách làm và Big-O"
