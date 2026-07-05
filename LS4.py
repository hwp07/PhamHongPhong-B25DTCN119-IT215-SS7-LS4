"""
phân tích:
input: order_id
output: thông báo 200/404/500

giải pháp
1. List
    + duyệt từ phần tử đầu
    + so sánh id
    + gặp thì dừng

2. Dict: tra cứu trực tiếp theo key

so sánh
| Tiêu chí             | Giải pháp 1: List                      | Giải pháp 2: Dict                          |
| -------------------- | -------------------------------------- | ------------------------------------------ |
| Tốc độ tìm kiếm      | Chậm (O(n)) vì phải duyệt từng phần tử | Nhanh (O(1)) vì tra cứu trực tiếp theo key |
| Bộ nhớ tiêu hao      | Ít bộ nhớ hơn                          | Tốn bộ nhớ hơn do lưu key                  |
| Độ dễ hiểu           | Dễ với người mới học                   | Hơi khó hơn nhưng rất phổ biến             |
| Khả năng bảo trì     | Kém khi dữ liệu lớn                    | Tốt khi dữ liệu lớn                        |
| Bối cảnh phù hợp     | Danh sách nhỏ                          | Hệ thống có nhiều dữ liệu                  |

=> chọn giải pháp 2: 
    + tìm kiếm rất nhanh
    + không cần duyệt toàn bộ danh sách
    + phù hợp với hệ thống có hàng chục nghìn hoặc hàng triệu đơn hàng
    + giảm thời gian phản hồi của API
"""

from fastapi import FastAPI, HTTPException, status

app = FastAPI()

orders_dict = {
    1: {"code": "SP001","payment_status": "PAID","method": "BANK_TRANSFER"},
    2: {"code": "SP002","payment_status": "UNPAID","method": "NONE"}
}


@app.get("/orders/{order_id}/payment")
def get_payment(order_id: int):
    try:
        order = orders_dict.get(order_id)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        return {
            "order_id": order_id,
            "payment_status": order["payment_status"],
            "method": order["method"]
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Đã xảy ra lỗi hệ thống. Vui lòng thử lại sau."
        )