"""Kiểm tra tồn kho trước giờ mở flash sale trên Shopee."""


def first_out_of_stock(products):
    # Trả về (mã sản phẩm hết hàng đầu tiên theo thứ tự trên trang, số sản phẩm đã xét).
    # Hết hàng: tồn kho từ 0 trở xuống (số âm là đã bán vượt tồn kho).
    # Gặp sản phẩm hết hàng đầu tiên thì dừng ngay. Không có thì trả về (None, số sản phẩm đã xét).
    result = products[0]["code"]
    checked = 0
    for p in products:
        checked += 1
        if p["stock"] == 0:
            result = p["code"]
    return result, checked


if __name__ == "__main__":
    shop = [
        {"code": "SP01", "stock": 12},
        {"code": "SP02", "stock": 0},
        {"code": "SP03", "stock": 5},
        {"code": "SP04", "stock": -2},
        {"code": "SP05", "stock": 30},
        {"code": "SP06", "stock": 0},
    ]
    print("Gian hàng 6 sản phẩm:", first_out_of_stock(shop))
    print("Gian hàng đủ hàng:", first_out_of_stock([shop[0], shop[2], shop[4]]))
    print("Bán vượt tồn kho:", first_out_of_stock([shop[0], shop[3], shop[4]]))
    print("Gian hàng chưa có sản phẩm:", first_out_of_stock([]))
    full = [{"code": "SP", "stock": 9}] * 999
    print("1.000 sản phẩm, hết hàng ở đầu:", first_out_of_stock([{"code": "SPX", "stock": 0}] + full))
    print("1.000 sản phẩm, hết hàng ở cuối:", first_out_of_stock(full + [{"code": "SPX", "stock": 0}]))
