from thoi_luong import Playlist, format_duration, longest_song, total_seconds


def make(songs):
    p = Playlist()
    for song in songs:
        p.add_last(song)
    return p


SONGS = ["ZM001 - 215", "ZM002 - 95", "ZM003 - 248", "ZM004 - 185"]


def test_tong_thoi_luong_tinh_ca_bai_dau():
    assert total_seconds(make(SONGS)) == 743
    assert total_seconds(make(["ZM001 - 215"])) == 215


def test_bai_dai_nhat_so_sanh_theo_so():
    assert longest_song(make(SONGS)) == "ZM003 - 248"
    assert longest_song(make(["ZM001 - 95", "ZM002 - 1000"])) == "ZM002 - 1000"


def test_bang_nhau_lay_bai_dung_truoc():
    assert longest_song(make(["ZM001 - 200", "ZM002 - 200"])) == "ZM001 - 200"


def test_dinh_dang_phut_giay():
    assert format_duration(743) == "12:23"
    assert format_duration(185) == "3:05"
    assert format_duration(60) == "1:00"
    assert format_duration(0) == "0:00"


def test_danh_sach_rong():
    assert total_seconds(Playlist()) == 0
    assert longest_song(Playlist()) is None


def test_khong_lam_doi_danh_sach():
    p = make(SONGS)
    total_seconds(p)
    longest_song(p)
    assert p.to_text() == " -> ".join(SONGS + ["None"]) and p.size == 4
