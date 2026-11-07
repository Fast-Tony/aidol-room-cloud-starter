# Aidol Room Cloud — AI Livestream Starter

**Tự xây dựng phần mềm livestream AI của bạn bằng API Aidol Room Cloud.**

Bộ mã nguồn mẫu giúp nhà phát triển tạo ứng dụng mang giao diện và trải nghiệm riêng, kết nối với phòng đã thuê trên Aidol Room Cloud và tích hợp tương tác khán giả vào phiên live AI. Bạn có thể chỉnh sửa, phân phối và phát triển sản phẩm thương mại theo giấy phép [MIT](LICENSE).

## Bạn có thể xây dựng gì?

- Ứng dụng livestream AI với giao diện và thương hiệu của riêng bạn.
- Công cụ tiếp nhận bình luận, tương tác từ các nguồn được phép truy cập và gửi vào phòng live.
- Bảng điều khiển kết nối phòng, theo dõi thao tác và lấy link Browser Source cho OBS.
- Tích hợp phiên live AI vào quy trình bán hàng và phần mềm hiện có.

## Chức năng đã có trong bản mẫu

| Chức năng | Hiện tại |
|---|---|
| Kết nối phòng đã thuê bằng mã ALC | Có |
| Gửi bình luận, vào xem, theo dõi, chia sẻ, thích, quà tặng | Có |
| Tự nhận link Browser Source theo phòng | Có |
| Sao chép link OBS và mở xem bằng trình duyệt | Có |
| Client Python và giao diện desktop mẫu | Có |
| Tạo/thuê phòng, cấu hình nhân vật, kịch bản, bật/tắt live qua client này | Chưa hỗ trợ; thao tác trên web Room |
| Tự quét TikTok, Facebook, Shopee | Chưa tích hợp trong bản mẫu |

Đây là bộ khởi đầu cho nhà phát triển. Phiên bản hiện tại kết nối và tương tác với phòng được chuẩn bị trên web Room; chưa cung cấp toàn bộ vòng đời phòng qua API mẫu.

## Bắt đầu

Cài Python 3.10+ có Tkinter. Client dùng thư viện chuẩn, không cần cài thêm thư viện.

```sh
python demo_gui.py
```

1. Đăng nhập Aidol Room Cloud và thuê phòng.
2. Chọn nhân vật, kịch bản và bật live trên web Room.
3. Lấy mã ALC trong mục kết nối Router của phòng.
4. Mở ứng dụng mẫu, nhập mã rồi bấm **Kết nối phòng**.
5. App tự nhận link; bấm **Sao chép link OBS**, dán vào nguồn Browser trong OBS.
6. Gửi bình luận hoặc sự kiện để thử tương tác. Bật phản hồi bình luận trong cấu hình phòng.

Nếu chưa có link phát, ứng dụng tự kiểm tra lại mỗi 15 giây.

## Tích hợp vào phần mềm của bạn

```python
from client import AidolClient

client = AidolClient()
room = client.connect('ALC-CODE-FROM-ROOM')
# room['browser_source_url'] là link xem riêng khi luồng đã có.
client.send(
    'comment',
    'Lan',
    'Sản phẩm có màu gì?',
    event_id='source-message-123',
)
```

- `client.py`: lớp gọi API để tích hợp vào ứng dụng của bạn.
- `demo_gui.py`: giao diện mẫu để tham khảo và phát triển tiếp.
- Mỗi key chỉ truy cập một phòng và không có quyền bật/tắt live.
- Giữ nguyên event_id và nội dung khi gửi lại để chống trùng.
- HTTP 202 xác nhận nhận sự kiện, không xác nhận AI đã phát lời phản hồi. Phản hồi phụ thuộc cấu hình, dịch vụ giọng nói/bộ não và phiên thuê còn hiệu lực.

## Nền tảng và tài liệu

- Aidol Room Cloud: https://room.genaidol.com
- API hiện tại: https://genaidol.com/cloud-api/developer/v1
- Tài liệu API: https://genaidol.com/cloud-api/developer/v1/docs

Không công khai API key, mã kết nối hoặc link xem riêng. App chỉ giữ key trong bộ nhớ. Giấy phép MIT áp dụng cho mã nguồn mẫu; việc dùng dịch vụ Aidol Room Cloud tuân theo tài khoản, quyền sử dụng và mức phí của nền tảng.
