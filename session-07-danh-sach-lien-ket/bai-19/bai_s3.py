"""S3 - Lịch sử phiên bản bản nháp có lùi và tiến."""
from lien_ket import DNode


class DraftHistory:
    """Lưu các phiên bản bản nháp theo thời gian bằng các DNode nối hai chiều.

    save(text): thêm phiên bản mới ngay sau phiên bản đang xem; các phiên bản đứng sau phiên bản
        đang xem (nếu đã lùi) bị bỏ. Phiên bản mới trở thành phiên bản đang xem.
    back(): lùi về phiên bản trước và trả text của nó; đang ở phiên bản đầu (hoặc rỗng) thì trả None, giữ nguyên.
    forward(): tiến tới phiên bản sau và trả text; không có thì trả None, giữ nguyên.
    current(): text của phiên bản đang xem, None nếu chưa lưu gì.
    """

    def __init__(self):
        raise NotImplementedError

    def save(self, text):
        raise NotImplementedError

    def back(self):
        raise NotImplementedError

    def forward(self):
        raise NotImplementedError

    def current(self):
        raise NotImplementedError


GIAI_THICH = ""


def tu_kiem_tra():
    raise NotImplementedError
