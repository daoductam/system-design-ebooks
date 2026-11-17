# Ngày 20: Containing a Failing Downstream Dependency

[← Ngày trước](day-19-read-your-writes-with-read-replicas.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-21-choosing-a-real-time-streaming-transport.md)

---


# DAY 20 · SYSTEM DESIGN: Khống Chế Sự Cố Phụ Thuộc Cấp Dưới Bị Hỏng (Containing a Failing Downstream Dependency)

![Sơ đồ kịch bản sự cố hệ thống](images/page_081_00.png)

## Đề bài tình huống (Scenario)

Dịch vụ thanh toán (**checkout service**) của bạn gọi một API kiểm tra gian lận (**fraud-check API**) của bên thứ ba (3rd-party) trên mỗi đơn hàng.

API đó vừa bắt đầu gặp sự cố timeout ở mức **30 giây** thay vì mức **200ms** thông thường.

Các Node.js checkout pod của bạn sử dụng một **connection pool** gồm **50 kết nối** chung. Chỉ trong vòng 90 giây, toàn bộ kết nối đều bị chiếm giữ ("đậu đỗ" - parked) để chờ phản hồi từ Fraud API. Các yêu cầu thanh toán mới bị dồn ứ trong hàng đợi (queue). Độ trễ **P99** trên endpoint `/checkout` vọt từ **300ms lên 28s**. Khách hàng bấm thử lại (**retry**). Các Pod bị tràn bộ nhớ dẫn đến sập (**OOM - Out of Memory**). Fraud API bị suy giảm hiệu năng (degraded) — và toàn bộ hệ thống checkout của bạn bị sập hoàn toàn (down).

Dưới đây là thiết lập hệ thống:
* **Checkout (NestJS) → Fraud API (bên thứ ba)**: Đang bị timeout 30s.
* Cùng các pod đó cũng xử lý các endpoint `/cart`, `/orders`, `/health` — tất cả các dependency này đều đang khỏe mạnh (healthy dependencies).
* Trang dashboard riêng của Fraud API thông báo dịch vụ sẽ phục hồi sau **khoảng 10 phút**.
* Ngân sách cam kết chất lượng dịch vụ (**SLO budget**) cho cả quý của bạn sắp sửa bốc hơi hết.

Bạn cần phải cầm máu (ngăn chặn thiệt hại) ngay lập tức mà không làm mất đi các phần còn lại của dịch vụ checkout. **Bạn sẽ làm gì?**

---

## Các phương án lựa chọn

* **A.** Giảm thời gian chờ (**timeout**) xuống **2s** và thêm **3 lần thử lại (retries)** với cơ chế lùi thời gian theo hàm mũ (**exponential backoff**).
* **B.** Thêm một **Circuit Breaker** (Bộ ngắt mạch) tự động kích hoạt chuyển sang trạng thái mở (**OPEN**) sau $N$ lần thất bại, sau đó chuyển sang bán mở (**HALF-OPEN**) với một yêu cầu thăm dò duy nhất (**probe request**) trước khi đóng hoàn toàn (**CLOSED**).
* **C.** Áp dụng mô hình **Bulkhead** (Vách ngăn cách ly) cho các lệnh gọi Fraud API vào một connection pool / thread pool riêng biệt để chúng không thể làm cạn kiệt tài nguyên của phần còn lại trong dịch vụ checkout.
* **D.** **Cả B và C** — **Circuit Breaker** cho dependency đang gặp sự cố, và **Bulkhead** để cô lập bán kính ảnh hưởng (**blast radius**).

---

## Đáp án & Giải thích chi tiết (Answers & Explanations)

![Minh họa giải pháp Circuit Breaker kết hợp Bulkhead](images/page_083_00.png)

### Câu trả lời đúng

> [!TIP]
> **ĐÁP ÁN ĐÚNG: D — Kết hợp cả Circuit Breaker + Bulkhead cùng lúc ✅**

Dưới đây là lý do tại sao, và lý do vì sao ba phương án còn lại dễ đánh lừa các kỹ sư giỏi:

---

### Phân tích 1: Vì sao D chiến thắng (Why D wins: Circuit Breaker + Bulkhead)

Hai mẫu thiết kế (pattern) này giải quyết hai trạng thái lỗi (**failure modes**) hoàn toàn khác nhau, và bạn bắt buộc phải cần cả hai.

#### 1. Circuit Breaker (Bộ ngắt mạch)
**Circuit Breaker** ngăn chặn bạn liên tục nã yêu cầu vào một dependency đã chết. Sau $N$ lần thất bại liên tiếp (hoặc chạm ngưỡng tỷ lệ lỗi trên một cửa sổ trượt — **rolling window**), nó lật sang trạng thái **MỞ (OPEN)** — mọi lệnh gọi tiếp theo đến Fraud API sẽ lập tức thất bại nhanh (**fail fast**) với một phương án dự phòng (**fallback**). 
* Không còn phải chờ 30 giây.
* Không có kết nối nào bị giữ làm con tin.

