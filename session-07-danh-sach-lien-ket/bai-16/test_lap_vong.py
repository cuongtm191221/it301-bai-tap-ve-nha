import pytest
from lap_vong import build, has_loop_v1, has_loop_v2, count_message

CODES = ["ZM001", "ZM002", "ZM003", "ZM004", "ZM005"]
BOTH = [has_loop_v1, has_loop_v2]


@pytest.mark.parametrize("check", BOTH)
def test_danh_sach_binh_thuong(check):
    assert check(build(CODES)) is False
    assert check(build(CODES[:2])) is False


@pytest.mark.parametrize("check", BOTH)
def test_cuoi_tro_ve_giua(check):
    assert check(build(CODES, loop_to=2)) is True
    assert check(build(CODES, loop_to=3)) is True


@pytest.mark.parametrize("check", BOTH)
def test_bay_1_cuoi_tro_ve_dau(check):
    assert check(build(CODES, loop_to=0)) is True


@pytest.mark.parametrize("check", BOTH)
def test_bay_2_node_tro_ve_chinh_no(check):
    assert check(build(["ZM001"], loop_to=0)) is True
    assert check(build(CODES, loop_to=4)) is True


@pytest.mark.parametrize("check", BOTH)
def test_bay_3_danh_sach_rong_va_mot_bai(check):
    assert check(None) is False
    assert check(build(["ZM001"])) is False


@pytest.mark.parametrize("check", BOTH)
def test_bay_4_bai_lap_lai_khong_phai_lap_vong(check):
    assert check(build(["ZM001", "ZM002", "ZM001", "ZM002"])) is False
    assert check(build(["ZM001", "ZM001"])) is False


@pytest.mark.parametrize("check", BOTH)
def test_moi_do_dai_va_moi_vi_tri_lap(check):
    for n in range(1, 9):
        values = [f"ZM{i:03d}" for i in range(n)]
        assert check(build(values)) is False
        for start in range(n):
            assert check(build(values, loop_to=start)) is True


@pytest.mark.parametrize("check", BOTH)
def test_bay_5_khong_lam_thay_doi_danh_sach(check):
    head = build(CODES)
    check(head)
    values, current = [], head
    while current is not None:
        values.append(current.value)
        current = current.next
    assert values == CODES


def test_thong_bao_dem():
    assert count_message(build(CODES)) == "Danh sách phát có 5 bài."
    assert count_message(build(["ZM001"])) == "Danh sách phát có 1 bài."
    assert count_message(None) == "Danh sách phát đang trống."
    assert count_message(build(CODES, loop_to=2)) == "Danh sách phát bị lặp vòng, không thể đếm."
    assert count_message(build(["ZM001"], loop_to=0)) == "Danh sách phát bị lặp vòng, không thể đếm."
