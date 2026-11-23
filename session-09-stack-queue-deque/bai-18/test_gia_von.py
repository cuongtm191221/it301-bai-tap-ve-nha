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
from gia_von import StockLedger, cost_report

EVENTS = [("IN", 10, 100000), ("IN", 5, 120000), ("OUT", 12), ("IN", 8, 130000), ("OUT", 6)]


def test_fifo_lay_mot_phan_lo():
    s = StockLedger("FIFO")
    s.receive(10, 100000)
    s.receive(5, 120000)
    assert s.issue(12) == 1240000
    assert s.lots() == [(3, 120000)] and s.on_hand() == 3 and s.stock_value() == 360000


def test_lifo_lay_lo_sau():
    s = StockLedger("LIFO")
    s.receive(10, 100000)
    s.receive(5, 120000)
    assert s.issue(12) == 1300000
    assert s.lots() == [(3, 100000)] and s.stock_value() == 300000


def test_bao_cao_hai_phuong_phap():
    assert cost_report("FIFO", EVENTS) == "FIFO: giá vốn 1990000đ, tồn 5 sp trị giá 650000đ"
    assert cost_report("LIFO", EVENTS) == "LIFO: giá vốn 2080000đ, tồn 5 sp trị giá 560000đ"


def test_thieu_hang_giu_nguyen_so():
    s = StockLedger("FIFO")
    s.receive(3, 50000)
    s.receive(2, 60000)
    with pytest.raises(ValueError, match="Không đủ hàng: còn 5"):
        s.issue(6)
    assert s.lots() == [(3, 50000), (2, 60000)] and s.on_hand() == 5 and s.stock_value() == 270000


def test_du_lieu_sai():
    with pytest.raises(ValueError, match="Phương pháp không hỗ trợ"):
        StockLedger("fifo")
    s = StockLedger("LIFO")
    for qty, cost in [(0, 10), (-1, 10), (2, 0), (2.0, 10), (True, 10), ("2", 10)]:
        with pytest.raises(ValueError, match="Số lượng và đơn giá phải là số nguyên dương"):
            s.receive(qty, cost)
    for qty in [0, -3, 1.5, "1"]:
        with pytest.raises(ValueError, match="Số lượng xuất phải là số nguyên dương"):
            s.issue(qty)
    assert cost_report("FIFO", [("IN", 3, 50000), ("OUT", 5)]) == "FIFO: lỗi ở bước 2: Không đủ hàng: còn 3"


def test_ket_thuc_bang_khong():
    s = StockLedger("FIFO")
    s.receive(4, 25000)
    assert s.issue(4) == 100000
    assert s.lots() == [] and s.on_hand() == 0 and s.stock_value() == 0


def test_nhieu_lo_nho():
    def job():
        s = StockLedger("FIFO")
        for k in range(100000):
            s.receive(1, 1000 + k)
            s.stock_value()
        total = 0
        for _ in range(100000):
            total += s.issue(1)
            s.stock_value()
        return total, s.on_hand()
    total, left = run_limited(job, 2, "100.000 lô quá 2 giây")
    assert total == 100000 * 1000 + 100000 * 99999 // 2 and left == 0


def test_xuat_mot_lan_nhieu_lo():
    def job():
        s = StockLedger("LIFO")
        for _ in range(100000):
            s.receive(1, 500)
        return s.issue(100000)
    assert run_limited(job, 2, "xuất một lần qua 100.000 lô quá 2 giây") == 50000000
