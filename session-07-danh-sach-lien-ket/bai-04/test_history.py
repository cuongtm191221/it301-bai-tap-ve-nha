import pytest

from history import History


def make(codes):
    h = History()
    for code in codes:
        h.add_last(code)
    return h


def test_xem_hai_chieu():
    h = make(["ZM001", "ZM002", "ZM003", "ZM004"])
    assert h.to_text() == "ZM001 -> ZM002 -> ZM003 -> ZM004 -> None"
    assert h.to_text_backward() == "ZM004 -> ZM003 -> ZM002 -> ZM001 -> None"


def test_bo_bai_cu_nhat():
    h = make(["ZM001", "ZM002", "ZM003", "ZM004"])
    assert h.remove_first() == "ZM001"
    assert h.head.prev is None and h.size == 3
    assert h.to_text_backward() == "ZM004 -> ZM003 -> ZM002 -> None"


def test_xoa_bai_duy_nhat():
    h = make(["ZM010"])
    assert h.remove_first() == "ZM010"
    assert h.head is None and h.tail is None and h.size == 0
    h.add_last("ZM011")
    assert h.to_text_backward() == "ZM011 -> None"


def test_xoa_khi_lich_su_trong():
    with pytest.raises(IndexError, match="lịch sử nghe đang trống"):
        History().remove_first()
