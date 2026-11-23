from dap_an_ma_hoa import O1, ON, wrong_keys
from bai_c3 import ANSWERS


def test_big_o_sau_thao_tac():
    key = {"a": O1, "b": O1, "c": ON, "d": ON, "e": ON, "f": O1}
    wrong = wrong_keys(ANSWERS, key)
    assert wrong == [], f"chưa đúng hoặc chưa ghi: {wrong}"
