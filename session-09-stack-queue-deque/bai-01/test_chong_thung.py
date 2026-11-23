import pytest
from chong_thung import BoxStack


def make(*boxes):
    s = BoxStack()
    for b in boxes:
        s.push(b)
    return s


def test_vao_sau_ra_truoc():
    s = make("TH01", "TH02", "TH03")
    assert [s.pop(), s.pop(), s.pop()] == ["TH03", "TH02", "TH01"]


def test_peek_khong_lay():
    s = make("TH01", "TH02")
    assert s.peek() == "TH02" and s.size() == 2
    s.push("TH09")
    assert s.peek() == "TH09"


def test_rong():
    s = BoxStack()
    with pytest.raises(IndexError, match="ngăn xếp rỗng"):
        s.peek()
    with pytest.raises(IndexError, match="ngăn xếp rỗng"):
        s.pop()


def test_nhanh():
    import time
    s = make(*range(100000))
    t = time.perf_counter()
    while not s.is_empty():
        s.pop()
    assert time.perf_counter() - t < 0.5, "lấy hết 100.000 thùng phải dưới 0,5 giây"
