from lien_ket import make_list
from bai_n3 import move_to_front


def test_dua_node_cuoi_len_dau():
    q = make_list(["A", "B", "C"])
    assert move_to_front(q, "C") is True
    assert q.to_text() == "C -> A -> B -> None"
    assert q.tail.value == "B"


def test_da_o_dau():
    q = make_list(["A", "B"])
    assert move_to_front(q, "A") is True
    assert q.to_text() == "A -> B -> None"


def test_khong_co():
    q = make_list(["A", "B"])
    assert move_to_front(q, "Z") is False
    assert q.to_text() == "A -> B -> None"
