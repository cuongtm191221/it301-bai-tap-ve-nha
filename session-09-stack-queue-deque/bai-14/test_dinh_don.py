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
from dinh_don import window_max_v1, window_max_v2, peak_message

BOTH = [("v1", window_max_v1), ("v2", window_max_v2)]
M = [12, 30, 25, 8, 41, 19, 7, 33, 33, 10]


def test_vi_du():
    for name, f in BOTH:
        assert f(M, 3) == [30, 30, 41, 41, 41, 33, 33, 33], name
        assert f(M, 1) == M and f(M, 10) == [41], name


def test_k_ngoai_khoang():
    for name, f in BOTH:
        assert f(M, 0) == [] and f(M, -2) == [] and f(M, 11) == [] and f([], 1) == [], name


def test_gia_tri_bang_nhau_va_giam_dan():
    for name, f in BOTH:
        assert f([5, 5, 5, 5], 2) == [5, 5, 5], name
        assert f([9, 7, 5, 3, 1], 2) == [9, 7, 5, 3], name


def test_hai_giai_phap_cung_ket_qua():
    rng = random.Random(3)
    for _ in range(200):
        data = [rng.randint(0, 9) for _ in range(rng.randint(0, 20))]
        k = rng.randint(-1, 21)
        assert window_max_v1(data, k) == window_max_v2(data, k), (data, k)


def test_thong_bao():
    assert peak_message(M, 3) == "Khung 3 phút: đỉnh cao nhất 41 đơn (khung bắt đầu phút 2), đỉnh thấp nhất 30 đơn."
    assert peak_message(M, 11) == "Chưa đủ dữ liệu cho khung 11 phút."
    assert peak_message(M, 0) == "Độ dài khung phải lớn hơn 0."


def test_khong_sua_dau_vao():
    data = list(M)
    for _, f in BOTH:
        f(data, 4)
    assert data == M


def test_du_lieu_lon():
    day = [(m * 37) % 211 for m in range(24 * 60 * 30)]
    got = run_limited(lambda: peak_message(day, 600), 2, "43.200 phút, khung 600 phút quá 2 giây")
    assert got.startswith("Khung 600 phút: đỉnh cao nhất 210 đơn")
