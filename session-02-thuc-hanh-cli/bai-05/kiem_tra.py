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


from quet_the import make_logs, parse_time, latest, add_swipe, count_card, busiest_hour, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_parse():
    assert [parse_time(t) for t in ["00:00", " 08:05", "23:59"]] == [0, 485, 1439], "parse_time sai"
    for bad in ["7:05", "24:00", "08:60", "08-30", "ab:cd", ""]:
        raises("Giờ quẹt phải có dạng HH:MM từ 00:00 đến 23:59", lambda: parse_time(bad))


def check_latest():
    logs = make_logs()
    assert latest(logs, 3) == [["VT4096", 810], ["VT3001", 725], ["VT1024", 720]], f"3 lượt gần nhất ra {latest(logs, 3)}"
    assert len(latest(logs, 20)) == 8 and logs == make_logs(), "k lớn hơn số lượt, hoặc nhật ký bị đổi"


def check_add():
    logs = make_logs()
    assert add_swipe(logs, " vt5000", "14:00") == ["VT5000", 840] and len(logs) == 9, "ghi lượt mới sai"
    assert add_swipe(logs, "VT5001", "14:00") == ["VT5001", 840], "giờ bằng lượt trước phải ghi được"
    cases = [(("VT12", "14:10"), "Mã thẻ phải gồm VT và 4 chữ số"), (("AB1234", "14:10"), "Mã thẻ phải gồm VT và 4 chữ số"),
             (("VT6000", "13:59"), "Giờ quẹt không được sớm hơn lượt trước (14:00)"), (("VT6000", "7:05"), "Giờ quẹt phải có dạng HH:MM từ 00:00 đến 23:59")]
    for args, message in cases:
        before = [log[:] for log in logs]
        raises(message, lambda: add_swipe(logs, *args))
        assert logs == before, f"{args}: nhật ký bị thay đổi dù dữ liệu sai"
    assert add_swipe([], "VT0001", "00:00") == ["VT0001", 0], "nhật ký rỗng phải ghi được lượt đầu"


def check_count_busiest():
    logs = make_logs()
    assert [count_card(logs, c) for c in ["vt1024", "VT2048", "VT9999"]] == [3, 2, 0], "đếm lượt theo thẻ sai"
    assert busiest_hour(logs) == (8, 3), f"giờ đông nhất ra {busiest_hour(logs)}"
    assert busiest_hour([["A", 600], ["B", 420], ["C", 610], ["D", 430]]) == (7, 2), "bằng nhau phải lấy giờ sớm hơn"
    assert busiest_hour([]) == (None, 0), "nhật ký rỗng phải trả (None, 0)"


def check_big():
    logs = [[f"VT{1000 + k % 500}", k * 1440 // 200000] for k in range(200000)]
    got = run_limited(lambda: (count_card(logs, "VT1000"), busiest_hour(logs)), 3, "200.000 lượt quá 3 giây")
    assert got[0] == 400 and got[1][1] == 8334, f"200.000 lượt ra {got}"


def check_benchmark():
    rows = run_limited(lambda: benchmark((1000, 2000), number=3), 10, "đo hiệu năng quá 10 giây")
    assert [r[0] for r in rows] == [1000, 2000], f"benchmark phải trả một bộ cho mỗi n, ra {rows}"
    assert all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), "mỗi bộ gồm (n, ms đếm lượt, ms giờ đông nhất), thời gian dương"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "1. 13:30 | VT4096", "3. 12:00 | VT1024", "Thẻ VT1024 quẹt 3 lượt.", "Đã ghi lượt VT5000 lúc 14:00. Tổng 9 lượt.",
        "Lỗi: Giờ quẹt không được sớm hơn lượt trước (14:00)", "Lỗi: Mã thẻ phải gồm VT và 4 chữ số",
        "Lỗi: Giờ quẹt phải có dạng HH:MM từ 00:00 đến 23:59", "Lỗi: Giờ quẹt phải có dạng HH:MM từ 00:00 đến 23:59",
        "Lỗi: Số lượt phải là số nguyên dương", "9. 07:50 | VT1024", "Lựa chọn không hợp lệ.",
        "n | đếm lượt một thẻ (ms) | giờ đông nhất (ms)", "80000 |",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã lưu nhật ký. Tạm biệt!",
    ])


CHECKS = [
    ("đọc giờ HH:MM", check_parse),
    ("k lượt gần nhất, mới nhất trước", check_latest),
    ("ghi lượt quẹt và dữ liệu sai", check_add),
    ("đếm lượt theo thẻ, giờ đông nhất", check_count_busiest),
    ("200.000 lượt quẹt", check_big),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '3',
    '2',
    '3',
    '1',
    'vt1024',
    '2',
    'vt5000',
    '14:00',
    '2',
    'VT6000',
    '13:59',
    '2',
    'VT12',
    '14:10',
    '2',
    'VT6000',
    '7:05',
    '2',
    'VT6000',
    '24:00',
    '1',
    '0',
    '1',
    '20',
    '3',
    '4',
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
