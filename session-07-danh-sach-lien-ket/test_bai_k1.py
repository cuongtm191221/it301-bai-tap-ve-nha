import pytest

from bai_k1 import LinkedList, Node


def build(values):
    """Dựng danh sách bằng cách nối tay các node (không dùng phương thức nào của bài)."""
    lst = LinkedList()
    for v in reversed(values):
        lst.head = Node(v, lst.head)
        if lst.tail is None:
            lst.tail = lst.head
    return lst


def test_count():
    assert build(["KH1", "KH2", "KH3"]).count() == 3
    assert build([]).count() == 0


def test_find_co_va_khong_co():
    lst = build(["KH1", "KH2", "KH3"])
    assert lst.find("KH1") == 0
    assert lst.find("KH3") == 2
    assert lst.find("KH9") is None


def test_get():
    lst = build(["KH1", "KH2", "KH3"])
    assert lst.get(0) == "KH1"
    assert lst.get(2) == "KH3"


def test_get_ngoai_pham_vi():
    lst = build(["KH1", "KH2"])
    with pytest.raises(IndexError, match="vị trí ngoài phạm vi"):
        lst.get(2)
    with pytest.raises(IndexError, match="vị trí ngoài phạm vi"):
        lst.get(-1)


def test_to_text():
    assert build(["KH1", "KH2"]).to_text() == "KH1 -> KH2 -> None"
    assert build([]).to_text() == "None"


def test_duyet_khong_lam_doi_danh_sach():
    lst = build(["KH1", "KH2", "KH3"])
    head, tail = lst.head, lst.tail
    lst.count(); lst.find("KH3"); lst.get(1); lst.to_text()
    assert lst.head is head and lst.tail is tail and lst.count() == 3
