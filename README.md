# Aidol Events — Developer Sample

Mã nguồn mở theo giấy phép [MIT](LICENSE).

Ứng dụng mẫu gửi bình luận và sự kiện vào phòng Aidol đã thuê, đồng thời tự nhận link Browser Source cho OBS.

## Chạy ứng dụng

Cần Python 3.10+ có Tkinter. Client dùng thư viện chuẩn, không cần cài thêm thư viện.

```sh
python demo_gui.py
```

1. Thuê phòng, lấy mã ALC trong mục kết nối Router.
2. Nhập mã và bấm **Kết nối phòng**.
3. Bật live và phản hồi bình luận trong phòng.
4. App tự nhận link; bấm **Sao chép link OBS**, dán vào nguồn Browser trong OBS.
5. Chọn sự kiện, tên người xem, nội dung rồi bấm **Gửi sự kiện**.

Nếu chưa có link, app kiểm tra lại mỗi 15 giây. Không công khai API key, mã kết nối hoặc link xem riêng. Key chỉ được giữ trong bộ nhớ ứng dụng.

## Tích hợp Python

```python
from client import AidolClient
client = AidolClient()
result = client.connect('ALC-CODE-FROM-ROOM')
client.send('comment', 'Lan', 'Sản phẩm có màu gì?', event_id='source-message-123')
```

`result['browser_source_url']` chứa link xem riêng khi đã có luồng phát.

API: https://genaidol.com/cloud-api/developer/v1

Tài liệu: https://genaidol.com/cloud-api/developer/v1/docs

Hỗ trợ comment, join, follow, share, like, gift. Mỗi key chỉ truy cập một phòng và không có quyền bật/tắt live. Gửi lại phải giữ nguyên event_id và nội dung để chống trùng.

HTTP 202 xác nhận nhận sự kiện, không xác nhận AI đã phát lời phản hồi. Phản hồi phụ thuộc cấu hình và phiên thuê của phòng.

Ứng dụng này không tự quét sự kiện từ nền tảng; phần mềm thu thập của bạn gọi client.send khi có sự kiện được phép truy cập.
