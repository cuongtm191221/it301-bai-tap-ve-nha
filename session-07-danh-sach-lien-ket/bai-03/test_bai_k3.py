import pytest

from bai_k3 import LinkedList


def make(values):
    lst = LinkedList()
    for v in values:
        lst.add_last(v)
    return lst


def test_remove_first():
    lst = make(["YC1", "YC2", "YC3"])
    assert lst.remove_first() == "YC1"
    assert lst.to_text() == "YC2 -> YC3 -> None" and lst.size == 2


def test_remove_first_node_duy_nhat():
    lst = make(["YC1"])
    assert lst.remove_first() == "YC1"
    assert lst.head is None and lst.tail is None and lst.size == 0


def test_remove_first_danh_sach_rong():
    with pytest.raises(IndexError, match="danh sách rỗng, không có phần tử để lấy"):
        make([]).remove_first()


def test_remove_o_giua():
    lst = make(["YC1", "YC2", "YC3"])
    assert lst.remove("YC2") is True
    assert lst.to_text() == "YC1 -> YC3 -> None" and lst.size == 2


def test_remove_node_cuoi_lui_tail():
    lst = make(["YC1", "YC2", "YC3"])
    assert lst.remove("YC3") is True
    assert lst.tail.value == "YC2" and lst.tail.next is None and lst.size == 2


def test_remove_khong_co():
    lst = make(["YC1", "YC2"])
    assert lst.remove("YC9") is False
    assert lst.to_text() == "YC1 -> YC2 -> None" and lst.size == 2
    assert make([]).remove("YC1") is False
