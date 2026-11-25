"""Nghiệp vụ nhật ký bút toán có hoàn tác trên phần mềm kế toán MISA.

Bút toán là tuple (mã, diễn giải, số tiền); số tiền dương là thu, âm là chi. Kế toán thường ghi rồi hoàn tác bút toán cuối.
SlowJournal (bản cũ) dùng danh sách liên kết đơn; FastJournal (bản mới) dùng danh sách liên kết đôi. Không dùng list Python để lưu.
"""
import timeit

EMPTY_MESSAGE = "danh sách rỗng, không có phần tử để xóa"


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class DNode:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


class SlowJournal:
    """Có sẵn. Bản cũ đang chạy, KHÔNG sửa. Danh sách liên kết đơn chỉ có head."""

    def __init__(self):
        self.head = None
        self.issued = 0

    def add_last(self, entry):
        """Có sẵn. Thêm bút toán vào cuối."""
        node = Node(entry)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = node

    def remove_last(self):
        """Có sẵn. Xóa và trả về bút toán cuối; rỗng báo IndexError(EMPTY_MESSAGE)."""
        if self.head is None:
            raise IndexError(EMPTY_MESSAGE)
        if self.head.next is None:
            entry = self.head.value
            self.head = None
            return entry
        current = self.head
        while current.next.next is not None:
            current = current.next
        entry = current.next.value
        current.next = None
        return entry

    def size(self):
        """Có sẵn. Số bút toán."""
        total, current = 0, self.head
        while current is not None:
            total, current = total + 1, current.next
        return total

    def balance(self):
        """Có sẵn. Tổng số tiền các bút toán."""
        total, current = 0, self.head
        while current is not None:
            total, current = total + current.value[2], current.next
        return total

    def recent(self, k):
        """Có sẵn. List tối đa k bút toán gần nhất, mới nhất trước."""
        entries, current = [], self.head
        while current is not None:
            entries.append(current.value)
            current = current.next
        return entries[::-1][:k]


class FastJournal:
    """Bản mới: cùng phương thức, cùng kết quả, cùng lỗi với SlowJournal (kể cả issued). add_last, remove_last, size, balance
    không duyệt danh sách; recent(k) chỉ đi qua tối đa k node. Dùng DNode; không dùng list Python để lưu."""

    def __init__(self):
        self.issued = 0
        # Tự chọn các thuộc tính còn lại (dùng DNode).

    def add_last(self, entry):
        """Thêm bút toán vào cuối."""
        raise NotImplementedError

    def remove_last(self):
        """Xóa và trả về bút toán cuối; rỗng báo IndexError(EMPTY_MESSAGE)."""
        raise NotImplementedError

    def size(self):
        """Số bút toán."""
        raise NotImplementedError

    def balance(self):
        """Tổng số tiền các bút toán."""
        raise NotImplementedError

    def recent(self, k):
        """List tối đa k bút toán gần nhất, mới nhất trước."""
        raise NotImplementedError


def money(value):
    """Có sẵn. 15000000 -> "+15.000.000đ", -850000 -> "-850.000đ"."""
    return ("+" if value >= 0 else "-") + f"{abs(value):,}".replace(",", ".") + "đ"


def record(journal, description, amount_text):
    """Ghi bút toán: diễn giải 1 đến 50 ký tự (bỏ khoảng trắng hai đầu), số tiền nguyên khác 0 (có thể có dấu -).
    Lỗi: "Diễn giải phải có từ 1 đến 50 ký tự", "Số tiền phải là số nguyên khác 0". Mã "BT" + 4 chữ số theo issued."""
    raise NotImplementedError


def undo(journal):
    """Hoàn tác bút toán cuối, trả về bút toán; không còn báo ValueError("Không còn bút toán để hoàn tác")."""
    raise NotImplementedError


def make_journal(cls):
    """Có sẵn. Nhật ký mẫu 4 bút toán trên lớp cls (SlowJournal hoặc FastJournal)."""
    journal = cls()
    for description, amount in [("Thu tiền khách hàng A", "15000000"), ("Chi mua văn phòng phẩm", "-850000"),
                                ("Chi lương tháng 11", "-9000000"), ("Thu tiền khách hàng B", "7200000")]:
        record(journal, description, amount)
    return journal


def workload(cls, n):
    """Có sẵn. Ghi n bút toán, rồi hoàn tác n // 2 lần; sau mỗi thao tác đọc số dư. Trả về số dư cuối."""
    journal = cls()
    for k in range(n):
        journal.add_last(("BT", "x", k + 1))
        journal.balance()
    for _ in range(n // 2):
        journal.remove_last()
        journal.balance()
    return journal.balance()


def benchmark(sizes, number=1):
    """Với từng n: đo (ms) workload trên SlowJournal và FastJournal. Trả về list bộ (n, ms bản cũ, ms bản mới)."""
    raise NotImplementedError
