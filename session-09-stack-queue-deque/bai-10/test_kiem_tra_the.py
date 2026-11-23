from kiem_tra_the import check_tags, review_message


def test_hop_le():
    assert check_tags("<b>Tai nghe</b> <i>chống ồn</i><br/>Pin <b>30 giờ</b>") is None
    assert check_tags("<b><i>x</i></b>") is None and check_tags("") is None


def test_khong_khop():
    assert check_tags("<b>Giảm <i>50%</b></i>") == "Thẻ </b> ở vị trí 14 không khớp với <i> ở vị trí 8"


def test_khong_co_the_mo():
    assert check_tags("Giá < 100k, </u>bảo hành") == "Thẻ </u> ở vị trí 12 không có thẻ mở"


def test_chua_dong():
    assert check_tags("<ul><li>Màu đen<li>Màu trắng</ul>") == "Thẻ </ul> ở vị trí 28 không khớp với <li> ở vị trí 15"
    assert check_tags("<b>Hàng <i>mới") == "Thẻ <i> ở vị trí 8 chưa đóng"


def test_khong_phan_biet_hoa_thuong():
    assert check_tags("<B>Hàng chính hãng</b>") is None


def test_dau_nho_hon_khong_phai_the():
    assert check_tags("Giá < 100k và > 50k") is None
    assert check_tags("a <b c> d") is None


def test_thong_bao():
    assert review_message("<b>A</b><br/>") == "Hợp lệ (3 thẻ)."
    assert review_message("<b>A") == "Từ chối: Thẻ <b> ở vị trí 0 chưa đóng"


def test_mo_ta_dai():
    text = "<b>" * 20000 + "x" + "</b>" * 20000
    assert check_tags(text) is None
