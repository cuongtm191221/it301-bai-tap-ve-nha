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
from hang_in_phieu import print_order_slow, print_order_fast, print_summary

DEMO = ["ADD TK1", "ADD TK2", "URGENT TK9", "ADD TK1", "URGENT TK8", "PRINT", "PRINT", "ADD TK8", "PRINT", "PRINT"]


def random_commands(rng, n, codes):
    out = []
    for _ in range(n):
        r = rng.random()
        if r < 0.4:
            out.append(f"ADD TK{rng.randint(1, codes)}")
        elif r < 0.6:
            out.append(f"URGENT TK{rng.randint(1, codes)}")
        else:
            out.append("PRINT")
    return out


def test_kich_ban():
    assert print_order_fast(DEMO) == (["TK8", "TK9", "TK1", "TK2"], ["TK8"])


def test_khop_ban_cu_ngau_nhien():
    rng = random.Random(9)
    for _ in range(200):
        cmds = random_commands(rng, rng.randint(0, 60), rng.randint(1, 8))
        assert print_order_fast(cmds) == print_order_slow(cmds), cmds


def test_gap_nhieu_lan_va_in_lai():
    cmds = ["URGENT A", "URGENT B", "URGENT A", "PRINT", "ADD B", "PRINT", "ADD B", "PRINT", "URGENT B"]
    assert print_order_fast(cmds) == print_order_slow(cmds) == (["B", "A", "B"], ["B"])


def test_hang_rong():
    assert print_order_fast([]) == ([], [])
    assert print_order_fast(["PRINT", "PRINT"]) == ([], [])
    assert print_summary(["PRINT", "ADD TK5", "PRINT"]) == "In 1 phiếu, còn chờ 0"


def test_kieu_tra_ve_va_khong_sua_dau_vao():
    cmds = list(DEMO)
    printed, waiting = print_order_fast(cmds)
    assert type(printed) is list and type(waiting) is list
    assert cmds == DEMO
    assert print_summary(DEMO) == "In 4 phiếu, còn chờ 1: TK8"


def test_200000_lenh():
    rng = random.Random(20)
    cmds = random_commands(rng, 200000, 50000)
    printed, waiting = run_limited(lambda: print_order_fast(cmds), 1, "200.000 lệnh quá 1 giây")
    assert len(printed) + len(waiting) <= 200000 and len(set(waiting)) == len(waiting)
