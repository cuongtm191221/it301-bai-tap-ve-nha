"""Nghiệp vụ soạn văn bản có hoàn tác, làm lại trên VNPT Smart Office.

Văn bản là list các dòng. Thao tác: thêm dòng vào cuối, sửa dòng i, xóa dòng i (i đếm từ 1); hoàn tác, làm lại.
SlowEditor (bản cũ) lưu bản chụp toàn bộ văn bản sau mỗi thao tác; FastEditor (bản mới) phải cùng kết quả, cùng lỗi.
"""
import timeit


def check_text(text):
    """Có sẵn. Bỏ khoảng trắng hai đầu; 1 đến 80 ký tự, sai báo ValueError("Nội dung dòng phải có từ 1 đến 80 ký tự")."""
    text = text.strip()
    if not 1 <= len(text) <= 80:
        raise ValueError("Nội dung dòng phải có từ 1 đến 80 ký tự")
    return text


def check_index(index_text, n):
    """Có sẵn. Số dòng 1..n. Văn bản rỗng báo ValueError("Văn bản chưa có dòng nào"); sai báo ValueError("Dòng phải từ 1 đến <n>")."""
    if n == 0:
        raise ValueError("Văn bản chưa có dòng nào")
    index_text = index_text.strip()
    if not index_text.isdigit() or not 1 <= int(index_text) <= n:
        raise ValueError(f"Dòng phải từ 1 đến {n}")
    return int(index_text)


class SlowEditor:
    """Có sẵn. Bản cũ đang chạy, KHÔNG sửa. Mọi phương thức thao tác trả về mô tả như "thêm dòng 3", "sửa dòng 2", "xóa dòng 1"."""

    def __init__(self):
        self._snapshots = [([], "")]             # (bản chụp, mô tả thao tác tạo ra nó)
        self._at = 0

    def lines(self):
        """Có sẵn. Bản sao các dòng hiện tại."""
        return self._snapshots[self._at][0][:]

    def add_line(self, text):
        """Có sẵn."""
        lines = self.lines()
        lines.append(check_text(text))
        return self._commit(lines, f"thêm dòng {len(lines)}")

    def edit_line(self, index_text, text):
        """Có sẵn. Kiểm tra số dòng trước, nội dung sau."""
        lines = self.lines()
        i = check_index(index_text, len(lines))
        lines[i - 1] = check_text(text)
        return self._commit(lines, f"sửa dòng {i}")

    def delete_line(self, index_text):
        """Có sẵn."""
        lines = self.lines()
        i = check_index(index_text, len(lines))
        del lines[i - 1]
        return self._commit(lines, f"xóa dòng {i}")

    def undo(self):
        """Có sẵn. Không còn báo ValueError("Không có thao tác để hoàn tác")."""
        if self._at == 0:
            raise ValueError("Không có thao tác để hoàn tác")
        self._at -= 1
        return self._snapshots[self._at + 1][1]

    def redo(self):
        """Có sẵn. Không còn báo ValueError("Không có thao tác để làm lại")."""
        if self._at == len(self._snapshots) - 1:
            raise ValueError("Không có thao tác để làm lại")
        self._at += 1
        return self._snapshots[self._at][1]


class FastEditor:
    """Bản mới: cùng phương thức, cùng kết quả, cùng mô tả, cùng lỗi với SlowEditor. Không chép cả văn bản trong add_line, edit_line,
    delete_line, undo, redo; workload(FastEditor, 50000) trong 1 giây."""

    def __init__(self):
        """Văn bản rỗng, chưa có thao tác."""
        # Tự chọn các thuộc tính lưu văn bản và lịch sử thao tác.

    def lines(self):
        """Bản sao các dòng hiện tại."""
        raise NotImplementedError

    def add_line(self, text):
        """Thêm dòng vào cuối."""
        raise NotImplementedError

    def edit_line(self, index_text, text):
        """Sửa dòng; kiểm tra số dòng trước, nội dung sau."""
        raise NotImplementedError

    def delete_line(self, index_text):
        """Xóa dòng."""
        raise NotImplementedError

    def undo(self):
        """Hoàn tác thao tác gần nhất."""
        raise NotImplementedError

    def redo(self):
        """Làm lại thao tác vừa hoàn tác."""
        raise NotImplementedError


def make_editor(cls):
    """Có sẵn. Văn bản mẫu 3 dòng trên lớp cls."""
    editor = cls()
    for text in ["CÔNG VĂN SỐ 125/VNPT", "Kính gửi: Phòng Kế hoạch", "V/v: Lịch bảo trì hệ thống tháng 12"]:
        editor.add_line(text)
    return editor


def workload(cls, n):
    """Có sẵn. Thêm n dòng, sửa n dòng, hoàn tác n lần, làm lại n // 2 lần."""
    editor = cls()
    for k in range(n):
        editor.add_line("Dòng %d" % k)
    for k in range(n):
        editor.edit_line(str(k + 1), "Sửa %d" % k)
    for _ in range(n):
        editor.undo()
    for _ in range(n // 2):
        editor.redo()
    return editor.lines()


def benchmark(sizes):
    """Với từng n: đo (ms) workload trên SlowEditor và FastEditor. Trả về list bộ (n, ms bản cũ, ms bản mới)."""
    raise NotImplementedError
