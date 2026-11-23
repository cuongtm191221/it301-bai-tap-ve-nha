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


import inspect
import pytest
from hang_cho_vong import KitchenQueue


def test_vao_truoc_ra_truoc():
    q = KitchenQueue(5)
    for c in ("A", "B", "C"):
        assert q.enqueue(c) is True
    assert [q.dequeue(), q.dequeue()] == ["A", "B"] and q.size() == 1 and q.peek() == "C"


def test_day_va_rong():
    q = KitchenQueue(2)
    assert q.enqueue("A") and q.enqueue("B") and q.enqueue("C") is False
    assert q.is_full() and q.to_list() == ["A", "B"]
    assert q.dequeue() == "A" and q.dequeue() == "B" and q.dequeue() is None and q.peek() is None


def test_vong_quanh():
    q = KitchenQueue(3)
    for c in ("A", "B", "C"):
        q.enqueue(c)
    q.dequeue()
    q.dequeue()
    q.enqueue("D")
    q.enqueue("E")
    assert q.to_list() == ["C", "D", "E"] and q.is_full()
    assert [q.dequeue() for _ in range(3)] == ["C", "D", "E"]


def test_mot_cho():
    q = KitchenQueue(1)
    for k in range(5):
        assert q.enqueue(k) and q.enqueue(99) is False and q.dequeue() == k


def test_suc_chua_sai():
    for bad in (0, -3, 2.5, "3"):
        with pytest.raises(ValueError, match="Sức chứa phải là số nguyên dương"):
            KitchenQueue(bad)


def test_khong_giu_tham_chieu_thua():
    q = KitchenQueue(3)
    q.enqueue("A")
    q.dequeue()
    assert all(x is None for x in q._data)


def test_vung_luu_tru_co_dinh():
    src = inspect.getsource(KitchenQueue)
    for word in (".pop(", ".insert(", ".append(", "del ", ".remove("):
        assert word not in src, f"không dùng {word.strip()} trên vùng lưu trữ"


def test_200000_thao_tac():
    def work():
        q = KitchenQueue(50)
        for k in range(200000):
            q.enqueue(k)
            if q.size() > 40:
                q.dequeue()
        return q.to_list()
    got = run_limited(work, 1, "200.000 thao tác quá 1 giây")
    assert got == list(range(199960, 200000))
