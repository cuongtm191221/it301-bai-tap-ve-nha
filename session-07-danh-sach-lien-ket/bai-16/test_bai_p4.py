from dap_an_ma_hoa import DOI, DON, LIST, wrong_keys
from bai_p4 import CHOICES, LY_DO


def test_lua_chon():
    wrong = wrong_keys(CHOICES, {"t1": LIST, "t2": DON, "t3": DOI, "t4": DOI, "t5": LIST})
    assert wrong == [], f"chưa đúng hoặc chưa ghi: {wrong}"


def test_co_ly_do():
    for k in ["t1", "t2", "t3", "t4", "t5"]:
        assert len(LY_DO.get(k, "").split()) >= 5, f"{k}: cần một câu lý do"
