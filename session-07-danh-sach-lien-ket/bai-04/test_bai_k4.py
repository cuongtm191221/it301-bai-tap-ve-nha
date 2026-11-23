import pytest

from bai_k4 import DoublyLinkedList


def make(values):
    dl = DoublyLinkedList()
    for v in values:
        dl.add_last(v)
    return dl


def test_add_last_noi_hai_chieu():
    dl = make(["V1", "V2", "V3"])
    assert dl.to_text() == "V1 -> V2 -> V3 -> None"
    assert dl.to_text_backward() == "V3 -> V2 -> V1 -> None"
    assert dl.size == 3 and dl.head.prev is None and dl.tail.next is None


def test_add_first_noi_hai_chieu():
    dl = DoublyLinkedList()
    for v in ["V1", "V2", "V3"]:
        dl.add_first(v)
    assert dl.to_text() == "V3 -> V2 -> V1 -> None"
    assert dl.to_text_backward() == "V1 -> V2 -> V3 -> None"
    assert dl.size == 3


def test_remove_first():
    dl = make(["V1", "V2", "V3"])
    assert dl.remove_first() == "V1"
    assert dl.head.value == "V2" and dl.head.prev is None and dl.size == 2
    assert dl.to_text_backward() == "V3 -> V2 -> None"


def test_remove_last():
    dl = make(["V1", "V2", "V3"])
    assert dl.remove_last() == "V3"
    assert dl.tail.value == "V2" and dl.tail.next is None and dl.size == 2
    assert dl.to_text() == "V1 -> V2 -> None"


def test_xoa_node_duy_nhat():
    dl = make(["V1"])
    assert dl.remove_last() == "V1"
    assert dl.head is None and dl.tail is None and dl.size == 0
    assert dl.to_text_backward() == "None"


def test_xoa_khi_rong():
    with pytest.raises(IndexError, match="danh sách rỗng, không có phần tử để xóa"):
        DoublyLinkedList().remove_first()
    with pytest.raises(IndexError, match="danh sách rỗng, không có phần tử để xóa"):
        DoublyLinkedList().remove_last()
