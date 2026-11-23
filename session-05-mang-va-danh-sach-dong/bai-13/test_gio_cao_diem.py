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
from gio_cao_diem import busiest_window_v1, busiest_window_v2, window_message

BOTH = [("v1", busiest_window_v1), ("v2", busiest_window_v2)]
DAY = [12, 8, 5, 4, 6, 20, 45, 60, 38, 25, 30, 41, 50, 33, 28, 31, 47, 66, 58, 40, 27, 22, 18, 15]


def test_vi_du():
    for name, f in BOTH:
        assert f(DAY, 3) == (16, 171), name
        assert f(DAY, 1) == (17, 66), name


def test_bang_nhau_lay_som_nhat():
    for name, f in BOTH:
        assert f([5, 9, 9, 5], 2) == (1, 18), name
        assert f([4, 4, 4], 1) == (0, 4), name


def test_k_ngoai_khoang():
    for name, f in BOTH:
        assert f(DAY[:2], 3) is None and f(DAY, 0) is None and f(DAY, -1) is None and f([], 1) is None, name
        assert f(DAY, 24)[0] == 0, name


def test_hai_giai_phap_cung_ket_qua():
    rng = random.Random(9)
    for _ in range(200):
        data = [rng.randint(0, 9) for _ in range(rng.randint(0, 15))]
        k = rng.randint(-1, 16)
        assert busiest_window_v1(data, k) == busiest_window_v2(data, k), (data, k)


def test_thong_bao():
    assert window_message(DAY, 3) == "Cao điểm 3 giờ: từ giờ thứ 16 đến giờ thứ 18, 171 chuyến."
    assert window_message(DAY[:2], 3) == "Chưa đủ dữ liệu: cần ít nhất 3 giờ."
    assert window_message(DAY, 0) == "Độ dài khung giờ phải lớn hơn 0."


def test_khong_sua_dau_vao():
    data = list(DAY)
    for _, f in BOTH:
        f(data, 4)
    assert data == DAY


def test_du_lieu_lon():
    year = [(h * 37) % 101 for h in range(24 * 365 * 20)]
    got = run_limited(lambda: window_message(year, 1000), 2, "175.200 giờ, khung 1.000 giờ quá 2 giây")
    assert got.startswith("Cao điểm 1000 giờ:")
