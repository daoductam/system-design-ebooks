# Ngày 10: Distributed Transactions Across Services

[← Ngày trước](day-09-splitting-read-and-write-data-models.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-11-handling-webhook-retries-idempotently.md)

---


# DAY 10 · SYSTEM DESIGN (THIẾT KẾ HỆ THỐNG)

## Distributed Transactions Across Services (Giao Dịch Phân Tán Qua Nhiều Dịch Vụ)

![Minh họa kịch bản giao dịch phân tán](images/page_040_00.png)

Đơn hàng **#4471** vừa đổ vào hệ thống của bạn lúc 14:02. Luồng xử lý diễn ra như sau:

1. **`OrderService`** tạo đơn hàng trong cơ sở dữ liệu (Postgres) ✅
2. **`PaymentService`** trừ $89.50 qua cổng thanh toán Stripe ✅
3. **`InventoryService`** cố gắng giữ hàng theo mã sản phẩm (SKU) → **thất bại** (bị bán vượt quá số lượng / oversold 3 sản phẩm) ❌
4. **`ShippingService`** không bao giờ được gọi đến

Hiện tại bạn đang rơi vào tình cảnh: **giữ tiền của khách hàng, không có hàng trong kho để giao, và đơn hàng bị mắc kẹt ở trạng thái `PENDING` (chờ xử lý)**. 

Trong kiến trúc nguyên khối (*monolith*), bạn chỉ việc bọc cả 4 bước này vào một transaction và thực hiện `ROLLBACK`. Nhưng bạn không thể làm điều đó xuyên suốt 4 dịch vụ (*services*) với 4 cơ sở dữ liệu (*databases*) độc lập.

**Bạn sẽ chọn giải pháp nào?**

---

### Các Phương Án Lựa Chọn:

* **A — Choreography Saga (Saga biên đạo / phân tán):** Mỗi service tự xuất bản sự kiện (*publishes events*), service tiếp theo lắng nghe và phản ứng; khi có lỗi xảy ra sẽ kích hoạt các sự kiện bù đắp (*compensating events*) đi ngược lại chuỗi quy trình.
* **B — Orchestration Saga (Saga điều phối tập trung):** Một bộ điều phối trung tâm (*central orchestrator* – một máy trạng thái / *state machine*) gọi từng service theo thứ tự và phân phối các thao tác bù đắp (*compensations*) khi có lỗi xảy ra.
* **C — Two-Phase Commit / 2PC (Cam kết hai pha):** Bộ điều phối (*coordinator*) khóa cả 4 service trong pha `PREPARE`, sau đó thực hiện commit đồng loạt (*atomically*) hoặc hủy bỏ (*aborts*).
* **D — Outbox + eventual consistency (Mô hình Outbox + tính nhất quán sau cùng):** Mỗi service ghi dữ liệu vào database cục bộ kèm theo một bản ghi outbox (*outbox row*), một tiến trình chuyển tiếp (*relay*) sẽ xuất bản sự kiện bất đồng bộ (*async*), các service hạ nguồn sẽ dần hội tụ tính nhất quán (*converge*).

---

## DAY 10 · ANSWERS & EXPLANATIONS (ĐÁP ÁN & GIẢI THÍCH CHI TIẾT)

![Sơ đồ kiến trúc Orchestration Saga](images/page_042_00.png)

### Câu trả lời 1
### ✓ ĐÁP ÁN CHÍNH XÁC

> [!TIP]
> **✅ Đáp án: B — Orchestration Saga (Saga điều phối tập trung)**

#### Why B wins (Vì sao B chiến thắng):
Quy trình thanh toán 4 bước với thứ tự thực thi nghiêm ngặt (*strict ordering*) + cơ chế bù đắp cho từng bước (*per-step compensations*) = chính xác là mục đích mà một bộ điều phối (*orchestrator*) được sinh ra để giải quyết. 

Hãy dựng một máy trạng thái **`CheckoutSaga`** (sử dụng Temporal, AWS Step Functions, Camunda, hoặc tự phát triển / *hand-rolled*). Nó sẽ gọi từng service theo đúng thứ tự: 

$$\text{OrderService} \longrightarrow \text{PaymentService} \longrightarrow \text{InventoryService} \longrightarrow \text{ShippingService}$$

Mỗi bước đều có một thao tác bù đắp (*compensation*) đã được đăng ký sẵn: 
- `CancelOrder` (Hủy đơn hàng)
- `RefundPayment` (Hoàn tiền)
- `ReleaseInventory` (Giải phóng tồn kho)

