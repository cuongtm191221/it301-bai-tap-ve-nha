"""Nghiệp vụ soạn tin nhắn có hoàn tác, làm lại trên ứng dụng Zalo.

Tin nhắn nháp là list các từ. Mỗi thao tác ("gõ", từ) hoặc ("xóa", từ) được đẩy vào ngăn xếp hoàn tác;
hoàn tác chuyển thao tác sang ngăn xếp làm lại. Ngăn xếp cài bằng list (ArrayStack), thêm, lấy ở cuối list.
"""


class ArrayStack:
    """Ngăn xếp cài bằng list _items: đỉnh là phần tử cuối list."""

    def __init__(self):
        self._items = []

    def push(self, value):
        """Đặt value lên đỉnh."""
        raise NotImplementedError

    def pop(self):
        """Lấy và trả về phần tử ở đỉnh; rỗng báo IndexError("ngăn xếp rỗng")."""
        raise NotImplementedError

    def peek(self):
        """Trả về phần tử ở đỉnh, không lấy ra; rỗng báo IndexError("ngăn xếp rỗng")."""
        raise NotImplementedError

    def is_empty(self):
        """True nếu ngăn xếp không có phần tử."""
        raise NotImplementedError

    def size(self):
        """Số phần tử."""
        raise NotImplementedError


class Draft:
    """Có sẵn. Tin nhắn nháp: words, ngăn xếp hoàn tác undo_stack, ngăn xếp làm lại redo_stack."""

    def __init__(self):
        self.words = []
        self.undo_stack = ArrayStack()
        self.redo_stack = ArrayStack()

    def text(self):
        """Có sẵn. Nội dung tin nhắn, "(trống)" nếu chưa có từ nào."""
        return " ".join(self.words) if self.words else "(trống)"


def type_word(draft, text):
    """Gõ thêm một từ vào cuối: bỏ khoảng trắng hai đầu, 1 đến 20 ký tự, không chứa khoảng trắng; sai báo
    ValueError("Mỗi lần gõ một từ, 1 đến 20 ký tự"). Ghi ("gõ", từ) vào ngăn xếp hoàn tác, xóa sạch ngăn xếp làm lại. Trả về từ."""
    raise NotImplementedError


def delete_word(draft):
    """Xóa từ cuối; tin nhắn trống báo ValueError("Tin nhắn đang trống"). Ghi ("xóa", từ), xóa sạch ngăn xếp làm lại. Trả về từ."""
    raise NotImplementedError


def undo(draft):
    """Hoàn tác thao tác gần nhất (gõ thì bỏ từ cuối, xóa thì thêm lại từ), chuyển thao tác sang ngăn xếp làm lại.
    Không còn báo ValueError("Không có thao tác để hoàn tác"). Trả về thao tác."""
    raise NotImplementedError


def redo(draft):
    """Làm lại thao tác vừa hoàn tác, chuyển nó về ngăn xếp hoàn tác. Không còn báo ValueError("Không có thao tác để làm lại").
    Trả về thao tác."""
    raise NotImplementedError
