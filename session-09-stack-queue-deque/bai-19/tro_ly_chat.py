"""Bộ nhớ hội thoại của trợ lý mua sắm Tiki: giữ k tin gần nhất, có hoàn tác và làm lại."""


UNDO_LIMIT = 50
ROLES = ("user", "bot")


class ChatMemory:
    """Giữ tối đa max_turns tin nhắn gần nhất để gửi kèm câu hỏi cho trợ lý. undo hủy lần thêm gần nhất (kể cả đưa lại tin cũ đã bị đẩy ra); redo làm lại. Chỉ nhớ UNDO_LIMIT lần thêm gần nhất để hoàn tác."""

    def __init__(self, max_turns):
        if type(max_turns) is not int or max_turns <= 0:
            raise ValueError("Số tin nhớ phải là số nguyên dương")

    def add(self, role, text):
        """Thêm tin (role, text). role phải thuộc ROLES, sai báo ValueError("Vai trò không hợp lệ"); text sau khi bỏ khoảng trắng hai đầu không được rỗng, sai báo ValueError("Tin nhắn rỗng"). Lưu text đã bỏ khoảng trắng."""
        raise NotImplementedError

    def undo(self):
        """Hủy lần thêm gần nhất; tin bị đẩy ra vì lần thêm đó trở lại đầu. Không còn gì để hủy trả False, ngược lại True."""
        raise NotImplementedError

    def redo(self):
        """Làm lại lần vừa hủy; không còn gì để làm lại trả False. Thêm tin mới thì mất khả năng làm lại."""
        raise NotImplementedError

    def context(self):
        """List các dòng "<role>: <text>" của tin đang nhớ, cũ nhất trước."""
        raise NotImplementedError


def run_commands(max_turns, commands):
    """commands: list chuỗi "user <text>", "bot <text>", "UNDO", "REDO". Trả về list ngữ cảnh cuối cùng; lệnh lỗi được bỏ qua."""
    raise NotImplementedError


if __name__ == "__main__":
    memory = ChatMemory(3)
    memory.add("user", "Tìm tai nghe dưới 500 nghìn")
    memory.add("bot", "Có 12 mẫu, bạn thích chống ồn không?")
    memory.add("user", "  Có, màu đen  ")
    memory.add("bot", "Gợi ý: SoundX Pro 459.000đ")
    print(memory.context())
    print("Hoàn tác:", memory.undo(), memory.context())
    print("Làm lại:", memory.redo(), memory.context())
    memory.undo()
    memory.add("user", "Thôi, xem loa")
    print("Làm lại sau khi thêm tin mới:", memory.redo())
    print(run_commands(2, ["user Xin chào", "bot Chào bạn", "UNDO", "UNDO", "UNDO", "user    ", "REDO"]))
