from dap_an_ma_hoa import X1, X2, wrong_keys
from bai_p2 import RATIOS, time_front_inserts


def test_ham_do_tra_so_mili_giay():
    for kind in ["list", "linked"]:
        ms = time_front_inserts(kind, 1000, number=50)
        assert isinstance(ms, float) and ms > 0, f"{kind}: cần trả số mili giây dương"


def test_ti_le_da_ghi():
    wrong = wrong_keys(RATIOS, {"list": X2, "linked": X1})
    assert wrong == [], f"chưa đúng hoặc chưa ghi: {wrong}"
