import pytest
from hang_dong_goi import PackingQueue


def make(*codes):
    q = PackingQueue()
    for c in codes:
        q.enqueue(c)
    return q


def test_fifo():
    q = make("A", "B", "C", "D")
    assert [q.dequeue() for _ in range(4)] == ["A", "B", "C", "D"]


def test_peek_dau_hang():
    q = make("A", "B")
    assert q.peek() == "A" and q.size() == 2


def test_rong_roi_them_lai():
    q = make("A")
    q.dequeue()
    assert q.tail is None
    q.enqueue("X")
    q.enqueue("Y")
    assert q.dequeue() == "X" and q.dequeue() == "Y"


def test_rong():
    q = PackingQueue()
    with pytest.raises(IndexError, match="hàng đợi rỗng"):
        q.dequeue()
    with pytest.raises(IndexError, match="hàng đợi rỗng"):
        q.peek()
