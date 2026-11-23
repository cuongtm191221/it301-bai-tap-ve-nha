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
from loc_don import remove_cancelled, keep_last, cleanup_message

ORDERS = [("GF1", "DONE"), ("GF2", "CANCELLED"), ("GF3", " cancelled "), ("GF4", "DONE"),
          ("GF5", "PENDING"), ("GF6", "Cancelled"), ("GF7", "DONE")]


def test_xoa_don_huy_lien_nhau():
    o = list(ORDERS)
    assert remove_cancelled(o) == 3
    assert [c for c, _ in o] == ["GF1", "GF4", "GF5", "GF7"]


def test_tai_cho():
    o = list(ORDERS)
    same = o
    remove_cancelled(o)
    keep_last(o, 2)
    assert same is o and [c for c, _ in o] == ["GF5", "GF7"]


def test_khong_co_va_toan_bo_huy():
    o = [("A", "DONE")]
    assert remove_cancelled(o) == 0 and o == [("A", "DONE")]
    o = [("A", "CANCELLED"), ("B", "cancelled")]
    assert remove_cancelled(o) == 2 and o == []
    assert remove_cancelled([]) == 0


def test_keep_last_bien():
    o = [1, 2, 3]
    assert keep_last(o, 5) == 0 and o == [1, 2, 3]
    assert keep_last(o, 3) == 0 and o == [1, 2, 3]
    assert keep_last(o, 1) == 2 and o == [3]
    assert keep_last(o, 0) == 1 and o == []
    o = [1, 2]
    assert keep_last(o, -4) == 2 and o == []


def test_message():
    o = list(ORDERS)
    assert cleanup_message(o, 3) == "Đã xóa 3 đơn hủy, bỏ 1 đơn cũ, còn 3 đơn."


def test_khong_xoa_trong_vong_lap():
    src = inspect.getsource(remove_cancelled) + inspect.getsource(keep_last)
    assert ".remove(" not in src and ".pop(" not in src and ".insert(" not in src


def test_200000_don():
    def work():
        big = [(f"GF{k}", "CANCELLED" if k % 3 == 0 else "DONE") for k in range(200000)]
        msg = cleanup_message(big, 1000)
        return msg, big[0][0], big[-1][0]
    got = run_limited(work, 1, "dọn 200.000 đơn quá 1 giây")
    assert got == ("Đã xóa 66667 đơn hủy, bỏ 132333 đơn cũ, còn 1000 đơn.", "GF198500", "GF199999")
