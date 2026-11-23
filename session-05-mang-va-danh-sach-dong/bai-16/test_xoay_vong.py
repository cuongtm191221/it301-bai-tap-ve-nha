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
from xoay_vong import rotate_v1, rotate_v2, next_round_message

BOTH = [("v1", rotate_v1), ("v2", rotate_v2)]
D = ["An", "Bình", "Chi", "Dũng", "Em"]


def test_xoay_trai():
    for name, f in BOTH:
        assert f(D, 2) == ["Chi", "Dũng", "Em", "An", "Bình"], name
        assert f(D, 0) == D and f(D, 5) == D, name


def test_k_lon_hon_n_va_am():
    for name, f in BOTH:
        assert f(D, 7) == f(D, 2), name
        assert f(D, -1) == ["Em", "An", "Bình", "Chi", "Dũng"], name


def test_rong_va_khong_sua():
    for name, f in BOTH:
        data = list(D)
        got = f(data, 3)
        assert data == D and got is not data and f([], 4) == [], name


def test_hai_giai_phap_cung_ket_qua():
    rng = random.Random(2)
    for _ in range(200):
        data = list(range(rng.randint(0, 12)))
        k = rng.randint(-30, 30)
        assert rotate_v1(data, k) == rotate_v2(data, k), (data, k)


def test_thong_bao():
    assert next_round_message(D, 2) == "Sau 2 lượt, tài xế ưu tiên: Chi, tiếp theo: Dũng, Em"
    assert next_round_message(["An"], 3) == "Sau 3 lượt, tài xế ưu tiên: An, tiếp theo: "
    assert next_round_message([], 3) == "Chưa có tài xế nào trong hàng."


def test_du_lieu_lon():
    fleet = [f"TX{k}" for k in range(100000)]
    got = run_limited(lambda: next_round_message(fleet, 99999), 1, "100.000 tài xế, 99.999 lượt quá 1 giây")
    assert got == "Sau 99999 lượt, tài xế ưu tiên: TX99999, tiếp theo: TX0, TX1" and fleet[0] == "TX0"
