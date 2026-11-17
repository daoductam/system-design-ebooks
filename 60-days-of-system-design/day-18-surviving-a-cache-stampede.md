# Ngày 18: Surviving a Cache Stampede

[← Ngày trước](day-17-backpressure-on-an-overwhelmed-consumer.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-19-read-your-writes-with-read-replicas.md)

---


# DAY 18 · THIẾT KẾ HỆ THỐNG (SYSTEM DESIGN)

## Sống sót qua thảm họa Cache Stampede (Surviving a Cache Stampede)

Khóa cache Redis (*cache key*) của bạn vừa hết hạn (*expired*) đối với một khóa mà có tới 8.000 người dùng truy cập mỗi giây.

Từng request đó giờ đây đang lao thẳng trực diện vào cơ sở dữ liệu (*database*) của bạn.

Đây chính là hiện tượng đàn bò dẫm đạp (*thundering herd / cache stampede*). Bạn vốn dĩ không gặp vấn đề về lưu lượng truy cập (*traffic*) — bạn đã gặp vấn đề về bộ nhớ đệm (*cache*). Và giờ thì bạn gặp cả hai vấn đề cùng lúc.

---

### Bối cảnh thiết lập hệ thống (The setup):

* **Dịch vụ (Service)** → Node.js API, 8.000 req/giây (*req/sec*) tại endpoint `/feed`.
* **Bộ nhớ đệm (Cache)** → Redis, thời gian sống TTL (*Time-To-Live*) = 60 giây đối với khóa `feed`.
* **Cơ sở dữ liệu (DB)** → Postgres, hoạt động ổn định ở mức chịu tải duy trì khoảng ~200 req/giây (*sustained*).
* **Điều gì đã xảy ra (What happened)** → TTL hết hạn đúng vào thời điểm lưu lượng đạt đỉnh (*peak traffic*), toàn bộ 8.000 req/giây đồng loạt ập vào Postgres cùng một lúc.

Cơ sở dữ liệu hiện đang quỵ ngã. Bạn chỉ còn vài phút trước khi nó sập hoàn toàn (*falls over*). Và lần hết hạn TTL tiếp theo sẽ diễn ra sau 60 giây nữa.

**Bạn sẽ làm gì?**

---

![Minh họa Cache Stampede](images/page_073_00.png)

---

### Các phương án lựa chọn:

* **A. Mutex lock (Khóa loại trừ tương hỗ / Distributed Lock):**
  Chỉ duy nhất một request giành được khóa để truy vấn cơ sở dữ liệu nhằm tái tạo bộ nhớ đệm (*rebuild cache*), các request còn lại phải xếp hàng chờ đợi phía sau.

* **B. Probabilistic early expiry (Hết hạn sớm theo xác suất):**
  Bắt đầu tái tạo cache ngẫu nhiên trước khi TTL thực sự chạm mốc 0.

* **C. Request coalescing (Gộp request đồng thời):**
  Gộp tất cả các request đang xử lý (*in-flight requests*) cho cùng một khóa thành một truy vấn DB duy nhất, sau đó trả về cùng một kết quả cho tất cả các request đó.

* **D. Cache pre-warming (Làm nóng cache chủ động trước):**
  Một tác vụ chạy ngầm (*background job*) tái tạo khóa theo lịch trình cố định, đảm bảo TTL không bao giờ chạm mốc 0 trên môi trường thực tế (*production*).

---

## NGÀY 18 · ĐÁP ÁN & GIẢI THÍCH CHI TIẾT (ANSWERS & EXPLANATIONS)

![Minh họa giải pháp xử lý](images/page_075_00.png)

### Đáp án 1

> [!TIP]
> ### ✓ CÂU TRẢ LỜI ĐÚNG:
> **Đáp án: D — Cache pre-warming (Làm nóng cache chủ động) ✅**

Dưới đây là lý do tại sao phương án D chiến thắng, và tại sao ba phương án còn lại đánh lừa được rất nhiều kỹ sư giỏi:

---

### Tại sao D chiến thắng (Why D wins — Cache pre-warming):

Làm nóng cache trước (*pre-warming*) triệt tiêu tận gốc hiện tượng thundering herd ngay từ căn nguyên. Một tiến trình chạy ngầm (*background job*) — có thể là một tác vụ định thời (*cron*), một hàm phi máy chủ (*scheduled Lambda*), hoặc một tiến trình xử lý hàng đợi (*Sidekiq worker*) — sẽ tái tạo khóa cache theo một chu kỳ cố định ngắn hơn thời gian sống TTL.

