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
from moi_nhat import latest_first_v1, latest_first_v2, recent_message

BOTH = [("v1", latest_first_v1), ("v2", latest_first_v2)]
EV = ["A", "B", "C", "D"]


def test_moi_nhat_truoc():
    for name, f in BOTH:
        assert f(EV) == ["D", "C", "B", "A"], name
        assert f([]) == [] and f(["X"]) == ["X"], name


def test_khong_sua_dau_vao_va_list_moi():
    for name, f in BOTH:
        data = list(EV)
        got = f(data)
        assert data == EV and got is not data, name


def test_hai_giai_phap_cung_ket_qua():
    rng = random.Random(4)
    for _ in range(100):
        data = [rng.randint(0, 5) for _ in range(rng.randint(0, 20))]
        assert latest_first_v1(data) == latest_first_v2(data)


def test_thong_bao():
    assert recent_message(EV, 2) == "2 hoạt động gần nhất: D, C"
    assert recent_message(EV, 10) == "4 hoạt động gần nhất: D, C, B, A"
    assert recent_message([], 3) == "Chưa có hoạt động nào."
    assert recent_message(EV, 0) == "Số sự kiện cần hiện phải lớn hơn 0."


def test_su_kien_trung_ten():
    for name, f in BOTH:
        assert f(["A", "A", "B"]) == ["B", "A", "A"], name


def test_du_lieu_lon():
    log = [f"SK{k}" for k in range(200000)]
    got = run_limited(lambda: recent_message(log, 2), 1, "200.000 sự kiện quá 1 giây")
    assert got == "2 hoạt động gần nhất: SK199999, SK199998" and log[0] == "SK0"
