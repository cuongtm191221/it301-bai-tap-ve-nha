from hang_cho import RideQueue


def make(*codes):
    q = RideQueue()
    for c in codes:
        q.join(c)
    return q


def test_den_truoc_phuc_vu_truoc():
    q = make("YC01", "YC02", "YC03")
    assert [q.serve(), q.serve(), q.serve()] == ["YC01", "YC02", "YC03"]


def test_hang_rong():
    q = make()
    assert q.serve() is None and q.size() == 0


def test_vi_tri_dem_tu_1():
    q = make("YC01", "YC02", "YC03")
    assert q.position("YC01") == 1 and q.position("YC03") == 3
    assert q.position("YC09") is None


def test_huy():
    q = make("YC01", "YC02", "YC03")
    assert q.cancel("YC02") is True and q.cancel("YC09") is False
    assert q.size() == 2 and q.serve() == "YC01" and q.serve() == "YC03"
