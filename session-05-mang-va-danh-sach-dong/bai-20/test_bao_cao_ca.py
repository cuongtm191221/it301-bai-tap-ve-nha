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


import random
from bao_cao_ca import summary_slow, summary_fast, shift_report

SHIFT = [("BK1", "DONE", 25000), ("BK2", "CANCELLED", 0), ("BK3", "DONE", 32000),
         ("BK4", "DONE", 18000), ("BK5", "CANCELLED", 0)]


def test_vi_du():
    assert summary_fast(SHIFT, 2) == (75000, 2, ["BK4", "BK3"])


def test_khop_ban_cu_ngau_nhien():
    rng = random.Random(8)
    for _ in range(200):
        trips = [(f"BK{k}", rng.choice(["DONE", "CANCELLED", "DONE"]), rng.randint(0, 5) * 1000) for k in range(rng.randint(0, 30))]
        top = rng.randint(0, 35)
        assert summary_fast(trips, top) == summary_slow(trips, top), (trips, top)


def test_top_bien():
    assert summary_fast(SHIFT, 0) == (75000, 2, [])
    assert summary_fast(SHIFT, 10)[2] == ["BK4", "BK3", "BK1"]
    assert summary_fast([], 3) == (0, 0, [])


def test_trang_thai_khac_va_ma_trung():
    trips = [("A", "DONE", 1000), ("A", "DONE", 1000), ("B", "PENDING", 500), ("C", "CANCELLED", 0)]
    assert summary_fast(trips, 5) == summary_slow(trips, 5)


def test_khong_sua_dau_vao():
    data = list(SHIFT)
    summary_fast(data, 3)
    assert data == SHIFT


def test_bao_cao():
    assert shift_report(SHIFT, 2) == "Thu 75.000đ, hủy 2 cuốc, gần nhất: BK4, BK3"
    assert shift_report([], 3) == "Thu 0đ, hủy 0 cuốc, gần nhất: (không có)"


def test_200000_cuoc():
    month = [(f"BK{k}", "CANCELLED" if k % 7 == 0 else "DONE", 20000 + k % 5 * 1000) for k in range(200000)]
    got = run_limited(lambda: shift_report(month, 3), 1, "200.000 cuốc quá 1 giây")
    assert got.startswith("Thu ") and got.endswith("gần nhất: BK199999, BK199998, BK199996")
