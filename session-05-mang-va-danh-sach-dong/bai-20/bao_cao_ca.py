"""Báo cáo cuối ca của tài xế GrabBike: bản cũ chạy rất chậm cần tối ưu."""


def summary_slow(trips, top):
    """Có sẵn. Bản cũ đang chạy. trips: list các bộ (mã cuốc, trạng thái, tiền); trả về (tổng tiền các cuốc DONE, số cuốc hủy, list mã top cuốc DONE mới nhất trước)."""
    done = []
    for trip in trips:
        done = done + [trip]                    # giữ toàn bộ rồi lọc sau
    cancelled = 0
    for trip in list(done):
        if trip[1] == "CANCELLED":
            done.remove(trip)
            cancelled += 1
    total = 0
    queue = list(done)
    while queue:
        total += queue.pop(0)[2]
    latest = []
    for trip in done:
        latest.insert(0, trip[0])
    return total, cancelled, latest[:top]


def summary_fast(trips, top):
    """Cùng kết quả với summary_slow với mọi dữ liệu, chạy 200.000 cuốc trong 1 giây; không sửa trips."""
    raise NotImplementedError


def shift_report(trips, top):
    """Dòng báo cáo cuối ca, dùng summary_fast."""
    raise NotImplementedError


if __name__ == "__main__":
    shift = [("BK1", "DONE", 25000), ("BK2", "CANCELLED", 0), ("BK3", "DONE", 32000),
             ("BK4", "DONE", 18000), ("BK5", "CANCELLED", 0)]
    print(summary_slow(shift, 2))
    print(summary_fast(shift, 2))
    print(shift_report(shift, 2))
    print(shift_report([], 3))
    month = [(f"BK{k}", "CANCELLED" if k % 7 == 0 else "DONE", 20000 + k % 5 * 1000) for k in range(200000)]
    print(shift_report(month, 3))
