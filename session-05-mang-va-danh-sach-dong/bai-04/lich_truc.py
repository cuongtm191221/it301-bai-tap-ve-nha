"""Lịch trực và danh sách tài xế GrabBike của một điểm đón."""
def make_board(days):
    # Lịch trực: mỗi ngày một list tài xế riêng.
    return [[]] * days


def assign(board, day, driver):
    board[day].append(driver)


def count_shifts(board, driver):
    total = 0
    for day in board:
        total += day.count(driver)
    return total


def remove_absent(drivers, absent):
    # Xóa tại chỗ khỏi drivers mọi tài xế có tên trong absent, giữ thứ tự những người còn lại.
    for name in drivers:
        if name in absent:
            drivers.remove(name)


if __name__ == "__main__":
    board = make_board(3)
    assign(board, 0, "An")
    assign(board, 1, "Bình")
    print("Lịch 3 ngày:", board)
    print("Số ca của An:", count_shifts(board, "An"))
    drivers = ["An", "Bình", "Chi", "Dũng", "Em"]
    remove_absent(drivers, ["Bình", "Chi"])
    print("Tài xế còn trực:", drivers)
