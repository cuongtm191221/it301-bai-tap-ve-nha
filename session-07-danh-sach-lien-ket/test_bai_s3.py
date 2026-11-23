import inspect

import bai_s3


def test_vi_du_trong_de():
    h = bai_s3.DraftHistory()
    for text in ["v1", "v2", "v3"]:
        h.save(text)
    assert h.back() == "v2"
    assert h.back() == "v1"
    assert h.back() is None
    assert h.forward() == "v2"
    h.save("v4")
    assert h.forward() is None
    assert h.current() == "v4"
    assert h.back() == "v2"


def test_tu_kiem_tra_va_giai_thich():
    assert inspect.getsource(bai_s3.tu_kiem_tra).count("assert ") >= 3, "tu_kiem_tra() cần ít nhất 3 lệnh assert"
    bai_s3.tu_kiem_tra()
    assert len(bai_s3.GIAI_THICH.split()) >= 8, "cần ghi giải thích cách làm và Big-O"
