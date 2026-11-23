"""Hàng yêu cầu hỗ trợ của tổng đài Tiki, dùng collections.deque."""
from collections import deque


class SupportDesk:
    # Hàng yêu cầu hỗ trợ của tổng đài Tiki: yêu cầu thường xếp cuối hàng, yêu cầu gấp (đơn giao trễ)
    # được đưa lên đầu hàng; luôn phục vụ người đứng đầu. Hàng rỗng: serve() trả None.
    # recent_list(): mã 3 yêu cầu được phục vụ gần nhất, mới nhất trước.
    def __init__(self):
        self.waiting = deque()
        self.recent = deque(maxlen=3)

    def add(self, code):
        self.waiting.append(code)

    def add_urgent(self, code):
        self.waiting.append(code)

    def serve(self):
        code = self.waiting.pop()
        self.recent.appendleft(code)
        return code

    def recent_list(self):
        return list(self.recent)


if __name__ == "__main__":
    desk = SupportDesk()
    for code in ("YC01", "YC02", "YC03"):
        desk.add(code)
    desk.add_urgent("GAP1")
    print("Phục vụ:", [desk.serve() for _ in range(3)])
    desk.add("YC04")
    print("Phục vụ:", desk.serve(), desk.serve(), desk.serve())
    print("3 yêu cầu gần nhất:", desk.recent_list())
