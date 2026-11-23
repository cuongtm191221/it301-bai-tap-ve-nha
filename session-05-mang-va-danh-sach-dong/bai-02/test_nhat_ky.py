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


import sys
from nhat_ky import simulate_append, build_log, log_bytes


def test_simulate_nho():
    assert simulate_append(1) == (1, 0)
    assert simulate_append(5) == (8, 7)
    assert simulate_append(10) == (16, 15)


def test_simulate_dem_chep_du():
    capacity, copies = simulate_append(1000)
    assert capacity == 1024 and copies == 1023
    assert simulate_append(0) == (1, 0)


def test_build_log_dung_thu_tu_va_nhanh():
    events = [f"GB{k}" for k in range(100000)]
    log = run_limited(lambda: build_log(events), 1, "100.000 chuyến phải ghi xong trong 1 giây")
    assert log == events and log is not events


def test_log_bytes_tinh_ca_ban_ghi():
    record = "GB2001 " + "x" * 1000
    assert log_bytes([record]) == sys.getsizeof([record]) + sys.getsizeof(record)
    assert log_bytes([]) == sys.getsizeof([])
