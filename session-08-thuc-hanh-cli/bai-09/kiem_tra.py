"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Các mục đầu kiểm tra hàm nghiệp vụ; mục cuối chạy main.py, tự gõ lần lượt các phím trong KEYS
(cuối tệp) và kiểm tra các dòng thông báo bắt buộc xuất hiện đúng thứ tự. Không sửa tệp này.
"""
import os as _os
import subprocess as _sp
import sys as _sys
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
    return box[0]


def run_cli(seconds=10):
    """Chạy python main.py, tự gõ các phím trong KEYS (mỗi dòng một lần Enter); trả về toàn bộ chữ in ra."""
    keys = "\n".join(KEYS) + "\n"
    env = dict(_os.environ, PYTHONIOENCODING="utf-8")
    try:
        r = _sp.run([_sys.executable, "main.py"], input=keys, capture_output=True, text=True,
                    encoding="utf-8", timeout=seconds, env=env)
    except _sp.TimeoutExpired:
        raise AssertionError("main.py không dừng: kiểm tra chức năng Thoát và vòng lặp menu")
    if "NotImplementedError" in r.stderr:
        raise NotImplementedError
    assert "Traceback" not in r.stderr, "main.py dừng vì lỗi: " + r.stderr.strip().split("\n")[-1]
    return r.stdout


def appear_in_order(out, lines):
    """Mỗi dòng trong lines phải xuất hiện trong out, theo đúng thứ tự."""
    pos = 0
    for line in lines:
        k = out.find(line, pos)
        assert k >= 0, f'không thấy "{line}" (hoặc xuất hiện sai thứ tự)'
        pos = k + len(line)


import random
import inspect
import nhat_ky_bom
from nhat_ky_bom import FUELS, PumpLog, make_log, make_big_log, record, report_slow, report_fast, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def snapshot(log):
    out, node = [], log.head
    while node is not None:
        out.append(node.value)
        node = node.next
    return out


def check_sample():
    log = make_log()
    before = snapshot(log)
    got = report_fast(log, 500)
    assert got == ((855, 257, 2400), "B00002", ["B00002", "B00004", "B00005"]), f"dữ liệu mẫu ra {got}"
    assert tuple(got[0]) == got[0] and type(got[0]) is tuple, "tổng phải là tuple như bản cũ"
    assert snapshot(log) == before, "report_fast làm đổi nhật ký"
    assert report_fast(PumpLog(), 10) == ((0, 0, 0), None, []), "nhật ký rỗng"


def check_same():
    rng = random.Random(9)
    for _ in range(200):
        log = PumpLog()
        for k in range(rng.randint(0, 15)):
            log.add_last(("B%05d" % k, rng.choice(FUELS), rng.choice([1, 5, 50, 50, 300, 2000])))
        threshold = rng.choice([1, 50, 51, 2000])
        assert report_fast(log, threshold) == report_slow(log, threshold), f"khác bản cũ với {snapshot(log)}, ngưỡng {threshold}"


def check_rules():
    body = inspect.getsource(nhat_ky_bom.report_fast).split('"""', 2)[-1]
    for banned in ("report_slow", ".get(", ".count("):
        assert banned not in body, f"report_fast không được dùng {banned}"
    log = make_big_log(200000)
    got = run_limited(lambda: report_fast(log, 1000), 1, "report_fast với 200.000 lần bơm quá 1 giây")
    assert got[1] == "B01027" and len(got[2]) == 100100 and sum(got[0]) == 200100000, f"200.000 lần bơm ra {got[1]}, {len(got[2])}, {sum(got[0])}"


def check_record():
    log = make_log()
    assert record(log, " ron95 ", "42,7") == ("B00007", "RON95", 427) and log.tail.value[0] == "B00007"
    raises("Nhiên liệu phải là RON95, E5 hoặc DO", lambda: record(log, "A95", "10"))
    for bad in ["250", "1.25", "0", "-5", "abc", "", "12.", ".5"]:
        raises("Số lít phải từ 0.1 đến 200, tối đa 1 chữ số thập phân", lambda: record(log, "DO", bad))
    assert record(log, "do", "200") == ("B00008", "DO", 2000) and record(log, "E5", "0.1")[2] == 1


def check_benchmark():
    rows = run_limited(lambda: benchmark((100, 200)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [100, 200] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "B00001 | RON95 | 35.5 lít", "B00006 | E5 | 7.5 lít", "RON95: 85.5 lít | E5: 25.7 lít | DO: 240.0 lít", "Lần bơm nhiều nhất: B00002",
        "Từ 50.0 lít trở lên: B00002, B00004, B00005", "Đã ghi B00007: RON95 42.7 lít.", "Lỗi: Nhiên liệu phải là RON95, E5 hoặc DO",
        "Lỗi: Số lít phải từ 0.1 đến 200, tối đa 1 chữ số thập phân", "Lỗi: Số lít phải từ 0.1 đến 200, tối đa 1 chữ số thập phân",
        "RON95: 128.2 lít | E5: 25.7 lít | DO: 240.0 lít", "Từ 40.0 lít trở lên: B00002, B00004, B00005, B00007",
        "Lỗi: Số lít phải từ 0.1 đến 200, tối đa 1 chữ số thập phân", "n | bản cũ (ms) | bản mới (ms)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã chốt ca. Tạm biệt!",
    ])


CHECKS = [
    ("report_fast trên dữ liệu mẫu, nhật ký rỗng, không đổi nhật ký", check_sample),
    ("khớp bản cũ trên 200 nhật ký ngẫu nhiên", check_same),
    ("không gọi bản cũ, get, count; 200.000 lần bơm trong 1 giây", check_rules),
    ("ghi lần bơm, dữ liệu sai", check_record),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '50',
    '2',
    'ron95',
    '42,7',
    '2',
    'A95',
    '10',
    '2',
    'DO',
    '250',
    '2',
    'E5',
    '1.25',
    '3',
    '40',
    '3',
    '0',
    '4',
    'x',
    '5',
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
