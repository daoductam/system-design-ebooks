# Sự tiến hóa của giao thức HTTP (HTTP/1.0 -> HTTP/1.1 -> HTTP/2.0 -> HTTP/3.0 QUIC)

[← Mục lục](README.md)

---

# Mục lục

* **HTTP 1.0 -> HTTP 1.1 -> HTTP 2.0 -> HTTP 3.0 (QUIC)** — *Trang 53*
* **Làm thế nào để mở rộng quy mô một website phục vụ hàng triệu người dùng? (How to scale a website to support millions of users?)** — *Trang 55*
* **Sách về DevOps (DevOps Books)** — *Trang 58*
* **Tại sao Kafka lại nhanh? (Why is Kafka fast?)** — *Trang 60*
* **SOAP vs REST vs GraphQL vs RPC** — *Trang 62*
* **Trình duyệt hiện đại hoạt động như thế nào? (How do modern browsers work?)** — *Trang 63*
* **Redis vs Memcached** — *Trang 64*
* **Khóa lạc quan (Optimistic locking)** — *Trang 65*
* **Đánh đổi giữa độ trễ và tính nhất quán (Tradeoff between latency and consistency)** — *Trang 67*
* **Tấn công xuyên thủng bộ nhớ đệm (Cache miss attack)** — *Trang 68*
* **Cách chẩn đoán một tiến trình bí ẩn ngốn quá nhiều CPU, bộ nhớ, I/O...?** — *Trang 70*
* **Các chiến lược bộ nhớ đệm hàng đầu là gì? (Top cache strategies)** — *Trang 71*
* **Tải lên các tệp tin lớn (Upload large files)** — *Trang 74*
* **Tại sao Redis lại nhanh đến vậy? (Why is Redis so Fast?)** — *Trang 76*
* **Mạng lưới thanh toán SWIFT (SWIFT payment network)** — *Trang 77*
* **At-most-once, at-least-once, và exactly-once** — *Trang 80*
* **Phân vùng dọc và phân vùng ngang (Vertical partitioning & Horizontal partitioning)** — *Trang 82*
* **Mạng phân phối nội dung (CDN - Content Delivery Network)** — *Trang 84*
* **Mã hóa xóa (Erasure coding)** — *Trang 87*
* **Giao dịch ngoại hối trong thanh toán (Foreign exchange in payment)** — *Trang 89*
* **Lưu trữ khối, lưu trữ tệp và lưu trữ đối tượng (Block storage, file storage and object storage)** — *Trang 94*
* **Lưu trữ khối, lưu trữ tệp và lưu trữ đối tượng (tiếp theo)** — *Trang 95*
* **Tra cứu Hệ thống Phân giải Tên miền (DNS lookup)** — *Trang 97*
* **Điều gì xảy ra khi bạn nhập một URL vào trình duyệt?** — *Trang 99*
* **Công cụ lập trình AI (AI Coding engine)** — *Trang 101*
* **Mô hình bản sao chỉ đọc (Read replica pattern)** — *Trang 103*

---

# HTTP 1.0 -> HTTP 1.1 -> HTTP 2.0 -> HTTP 3.0 (QUIC)

Mỗi thế hệ giao thức HTTP giải quyết vấn đề gì?

Sơ đồ dưới đây minh họa các tính năng cốt lõi:

![Sơ đồ tiến hóa HTTP](images/page_054_00.jpeg)

* **HTTP 1.0 (hoàn thiện và chuẩn hóa vào năm 1996):**
  * Mỗi request gửi đến cùng một server đều yêu cầu khởi tạo một **TCP connection** riêng biệt.

* **HTTP 1.1 (phát hành năm 1997):**
  * Hỗ trợ tái sử dụng kết nối TCP (**persistent connection**), nhưng **chưa giải quyết được vấn đề Head-of-line (HOL) blocking**.
  * **HOL blocking:** Xảy ra khi số lượng request song song cho phép trong trình duyệt đạt mức tối đa; các request đến sau buộc phải chờ các request phía trước hoàn tất.

---

* **HTTP 2.0 (phát hành năm 2015):**
  * Giải quyết vấn đề HOL thông qua kỹ thuật **đa luồng yêu cầu (request multiplexing)**, giúp loại bỏ HOL blocking tại **tầng ứng dụng (application layer)**; tuy nhiên, HOL vẫn tồn tại ở **tầng giao vận (transport / TCP layer)**.
  * Giới thiệu khái niệm **HTTP “streams”**: một tầng trừu tượng cho phép ghép kênh nhiều lượt trao đổi dữ liệu HTTP khác nhau trên cùng một kết nối TCP duy nhất. Dữ liệu trên mỗi stream không bắt buộc phải gửi tuần tự theo thứ tự ban đầu.

* **HTTP 3.0 (bản thảo đầu tiên công bố năm 2020):**
  * Là thế hệ kế tiếp của HTTP 2.0. Giao thức này sử dụng **QUIC** thay vì TCP ở tầng giao vận cơ sở, qua đó loại bỏ hoàn toàn tình trạng **HOL blocking tại tầng giao vận**.
  * **QUIC được xây dựng trên nền tảng UDP**, đưa khái niệm *stream* thành thành phần cốt lõi (first-class citizens) ngay tại tầng giao vận.
  * Các QUIC stream dùng chung một kết nối QUIC, do đó không cần lặp lại các bước bắt tay (**handshake**) hay khởi động chậm (**slow start**) khi tạo luồng mới.
  * Các stream trong QUIC được phân phối độc lập; trong hầu hết trường hợp, việc mất gói tin trên một stream sẽ không gây tắc nghẽn các stream còn lại.

> **Câu hỏi thảo luận:** Khi nào chúng ta nên nâng cấp lên HTTP 3.0? Đâu là những ưu điểm và nhược điểm cần cân nhắc?

---

# Làm thế nào để mở rộng quy mô một website phục vụ hàng triệu người dùng?
*(How to scale a website to support millions of users?)*

Chúng tôi sẽ giải thích điều này qua từng bước cụ thể.

Sơ đồ dưới đây minh họa quá trình tiến hóa kiến trúc của một website thương mại điện tử đơn giản: từ kiến trúc **nguyên khối (monolithic design)** trên một máy chủ duy nhất chuyển dần sang kiến trúc **hướng dịch vụ / vi dịch vụ (service-oriented / microservice architecture)**.

---

[← Mục lục](README.md)
