# Ngày 22: Reliable Messaging Across Services

[← Ngày trước](day-21-choosing-a-real-time-streaming-transport.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-23-feed-fanout-for-celebrity-accounts.md)

---


# NGÀY 22 · SYSTEM DESIGN (THIẾT KẾ HỆ THỐNG)
## Truyền Nhận Thông Điệp Đáng Tin Cậy Giữa Các Dịch Vụ (Reliable Messaging Across Services)

Dịch vụ thanh toán (**PaymentService**) của bạn vừa trừ tiền của khách hàng thành công.  
Nó ghi dữ liệu vào cơ sở dữ liệu (**DB**). Bây giờ nó cần thông báo cho dịch vụ gửi thông báo (**NotificationService**): *"Hãy gửi email xác nhận."*  

Lời gọi HTTP bị vượt quá thời gian chờ (**HTTP call times out**). Liệu request có đến nơi không? Bạn không thể biết được. Bạn thực hiện thử lại (**retry**). Khách hàng nhận được hai email giống hệt nhau.  

Bạn vừa gặp phải **Bài toán hai vị tướng (Two Generals Problem)**. Đây không phải là lỗi phần mềm (bug). Đây là một định lý toán học đã được chứng minh.  
Không một giao thức nào trên kênh truyền không đáng tin cậy (**unreliable channel**) có thể đảm bảo cả hai phía cùng thống nhất được thông điệp cuối cùng. Dù đó là HTTP, TCP hay vòng lặp thử lại (**retry loop**) của bạn. Sự bất định này về mặt toán học là không thể triệt tiêu (**mathematically irreducible**).  

> [!NOTE]
> ### Thiết lập kiến trúc bài toán (Architecture Setup)
> * **PaymentService** (Node.js, PostgreSQL) $\rightarrow$ **NotificationService** (Go)  
> * Độ trễ p99: **~40ms** (**latency**), thỉnh thoảng gặp lỗi **504 Gateway Timeout** khi hệ thống chịu tải cao (**under load**).  
> * **Yêu cầu cốt lõi:** Bạn cần gửi **chính xác một email xác nhận** (exactly one confirmation email) cho mỗi giao dịch thanh toán — **không được gửi trùng lặp** (no double-sends), **không được bỏ sót** (no missed sends).  

**Bạn sẽ xây dựng giải pháp nào?**

![Minh họa bài toán truyền thông tin cậy](images/page_090_00.png)

---

### Các phương án lựa chọn:

* **A)** Thử lại với thời gian chờ tăng theo cấp số nhân (**Retry with exponential backoff**) cho đến khi **NotificationService** trả về mã HTTP 200. Nếu bạn tiếp tục thử lại cho đến khi nhận được xác nhận (**ACK - Acknowledgment**), bạn biết chắc chắn thông điệp đã đến nơi.
* **B)** Đóng gói cả hai tác vụ trong một giao dịch phân tán (**Distributed Transaction - 2PC: Two-Phase Commit**) — **PaymentService** và **NotificationService** cùng commit (ghi nhận) đồng thời hoặc cả hai đều không làm gì cả (rollback).
* **C)** Sử dụng mô hình Outbox (**Outbox Pattern**) — **PaymentService** ghi sự kiện thông báo vào một bảng `outbox` trong cùng một giao dịch cơ sở dữ liệu (**DB transaction**) với giao dịch thanh toán. Một tiến trình chuyển tiếp độc lập (**relay process**) sẽ đọc và phân phối sự kiện đó riêng biệt.
* **D)** Đẩy message vào **SQS** với cơ chế phân phối ít nhất một lần (**At-least-once delivery**). **NotificationService** sẽ khử trùng lặp (**deduplicate**) dựa trên một khóa idempotent ổn định (**stable idempotency key**). Chấp nhận khả năng có thể gửi trùng thông điệp, nhưng không bao giờ bỏ sót.

---

![Minh họa phân tích và giải thích](images/page_092_00.png)

# NGÀY 22 · CÂU TRẢ LỜI & GIẢI THÍCH CHI TIẾT (ANSWERS & EXPLANATIONS)

### Câu trả lời 1
> [!TIP]
> ### ✓ CÂU TRẢ LỜI ĐÚNG: D — SQS + At-least-once + Idempotency Key (CORRECT)
>
> **D là câu trả lời duy nhất chấp nhận thực tế bất khả thi của kênh truyền và thiết kế kiến trúc xoay quanh giới hạn đó.**  
>
> * **At-least-once (Phân phối ít nhất một lần):** Đồng nghĩa với việc thông điệp chắc chắn sẽ đến nơi — có thể đến hai lần hoặc nhiều hơn.  
> * **Idempotency ở phía Consumer (Bảo toàn tính Idempotent):** Bằng cách lưu khóa (`payment_id:email:v1`) vào một bảng khử trùng lặp (**dedup table**), lượt phân phối thứ hai sẽ trở thành một tác vụ rỗng (**no-op - no operation**).  
>
> **Kết quả thực tế:** Không bao giờ bỏ sót lượt gửi (**no missed sends**) và không bao giờ gửi trùng email (**no double-sends**). Đây chính xác là cách mà các hệ thống lớn như **Stripe** và **AWS** xử lý.  
> * Hàng đợi (**Queue**) hấp thụ sự bất định (**absorbs uncertainty**).  
> * Tính Idempotent (**Idempotency**) hấp thụ các bản ghi trùng lặp (**absorbs duplicates**).

