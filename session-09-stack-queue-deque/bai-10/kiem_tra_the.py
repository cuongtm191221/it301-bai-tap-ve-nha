"""Kiểm tra thẻ định dạng trong mô tả sản phẩm người bán đăng lên Tiki."""


def find_tags(text):
    """Có sẵn. List các bộ (vị trí, thẻ) theo thứ tự xuất hiện; thẻ là chuỗi dạng <ten>, </ten> hoặc <ten/> với ten chỉ gồm chữ cái."""
    tags = []
    i = 0
    while i < len(text):
        if text[i] == "<":
            end = text.find(">", i)
            if end != -1:
                inner = text[i + 1:end]
                core = inner[1:] if inner.startswith("/") else inner
                core = core[:-1] if core.endswith("/") and not inner.startswith("/") else core
                if core.isalpha():
                    tags.append((i, text[i:end + 1]))
                    i = end + 1
                    continue
        i += 1
    return tags


def check_tags(text):
    """None nếu mọi thẻ mở, đóng đúng cặp và đúng thứ tự lồng; ngược lại là dòng mô tả lỗi đầu tiên."""
    raise NotImplementedError


def review_message(text):
    """Dòng kết quả duyệt mô tả."""
    raise NotImplementedError


if __name__ == "__main__":
    samples = [
        "<b>Tai nghe</b> <i>chống ồn</i><br/>Pin <b>30 giờ</b>",
        "<b>Giảm <i>50%</b></i>",
        "Giá < 100k, </u>bảo hành 12 tháng",
        "<B>Hàng chính hãng</b>",
        "<ul><li>Màu đen<li>Màu trắng</ul>",
        "Không có thẻ nào",
    ]
    for text in samples:
        print(review_message(text))
