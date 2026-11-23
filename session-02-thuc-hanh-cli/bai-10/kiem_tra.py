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
import xep_hang
from xep_hang import make_players, make_big_players, top_slow, top_fast, rank_slow, rank_fast, apply_match, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def names(rows):
    return [p[0] for p in rows]


def check_top():
    ps = make_players()
    assert names(top_fast(ps, 6)) == ["ShadowFox", "KiraVN", "Tí Nị", "Bông", "Zed99", "MèoMun"], f"bảng xếp hạng ra {names(top_fast(ps, 6))}"
    assert top_fast(ps, 2) == top_slow(ps, 2) and top_fast(ps, 10) == top_slow(ps, 10) and top_fast([], 3) == [], "top ở biên khác bản cũ"
    assert ps == make_players(), "top_fast làm đổi danh sách đăng ký"


def check_rank():
    ps = make_players()
    got = [rank_fast(ps, n) for n in ["ShadowFox", " kiravn ", "Zed99", "MèoMun", "Faker"]]
    assert got == [1, 2, 5, 6, None], f"hạng ra {got}"
    assert ps == make_players(), "rank_fast làm đổi danh sách đăng ký"


def check_random():
    rng = random.Random(10)
    for _ in range(200):
        ps = [[f"N{k}", rng.randint(0, 6)] for k in range(rng.randint(0, 25))]
        k = rng.randint(0, 30)
        assert top_fast(ps, k) == top_slow(ps, k), f"top khác bản cũ với {ps}, k = {k}"
        for p in ps[:5]:
            assert rank_fast(ps, p[0]) == rank_slow(ps, p[0]), f"hạng của {p[0]} khác bản cũ với {ps}"


def check_rules():
    for f in (xep_hang.top_fast, xep_hang.rank_fast):
        body = inspect.getsource(f).split('"""', 2)[-1]
        assert "_slow" not in body, f"{f.__name__} không được gọi bản cũ"
    body = inspect.getsource(xep_hang.rank_fast).split('"""', 2)[-1]
    assert "sort" not in body and "top_" not in body, "rank_fast không được sắp xếp"


def check_fast():
    ps = make_big_players(200000)
    got = run_limited(lambda: (len(top_fast(ps, 10)), rank_fast(ps, ps[-1][0])), 2, "200.000 người chơi quá 2 giây")
    assert got[0] == 10 and 1 <= got[1] <= 200000


def check_match():
    ps = make_players()
    assert apply_match(ps, "zed99", "+25") == ["Zed99", 2005] and rank_fast(ps, "Zed99") == 4, "Zed99 +25 phải lên 2005 điểm, hạng 4"
    low = [["Tân Binh", 40]]
    assert apply_match(low, "tân binh", "-100") == ["Tân Binh", 0], "trừ quá số điểm phải về 0"
    raises("Điểm trận phải là số nguyên từ -100 đến 100", lambda: apply_match(ps, "MèoMun", "-2000"))
    raises("Điểm trận phải là số nguyên từ -100 đến 100", lambda: apply_match(ps, "Bông", "1.5"))
    raises("Không có người chơi Faker", lambda: apply_match(ps, " Faker ", "10"))
    assert apply_match(ps, "MèoMun", "-100")[1] == 1420


def check_benchmark():
    rows = run_limited(lambda: benchmark((100, 200)), 10, "đo hiệu năng quá 10 giây")
    assert [r[0] for r in rows] == [100, 200] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "1. ShadowFox - 2350 điểm", "2. KiraVN - 2350 điểm", "6. MèoMun - 1520 điểm", "Hạng của KiraVN: 2/6 (2350 điểm).",
        "Zed99 có 2005 điểm, hạng 4/6.", "Lỗi: Điểm trận phải là số nguyên từ -100 đến 100", "MèoMun có 1420 điểm, hạng 6/6.",
        "Lỗi: Không có người chơi Faker", "Lỗi: Điểm trận phải là số nguyên từ -100 đến 100", "Không có người chơi Không Tên",
        "Lỗi: Số người phải là số nguyên dương", "3. Tí Nị - 2100 điểm", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.",
        "Đã khóa bảng xếp hạng. GG!",
    ])


CHECKS = [
    ("bảng xếp hạng top k", check_top),
    ("tra cứu hạng", check_rank),
    ("khớp bản cũ trên 200 danh sách ngẫu nhiên", check_random),
    ("ràng buộc của bản mới", check_rules),
    ("bản mới với 200.000 người chơi", check_fast),
    ("cập nhật điểm sau trận", check_match),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '6',
    '3',
    'kiravn',
    '2',
    'zed99',
    '+25',
    '2',
    'MèoMun',
    '-2000',
    '2',
    'MèoMun',
    '-100',
    '2',
    'Faker',
    '10',
    '2',
    'Bông',
    '1.5',
    '3',
    'Không Tên',
    '1',
    '0',
    '1',
    '3',
    '9',
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
