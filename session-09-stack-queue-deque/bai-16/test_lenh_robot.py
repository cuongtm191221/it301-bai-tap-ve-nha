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
import pytest
from lenh_robot import decode_v1, decode_v2, route_message

BOTH = [("v1", decode_v1), ("v2", decode_v2)]


def test_co_ban():
    for name, f in BOTH:
        assert f("3[R]U") == "RRRU" and f("2[L3[R]]D") == "LRRRLRRRD" and f("LR") == "LR", name


def test_so_nhieu_chu_so_va_ngoac_rong():
    for name, f in BOTH:
        assert f("10[U]") == "U" * 10 and f("R2[]L") == "RL" and f("") == "", name


def test_sai_cu_phap():
    for name, f in BOTH:
        for bad in ("3[R", "2]R", "[R]", "0[R]", "2[x]", "3R", "2[R]3", "R]["):
            with pytest.raises(ValueError, match="Chuỗi lệnh không hợp lệ"):
                f(bad)


def test_hai_giai_phap_cung_ket_qua():
    rng = random.Random(5)

    def gen(depth):
        out = ""
        for _ in range(rng.randint(0, 3)):
            if depth < 3 and rng.random() < 0.4:
                out += str(rng.randint(1, 3)) + "[" + gen(depth + 1) + "]"
            else:
                out += rng.choice("LRUD")
        return out
    for _ in range(200):
        s = gen(0)
        assert decode_v1(s) == decode_v2(s), s


def test_thong_bao():
    assert route_message("2[L3[R]]D") == "9 bước: LRRRLRRRD"
    assert route_message("20[R]") == "20 bước: RRRRRRRRRRRR..."
    assert route_message("3[R") == "Từ chối: Chuỗi lệnh không hợp lệ"


def test_long_sau():
    s = "1[" * 3000 + "R" + "]" * 3000
    assert run_limited(lambda: route_message(s), 2, "chuỗi lồng 3.000 tầng quá 2 giây") == "1 bước: R"
