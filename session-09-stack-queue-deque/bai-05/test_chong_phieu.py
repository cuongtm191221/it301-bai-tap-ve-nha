import pytest
from chong_phieu import SlipStack


def make(*codes):
    s = SlipStack()
    for c in codes:
        s.push(c)
    return s


def test_pop_lifo():
    s = make("A", "B", "C")
    assert [s.pop(), s.pop(), s.pop()] == ["C", "B", "A"] and s.is_empty()


def test_size_sau_pop():
    s = make("A", "B", "C")
    s.pop()
    assert s.size() == 2 and s.peek() == "B"


def test_rong():
    s = make("A")
    s.pop()
    with pytest.raises(IndexError, match="ngăn xếp rỗng"):
        s.peek()
    with pytest.raises(IndexError, match="ngăn xếp rỗng"):
        s.pop()


def test_push_sau_pop():
    s = make("A", "B")
    s.pop()
    s.push("X")
    assert s.pop() == "X" and s.pop() == "A" and s.size() == 0
