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
from dieu_phoi import DispatchQueue, handle


def run(lines):
    q = DispatchQueue()
    return [handle(q, line) for line in lines], q


def test_vao_truoc_giao_truoc():
    out, q = run(["ADD GC1", "ADD GC2", "ADD GC3", "NEXT", "NEXT"])
    assert out[-2:] == ["Giao GC1.", "Giao GC2."] and q.size() == 1


def test_go_voi_chu_thuong_khoang_trang():
    out, _ = run(["  add   gc7 ", "next"])
    assert out == ["Đã nhận GC7.", "Giao GC7."]


def test_ma_trung_va_huy():
    out, q = run(["ADD GC1", "ADD GC1", "ADD GC2", "CANCEL GC1", "CANCEL GC1", "NEXT"])
    assert out == ["Đã nhận GC1.", "GC1 đã có trong hàng.", "Đã nhận GC2.", "Đã hủy GC1.", "Không có GC1 trong hàng.", "Giao GC2."]


def test_hang_rong_va_view():
    out, _ = run(["NEXT", "VIEW 3", "ADD A", "ADD B", "VIEW 1", "VIEW 9"])
    assert out[0] == "Không còn cuốc chờ." and out[1] == "Hàng chờ: (trống)"
    assert out[4] == "Hàng chờ: A" and out[5] == "Hàng chờ: A, B"


def test_lenh_sai():
    out, _ = run(["", "ADD", "CANCEL", "VIEW 0", "VIEW -2", "VIEW ba", "PRINT"])
    assert out == ["Lệnh trống.", "Cú pháp: ADD <mã cuốc>", "Cú pháp: CANCEL <mã cuốc>",
                   "Cú pháp: VIEW <số cuốc lớn hơn 0>", "Cú pháp: VIEW <số cuốc lớn hơn 0>",
                   "Cú pháp: VIEW <số cuốc lớn hơn 0>", "Lệnh không hỗ trợ: PRINT"]


def test_ma_da_giao_co_the_them_lai():
    out, _ = run(["ADD GC1", "NEXT", "ADD GC1", "COUNT"])
    assert out[2] == "Đã nhận GC1." and out[3] == "Đang chờ 1 cuốc."


def test_khong_dung_pop0():
    src = inspect.getsource(DispatchQueue)
    assert "pop(0)" not in src and "insert(0" not in src


def test_200000_lenh():
    def work():
        q = DispatchQueue()
        for k in range(200000):
            q.add(f"GC{k}")
            q.next()
        return q.size()
    assert run_limited(work, 2, "200.000 lần thêm và giao quá 2 giây") == 0
