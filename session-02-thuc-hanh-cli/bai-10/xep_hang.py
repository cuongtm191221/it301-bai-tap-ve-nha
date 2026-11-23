"""Nghiệp vụ bảng xếp hạng mùa giải của giải đấu Liên Quân Mobile do Garena tổ chức.

Mỗi người chơi là một list: [tên trong game, điểm xếp hạng]. Tên không trùng nhau (không phân biệt hoa thường).
Bảng xếp hạng: điểm cao trước; bằng điểm thì ai đứng trước trong danh sách đăng ký xếp trước.
"""
import timeit

SAMPLE_PLAYERS = [
    ["ShadowFox", 2350], ["Bông", 1980], ["KiraVN", 2350],
    ["MèoMun", 1520], ["Tí Nị", 2100], ["Zed99", 1980],
]


def make_players():
    """Có sẵn. Trả về bản sao danh sách đăng ký mẫu."""
    return [p[:] for p in SAMPLE_PLAYERS]


def make_big_players(n):
    """Có sẵn. Danh sách giả lập n người chơi, nhiều người bằng điểm."""
    return [[f"P{k:06d}", 1000 + (k * 7919) % 1500] for k in range(n)]


def top_slow(players, k):
    """Có sẵn. Bản cũ, KHÔNG sửa. List k người đứng đầu bảng xếp hạng (ít hơn k thì trả tất cả); không làm đổi players."""
    pool = players[:]
    result = []
    while pool and len(result) < k:
        best = 0
        for i in range(1, len(pool)):
            if pool[i][1] > pool[best][1]:
                best = i
        result.append(pool.pop(best))
    return result


def rank_slow(players, name):
    """Có sẵn. Bản cũ, KHÔNG sửa. Hạng (đếm từ 1) của người chơi có tên name hoặc None."""
    ranked = top_slow(players, len(players))
    for i, p in enumerate(ranked):
        if p[0].lower() == name.strip().lower():
            return i + 1
    return None


def top_fast(players, k):
    """Cùng kết quả với top_slow; không gọi bản cũ; 200.000 người chơi trong 2 giây."""
    raise NotImplementedError


def rank_fast(players, name):
    """Cùng kết quả với rank_slow; không gọi bản cũ, không sắp xếp; một lượt duyệt sau khi biết điểm của người cần tìm."""
    raise NotImplementedError


def find_player(players, name):
    """Người chơi có tên name (không phân biệt hoa thường, bỏ khoảng trắng hai đầu) hoặc None."""
    raise NotImplementedError


def apply_match(players, name, delta_text):
    """Cộng điểm trận (có thể âm) cho người chơi; điểm không xuống dưới 0. Trả về người chơi. Lỗi (bảng giữ nguyên):
    "Không có người chơi <tên>", "Điểm trận phải là số nguyên từ -100 đến 100"."""
    raise NotImplementedError


def benchmark(sizes, number=1):
    """Với từng n trong sizes, trên make_big_players(n), tra hạng của người cuối danh sách:
    đo bằng timeit một lần rank_slow và rank_fast (ms). Trả về list bộ (n, ms bản cũ, ms bản mới)."""
    raise NotImplementedError
