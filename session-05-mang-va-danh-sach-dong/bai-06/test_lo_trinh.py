from lo_trinh import Route


def make(*stops):
    r = Route()
    for s in stops:
        r.append(s)
    return r


def test_chen_giua_khong_mat_diem():
    r = make("A", "B", "C", "D")
    r.moves = 0
    r.insert(1, "X")
    assert r.stops() == ["A", "X", "B", "C", "D"]
    assert r.moves == 3, "chèn vào chỉ số 1 của 4 phần tử phải dịch 3 tham chiếu"


def test_chen_khi_day():
    r = make("A", "B")
    r.insert(0, "X")
    r.insert(0, "Y")
    assert r.stops() == ["Y", "X", "A", "B"] and len(r) == 4


def test_chi_so_am_va_vuot():
    r = make("A", "B", "C")
    r.insert(-1, "X")
    assert r.stops() == ["A", "B", "X", "C"]
    r.insert(-99, "Y")
    r.insert(99, "Z")
    assert r.stops() == ["Y", "A", "B", "X", "C", "Z"]


def test_chen_cuoi_khong_dich_va_rong():
    r = make("A", "B", "C", "D")
    r.moves = 0
    r.insert(4, "E")
    assert r.moves == 0 and r.stops()[-1] == "E"
    e = Route()
    e.insert(0, "A")
    assert e.stops() == ["A"]
