from tong_dai import SupportDesk


def make(*codes):
    d = SupportDesk()
    for c in codes:
        d.add(c)
    return d


def test_fifo():
    d = make("A", "B", "C")
    assert [d.serve(), d.serve(), d.serve()] == ["A", "B", "C"]


def test_yeu_cau_gap_len_dau():
    d = make("A", "B")
    d.add_urgent("G1")
    d.add_urgent("G2")
    assert [d.serve() for _ in range(4)] == ["G2", "G1", "A", "B"]


def test_hang_rong():
    d = make("A")
    d.serve()
    assert d.serve() is None and d.recent_list() == ["A"]


def test_gan_nhat():
    d = make("A", "B", "C", "D", "E")
    for _ in range(5):
        d.serve()
    assert d.recent_list() == ["E", "D", "C"]
