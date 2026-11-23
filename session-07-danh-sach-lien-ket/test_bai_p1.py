from dap_an_ma_hoa import DUNG, SAI, wrong_keys
from lien_ket import make_list
from bai_p1 import CLAIMS, count_waiting_fixed, newest_submission_fixed


def test_nhan_xet_cua_ai():
    wrong = wrong_keys(CLAIMS, {"count_waiting": SAI, "newest_submission": SAI, "has_code": DUNG})
    assert wrong == [], f"chưa đúng hoặc chưa ghi: {wrong}"


def test_dem_khong_lam_hong_danh_sach():
    q = make_list(["BN1", "BN2", "BN3"])
    assert count_waiting_fixed(q) == 3
    assert count_waiting_fixed(q) == 3
    assert q.to_text() == "BN1 -> BN2 -> BN3 -> None"


def test_bai_moi_nhat():
    assert newest_submission_fixed(make_list(["BN1", "BN2"])) == "BN2"
    assert newest_submission_fixed(make_list([])) is None
