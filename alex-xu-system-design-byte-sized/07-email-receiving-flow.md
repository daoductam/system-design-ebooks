# Quy trình tiếp nhận và phân loại Email (Email Receiving Architecture)

[← Mục lục](README.md)

---

### Trang 107

Trong một số trường hợp nhất định (độ trễ mạng (*network delay*), máy chủ bị quá tải (*server overload*), v.v.), dữ liệu trong các bản sao (*replicas*) có thể bị chậm trễ vài giây hoặc thậm chí vài phút. Trong tình huống này, nếu Alice kiểm tra ngay trạng thái đơn hàng (truy vấn được xử lý bởi bản sao - *replica*) ngay sau khi đơn hàng được đặt, cô ấy có thể sẽ không thấy đơn hàng đó đâu cả. Điều này khiến Alice hoang mang. Trong trường hợp này, chúng ta cần tính nhất quán **“đọc-sau-khi-ghi” (*read-after-write consistency*)**.

**Các giải pháp khả thi để giảm thiểu vấn đề này:**

1️⃣ **Các thao tác đọc nhạy cảm với độ trễ (*latency sensitive reads*)** được chuyển thẳng đến cơ sở dữ liệu chính (*primary database*).

2️⃣ **Các thao tác đọc diễn ra ngay sau thao tác ghi** được định tuyến tới cơ sở dữ liệu chính (*primary database*).

3️⃣ **Một cơ sở dữ liệu quan hệ (*relational DB*)** thường cung cấp cơ chế để kiểm tra xem một bản sao (*replica*) đã bắt kịp tiến độ với nút chính (*primary*) hay chưa. Nếu dữ liệu đã cập nhật (*up to date*), thực hiện truy vấn trên bản sao (*replica*). Ngược lại, từ chối/báo lỗi yêu cầu đọc (*fail the read request*) hoặc chuyển sang đọc từ cơ sở dữ liệu chính (*primary*).

---

### Trang 108

#### Luồng tiếp nhận Email (*Email receiving flow*)

Sơ đồ sau đây minh họa luồng tiếp nhận email:

![Sơ đồ luồng tiếp nhận Email](images/page_108_00.jpeg)

1. **Email gửi đến** sẽ đi vào bộ cân bằng tải SMTP (*SMTP load balancer*).
2. **Bộ cân bằng tải (*load balancer*)** phân phối lưu lượng truy cập giữa các máy chủ SMTP (*SMTP servers*). Chính sách chấp nhận email (*Email acceptance policy*) có thể được cấu hình và áp dụng ngay tại cấp độ kết nối SMTP (*SMTP-connection level*). Ví dụ: các email không hợp lệ sẽ bị trả về ngay lập tức (*bounced*) nhằm tránh việc xử lý email không cần thiết.
3. **Nếu tệp đính kèm (*attachment*)** của email quá lớn để đưa vào hàng đợi (*queue*), chúng ta có thể lưu trữ nó vào kho lưu trữ tệp đính kèm (*attachment store - ví dụ: S3*).
4. **Các email được đưa vào hàng đợi email đến (*incoming email queue*)**. Hàng đợi này giúp tách rời (*decouples*) các worker xử lý thư (*mail processing workers*) khỏi các máy chủ SMTP (*SMTP servers*), cho phép chúng có thể mở rộng quy mô độc lập (*scaled independently*). Hơn nữa, hàng đợi còn đóng vai trò như một bộ đệm (*buffer*) trong trường hợp lượng email tăng đột biến (*email volume surges*).
5. **Các worker xử lý thư (*mail processing workers*)** chịu trách nhiệm cho rất nhiều tác vụ, bao gồm lọc thư rác (*filtering out spam mails*), ngăn chặn virus, v.v. Các bước tiếp theo dưới đây giả định rằng email đã vượt qua quá trình xác thực (*validation*).
6. **Email được lưu trữ** vào kho lưu trữ thư (*mail storage*), bộ nhớ đệm (*cache*), và kho lưu trữ dữ liệu đối tượng (*object data store*).

---

[← Mục lục](README.md)
