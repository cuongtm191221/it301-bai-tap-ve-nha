"""Ba hàm do AI sinh cho hàng chờ chấm bài. Mỗi hàm có một dòng nhận xét của AI.

Kết quả của cả ba hàm đều đúng với dữ liệu thường. Không sửa tệp này; viết bản sửa trong bai_p1.py.
"""


def count_waiting(queue):
    # AI: "Thời gian O(n), không làm thay đổi danh sách."
    total = 0
    while queue.head is not None:
        total += 1
        queue.head = queue.head.next
    return total


def newest_submission(queue):
    # AI: "Thời gian O(1), vì danh sách có tail."
    if queue.head is None:
        return None
    current = queue.head
    while current.next is not None:
        current = current.next
    return current.value


def has_code(queue, code):
    # AI: "Thời gian O(n), dừng ngay khi gặp mã."
    current = queue.head
    while current is not None:
        if current.value == code:
            return True
        current = current.next
    return False
