import pytest
from nghe_lai import build_log, kth_from_end_v1, kth_from_end_v2, replay_message

SONGS = ["ZM001 - Bình minh trên phố", "ZM002 - Mưa đêm", "ZM003 - Đường về nhà", "ZM002 - Mưa đêm", "ZM004 - Phố cũ"]
BOTH = [kth_from_end_v1, kth_from_end_v2]


@pytest.mark.parametrize("solve", BOTH)
def test_bai_o_cuoi_o_giua_o_dau(solve):
    log = build_log(SONGS)
    assert solve(log, 1) == "ZM004 - Phố cũ"
    assert solve(log, 3) == "ZM003 - Đường về nhà"
    assert solve(log, 5) == "ZM001 - Bình minh trên phố"


@pytest.mark.parametrize("solve", BOTH)
def test_bay_1_k_lon_hon_so_bai(solve):
    log = build_log(SONGS)
    assert solve(log, 6) is None
    assert solve(log, 100) is None


@pytest.mark.parametrize("solve", BOTH)
def test_bay_2_k_khong_hop_le(solve):
    log = build_log(SONGS)
    assert solve(log, 0) is None
    assert solve(log, -2) is None


@pytest.mark.parametrize("solve", BOTH)
def test_bay_3_nhat_ky_rong_va_mot_bai(solve):
    assert solve(None, 1) is None
    one = build_log(["ZM001 - Bình minh trên phố"])
    assert solve(one, 1) == "ZM001 - Bình minh trên phố"
    assert solve(one, 2) is None


@pytest.mark.parametrize("solve", BOTH)
def test_bay_4_khong_lam_thay_doi_nhat_ky(solve):
    log = build_log(SONGS)
    solve(log, 2)
    solve(log, 9)
    values, current = [], log
    while current is not None:
        values.append(current.value)
        current = current.next
    assert values == SONGS


@pytest.mark.parametrize("solve", BOTH)
def test_hai_giai_phap_cho_cung_ket_qua(solve):
    for n in range(0, 8):
        log = build_log([f"ZM{i:03d} - Bài {i}" for i in range(1, n + 1)])
        for k in range(-1, n + 3):
            expected = f"ZM{n - k + 1:03d} - Bài {n - k + 1}" if 1 <= k <= n else None
            assert solve(log, k) == expected


def test_thong_bao_nghe_lai():
    log = build_log(SONGS)
    assert replay_message(log, 1) == "Bài cách đây 1 lượt nghe: ZM004 - Phố cũ"
    assert replay_message(log, 2) == "Bài cách đây 2 lượt nghe: ZM002 - Mưa đêm"
    assert replay_message(log, 6) == "Không có bài cách đây 6 lượt nghe."


def test_bay_5_thong_bao_khi_du_lieu_la():
    log = build_log(SONGS)
    assert replay_message(log, 0) == "Số lượt phải từ 1 trở lên."
    assert replay_message(None, 1) == "Nhật ký nghe đang trống."
    assert replay_message(None, 0) == "Nhật ký nghe đang trống."
