import threading as _threading

_threading.stack_size(64 * 1024 * 1024)


def run_limited(task, seconds, message):
    """Chạy task tối đa seconds giây; quá giờ thì test thất bại với lời nhắn message."""
    box, errors = [], []

    def target():
        try:
            box.append(task())
        except BaseException as error:
            errors.append(error)

    worker = _threading.Thread(target=target, daemon=True)
    worker.start()
    worker.join(seconds)
    if errors:
        raise errors[0]
    assert box, message
    return box[0]


import pytest
from tro_ly_chat import ChatMemory, run_commands, UNDO_LIMIT


def make(n, k):
    m = ChatMemory(n)
    for i in range(k):
        m.add("user" if i % 2 == 0 else "bot", f"tin {i}")
    return m


def test_chi_giu_k_tin():
    m = make(3, 5)
    assert m.context() == ["user: tin 2", "bot: tin 3", "user: tin 4"]
    m.add("bot", "   Gợi ý SoundX   ")
    assert m.context()[-1] == "bot: Gợi ý SoundX"


def test_hoan_tac_dua_lai_tin_bi_day_ra():
    m = make(3, 5)
    assert m.undo() is True
    assert m.context() == ["bot: tin 1", "user: tin 2", "bot: tin 3"]
    assert m.undo() is True
    assert m.context() == ["user: tin 0", "bot: tin 1", "user: tin 2"]


def test_lam_lai():
    m = make(3, 4)
    m.undo()
    m.undo()
    assert m.redo() and m.redo() and not m.redo()
    assert m.context() == ["bot: tin 1", "user: tin 2", "bot: tin 3"]
    m.undo()
    m.add("user", "Thôi, xem loa")
    assert m.redo() is False


def test_rong_va_du_lieu_sai():
    m = ChatMemory(2)
    assert m.undo() is False and m.redo() is False and m.context() == []
    for bad in [0, -1, 2.0, "3", True]:
        with pytest.raises(ValueError, match="Số tin nhớ phải là số nguyên dương"):
            ChatMemory(bad)
    with pytest.raises(ValueError, match="Vai trò không hợp lệ"):
        m.add("admin", "xin chào")
    for bad in ["", "   ", "\n\t"]:
        with pytest.raises(ValueError, match="Tin nhắn rỗng"):
            m.add("user", bad)
    assert m.undo() is False


def test_chay_lenh():
    got = run_commands(2, ["user Xin chào", "bot Chào bạn", "UNDO", "UNDO", "UNDO", "user    ", "REDO"])
    assert got == ["user: Xin chào"]


def test_gioi_han_hoan_tac():
    m = make(5, UNDO_LIMIT + 30)
    count = 0
    while m.undo():
        count += 1
    assert count == UNDO_LIMIT
    assert len(m.context()) == 5


def test_hoan_tac_nhieu_lan_dung_thu_tu():
    m = make(4, 20)
    for _ in range(10):
        m.undo()
    assert m.context() == ["user: tin 6", "bot: tin 7", "user: tin 8", "bot: tin 9"]


def test_200000_tin():
    def job():
        m = ChatMemory(1000)
        for i in range(200000):
            m.add("user", f"tin {i}")
            if i % 10 == 9:
                m.undo()
                m.redo()
        return m.context()
    got = run_limited(job, 2, "200.000 tin quá 2 giây")
    assert len(got) == 1000 and got[-1] == "user: tin 199999"
