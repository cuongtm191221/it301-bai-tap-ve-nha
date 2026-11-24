"""Nghiệp vụ quầy thuốc Long Châu: danh sách thuốc trên quầy lưu bằng mảng động tự cài.

Mỗi phần tử là một list [mã thuốc, tên thuốc, số hộp]. Lớp DrugArray dùng _data = [None] * capacity như vùng lưu trữ
có số ô cố định: chỉ đọc, gán theo chỉ số; đầy thì tạo vùng gấp đôi và chép sang (đếm vào copies).
"""


class DrugArray:
    """Mảng động chứa thuốc trên quầy: capacity ban đầu 1, gấp đôi khi đầy, không thu gọn."""

    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._data = [None] * self._capacity
        self.copies = 0                          # số phần tử đã chép khi đổi vùng lưu trữ
        self.checks = 0                          # số lần so sánh mã khi tìm

    def size(self):
        """Có sẵn. Số thuốc đang lưu."""
        return self._size

    def capacity(self):
        """Có sẵn. Số ô của vùng lưu trữ hiện tại."""
        return self._capacity

    def get(self, i):
        """Có sẵn. Phần tử tại chỉ số i (0 đến size() - 1); sai báo IndexError("Chỉ số ngoài phạm vi phần tử")."""
        if type(i) is not int or not 0 <= i < self._size:
            raise IndexError("Chỉ số ngoài phạm vi phần tử")
        return self._data[i]

    def append(self, item):
        """Thêm item vào cuối; đầy thì gấp đôi số ô (dùng hàm phụ đổi vùng lưu trữ, đếm copies). Không dùng list.append trên _data."""
        raise NotImplementedError

    def find(self, code):
        """Chỉ số đầu tiên của thuốc có mã code (không phân biệt hoa thường) hoặc None; mỗi lần so sánh mã tăng checks 1."""
        raise NotImplementedError

    def items(self):
        """List các thuốc theo thứ tự (chỉ lấy size phần tử đầu, không lấy ô trống)."""
        raise NotImplementedError


SAMPLE = [["LC101", "Panadol Extra", 24], ["LC102", "Berberin", 15], ["LC103", "Vitamin C 500mg", 40]]


def make_shelf():
    """Có sẵn. DrugArray chứa 3 thuốc mẫu (đã đặt lại copies, checks về 0)."""
    shelf = DrugArray()
    for row in SAMPLE:
        shelf.append(row[:])
    shelf.copies = shelf.checks = 0
    return shelf


def receive(shelf, code, name, qty_text):
    """Nhập thuốc: mã đã có thì cộng số hộp (bỏ qua tên), mã mới thì thêm vào cuối. Trả về ("cộng", thuốc) hoặc ("thêm", thuốc).
    Lỗi (quầy giữ nguyên): "Mã thuốc phải có dạng LC và 3 chữ số", "Số hộp phải là số nguyên dương", "Tên thuốc không được để trống"."""
    raise NotImplementedError


def sell(shelf, code, qty_text):
    """Bán thuốc, trả về thuốc sau khi bán. Lỗi (quầy giữ nguyên): "Không có thuốc <MÃ>",
    "Số hộp phải là số nguyên dương", "Không đủ hàng: còn <n> hộp"."""
    raise NotImplementedError
