from playlist import Playlist


def test_add_last_ba_bai():
    p = Playlist()
    for code in ["ZM001", "ZM002", "ZM003"]:
        p.add_last(code)
    assert p.to_text() == "ZM001 -> ZM002 -> ZM003 -> None"
    assert p.tail.value == "ZM003" and p.size == 3


def test_add_first_sau_khi_da_co_bai():
    p = Playlist()
    for code in ["ZM001", "ZM002", "ZM003"]:
        p.add_last(code)
    p.add_first("ZM000")
    assert p.to_text() == "ZM000 -> ZM001 -> ZM002 -> ZM003 -> None"
    assert p.tail.value == "ZM003" and p.size == 4


def test_add_first_vao_danh_sach_rong_roi_add_last():
    p = Playlist()
    p.add_first("ZM010")
    assert p.head is p.tail and p.size == 1
    p.add_last("ZM011")
    assert p.to_text() == "ZM010 -> ZM011 -> None"
    assert p.tail.value == "ZM011" and p.size == 2
