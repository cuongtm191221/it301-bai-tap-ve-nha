from gop_danh_sach import Playlist, append_all


def make(codes):
    p = Playlist()
    for code in codes:
        p.add_last(code)
    return p


def test_gop_va_bo_qua_bai_trung():
    mine = make(["ZM001", "ZM002", "ZM003"])
    shared = make(["ZM003", "ZM004", "ZM005"])
    assert append_all(mine, shared) == 2
    assert mine.to_text() == "ZM001 -> ZM002 -> ZM003 -> ZM004 -> ZM005 -> None"
    assert mine.size == 5 and mine.tail.value == "ZM005"


def test_hai_danh_sach_doc_lap_sau_khi_gop():
    mine = make(["ZM001"])
    shared = make(["ZM002", "ZM003"])
    append_all(mine, shared)
    shared.add_last("ZM006")
    assert mine.to_text() == "ZM001 -> ZM002 -> ZM003 -> None"
    mine.add_last("ZM007")
    assert shared.to_text() == "ZM002 -> ZM003 -> ZM006 -> None"


def test_nguon_khong_doi():
    mine = make(["ZM001"])
    shared = make(["ZM002", "ZM003"])
    append_all(mine, shared)
    assert shared.to_text() == "ZM002 -> ZM003 -> None" and shared.size == 2


def test_dich_rong():
    new_list = Playlist()
    assert append_all(new_list, make(["ZM001", "ZM002"])) == 2
    assert new_list.to_text() == "ZM001 -> ZM002 -> None"
    assert new_list.size == 2 and new_list.tail.value == "ZM002"


def test_nguon_rong_va_trung_het():
    mine = make(["ZM001", "ZM002"])
    assert append_all(mine, Playlist()) == 0
    assert append_all(mine, make(["ZM002", "ZM001"])) == 0
    assert mine.to_text() == "ZM001 -> ZM002 -> None" and mine.size == 2