---

### Câu trả lời 2
> [!WARNING]
> ### A — Thử lại cho đến khi nhận ACK (SENIOR ENGINEER TRAP - CẠM BẪY CỦA KỸ SƯ SENIOR)
>
> Phương án này mang lại cảm giác cực kỳ chặt chẽ, không có kẽ hở. Nhưng thực tế thì hoàn toàn không.  
>
> Điều gì sẽ xảy ra nếu **chính phản hồi 200 mới là thứ bị vượt quá thời gian chờ (timed out)** — chứ không phải request ban đầu?  
> **NotificationService** đã gửi email thành công VÀ đã trả về mã 200, nhưng **PaymentService** không bao giờ nhận được phản hồi đó do rớt mạng giữa chừng. Vì vậy, bạn thực hiện **retry**. Email thứ hai ngay lập tức được gửi đi.  
>
> Lúc này, bạn lại cần cơ chế để xác nhận xem gói tin ACK của bạn đã tới nơi chưa... và đây chính là **vòng lặp đệ quy vô tận của Bài toán hai vị tướng (Two Generals recursion)**. Không một số lượng lần thử lại hữu hạn nào có thể khép kín được vòng lặp này.  
> **Càng bắt tay bắt cặp nhiều (More handshakes) = Càng gia tăng độ trễ (latency) và càng mở rộng bề mặt lỗi (failure surfaces), chứ không mang lại thêm sự chắc chắn nào.**

---

### Câu trả lời 3
> [!CAUTION]
> ### B — 2PC (Two-Phase Commit) (SAI - WRONG)
>
> Bộ điều phối (**Coordinator**) trong mô hình 2PC chính là một **điểm lỗi đơn lẻ (Single Point of Failure - SPOF)**.  
> Nếu Coordinator bị sập giữa Giai đoạn 1 (**Phase 1 - Prepare**) và Giai đoạn 2 (**Phase 2 - Commit**), cả hai dịch vụ sẽ bị treo cứng với các khóa tài nguyên đang bị giữ chặt (**locks held**), ngồi chờ đợi một quyết định commit/abort không bao giờ đến.  
>
> Bạn vừa đánh đổi sự bất định của việc truyền thông điệp (**message uncertainty**) lấy sự bất định do lỗi của bộ điều phối (**coordinator-failure uncertainty**) — bản chất vẫn là một bài toán cũ nhưng độ phức tạp tăng lên gấp bội.

---

### Câu trả lời 4
> [!NOTE]
> ### C — Outbox Pattern (ĐÚNG nhưng nặng nề hơn - CORRECT but heavier)
>
> Về bản chất, đây là một phương án rất vững chắc — đảm bảo tính nguyên tử (**atomicity**) ở tầng cơ sở dữ liệu (**DB level**), sự kiện (**event**) và bản ghi thanh toán (**payment**) sẽ luôn luôn đồng bộ tuyệt đối với nhau.  
>
> Tuy nhiên, hệ thống của bạn giờ đây phải vận hành thêm:
> 1. Một tiến trình chuyển tiếp riêng (**relay process**).
> 2. Đường ống bắt và đồng bộ dữ liệu thay đổi (**CDC pipeline - Change Data Capture**).
> 3. Cơ chế định kỳ dọn dẹp bảng outbox (**outbox cleanup**).
>
> Đối với hầu hết các đội ngũ kỹ thuật đã có sẵn hàng đợi **SQS**, **Phương án D đạt được 95% mức độ đảm bảo tương tự nhưng chỉ với một phần nhỏ chi phí hạ tầng (fraction of infrastructure)**.  
> * **Phương án C** phát huy tối đa sức mạnh khi hệ thống ở quy mô cực lớn (**scale**) hoặc khi bắt buộc phải đảm bảo thứ tự sự kiện nghiêm ngặt (**strict ordering**).  
> * **Phương án D** là câu trả lời tối ưu và phù hợp nhất cho phần lớn các đội ngũ kỹ sư hiện nay.

---

### Bảng so sánh tổng hợp các giải pháp

| Phương án | Cơ chế cốt lõi | Rủi ro chính | Đánh giá kiến trúc |
| :--- | :--- | :--- | :--- |
| **A. Retry until ACK** | Lặp lại HTTP request đến khi nhận 200 | Gửi trùng email khi timeout xảy ra ở chiều response (Two Generals Problem) | ❌ **Cạm bẫy (Senior Engineer Trap)** |
| **B. 2PC** | Commit phân tán 2 pha | Treo lock, Coordinator là Single Point of Failure | ❌ **Sai (Wrong Architecture)** |
| **C. Outbox Pattern** | Ghi chung DB transaction + Relay/CDC | Đòi hỏi thêm hạ tầng trung gian, tốn công bảo trì/dọn dẹp | ⚠️ **Đúng nhưng phức tạp (Overkill/Heavier)** |
| **D. SQS + Deduplication** | At-least-once queue + Idempotency key ở consumer | Cần thiết kế logic idempotent |  **Tối ưu nhất (Correct / Industry Standard)** |


---

[← Ngày trước](day-21-choosing-a-real-time-streaming-transport.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-23-feed-fanout-for-celebrity-accounts.md)