Sau một khoảng thời gian hạ nhiệt (**cooldown**, ví dụ 30s), nó chuyển sang trạng thái **BÁN MỞ (HALF-OPEN)**: nó chỉ cho phép duy nhất một yêu cầu thăm dò (**probe request**) đi qua:
* Nếu yêu cầu thăm dò đó thành công, bộ ngắt mạch sẽ **ĐÓNG LẠI (CLOSED)** và lưu lượng truy cập bình thường được phục hồi.
* Nếu nó thất bại, nó lập tức quay về trạng thái **OPEN** cho một chu kỳ hạ nhiệt tiếp theo.

> [!NOTE]
> Trạng thái **HALF-OPEN** chính là phần mà hầu hết các bài hướng dẫn thường bỏ qua — nhưng đây chính là cơ chế ngăn chặn hiện tượng **đàn trâu giẫm đạp (thundering herd)** làm sập trở lại một dịch vụ vừa mới gượng dậy phục hồi.

#### 2. Bulkhead (Vách ngăn cách ly)
**Bulkhead** là phần mà hầu hết các kỹ sư quên mất sự tồn tại của nó cho đến khi họ phải trả giá đắt trong thực tế. Nó có nhiệm vụ **cô lập các nhóm tài nguyên (resource pools)**.

Fraud API của bạn được cấp một pool riêng biệt gồm, chẳng hạn, **10 kết nối** — tách biệt hoàn toàn khỏi **40 kết nối** còn lại dùng để phục vụ các endpoint `/cart`, `/orders`, `/health`.

Khi Fraud API bị treo:
* Nó có thể làm nghẽn (saturate) toàn bộ 10 kết nối của riêng nó.
* Nhưng 40 kết nối kia vẫn hoàn toàn rảnh rỗi.
* `/cart` vẫn tiếp tục hoạt động.
* `/health` vẫn tiếp tục hoạt động.
* Bán kính ảnh hưởng (**blast radius**) dừng lại cục bộ tại tính năng kiểm tra gian lận.

> [!IMPORTANT]
> **Triết lý Bulkhead:** Con tàu không bị chìm chỉ vì một khoang chứa bị ngập nước — đó chính xác là nguồn gốc nguyên bản của cái tên vách ngăn tàu (**Bulkhead**).

Các thư viện như **Resilience4j**, **Polly** (.NET), và **Hystrix** (legacy) đều hỗ trợ sẵn cả hai pattern này. **AWS App Mesh** + **Envoy** cung cấp cho bạn cơ chế bulkhead ngay tại tầng proxy (**proxy layer**). **Netflix** viết ra Hystrix chính vì họ đã rút ra bài học đắt giá này từ thực tế: một dependency chạy chậm duy nhất lan truyền qua các **shared thread pools** dùng chung đã kéo sập toàn bộ hệ thống gợi ý (recommendations) trong khung giờ cao điểm.

---

### Phân tích 2: Vì sao chỉ chọn B là chiếc bẫy dành cho Staff Engineer (Why B alone is the staff-engineer trap answer)

Một **Circuit Breaker** mà không có **Bulkhead** là câu trả lời nghe có vẻ hoàn chỉnh và rất chuẩn mực trong một buổi phỏng vấn. Nó là pattern được nhắc đến nhiều nhất trong các buổi diễn thuyết về khả năng phục hồi hệ thống (**resilience**). Và nó quả thực giải quyết được lỗi cụ thể được mô tả — một khi bộ ngắt mạch mở ra (**OPEN**), các lệnh gọi fraud sẽ thất bại nhanh (**fail fast**) và ngừng chiếm dụng kết nối.

**Nhưng đây là thực tế tàn khốc trên môi trường Production:**