Khóa dữ liệu này sẽ không bao giờ bị nguội (*cold*) trên môi trường production. Không còn tồn tại "vách đá hết hạn" (*expiry cliff*) để 8.000 requests cùng lao đầu rơi xuống vực nữa.

* Bạn biết rõ dữ liệu này là dữ liệu nóng (*hot data*).
* Bạn biết rõ khi nào nó hết hạn.
* Bạn có đủ năng lực tính toán (*compute*) để chủ động tái tạo nó trước.

Chi phí bỏ ra chỉ là một tác vụ chạy ngầm mỗi ~45 giây; đổi lại, cơ sở dữ liệu của bạn sẽ không bao giờ phải hứng chịu đợt tăng vọt đột biến (*spike*) nào nữa. Netflix chủ động làm nóng dữ liệu metadata của nội dung. Twitter chủ động dựng sẵn dòng thời gian (*timelines*) cho các tài khoản có lượng người theo dõi khủng.

Mô hình thiết kế này hiện diện ở khắp mọi nơi — chỉ là nó không đủ hào nhoáng, bóng bẩy để xuất hiện thường xuyên trong các bài viết về kiến trúc hệ thống.

> [!NOTE]
> **Một chi tiết kỹ thuật cốt lõi cần lưu ý:**
> Hãy kết hợp phương pháp này với cơ chế **Stale-While-Revalidate (SWR)**. Trả về giá trị cũ/hơi lỗi thời (*stale value*) trong lúc tác vụ chạy ngầm đang làm mới dữ liệu, nhờ vậy việc tái tạo cache có chậm trễ một chút cũng không bao giờ gây ra hiện tượng trượt cache (*cache miss*).

---

### Đáp án 2

### Tại sao C là phương án bẫy (Why C is the trap answer — Request coalescing):

Kỹ thuật gộp request (*Request coalescing / Singleflight*) nghe có vẻ tinh vi và cao cấp nhất — gộp toàn bộ các request đồng thời (*concurrent requests*) cho cùng một khóa thành một truy vấn DB duy nhất, rồi trả về cùng kết quả đó cho tất cả. Không có thảm họa stampede, không có tranh chấp khóa (*lock contention*). Cực kỳ thanh lịch.

**Nhưng đây là điểm nó sụp đổ:**
Kỹ thuật coalescing đòi hỏi sự điều phối ngay trong tiến trình (*in-process coordination*). Nó hoạt động hoàn hảo trên một máy chủ đơn lẻ (*single server*). Nhưng trên 50 máy ảo/container Node.js chạy phía sau một bộ cân bằng tải (*Load Balancer*), mỗi phiên bản Node.js sẽ gộp request hoàn toàn độc lập — kết quả là bạn sẽ có 50 truy vấn DB đồng thời thay vì 8.000. Dù có đỡ hơn, nhưng đó vẫn là một đợt xung đột lưu lượng gấp **50 lần** mức tải bình thường mỗi khi TTL hết hạn.

Để có thể gộp request xuyên suốt giữa các phiên bản (*across instances*), bạn buộc phải dựng một tầng điều phối phân tán (*distributed coordination layer*), và lúc này bạn vừa tự tay xây dựng một thứ phức tạp gần ngang ngửa với mutex mà lại đánh mất đi tính đơn giản ban đầu.

> [!WARNING]
> Đây là câu trả lời đúng cho một máy chủ đơn tiến trình (*single-process server*). Nhưng ở quy mô phân tán lớn (*at scale*), nó chỉ là một giải pháp nửa vời mà các kỹ sư thường tự huyễn hoặc bản thân rằng nó đã hoàn chỉnh.

---

### Đáp án 3

### Tại sao A sai (Why A is wrong — Mutex lock):

Khóa Mutex (*Distributed Lock*) nhìn qua tưởng chừng rất gọn gàng: một request giành được khóa, đi tái tạo cache, tất cả những request khác đứng chờ. Không còn các truy vấn trùng lặp vào DB nữa.

