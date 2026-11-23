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


from bang_chuyen import PackingLine


def make(*codes):
    line = PackingLine()
    for c in codes:
        line.enqueue(c)
    return line


def test_fifo_va_peek():
    line = make("A", "B", "C")
    assert line.peek() == "A" and line.dequeue() == "A" and line.peek() == "B"


def test_lo_thieu_don():
    line = make("A", "B")
    assert line.take_batch(3) == ["A", "B"] and line.take_batch(2) == [] and line.peek() is None


def test_lo_dung_thu_tu():
    line = make("A", "B", "C", "D")
    assert line.take_batch(2) == ["A", "B"] and line.size() == 2


def test_200000_don():
    def work():
        line = PackingLine()
        for k in range(200000):
            line.enqueue(k)
        return line.peek(), line.take_batch(2), line.size()
    assert run_limited(work, 1, "thêm 200.000 đơn quá 1 giây") == (0, [0, 1], 199998)
