from lich_truc import make_board, assign, count_shifts, remove_absent


def test_moi_ngay_mot_list_rieng():
    board = make_board(3)
    assign(board, 0, "An")
    assign(board, 1, "Bình")
    assert board == [["An"], ["Bình"], []]
    assert board[0] is not board[1]


def test_dem_ca():
    board = make_board(4)
    assign(board, 0, "An")
    assign(board, 3, "An")
    assert count_shifts(board, "An") == 2 and count_shifts(board, "Chi") == 0


def test_xoa_hai_nguoi_lien_nhau():
    drivers = ["An", "Bình", "Chi", "Dũng", "Em"]
    remove_absent(drivers, ["Bình", "Chi"])
    assert drivers == ["An", "Dũng", "Em"]


def test_xoa_tai_cho_va_trung_ten():
    drivers = ["An", "An", "Bình", "An"]
    same = drivers
    remove_absent(drivers, ["An"])
    assert same is drivers and drivers == ["Bình"]
    remove_absent(drivers, [])
    assert drivers == ["Bình"]
