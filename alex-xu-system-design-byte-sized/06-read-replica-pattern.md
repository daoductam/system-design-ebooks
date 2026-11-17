# Mô hình bản sao đọc (Read Replica Pattern)

[← Mục lục](README.md)

---

# MỤC LỤC & TỔNG QUAN KIẾN TRÚC

---

## --- Trang 4 ---

| Chủ đề / Tiêu đề kiến trúc | Trang |
| :--- | :--- |
| **Mô hình bản sao đọc (Read replica pattern)** | 105 |
| **Luồng nhận email (Email receiving flow)** | 107 |
| **Luồng gửi email (Email sending flow)** | 109 |
| **Câu hỏi phỏng vấn: Thiết kế Gmail (Interview Question: Design Gmail)** | 111 |
| **Kết xuất bản đồ (Map rendering)** | 113 |
| **Câu hỏi phỏng vấn: Thiết kế Google Maps (Interview Question: Design Google Maps)** | 115 |
| **Mô hình Kéo và Đẩy (Pull vs push models)** | 117 |
| **Dòng chu chuyển tiền tệ (Money movement)** | 119 |
| **Đối soát (Reconciliation)** | 122 |
| **Tôi nên sử dụng cơ sở dữ liệu nào cho hệ thống thu thập số liệu (metrics)? (Which database shall I use for the metrics collecting system?)** | 126 |
| **Hệ thống giám sát và cảnh báo chỉ số (Metrics monitoring and altering system)** | 129 |
| **Đối soát (Reconciliation)** | 131 |
| **Các bài báo khoa học về Dữ liệu lớn (Big data papers)** | 134 |
| **Tránh trừ tiền trùng lặp (Avoid double charge)** | 136 |
| **Bảo mật thanh toán (Payment security)** | 138 |
| **Mẹo phỏng vấn Thiết kế Hệ thống (System Design Interview Tip)** | 139 |
| **Sự phát triển/tiến hóa của Dữ liệu lớn (Big data evolvement)** | 140 |
| **Cây tứ phân (Quadtree)** | 142 |
| **Làm thế nào để tìm các nhà hàng lân cận trên Yelp? (How do we find nearby restaurants on Yelp?)** | 144 |
| **Một sàn giao dịch chứng khoán hiện đại đạt được độ trễ mức microsecond như thế nào? (How does a modern stock exchange achieve microsecond latency?)** | 147 |
| **Khớp lệnh mua và bán (Match buy and sell orders)** | 149 |
| **Thiết kế sàn giao dịch chứng khoán (Stock exchange design)** | 151 |
| **Thiết kế hệ thống thanh toán (Design a payment system)** | 153 |
| **Thiết kế hệ thống bán hàng chớp nhoáng (Design a flash sale system)** | 155 |
| **Ước tính sơ bộ (Back-of-the-envelope estimation)** | 157 |

3

---

## --- Trang 105 ---

### Luồng hoạt động qua Database Middleware

1. Khi Alice đặt một đơn hàng trên Amazon, yêu cầu (**request**) sẽ được gửi đến **Order Service** (Dịch vụ Đơn hàng).
2. **Order Service** không tương tác trực tiếp với cơ sở dữ liệu (**database**). Thay vào đó, nó gửi các truy vấn cơ sở dữ liệu (**database queries**) tới phần mềm trung gian cơ sở dữ liệu (**database middleware**).
3. **Database middleware** điều hướng các tác vụ ghi (**writes**) tới cơ sở dữ liệu chính (**primary database**). Dữ liệu sau đó được nhân bản/sao chép (**replicated**) tới hai bản sao (**replicas**).
4. Alice xem chi tiết đơn hàng (đọc - **read**). Yêu cầu được gửi thông qua **middleware**.
5. Alice xem lịch sử đơn hàng gần đây (đọc - **read**). Yêu cầu được gửi thông qua **middleware**.

**Database middleware** đóng vai trò như một **proxy** giữa tầng ứng dụng (**application**) và các cơ sở dữ liệu (**databases**). Nó sử dụng giao thức mạng chuẩn của MySQL (**standard MySQL network protocol**) để giao tiếp.

#### Ưu điểm (Pros):
- **Đơn giản hóa mã nguồn ứng dụng (Simplified application code):** Ứng dụng không cần phải nắm rõ cấu trúc tô-pô của cơ sở dữ liệu (**database topology**) cũng như không phải trực tiếp quản lý việc truy cập vào cơ sở dữ liệu.
- **Khả năng tương thích tốt hơn (Better compatibility):** Lớp **middleware** sử dụng giao thức mạng của MySQL (**MySQL network protocol**). Bất kỳ **client** nào tương thích với MySQL đều có thể kết nối tới **middleware** một cách dễ dàng. Điều này giúp quá trình di chuyển cơ sở dữ liệu (**database migration**) trở nên thuận tiện hơn.

#### Nhược điểm (Cons):
- **Tăng độ phức tạp của hệ thống (Increased system complexity):** Một **database middleware** là một hệ thống phức tạp. Vì tất cả các truy vấn cơ sở dữ liệu đều đi qua lớp **middleware**, nó thường đòi hỏi phải thiết lập cơ chế sẵn sàng cao (**high availability setup**) để tránh điểm nghẽn lỗi đơn lẻ (**single point of failure - SPOF**).
- **Thêm lớp middleware đồng nghĩa với việc gia tăng độ trễ mạng (network latency):** Do đó, tầng kiến trúc này đòi hỏi phải có hiệu năng cực kỳ xuất sắc (**excellent performance**).

104

---

## --- Trang 106 ---

# Mô hình bản sao đọc (Read replica pattern)

Trong bài viết này, chúng ta sẽ thảo luận về một mẫu thiết kế cơ sở dữ liệu (thiết lập) đơn giản nhưng được sử dụng rất phổ biến: **Mô hình bản sao đọc (Read replica pattern)**.

Trong cấu hình thiết lập này, tất cả các lệnh sửa đổi dữ liệu (**data-modifying commands**) như chèn mới (`insert`), xóa (`delete`), hoặc cập nhật (`update`) đều được gửi đến **DB chính (primary DB)**, còn các truy vấn đọc (**reads**) được gửi đến các **bản sao đọc (read replicas)**.

Sơ đồ dưới đây minh họa cho cấu hình thiết lập này:

![Read replica pattern](images/page_106_00.jpeg)

### Các bước vận hành:
1. Khi Alice đặt một đơn hàng trên **amazon.com**, yêu cầu (**request**) được gửi đến **Order Service**.
2. **Order Service** tạo một bản ghi về đơn hàng trong **primary DB** (tác vụ ghi - **write**). Dữ liệu được sao chép/nhân bản (**replicated**) tới hai bản sao (**replicas**).
3. Alice xem thông tin chi tiết đơn hàng. Dữ liệu được phục vụ từ một bản sao (**replica**) (tác vụ đọc - **read**).
4. Alice xem lịch sử đơn hàng gần đây. Dữ liệu được phục vụ từ một bản sao (**replica**) (tác vụ đọc - **read**).

Có một vấn đề nghiêm trọng cốt lõi trong mô hình thiết lập này: **Độ trễ sao chép dữ liệu (Replication lag)**.

105

---

[← Mục lục](README.md)