Giữa lần thất bại số 1 (failure #1) và thời điểm bộ ngắt mạch thực sự bị kích hoạt (failure #N), **mỗi một request trong số $N$ request đó vẫn đang nắm giữ một kết nối từ pool dùng chung**.

Nếu ngưỡng kích hoạt của bạn là 20 lỗi trong 10 giây, bạn hoàn toàn có thể làm nghẽn sạch **connection pool 50 kết nối** trước khi Circuit Breaker kịp nhận biết sự cố. Bạn chỉ mới thu hẹp khoảng thời gian ngừng hoạt động (**outage window**), chứ chưa hề loại bỏ được sự cố sụp đổ dây chuyền (**cascading failure**).

> [!TIP]
> **Bulkhead** giúp cho ngưỡng kích hoạt của breaker trở nên **chịu đựng được độ trễ (latency-tolerant)**. Nó tạo ra một khoảng đệm an toàn (**slack**) để hệ thống phát hiện và phản ứng mà không khiến phần còn lại bốc cháy.

Đây là một cái bẫy vì phương án B **vừa đúng nhưng lại chưa đủ (incomplete)**. Các Senior Engineer thường dừng lại ở B trong các buổi review thiết kế vì nghe nó có vẻ thỏa đáng. Nhưng các **Staff Engineer** sẽ đưa D lên môi trường production vì họ đã từng chứng kiến B thất bại thảm hại ngoài đời thực lúc 3 giờ sáng.

---

### Phân tích 3: Vì sao chỉ chọn C là chưa trọn vẹn (Why C alone is partial)

Chỉ dùng một mình **Bulkhead** thì tốt hơn là không có gì — nó giúp khoanh vùng thiệt hại.

Tuy nhiên:
* 10 kết nối chuyên dụng dành cho fraud của bạn vẫn sẽ tiêu tốn trọn vẹn **30 giây** cho mỗi một lệnh gọi cầm chắc thất bại.
* Bạn đang phải trả toàn bộ chi phí về độ trễ (**latency cost**) trên mỗi tiến trình thanh toán, chỉ là trên một pool nhỏ hơn.
* Khách hàng vẫn phải trải nghiệm quá trình checkout cực kỳ chậm chạp; điều an ủi duy nhất là bạn không làm mất luôn tính năng giỏ hàng `/cart` đi cùng với chúng.

> [!WARNING]
> **Bulkhead mà không có Circuit Breaker** chẳng khác nào: *"Chỗ rò rỉ đã được cách ly trong khoang, nhưng căn phòng đó thì vẫn đang ngập đầy nước."*

---

### Phân tích 4: Vì sao A là sai và cực kỳ nguy hiểm (Why A is wrong and dangerous)

Hạ thấp timeout + thử lại với cơ chế lùi thời gian (**Lower timeout + retries with backoff**) là **điều tồi tệ nhất duy nhất** mà bạn có thể làm đối với một dependency đang bị suy kiệt (degraded). Đây là một mẫu hình phản thiết kế kinh điển (**canonical anti-pattern**).

* Fraud API vốn dĩ đã đang quá tải và chật vật.
* Bạn lại quyết định **bơm thêm lượng traffic gấp 3 lần bình thường** vào nó.
* Mọi cơn bão thử lại (**retry storm**) từ từng pod checkout sẽ hội tụ dồn dập vào một dịch vụ đang cần giảm tải để hồi phục.

Đây chính là cách một sự cố cục bộ (**partial outage**) biến thành một vụ sập toàn diện (**total outage**) — và cách một sự cố chỉ mất 10 phút biến thành một thảm họa kéo dài 4 tiếng đồng hồ.

> [!CAUTION]
> Cơ chế **Retries** chỉ thuộc về các **lỗi tạm thời (transient errors)** như một lỗi mạng đơn lẻ, mã 503 thoáng qua hoặc một kết nối bị reset (**connection reset**), chứ tuyệt đối **không được áp dụng cho tình trạng suy thoái có tính hệ thống (systemic degradation)**. 
> 
> Và chúng luôn luôn cần một **Circuit Breaker** ở phía thượng nguồn (**upstream**) để chặn đứng bán kính thiệt hại.

Nếu bạn từng đọc một báo cáo mổ xẻ sự cố (**postmortem**) có chứa cụm từ *"cơn bão thử lại đã góp phần kéo dài thời gian khôi phục hệ thống (retry storm contributed to extended recovery time)"* — thì đó chính xác là những gì đề bài đang ám chỉ.

---

### Bảng tổng hợp so sánh các chiến lược

| Chiến lược | Ngăn chặn cạn kiệt tài nguyên dùng chung? | Loại bỏ độ trễ 30s cho Checkout? | Bảo vệ Dependency bên thứ ba? | Đánh giá kiến trúc |
| :--- | :---: | :---: | :---: | :--- |
| **A. Timeout 2s + 3 Retries** | ❌ Không | ❌ Không | ❌ Gây quá tải thêm (**Retry Storm**) | **Anti-pattern nguy hiểm** |
| **B. Chỉ Circuit Breaker** | ❌ Không (vẫn nghẽn trong $N$ request đầu) | ✅ Có (sau khi ngắt mạch mở) | ✅ Có (giảm tải khi OPEN) | **Trap answer (Chưa đủ an toàn)** |
| **C. Chỉ Bulkhead** | ✅ Có (cô lập pool 10 kết nối) | ❌ Không (10 kết nối vẫn chờ 30s) | ❌ Không (vẫn nã request chậm liên tục) | **Chỉ giảm nhẹ một phần** |
| **D. Circuit Breaker + Bulkhead** | ✅ **Có** (bảo vệ 40 kết nối còn lại) | ✅ **Có** (Fail-fast ngay khi OPEN) | ✅ **Có** (Dừng nã request, probe an toàn) | **Chuẩn Production / Staff-level** |


---

[← Ngày trước](day-19-read-your-writes-with-read-replicas.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-21-choosing-a-real-time-streaming-transport.md)
