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
from cho_giam_gia import wait_days_v1, wait_days_v2, wait_message

BOTH = [("v1", wait_days_v1), ("v2", wait_days_v2)]
H = [129000, 125000, 135000, 140000, 119000, 119000, 139000, 99000]


def test_vi_du():
    for name, f in BOTH:
        assert f(H) == [1, 3, 2, 1, 3, 2, 1, 0], name


def test_gia_bang_khong_tinh_la_giam():
    for name, f in BOTH:
        assert f([5, 5, 5]) == [0, 0, 0] and f([5, 5, 4]) == [2, 1, 0], name


def test_tang_dan_giam_dan():
    for name, f in BOTH:
        assert f([1, 2, 3, 4]) == [0, 0, 0, 0] and f([4, 3, 2, 1]) == [1, 1, 1, 0], name
        assert f([]) == [] and f([7]) == [0], name


def test_hai_giai_phap_cung_ket_qua():
    rng = random.Random(1)
    for _ in range(200):
        data = [rng.randint(1, 6) for _ in range(rng.randint(0, 25))]
        assert wait_days_v1(data) == wait_days_v2(data), data


def test_thong_bao():
    assert wait_message(H, 3) == "Ngày 3 (135.000đ): giá thấp hơn sau 2 ngày (ngày 5, 119.000đ)."
    assert wait_message(H, 8) == "Ngày 8 (99.000đ): chưa có ngày nào sau đó rẻ hơn."
    assert wait_message(H, 0) == "Ngày không hợp lệ." and wait_message(H, 9) == "Ngày không hợp lệ."


def test_khong_sua_dau_vao():
    data = list(H)
    for _, f in BOTH:
        f(data)
    assert data == H


def test_du_lieu_lon():
    long = list(range(200000, 0, -1))[::-1]
    got = run_limited(lambda: wait_message(long, 1), 1, "200.000 ngày quá 1 giây")
    assert got == "Ngày 1 (1đ): chưa có ngày nào sau đó rẻ hơn."
