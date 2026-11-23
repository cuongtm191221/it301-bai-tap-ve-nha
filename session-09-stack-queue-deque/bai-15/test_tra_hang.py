from tra_hang import TwoStackQueue


def test_ai_fifo():
    q = TwoStackQueue()
    for t in ("A", "B", "C"):
        q.enqueue(t)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == ["A", "B", "C"]


def test_ai_peek_sau_dequeue():
    q = TwoStackQueue()
    for t in ("A", "B", "C"):
        q.enqueue(t)
    q.dequeue()
    assert q.peek() == "B"


def test_ai_size():
    q = TwoStackQueue()
    q.enqueue("A")
    q.enqueue("B")
    assert q.size() == 2
