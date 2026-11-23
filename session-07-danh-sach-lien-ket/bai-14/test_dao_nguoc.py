from dao_nguoc import Playlist, reversed_copy, reverse_in_place


def make(codes):
    p = Playlist()
    for code in codes:
        p.add_last(code)
    return p


def nodes(p):
    result, current = [], p.head
    while current is not None:
        result.append(current)
        current = current.next
    return result


def check(p, codes):
    assert [n.value for n in nodes(p)] == codes
    assert p.size == len(codes)
    if codes:
        assert p.tail is nodes(p)[-1] and p.tail.next is None
    else:
        assert p.head is None and p.tail is None


def test_ban_dao_dung_thu_tu():
    p = make(["ZM001", "ZM002", "ZM003", "ZM004"])
    check(reversed_copy(p), ["ZM004", "ZM003", "ZM002", "ZM001"])


def test_bay_1_ban_dao_doc_lap_voi_danh_sach_goc():
    p = make(["ZM001", "ZM002", "ZM003"])
    before = nodes(p)
    copy = reversed_copy(p)
    check(p, ["ZM001", "ZM002", "ZM003"])
    assert nodes(p) == before
    assert not set(map(id, nodes(copy))) & set(map(id, before))
    copy.add_last("ZM009")
    p.add_last("ZM004")
    check(copy, ["ZM003", "ZM002", "ZM001", "ZM009"])
    check(p, ["ZM001", "ZM002", "ZM003", "ZM004"])


def test_dao_tai_cho_dung_thu_tu():
    p = make(["ZM001", "ZM002", "ZM003", "ZM004"])
    assert reverse_in_place(p) is None
    check(p, ["ZM004", "ZM003", "ZM002", "ZM001"])


def test_bay_2_dao_tai_cho_khong_tao_node_moi():
    p = make(["ZM001", "ZM002", "ZM003"])
    before = nodes(p)
    reverse_in_place(p)
    assert nodes(p) == before[::-1]


def test_bay_3_tail_dung_sau_khi_dao_roi_them():
    p = make(["ZM001", "ZM002", "ZM003"])
    reverse_in_place(p)
    assert p.head.value == "ZM003" and p.tail.value == "ZM001"
    p.add_last("ZM004")
    check(p, ["ZM003", "ZM002", "ZM001", "ZM004"])


def test_bay_4_danh_sach_rong_va_mot_bai():
    empty = Playlist()
    reverse_in_place(empty)
    check(empty, [])
    check(reversed_copy(empty), [])
    one = make(["ZM001"])
    reverse_in_place(one)
    check(one, ["ZM001"])
    check(reversed_copy(one), ["ZM001"])
    one.add_last("ZM002")
    check(one, ["ZM001", "ZM002"])


def test_bay_5_dao_hai_lan_ve_thu_tu_cu():
    p = make(["ZM001", "ZM002", "ZM003", "ZM004", "ZM005"])
    reverse_in_place(p)
    reverse_in_place(p)
    check(p, ["ZM001", "ZM002", "ZM003", "ZM004", "ZM005"])
    check(reversed_copy(reversed_copy(p)), ["ZM001", "ZM002", "ZM003", "ZM004", "ZM005"])


def test_danh_sach_co_bai_lap_lai():
    p = make(["ZM001", "ZM002", "ZM001"])
    check(reversed_copy(p), ["ZM001", "ZM002", "ZM001"])
    reverse_in_place(p)
    check(p, ["ZM001", "ZM002", "ZM001"])
