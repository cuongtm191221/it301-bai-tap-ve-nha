import threading as _threading

_threading.stack_size(64 * 1024 * 1024)


def run_limited(task, seconds, message):
    """Chạy task tối đa seconds giây; quá giờ thì test thất bại với lời nhắn message."""
    box, errors = [], []

    def target():
        try:
            box.append(task())
        except BaseException as error:
            errors.append(error)

    worker = _threading.Thread(target=target, daemon=True)
    worker.start()
    worker.join(seconds)
    if errors:
        raise errors[0]
    assert box, message
    return box[0]


import pytest
from xem_gan_day import RecentlyViewed


def test_moi_nhat_truoc_va_gioi_han():
    h = RecentlyViewed(3)
    for p in ("A", "B", "C", "D"):
        h.view(p)
    assert h.items() == ["D", "C", "B"]


def test_xem_lai_dua_len_dau_khong_trung():
    h = RecentlyViewed(3)
    for p in ("A", "B", "C", "A"):
        h.view(p)
    assert h.items() == ["A", "C", "B"]


def test_chuan_hoa_ma():
    h = RecentlyViewed(3)
    for p in ("sp01", " SP01 ", "   ", ""):
        h.view(p)
    assert h.items() == ["SP01"]


def test_gioi_han_1():
    h = RecentlyViewed(1)
    h.view("A")
    h.view("B")
    assert h.items() == ["B"]


def test_doi_gioi_han():
    h = RecentlyViewed(4)
    for p in "ABCD":
        h.view(p)
    h.set_limit(2)
    assert h.items() == ["D", "C"]
    h.set_limit(3)
    h.view("E")
    h.view("F")
    assert h.items() == ["F", "E", "D"]


def test_gioi_han_sai():
    for bad in (0, -1, 2.5, "3"):
        with pytest.raises(ValueError, match="Giới hạn phải là số nguyên dương"):
            RecentlyViewed(bad)
    with pytest.raises(ValueError):
        RecentlyViewed(3).set_limit(0)


def test_clear():
    h = RecentlyViewed(2)
    h.view("A")
    h.clear()
    assert h.items() == []
    h.view("B")
    assert h.items() == ["B"]


def test_nhieu_luot_xem():
    def work():
        h = RecentlyViewed(20)
        for k in range(200000):
            h.view(f"SP{k % 50}")
        return h.items()[:2]
    assert run_limited(work, 2, "200.000 lượt xem quá 2 giây") == ["SP49", "SP48"]
