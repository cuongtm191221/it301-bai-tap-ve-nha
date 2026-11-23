from hoan_tac import UndoablePlaylist


def check(p, codes):
    result, current = [], p.head
    while current is not None:
        result.append(current.value[:5])
        current = current.next
    assert result == codes and p.size == len(codes)
    if codes:
        assert p.tail.value[:5] == codes[-1] and p.tail.next is None
    else:
        assert p.head is None and p.tail is None


def make(limit=3):
    p = UndoablePlaylist(limit)
    p.add_song("ZM001", "Bình minh trên phố")
    p.add_song("ZM002", "Mưa đêm")
    p.add_song("ZM003", "Đường về nhà")
    return p


def test_them_bo_hien_thi():
    p = UndoablePlaylist()
    assert p.to_lines() == ["Danh sách phát đang trống."]
    assert p.add_song("  zm001 ", " Bình minh trên phố ") == "Đã thêm: ZM001 - Bình minh trên phố"
    assert p.add_song("ZM002", "Mưa đêm") == "Đã thêm: ZM002 - Mưa đêm"
    assert p.remove_song(" zm001") == "Đã bỏ: ZM001 - Bình minh trên phố"
    assert p.to_lines() == ["1. ZM002 - Mưa đêm"]
    check(p, ["ZM002"])


def test_hoan_tac_them():
    p = make()
    assert p.undo() == "Đã hoàn tác thêm: ZM003 - Đường về nhà"
    check(p, ["ZM001", "ZM002"])
    p.add_song("ZM004", "Phố cũ")
    check(p, ["ZM001", "ZM002", "ZM004"])


def test_bay_1_thao_tac_khong_thanh_cong_khong_duoc_ghi():
    p = make()
    assert p.add_song("zm001", "Bình minh trên phố") == "Bài ZM001 đã có trong danh sách phát."
    assert p.remove_song("ZM999") == "Không tìm thấy bài ZM999 trong danh sách phát."
    assert p.undo() == "Đã hoàn tác thêm: ZM003 - Đường về nhà"
    check(p, ["ZM001", "ZM002"])


def test_bay_2_hoan_tac_bo_tra_bai_ve_dung_vi_tri():
    for code, position, title in [("ZM001", 1, "Bình minh trên phố"), ("ZM002", 2, "Mưa đêm"), ("ZM003", 3, "Đường về nhà")]:
        p = make()
        p.remove_song(code)
        assert p.undo() == f"Đã hoàn tác bỏ: {code} - {title} (về vị trí {position})"
        check(p, ["ZM001", "ZM002", "ZM003"])
        p.add_song("ZM004", "Phố cũ")
        check(p, ["ZM001", "ZM002", "ZM003", "ZM004"])


def test_bay_3_het_thao_tac_de_hoan_tac():
    p = UndoablePlaylist()
    assert p.undo() == "Không còn thao tác nào để hoàn tác."
    p.add_song("ZM001", "Bình minh trên phố")
    p.undo()
    check(p, [])
    assert p.undo() == "Không còn thao tác nào để hoàn tác."
    assert p.add_song("ZM002", "Mưa đêm") == "Đã thêm: ZM002 - Mưa đêm"
    check(p, ["ZM002"])


def test_bay_4_chi_giu_ba_thao_tac_gan_nhat():
    p = UndoablePlaylist(limit=3)
    for code in ["ZM001", "ZM002", "ZM003", "ZM004", "ZM005"]:
        p.add_song(code, "Bài")
    assert p.undo() == "Đã hoàn tác thêm: ZM005 - Bài"
    assert p.undo() == "Đã hoàn tác thêm: ZM004 - Bài"
    assert p.undo() == "Đã hoàn tác thêm: ZM003 - Bài"
    assert p.undo() == "Không còn thao tác nào để hoàn tác."
    check(p, ["ZM001", "ZM002"])


def test_bay_5_hoan_tac_nhieu_thao_tac_dan_xen():
    p = make(limit=5)
    p.remove_song("ZM002")
    p.add_song("ZM004", "Phố cũ")
    p.remove_song("ZM001")
    check(p, ["ZM003", "ZM004"])
    assert p.undo() == "Đã hoàn tác bỏ: ZM001 - Bình minh trên phố (về vị trí 1)"
    assert p.undo() == "Đã hoàn tác thêm: ZM004 - Phố cũ"
    assert p.undo() == "Đã hoàn tác bỏ: ZM002 - Mưa đêm (về vị trí 2)"
    check(p, ["ZM001", "ZM002", "ZM003"])


def test_thao_tac_moi_sau_khi_hoan_tac():
    p = make()
    p.undo()
    p.add_song("ZM005", "Gió qua thềm")
    assert p.undo() == "Đã hoàn tác thêm: ZM005 - Gió qua thềm"
    assert p.undo() == "Đã hoàn tác thêm: ZM002 - Mưa đêm"
    check(p, ["ZM001"])


def test_gioi_han_mot_thao_tac():
    p = UndoablePlaylist(limit=1)
    p.add_song("ZM001", "Bình minh trên phố")
    p.add_song("ZM002", "Mưa đêm")
    p.remove_song("ZM001")
    assert p.undo() == "Đã hoàn tác bỏ: ZM001 - Bình minh trên phố (về vị trí 1)"
    assert p.undo() == "Không còn thao tác nào để hoàn tác."
    check(p, ["ZM001", "ZM002"])
