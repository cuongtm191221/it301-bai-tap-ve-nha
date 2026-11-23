import pytest
from cong_thuc_gia import evaluate, price_message


def test_tinh_dung():
    assert evaluate("120000 2 * 15000 -") == 225000
    assert evaluate("500000 500000 10 * 100 / -") == 450000
    assert evaluate("99000") == 99000


def test_thu_tu_toan_hang():
    assert evaluate("10 3 -") == 7 and evaluate("10 3 /") == 3 and evaluate("3 10 -") == -7


def test_khoang_trang_va_so_am():
    assert evaluate("   7   -2   * ") == -14


def test_thieu_so():
    with pytest.raises(ValueError, match="Thiếu số cho phép tính"):
        evaluate("120000 * 2")
    with pytest.raises(ValueError, match="Thiếu số"):
        evaluate("+")


def test_thua_so_va_rong():
    with pytest.raises(ValueError, match="Thừa số, công thức chưa hoàn chỉnh"):
        evaluate("120000 2 3 *")
    with pytest.raises(ValueError, match="Công thức rỗng"):
        evaluate("   ")


def test_chia_0_va_ky_hieu_la():
    with pytest.raises(ValueError, match="Chia cho 0"):
        evaluate("100000 0 /")
    for bad in ("120000 2 x", "12a 3 +", "1.5 2 *", "2 3 ^"):
        with pytest.raises(ValueError, match="Ký hiệu không hợp lệ"):
            evaluate(bad)


def test_thong_bao():
    assert price_message("120000 2 * 15000 -") == "Giá: 225.000đ"
    assert price_message("5000 8000 -") == "Giá: -3.000đ"
    assert price_message("") == "Lỗi công thức: Công thức rỗng"


def test_cong_thuc_dai():
    formula = "1 " + "1 + " * 50000
    assert evaluate(formula) == 50001
