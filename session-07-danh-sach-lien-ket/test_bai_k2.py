from bai_k2 import LinkedList


def test_add_first_vao_danh_sach_rong():
    lst = LinkedList()
    lst.add_first("YC1")
    assert lst.to_text() == "YC1 -> None"
    assert lst.head is lst.tail and lst.size == 1


def test_add_first_nhieu_lan():
    lst = LinkedList()
    for code in ["YC1", "YC2", "YC3"]:
        lst.add_first(code)
    assert lst.to_text() == "YC3 -> YC2 -> YC1 -> None"
    assert lst.tail.value == "YC1" and lst.size == 3


def test_add_last_vao_danh_sach_rong():
    lst = LinkedList()
    lst.add_last("YC1")
    assert lst.to_text() == "YC1 -> None"
    assert lst.head is lst.tail and lst.size == 1


def test_add_last_nhieu_lan():
    lst = LinkedList()
    for code in ["YC1", "YC2", "YC3"]:
        lst.add_last(code)
    assert lst.to_text() == "YC1 -> YC2 -> YC3 -> None"
    assert lst.tail.value == "YC3" and lst.tail.next is None and lst.size == 3


def test_xen_ke_hai_thao_tac():
    lst = LinkedList()
    lst.add_last("YC2")
    lst.add_first("YC1")
    lst.add_last("YC3")
    assert lst.to_text() == "YC1 -> YC2 -> YC3 -> None"
    assert lst.head.value == "YC1" and lst.tail.value == "YC3" and lst.size == 3
