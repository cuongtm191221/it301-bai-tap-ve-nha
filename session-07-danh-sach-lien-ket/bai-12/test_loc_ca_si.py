from loc_ca_si import ArtistPlaylist

SONGS = [
    ("ZM001", "Bình minh trên phố", "Hoàng Lan"),
    ("ZM002", "Mưa đêm", "Hoàng Lan"),
    ("ZM003", "Đường về nhà", "Minh Khôi"),
    ("ZM004", "Phố cũ", "Hoàng Lan"),
    ("ZM005", "Gió qua thềm", "Thu An"),
    ("ZM006", "Ngày nắng", "Thu An"),
]


def make():
    p = ArtistPlaylist()
    for code, title, artist in SONGS:
        p.add_song(code, title, artist)
    return p


def codes(p):
    result, current = [], p.head
    while current is not None:
        result.append(current.value[:5])
        current = current.next
    assert len(result) == p.size
    if result:
        assert p.tail.value[:5] == result[-1] and p.tail.next is None
    else:
        assert p.tail is None
    return result


def test_them_va_hien_thi():
    p = ArtistPlaylist()
    assert p.to_lines() == ["Danh sách phát đang trống."]
    assert p.add_song("ZM001", "Bình minh trên phố", "Hoàng Lan") == "Đã thêm: ZM001 - Bình minh trên phố - Hoàng Lan"
    assert p.to_lines() == ["1. ZM001 - Bình minh trên phố - Hoàng Lan"]
    assert codes(p) == ["ZM001"]


def test_bay_1_chuan_hoa_du_lieu_nhap():
    p = ArtistPlaylist()
    assert p.add_song("  zm002 ", " Mưa đêm ", "  hoàng lan ") == "Đã thêm: ZM002 - Mưa đêm - Hoàng Lan"
    assert p.count_by_artist(" HOÀNG LAN ") == 1
    assert p.remove_by_artist(" hoàng lan") == "Đã bỏ 1 bài của Hoàng Lan."


def test_dem_theo_ca_si():
    p = make()
    assert p.count_by_artist("Hoàng Lan") == 3
    assert p.count_by_artist("Minh Khôi") == 1
    assert p.count_by_artist("Lê Vy") == 0
    assert ArtistPlaylist().count_by_artist("Hoàng Lan") == 0


def test_bay_2_nhieu_bai_lien_nhau_o_dau():
    p = make()
    assert p.remove_by_artist("Hoàng Lan") == "Đã bỏ 3 bài của Hoàng Lan."
    assert codes(p) == ["ZM003", "ZM005", "ZM006"]
    assert p.head.value == "ZM003 - Đường về nhà - Minh Khôi"


def test_bay_3_bai_o_cuoi_roi_them():
    p = make()
    assert p.remove_by_artist("Thu An") == "Đã bỏ 2 bài của Thu An."
    assert p.tail.value == "ZM004 - Phố cũ - Hoàng Lan"
    p.add_song("ZM007", "Đêm thành phố", "Minh Khôi")
    assert codes(p) == ["ZM001", "ZM002", "ZM003", "ZM004", "ZM007"]


def test_bay_4_bo_het_danh_sach():
    p = ArtistPlaylist()
    p.add_song("ZM001", "Bình minh trên phố", "Hoàng Lan")
    p.add_song("ZM002", "Mưa đêm", "Hoàng Lan")
    assert p.remove_by_artist("Hoàng Lan") == "Đã bỏ 2 bài của Hoàng Lan."
    assert p.head is None and p.tail is None and p.size == 0
    assert p.to_lines() == ["Danh sách phát đang trống."]
    assert p.add_song("ZM003", "Đường về nhà", "Minh Khôi") == "Đã thêm: ZM003 - Đường về nhà - Minh Khôi"
    assert codes(p) == ["ZM003"]


def test_bay_5_khong_co_bai_nao():
    p = make()
    assert p.remove_by_artist("Lê Vy") == "Không có bài nào của Lê Vy."
    assert codes(p) == ["ZM001", "ZM002", "ZM003", "ZM004", "ZM005", "ZM006"]
    assert ArtistPlaylist().remove_by_artist("Lê Vy") == "Không có bài nào của Lê Vy."


def test_bai_cua_ca_si_nam_xen_ke():
    p = ArtistPlaylist()
    for i, artist in enumerate(["Thu An", "Hoàng Lan", "Thu An", "Hoàng Lan", "Hoàng Lan", "Thu An"], start=1):
        p.add_song(f"ZM00{i}", f"Bài {i}", artist)
    assert p.remove_by_artist("Hoàng Lan") == "Đã bỏ 3 bài của Hoàng Lan."
    assert codes(p) == ["ZM001", "ZM003", "ZM006"]
