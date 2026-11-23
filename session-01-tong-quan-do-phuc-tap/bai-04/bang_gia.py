"""Báo cáo bảng giá của một gian hàng trên Shopee."""


def top_prices(prices, k):
    # Trả về k giá cao nhất, từ cao xuống thấp.
    # Danh sách prices phải giữ nguyên thứ tự niêm yết (màn hình gian hàng dùng thứ tự này).
    prices.sort(reverse=True)
    return prices[:k]


def average_price(prices):
    # Giá trung bình. Gian hàng chưa có sản phẩm thì trả về None. Chỉ cần bộ nhớ phụ O(1).
    copy = prices[:]
    total = 0
    for p in copy:
        total += p
    return total / len(copy)


def cheapest_after_discount(prices, percent):
    # Giá thấp nhất sau khi giảm percent% (làm tròn xuống đồng). Không được sửa danh sách prices.
    discounted = prices
    for i in range(len(discounted)):
        discounted[i] = discounted[i] * (100 - percent) // 100
    return min(discounted)


if __name__ == "__main__":
    prices = [259000, 99000, 1490000, 459000, 189000]
    print("Giá niêm yết:", prices)
    print("3 giá cao nhất:", top_prices(prices, 3))
    print("Giá niêm yết sau khi lập top:", prices)
    print("Giá trung bình:", average_price(prices))
    print("Rẻ nhất sau khi giảm 10%:", cheapest_after_discount(prices, 10))
    print("Giá niêm yết sau khi tính giảm giá:", prices)
    print("Giá trung bình của gian hàng mới:", average_price([]))
