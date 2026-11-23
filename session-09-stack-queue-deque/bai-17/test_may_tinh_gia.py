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


import pytest
from may_tinh_gia import tokenize, to_postfix, calculate, price_message


def test_tach_token():
    assert tokenize(" (12+3) *40/ 5") == ["(", 12, "+", 3, ")", "*", 40, "/", 5]
    with pytest.raises(ValueError, match="Ký tự không hợp lệ: ,"):
        tokenize("50000 * 0,9")


def test_hau_to_va_thu_tu_uu_tien():
    assert to_postfix(tokenize("2 + 3 * 4")) == [2, 3, 4, "*", "+"]
    assert to_postfix(tokenize("(2 + 3) * 4")) == [2, 3, "+", 4, "*"]
    assert calculate("(199000 - 20000) * 90 / 100") == 161100


def test_cung_muc_tinh_tu_trai():
    assert calculate("100000 - 20000 - 10000") == 70000
    assert calculate("1000 / 10 / 2") == 50
    assert calculate("10 - 2 + 3") == 11


def test_ngoac_khong_khop():
    for bad in ["(1 + 2", "1 + 2)", "((1)", ")1 + 2("]:
        with pytest.raises(ValueError):
            calculate(bad)
    with pytest.raises(ValueError, match="Ngoặc không khớp"):
        calculate("(150000 + 5000")


def test_sai_cu_phap():
    for bad in ["", "   ", "300000 +", "+ 5", "2 3", "2 * * 3", "()", "-5 + 2", "(2)(3)"]:
        with pytest.raises(ValueError, match="Biểu thức sai cú pháp"):
            calculate(bad)


def test_thong_bao():
    assert price_message("tai nghe", "(199000 - 20000) * 90 / 100") == "Giá tai nghe: 161100đ"
    assert price_message("pin", "80000 / (2 - 2)") == "Lỗi công thức pin: Chia cho 0"
    assert price_message("cáp", "50000 * 0,9") == "Lỗi công thức cáp: Ký tự không hợp lệ: ,"


def test_khong_dung_eval():
    import may_tinh_gia
    src = open(may_tinh_gia.__file__, encoding="utf-8").read()
    assert "eval(" not in src.replace("evaluate_postfix(", "")
    assert "exec(" not in src


def test_ngoac_sau_va_bieu_thuc_dai():
    deep = "(" * 3000 + "7" + ")" * 3000
    long_expr = " + ".join(["3 * 2"] * 50000)
    got = run_limited(lambda: (calculate(deep), calculate(long_expr)), 2, "biểu thức dài quá 2 giây")
    assert got == (7, 300000)
