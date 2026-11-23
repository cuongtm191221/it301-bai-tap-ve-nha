"""Trình soạn mô tả sản phẩm có hoàn tác và làm lại cho người bán Tiki."""
class DescriptionEditor:
    # Trình soạn mô tả sản phẩm cho người bán trên Tiki: viết từng cụm từ, hoàn tác, làm lại.
    # undo() và redo() khi không có gì để làm thì giữ nguyên, không báo lỗi.
    def __init__(self):
        self.parts = []
        self.undo_stack = []
        self.redo_stack = []

    def write(self, part):
        self.parts.append(part)
        self.undo_stack.append(part)

    def undo(self):
        part = self.undo_stack.pop()
        self.parts.pop()
        self.redo_stack.append(part)

    def redo(self):
        if self.redo_stack:
            part = self.redo_stack.pop()
            self.parts.append(part)

    def text(self):
        return " ".join(self.parts)


if __name__ == "__main__":
    ed = DescriptionEditor()
    for part in ("Tai nghe", "không dây", "chống ồn"):
        ed.write(part)
    ed.undo()
    print("Hoàn tác:", ed.text())
    ed.redo()
    ed.undo()
    print("Làm lại rồi hoàn tác:", ed.text())
    ed.write("pin 30 giờ")
    ed.redo()
    print("Viết mới rồi làm lại:", ed.text())
    for _ in range(5):
        ed.undo()
    print("Hoàn tác 5 lần:", repr(ed.text()))
