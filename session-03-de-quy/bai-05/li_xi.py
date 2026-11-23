"""Đếm số cách đi trên bản đồ trò chơi "Lì xì" của ví MoMo."""


def route_count(cells):
    # Số cách đi hết bản đồ cells ô, mỗi lượt tiến 1 ô hoặc 2 ô.
    # Bản đồ 0 ô: đã ở đích, có đúng 1 cách (không đi). cells âm: 0 cách.
    if cells <= 1:
        return cells
    return route_count(cells - 1) + route_count(cells - 2)


if __name__ == "__main__":
    for cells in (1, 2, 5, 10):
        print(f"Bản đồ {cells} ô:", route_count(cells), "cách đi")
    print("Bản đồ 0 ô (đã ở đích):", route_count(0), "cách đi")
    print("Bản đồ 40 ô:", route_count(40), "cách đi")
    print("Bản đồ 80 ô:", route_count(80), "cách đi")
