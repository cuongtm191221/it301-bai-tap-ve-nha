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


import inspect
from gop_don import merge_by_time, merge_unique, merge_report

A = [("07:05", "GF1001"), ("07:20", "GF1003"), ("08:10", "GF1006")]
B = [("07:10", "GF1002"), ("07:20", "GF1004"), ("07:20", "GF1003"), ("09:00", "GF1009")]


def test_gop_theo_gio():
    got = merge_by_time(A, B)
    assert [t for t, _ in got] == ["07:05", "07:10", "07:20", "07:20", "07:20", "08:10", "09:00"]
    assert len(got) == 7


def test_cung_gio_first_truoc():
    got = merge_by_time([("07:00", "A1"), ("07:00", "A2")], [("07:00", "B1")])
    assert got == [("07:00", "A1"), ("07:00", "A2"), ("07:00", "B1")]


def test_list_rong():
    assert merge_by_time([], B) == B and merge_by_time(A, []) == A and merge_by_time([], []) == []
    assert merge_by_time(A, []) is not A


def test_khong_sua_dau_vao():
    a, b = list(A), list(B)
    merge_unique(a, b)
    assert a == A and b == B


def test_bo_trung():
    orders, dropped = merge_unique(A, B)
    assert dropped == 1 and len(orders) == 6
    assert orders.count(("07:20", "GF1003")) == 1
    assert merge_unique([("07:00", "X")], [("07:00", "X"), ("07:00", "X")]) == ([("07:00", "X")], 2)


def test_report():
    assert merge_report(A, B) == "Gộp 6 đơn (bỏ 1 đơn trùng), đơn đầu 07:05 GF1001, đơn cuối 09:00 GF1009."
    assert merge_report([], []) == "Không có đơn nào."


def test_khong_sap_xep_lai():
    src = inspect.getsource(merge_by_time)
    assert "sort" not in src and "pop(" not in src and "insert(" not in src


def test_100000_don_moi_ben():
    a = [(f"{k // 60 % 24:02d}:{k % 60:02d}", f"A{k}") for k in range(0, 200000, 2)]
    b = [(f"{k // 60 % 24:02d}:{k % 60:02d}", f"B{k}") for k in range(1, 200000, 2)]
    a.sort()
    b.sort()
    got = run_limited(lambda: merge_by_time(a, b), 1, "gộp 2 x 100.000 đơn quá 1 giây")
    assert len(got) == 200000 and all(got[k][0] <= got[k + 1][0] for k in range(len(got) - 1))
