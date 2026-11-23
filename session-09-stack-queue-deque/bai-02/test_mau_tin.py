from mau_tin import matches, is_balanced


def test_cap_dung():
    assert matches("(", ")") and matches("[", "]") and matches("{", "}")
    assert not matches("(", "]") and not matches("{", ")")


def test_hop_le():
    assert is_balanced("Chào {ten}, đơn [{ma_don}] đã giao (dự kiến {ngay}).")
    assert is_balanced("Không có ngoặc") and is_balanced("")


def test_lech_cap():
    assert not is_balanced("Mã {ma_giam] giảm 10%")
    assert not is_balanced("([)]")


def test_mo_thua_dong_thua():
    assert not is_balanced("Đơn (dự kiến {ngay}")
    assert not is_balanced("Hoàn tiền) cho đơn {ma_don}")
    assert not is_balanced(")(")
