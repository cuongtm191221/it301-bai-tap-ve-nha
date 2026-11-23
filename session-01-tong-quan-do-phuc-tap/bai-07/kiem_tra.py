"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
import threading as _threading


def run_limited(task, seconds, message):
    """Chạy task tối đa seconds giây; quá giờ thì mục kiểm tra CHƯA ĐẠT với lời nhắn message."""
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
    return box


from khach_hang import above_average

CUSTOMERS = [
    {"code": "KH01", "spent": 1000000},
    {"code": "KH02", "spent": 2000000},
    {"code": "KH03", "spent": 1500000},
    {"code": "KH04", "spent": 1500001},
]


def check_example():
    assert above_average(CUSTOMERS)[0] == ["KH02", "KH04"], f"4 khách ra {above_average(CUSTOMERS)[0]}"


def check_strict():
    same = [{"code": "KH05", "spent": 500000}, {"code": "KH06", "spent": 500000}]
    assert above_average(same)[0] == [], "khách chi đúng bằng mức trung bình không được chọn"


def check_empty():
    assert above_average([]) == ([], 0), f"chưa có khách ra {above_average([])}"


def check_additions():
    for n in (1, 100, 1000):
        many = [{"code": f"KH{i}", "spent": i * 1000} for i in range(n)]
        got = above_average(many)[1]
        assert got == n, f"{n} khách: {got} lần cộng, mong đợi {n}"


def check_large():
    many = [{"code": f"KH{i}", "spent": i * 1000} for i in range(20000)]
    box = run_limited(lambda: above_average(many), 3, "20.000 khách chạy quá 3 giây (báo cáo thật có hàng trăm nghìn khách)")
    result, additions = box[0]
    assert len(result) == 10000 and additions == 20000, f"20.000 khách ra {len(result)} khách, {additions} lần cộng"


CHECKS = [
    ("ví dụ 4 khách", check_example),
    ("lớn hơn hẳn mức trung bình", check_strict),
    ("chưa có khách", check_empty),
    ("số lần cộng bằng n", check_additions),
    ("20.000 khách chạy xong trong 3 giây", check_large),
]


if __name__ == "__main__":
    passed = 0
    for name, check in CHECKS:
        try:
            check()
            print("ĐẠT      |", name)
            passed += 1
        except NotImplementedError:
            print("CHƯA LÀM |", name)
        except AssertionError as error:
            print("CHƯA ĐẠT |", name, "-", error)
        except Exception as error:
            print("LỖI      |", name, "-", type(error).__name__, error)
    print(f"Kết quả: {passed}/{len(CHECKS)} mục đạt")
