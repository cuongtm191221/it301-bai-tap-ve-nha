"""Hàm so đáp án dạng mã băm cho các test (đọc tệp này không lộ đáp án). Không sửa tệp này."""
import hashlib
import unicodedata


def norm(text):
    text = unicodedata.normalize("NFD", str(text))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn").replace("đ", "d").replace("Đ", "D")
    return text.lower().replace(" ", "").replace("²", "^2").replace("**", "^")


def h(text):
    return hashlib.sha256(norm(text).encode()).hexdigest()[:16]


O1, ON = "79a6652f8ffde77c", "3963250267e2da89"
DUNG, SAI = "05b3b66d444b8ed7", "83eb5874f315bf4b"
X1, X2 = "ec31682fde561917", "844ecc08164e2eab"
LIST, DON, DOI = "a330395cc0a53ad1", "4a2326c64ab2287e", "cc19ad25eef37f44"


def wrong_keys(table, key):
    """Trả danh sách khóa chưa đúng; báo NotImplementedError nếu bảng còn nguyên dấu '?'."""
    if all(str(v).strip() == "?" for v in table.values()):
        raise NotImplementedError("chưa ghi đáp án")
    return [k for k, ok in key.items() if h(table.get(k, "?")) != ok]
