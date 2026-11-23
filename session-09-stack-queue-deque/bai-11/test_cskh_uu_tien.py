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


from cskh_uu_tien import PriorityDesk, serve_all


def make(normal, vip):
    d = PriorityDesk()
    for c in normal:
        d.add(c)
    for c in vip:
        d.add(c, is_vip=True)
    return d


def test_vip_truoc():
    assert serve_all(make(["T1"], ["V1"])) == ["V1", "T1"]


def test_sau_3_vip_den_1_khach_thuong():
    d = make(["T1", "T2"], ["V1", "V2", "V3", "V4", "V5"])
    assert serve_all(d) == ["V1", "V2", "V3", "T1", "V4", "V5", "T2"]


def test_chi_co_vip_hoac_chi_co_thuong():
    assert serve_all(make([], ["V1", "V2", "V3", "V4"])) == ["V1", "V2", "V3", "V4"]
    assert serve_all(make(["T1", "T2"], [])) == ["T1", "T2"]


def test_dem_lai_sau_khach_thuong():
    d = make(["T1"], ["V1", "V2", "V3"])
    assert [d.serve() for _ in range(3)] == ["V1", "V2", "V3"]
    d.add("V4", is_vip=True)
    d.add("V5", is_vip=True)
    d.add("V6", is_vip=True)
    d.add("V7", is_vip=True)
    d.add("T2")
    assert serve_all(d) == ["T1", "V4", "V5", "V6", "T2", "V7"]


def test_trung_ma():
    d = make(["T1"], ["V1"])
    assert d.add("T1") is False and d.add("T1", is_vip=True) is False and d.add("V1") is False
    assert d.waiting() == (1, 1)


def test_rong():
    d = PriorityDesk()
    assert d.serve() is None and d.waiting() == (0, 0) and serve_all(d) == []


def test_them_sau_khi_rong():
    d = make([], ["V1"])
    serve_all(d)
    d.add("T9")
    assert d.serve() == "T9"


def test_nhieu_khach():
    d = make([f"T{k}" for k in range(2000)], [f"V{k}" for k in range(6000)])
    order = run_limited(lambda: serve_all(d), 1, "phục vụ 8.000 khách quá 1 giây")
    assert len(order) == 8000 and order[:5] == ["V0", "V1", "V2", "T0", "V3"] and order[-1] == "T1999"