Khi `InventoryService` thất bại, bộ điều phối sẽ tự động duyệt ngược lại quy trình và hoàn tiền tự động. Trạng thái có tính bền vững (*durable*), khả năng quan sát cao (*observable*), và có thể phát lại được (*replayable*). Vào lúc 3 giờ sáng, bạn chỉ cần mở giao diện người dùng (UI) của orchestrator lên là có thể thấy chính xác bước nào bị lỗi cùng toàn bộ dữ liệu đầu vào/đầu ra (*full inputs/outputs*).

---

### Câu trả lời 2

> [!WARNING]
> #### Why A is the trap (Vì sao A là câu trả lời bẫy - Choreography):
> Rất thanh lịch trên lý thuyết (*elegant on paper*). Nhưng sẽ vỡ vụn khi quy trình có từ 4 bước trở lên kèm các nhánh bù đắp phức tạp (*branching compensations*). 
> 
> Logic nghiệp vụ cho kịch bản *"điều gì sẽ xảy ra khi tồn kho thất bại sau khi thanh toán đã thành công"* bị xé lẻ và rải rác (*smeared*) trên cả 3 services — những service này đều phải tự nắm rõ chế độ thất bại (*failure modes*) của nhau. Không ai thực sự làm chủ luồng xử lý (*nobody owns the flow*). Không có một nơi duy nhất để kiểm tra: *"trạng thái hiện tại của đơn hàng #4471 là gì?"*. Vào lúc 3 giờ sáng, bạn sẽ phải tự chắp vá thông tin từ các sự kiện nằm rải rác trên 4 Kafka topics khác nhau. 
> 
> **Choreography** chỉ phù hợp cho các tác vụ lỏng lẻo (*loose*), tác vụ phụ kiểu bắn-rồi-quên (*fire-and-forget side effects*) — chứ không dành cho các quy trình thanh toán tuần tự với các thao tác bù trừ cụ thể.

---

### Câu trả lời 3

> [!CAUTION]
> #### Why C is wrong (Vì sao C sai - 2PC):
> **Stripe không hỗ trợ 2PC.** Các API của các đơn vị vận chuyển (*shipping carrier APIs*) cũng vậy. 
> 
> Xa hơn thế, cơ chế 2PC phải giữ các khóa tài nguyên (*holds locks*) trong suốt pha `PREPARE` — chỉ cần một service phản hồi chậm sẽ làm nghẽn toàn bộ hệ thống (*stalls everything*). Ở quy mô lưu lượng thanh toán thực tế, chỉ riêng việc tranh chấp khóa (*lock contention*) đã đủ sức đánh sập hệ thống của bạn. Đây là câu trả lời mang tính sách vở giáo trình (*textbook answer*) và sẽ "chết" ngay khi va chạm với thực tế.

---

### Câu trả lời 4

> [!NOTE]
> #### Why D is wrong (Vì sao D sai - Outbox):
> **Outbox là mô hình hạ tầng (*infrastructure*), không phải là một Saga.** 
> 
> Nó giải quyết bài toán làm thế nào để xuất bản sự kiện một cách đáng tin cậy sau khi đã commit vào database cục bộ. Nó không định nghĩa thứ tự các bước (*step ordering*), không định nghĩa các hành động bù đắp (*compensations*), và không đưa ra câu trả lời cho việc điều gì sẽ xảy ra khi `InventoryService` gặp lỗi. Bạn vẫn sẽ cần phải xây dựng một Saga nằm bên trên mô hình Outbox này.

---

### Bảng Tổng Hợp So Sánh Các Giải Pháp

| Giải pháp | Tính toàn vẹn dữ liệu | Khả năng quan sát (Observability) | Khả năng mở rộng (Scalability) | Phù hợp với bài toán |
| :--- | :--- | :--- | :--- | :--- |
| **A. Choreography Saga** | Khó kiểm soát khi logic rẽ nhánh | Rất thấp (phân tán nhiều topic/log) | Cao | ❌ Không (dễ mất kiểm soát luồng lỗi) |
| **B. Orchestration Saga** | Rất cao (State Machine quản lý) | Rất cao (giao diện tập trung, rõ ràng) | Cao | ✅ **Tối ưu nhất cho Checkout flow** |
| **C. Two-Phase Commit (2PC)** | Tuyệt đối (ACID phân tán) | Trung bình | Rất kém (dễ tắc nghẽn do lock) | ❌ Không (không khả thi với bên thứ 3) |
| **D. Outbox Pattern** | Đảm bảo gửi message At-least-once | Phụ thuộc vào Message Broker | Cao | ❌ Không (chỉ là tầng transport, thiếu orchestration) |


---

[← Ngày trước](day-09-splitting-read-and-write-data-models.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-11-handling-webhook-retries-idempotently.md)
