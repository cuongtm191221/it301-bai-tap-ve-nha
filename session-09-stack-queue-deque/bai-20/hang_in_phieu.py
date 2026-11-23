"""Tối ưu hàng in phiếu giao hàng ở kho Tiki."""


def print_order_slow(commands):
    """Có sẵn. Bản cũ đang chạy. commands: list chuỗi "ADD <mã>", "URGENT <mã>", "PRINT". Trả về (list mã đã in theo thứ tự, list mã còn chờ từ đầu đến cuối hàng)."""
    waiting = []
    printed = []
    for command in commands:
        parts = command.split()
        if parts[0] == "ADD":
            if parts[1] not in waiting:
                waiting = waiting + [parts[1]]
        elif parts[0] == "URGENT":
            if parts[1] not in waiting:
                waiting.insert(0, parts[1])
        elif parts[0] == "PRINT":
            if len(waiting) > 0:
                printed = printed + [waiting.pop(0)]
    return printed, waiting


def print_order_fast(commands):
    """Cùng kết quả với print_order_slow cho mọi commands; 200.000 lệnh chạy dưới 1 giây; không sửa commands."""
    raise NotImplementedError


def print_summary(commands):
    """Dùng print_order_fast, trả về "In <a> phiếu, còn chờ <b>: <mã1>, <mã2>, ..." hoặc "In <a> phiếu, còn chờ 0"."""
    raise NotImplementedError


if __name__ == "__main__":
    commands = ["ADD TK1", "ADD TK2", "URGENT TK9", "ADD TK1", "URGENT TK8", "PRINT", "PRINT", "ADD TK8", "PRINT", "PRINT"]
    print(print_order_slow(commands))
    print(print_order_fast(commands))
    print(print_summary(commands))
    print(print_summary(["PRINT", "ADD TK5", "PRINT"]))
