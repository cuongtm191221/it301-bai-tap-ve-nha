from bai_c2 import from_codes


def test_vi_du_trong_de():
    q = from_codes(["BN201", "BN202", "BN203"])
    assert q.to_text() == "BN201 -> BN202 -> BN203 -> None"
    assert q.tail.value == "BN203"


def test_danh_sach_rong():
    q = from_codes([])
    assert q.head is None
    assert q.tail is None


def test_them_cuoi_sau_khi_tao():
    q = from_codes(["BN201"])
    q.add_last("BN202")
    assert q.to_text() == "BN201 -> BN202 -> None"