Nhưng vấn đề chết người nằm ở chỗ **"tất cả những request khác đứng chờ"**. Dưới áp lực 8.000 req/giây, việc chờ đợi đồng nghĩa với việc các luồng API bị nghẽn (*threads blocked*), hàng đợi request (*request queue*) nhanh chóng bị lấp đầy, độ trễ phân vị p99 (*p99 latency*) vọt lên tới vài giây.

Bạn vừa mới đánh đổi việc quá tải DB lấy sự tắc nghẽn toàn diện ở tầng ứng dụng (*application-layer backup*). Cơ sở dữ liệu sống sót; nhưng trải nghiệm người dùng thì chết hẳn. Và nếu tiến trình giữ khóa bị chậm — ví dụ DB đang chật vật phản hồi khiến việc tái tạo mất 500ms — thì toàn bộ request trong hệ thống sẽ bị đóng băng (*stalls*) trong suốt khoảng thời gian đó.

---

### Đáp án 4

### Tại sao B sai (Why B is wrong — Probabilistic early expiry):

Thuật toán XFetch hoặc cơ chế hết hạn dựa trên độ trôi lệch ngẫu nhiên (*jitter-based expiry*) rất thông minh: khi thời gian sống TTL đếm ngược dần về 0, mỗi lượt đọc cache sẽ có một xác suất ngẫu nhiên nhỏ kích hoạt việc tái tạo cache sớm. Không cần khóa, không cần tầng điều phối. Toán học thuần túy và thanh lịch.

Tuy nhiên, điểm yếu là nó mang tính **xác suất (*probabilistic*)**, chứ **không có sự bảo đảm chắc chắn (*not guaranteed*)**.

Rơi vào đúng thời điểm bất lợi (ví dụ: lượng traffic xuống thấp ngay trước thời điểm TTL hết hạn, sau đó bất ngờ tăng vọt đột biến), khóa cache vẫn bị hết hạn trong trạng thái nguội (*expires cold*). Bạn chỉ mới làm giảm xác suất xảy ra hiện tượng thundering herd chứ chưa hề loại bỏ triệt để nó.

Đối với một endpoint đang phải gánh 8.000 req/giây liên tục 24/7, bạn cần một **sự đảm bảo tất định tuyệt đối (*deterministic guarantee*)** — chứ không phải chỉ trông chờ vào tỷ lệ may rủi.

---

### Bảng tổng hợp so sánh 4 giải pháp chống Cache Stampede

| Tiêu chí so sánh | A. Mutex Lock | B. Probabilistic Expiry (XFetch) | C. Request Coalescing | D. Cache Pre-warming + SWR |
| :--- | :--- | :--- | :--- | :--- |
| **Bản chất kỹ thuật** | Khóa phân tán (*Distributed Lock*), chặn các luồng khác chờ đợi | Kích hoạt làm mới sớm dựa trên xác suất toán học | Gộp các request đồng thời trong tiến trình (*In-process batching*) | Tác vụ ngầm (*Background Job*) chủ động làm mới trước khi hết hạn |
| **Tác động lên Database** | Tối đa 1 query, an toàn cho DB | Tối đa vài query, vẫn có rủi ro spike nếu lệch timing | Giảm từ 8.000 xuống $N$ truy vấn (với $N$ là số lượng server nodes) | **0 query đột biến** vào DB tại thời điểm hết hạn |
| **Độ trễ người dùng (p99 Latency)** | Rất tệ (bị nghẽn hàng đợi khi lock contention) | Tốt, hầu hết các request nhận cache nhanh | Tốt trên single server, nhưng tăng khi phân tán | **Tốt nhất (luôn trả về kết quả ngay lập tức)** |
| **Độ phức tạp hạ tầng** | Trung bình (cần Redis lock, xử lý timeout/deadlock) | Thấp (chỉ cần logic code toán học tại app layer) | Cao nếu chạy multi-instance (cần distributed coordination) | Rất thấp (chỉ cần 1 cronjob / worker định kỳ) |
| **Mức độ đảm bảo** | Tất định, nhưng hy sinh tầng ứng dụng | Xác suất (không cam kết 100% không bị miss) | Một phần (không xử lý triệt để bài toán multi-node) | **Cam kết tất định 100% (*Deterministic*)** |


---

[← Ngày trước](day-17-backpressure-on-an-overwhelmed-consumer.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-19-read-your-writes-with-read-replicas.md)
