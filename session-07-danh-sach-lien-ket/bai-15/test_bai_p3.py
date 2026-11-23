from dap_an_ma_hoa import ON, h
from lien_ket import make_list
from bai_p3 import FIND_WORST, best_case_find, tail_case_remove, worst_case_find


def comparisons(values, target):
    for i, v in enumerate(values):
        if v == target:
            return i + 1
    return len(values)


def test_tot_nhat():
    values, target = best_case_find(6)
    assert len(values) == 6 and comparisons(values, target) == 1


def test_xau_nhat():
    values, target = worst_case_find(6)
    assert len(values) == 6 and comparisons(values, target) == 6
    assert make_list(values).find(target) is None


def test_xoa_node_cuoi():
    values, target = tail_case_remove(5)
    lst = make_list(values)
    assert len(values) == 5 and lst.remove(target) is True
    assert lst.tail.value == values[-2] and lst.count() == 4


def test_big_o():
    assert h(FIND_WORST) == ON, "chưa đúng hoặc chưa ghi Big-O"
