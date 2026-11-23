"""Nhật ký chuyến đi GrabBike và mô phỏng mảng động."""
import sys


def simulate_append(n, capacity=1):
    # Mô phỏng n lần append vào mảng động: đầy thì cấp vùng gấp đôi và chép mọi tham chiếu đang có sang.
    # Trả về (capacity cuối, tổng số tham chiếu đã chép).
    size = 0
    copies = 0
    for _ in range(n):
        if size == capacity:
            copies += 1
            capacity *= 2
        size += 1
    return capacity, copies


def build_log(events):
    # Nhật ký chuyến đi: list mới chứa các sự kiện theo đúng thứ tự.
    log = []
    for event in events:
        log = log + [event]
    return log


def log_bytes(log):
    # Tổng số byte của nhật ký: phần list và mọi bản ghi trong đó.
    return sys.getsizeof(log)


if __name__ == "__main__":
    for n in (1, 5, 10, 1000):
        print(f"{n} lần append:", "(capacity, số tham chiếu đã chép) =", simulate_append(n))
    log = build_log([f"GB{2000 + k}" for k in range(5)])
    print("Nhật ký 5 chuyến:", log)
    record = "GB2001 | Nguyễn Văn An | Quận 1 -> Quận 7 | " + "ghi chú " * 50
    print("Byte của nhật ký 1 bản ghi dài lớn hơn 400:", log_bytes([record]) > 400)
    print("Nhật ký 100.000 chuyến:", len(build_log([f"GB{k}" for k in range(100000)])), "dòng")
