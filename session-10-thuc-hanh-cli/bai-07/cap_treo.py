"""Nghiệp vụ hàng chờ lên cáp treo Vinpearl có sức chứa giới hạn.

Khu chờ chứa tối đa capacity khách; khách đến trước lên cabin trước, mỗi cabin chở CABIN khách.
Hai cách cài cùng giao diện: QueueV1, QueueV2. Không dùng collections.deque.
"""
import timeit

CABIN = 6
FULL_MESSAGE = "Hàng chờ đã đầy"


class QueueV1:
    """Giải pháp 1. Hàng đợi có sức chứa capacity. enqueue khi đầy báo ValueError(FULL_MESSAGE); dequeue, peek khi rỗng
    báo IndexError("hàng đợi rỗng"); items() trả list từ đầu hàng tới cuối hàng (không làm đổi hàng đợi)."""

    def __init__(self, capacity):
        """Hàng đợi rỗng có sức chứa capacity (giữ trong thuộc tính capacity)."""
        self.capacity = capacity
        # Tự chọn các thuộc tính lưu trữ của giải pháp 1.

    def enqueue(self, value):
        """Thêm vào cuối hàng."""
        raise NotImplementedError

    def dequeue(self):
        """Lấy đầu hàng."""
        raise NotImplementedError

    def peek(self):
        """Xem đầu hàng."""
        raise NotImplementedError

    def size(self):
        """Số phần tử."""
        raise NotImplementedError

    def is_full(self):
        """True nếu đã đủ capacity."""
        raise NotImplementedError

    def items(self):
        """List từ đầu tới cuối hàng."""
        raise NotImplementedError


class QueueV2:
    """Giải pháp 2: cùng giao diện, cùng kết quả, cách làm khác, mọi thao tác trừ items() là O(1): khu chờ 100.000 chỗ,
    200.000 lượt thêm và 200.000 lượt lấy trong 1 giây. Chỉ tạo list lưu trữ một lần trong __init__; sau đó không append,
    pop, insert, del, cắt lát trên list đó."""

    def __init__(self, capacity):
        """Hàng đợi rỗng có sức chứa capacity (giữ trong thuộc tính capacity)."""
        self.capacity = capacity
        # Tự chọn các thuộc tính lưu trữ của giải pháp 2.

    def enqueue(self, value):
        """Thêm vào cuối hàng."""
        raise NotImplementedError

    def dequeue(self):
        """Lấy đầu hàng."""
        raise NotImplementedError

    def peek(self):
        """Xem đầu hàng."""
        raise NotImplementedError

    def size(self):
        """Số phần tử."""
        raise NotImplementedError

    def is_full(self):
        """True nếu đã đủ capacity."""
        raise NotImplementedError

    def items(self):
        """List từ đầu tới cuối hàng."""
        raise NotImplementedError


class Station:
    """Có sẵn. Ga cáp treo: hàng chờ queue và số vé đã cấp."""

    def __init__(self, queue):
        self.queue = queue
        self.issued = 0


def join(station, n_text):
    """n khách (1 đến 10) cùng xếp hàng, cấp vé "CT" + 4 chữ số. Sai báo ValueError("Số khách phải từ 1 đến 10");
    không đủ chỗ cho cả nhóm báo ValueError("Hàng chờ chỉ còn <r> chỗ") và không thêm ai. Trả về list vé."""
    raise NotImplementedError


def board(station):
    """Một cabin rời ga: lấy tối đa CABIN khách đầu hàng, trả về list vé. Hàng trống báo ValueError("Không có khách đang chờ")."""
    raise NotImplementedError


def switch(station, cls):
    """Chuyển ga sang hàng chờ lớp cls (cùng capacity), giữ nguyên khách và thứ tự. Trả về hàng chờ mới."""
    raise NotImplementedError


def make_station(cls=QueueV1):
    """Có sẵn. Ga mẫu: sức chứa 12, đã có 8 khách."""
    station = Station(cls(12))
    join(station, "5")
    join(station, "3")
    return station


def workload(cls, n):
    """Có sẵn. Hàng chờ n chỗ: thêm đầy, lấy hết, làm hai vòng."""
    queue = cls(n)
    for _ in range(2):
        for k in range(n):
            queue.enqueue(k)
        while queue.size() > 0:
            queue.dequeue()


def benchmark(sizes):
    """Với từng n: đo (ms) workload trên QueueV1 và QueueV2. Trả về list bộ (n, ms 1, ms 2)."""
    raise NotImplementedError
