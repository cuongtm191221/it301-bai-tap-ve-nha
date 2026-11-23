import pytest
from chi_phi import shift_cost, queue_cost


def test_pop():
    assert shift_cost("pop", 6, 0) == 5 and shift_cost("pop", 6, 5) == 0
    assert shift_cost("pop", 6, -1) == 0 and shift_cost("pop", 6, -6) == 5
    assert shift_cost("pop_end", 6) == 0 and shift_cost("append", 6) == 0


def test_insert():
    assert shift_cost("insert", 6, 0) == 6 and shift_cost("insert", 6, 2) == 4
    assert shift_cost("insert", 6, 6) == 0 and shift_cost("insert", 6, 99) == 0
    assert shift_cost("insert", 6, -2) == 2 and shift_cost("insert", 6, -99) == 6


def test_chi_so_sai():
    with pytest.raises(ValueError, match="chỉ số không hợp lệ"):
        shift_cost("pop", 6, 6)
    with pytest.raises(ValueError):
        shift_cost("pop", 0, 0)


def test_queue_cost():
    assert queue_cost(5, 3) == 4 + 3 + 2
    assert queue_cost(5, 9) == 4 + 3 + 2 + 1 + 0
    assert queue_cost(200000, 200000) == 200000 * 199999 // 2
    assert queue_cost(0, 3) == 0
