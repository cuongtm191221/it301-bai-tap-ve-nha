import pytest
from bai_xe import make_lot, park, leave, find, slot_number, occupancy


def test_moi_hang_mot_list_rieng():
    lot = make_lot(3, 2)
    assert lot == [[None, None], [None, None], [None, None]]
    lot[0][0] = "X"
    assert lot[1][0] is None and lot[2][0] is None


def test_kich_thuoc_sai():
    for r, c in ((0, 3), (2, -1), (2.0, 3), ("2", 3)):
        with pytest.raises(ValueError, match="Kích thước bãi không hợp lệ"):
            make_lot(r, c)


def test_do_theo_thu_tu_hang():
    lot = make_lot(2, 3)
    assert [park(lot, f"X{k}") for k in range(4)] == [(0, 0), (0, 1), (0, 2), (1, 0)]
    assert occupancy(lot) == [3, 1]


def test_xe_trung_va_bai_day():
    lot = make_lot(1, 2)
    assert park(lot, "A") == (0, 0) and park(lot, "A") is None
    assert park(lot, "B") == (0, 1) and park(lot, "C") is None


def test_roi_bai_va_o_trong_dau_tien():
    lot = make_lot(2, 2)
    for code in "ABCD":
        park(lot, code)
    assert leave(lot, "B") is True and leave(lot, "Z") is False
    assert find(lot, "B") is None and park(lot, "E") == (0, 1) and find(lot, "E") == (0, 1)


def test_so_o():
    lot = make_lot(3, 4)
    assert slot_number(lot, 0, 0) == 1 and slot_number(lot, 1, 0) == 5 and slot_number(lot, 2, 3) == 12
    with pytest.raises(IndexError):
        slot_number(lot, 3, 0)
