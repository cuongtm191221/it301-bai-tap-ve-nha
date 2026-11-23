"""P2 - Đo tỉ lệ thời gian chèn ở đầu: list và danh sách liên kết."""
import timeit


def time_front_inserts(kind, n, number=1000):
    """Đo thời gian (mili giây) của `number` lần chèn ở đầu vào cấu trúc có sẵn n phần tử.

    kind: "list" (dùng list.insert(0, x)) hoặc "linked" (dùng LinkedList.add_first(x)).
    Cấu trúc được tạo trong phần chuẩn bị (setup) của timeit, không tính vào thời gian.
    Lặp đo 5 lần, lấy lần nhỏ nhất.
    """
    raise NotImplementedError


# Sau khi chạy: n gấp đôi thì thời gian gấp khoảng bao nhiêu lần? Ghi "x1", "x2" hoặc "x4".
RATIOS = {
    "list": "?",
    "linked": "?",
}


if __name__ == "__main__":
    for kind in ["list", "linked"]:
        a = time_front_inserts(kind, 50_000)
        b = time_front_inserts(kind, 100_000)
        print(kind, round(a, 3), "ms ->", round(b, 3), "ms, tỉ lệ", round(b / a, 1))
