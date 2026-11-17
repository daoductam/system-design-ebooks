# Ngày 16: Taming a Hot Partition Key

[← Ngày trước](day-15-fast-has-the-user-seen-this-checks.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-17-backpressure-on-an-overwhelmed-consumer.md)

---


# NGÀY 16 · THIẾT KẾ HỆ THỐNG (DAY 16 · SYSTEM DESIGN)
## Thuần hóa Hot Partition Key (Taming a Hot Partition Key)

Bạn đang vận hành một đường ống phân tích dữ liệu đa người thuê (**multi-tenant analytics pipeline**) trên DynamoDB với **200 tenant**, tổng lưu lượng là **12.000 lượt ghi/giây (12K writes/sec)**.

Mọi thứ đều êm đẹp — cho đến một ngày nọ.

Một tenant vừa tích hợp (onboard) một khách hàng khổng lồ chỉ sau một đêm. Khối lượng sự kiện (**event volume**) của họ tăng vọt **gấp 100 lần**. Giờ đây, riêng tenant duy nhất đó đang nã **9.000 lượt ghi/giây (9K writes/sec)** vào một **khóa phân vùng đơn lẻ (single partition key)**. Trong khi đó, 199 tenant còn lại hầu như chỉ ngồi chơi xơi nước.

Hàng loạt lỗi `ProvisionedThroughputExceeded` bắt đầu bắn ra tới tấp. Độ trễ ghi P99 (**P99 write latency**) tăng vọt từ **8ms lên 400ms**. Kỹ sư trực nhật (**on-call**) bị kích hoạt cảnh báo gọi dậy (paged). Tất cả mọi người đều đang bị bóp nghẽn lưu lượng (**throttled**) chỉ vì đúng một chiếc khóa (**single key**).

### Bối cảnh thiết lập hệ thống (Setup):
- **Bảng (Table)**: `events` (DynamoDB, chế độ dung lượng theo yêu cầu - *on-demand capacity*)
- **PK (Partition Key)**: `tenant_id` · **SK (Sort Key)**: `event_timestamp`
- **Tenant bị nghẽn nhiệt (Hot tenant)**: ~9.000 WPS (Writes Per Second) · **Tất cả các tenant khác**: ~15 WPS mỗi bên
- **Một khóa phân vùng duy nhất hấp thụ toàn bộ 9.000 lượt ghi** — Giới hạn trần trên từng phân vùng (**per-partition limit**) của DynamoDB chính là bức tường ngăn cản bạn

![Minh họa tình huống Hot Partition Key](images/page_065_00.png)

> [!WARNING]
> Đây là tình huống **Hot Partition** kinh điển trong các hệ thống lưu trữ phân tán NoSQL. Bạn sẽ xử lý tình huống này như thế nào?

---

### Các phương án lựa chọn (Options):

* **A. Phân mảnh khóa ghi (Write sharding)** — Nối thêm một hậu tố ngẫu nhiên (*random suffix*) vào PK (`tenant_id#0` … `tenant_id#9`).
* **B. Thêm độ trễ ngẫu nhiên cho các lượt ghi (Jitter the writes)** — Thêm một khoảng trễ ngẫu nhiên (0–500ms) ở phía client đẩy dữ liệu (*producer client*).
* **C. Tách phân vùng (Partition splitting)** — Tăng WCU (Write Capacity Units) của bảng và để DynamoDB tự động tách phân vùng bị nghẽn nhiệt (*auto-split the hot partition*).
* **D. Phân nhóm khóa theo khoảng thời gian (Time-bucket the key)** — Đổi cấu trúc PK thành `tenant_id#YYYY-MM-DD-HH`.

---

## NGÀY 16 · ĐÁP ÁN & GIẢI THÍCH CHI TIẾT (DAY 16 · ANSWERS & EXPLANATIONS)

![Sơ đồ kiến trúc giải pháp xử lý Hot Partition](images/page_067_00.png)

---

### Lời giải 1: Phương án A (Answer 1)

> [!TIP]
> ### ✓ CÂU TRẢ LỜI ĐÚNG: A — Write Sharding (ĐÁP ÁN CHÍNH XÁC)

DynamoDB sử dụng hàm băm (**hash function**) trên khóa phân vùng (**partition key**) để quyết định phân mảnh vật lý (**physical shard**) nào sẽ xử lý tác vụ ghi. 
$$\text{Một giá trị PK} = \text{Một shard} = \text{Một bức tường giới hạn.}$$
Khi tenant đó chạm mốc 9.000 WPS, shard vật lý đó sẽ chạm trần dung lượng ngay lập tức.

**Giải pháp (The fix):** 
Gắn thêm một hậu tố ngẫu nhiên (**random suffix**) ngay tại thời điểm ghi dữ liệu — từ `tenant_id#0` đến `tenant_id#9`. Giờ đây, hàm băm sẽ nhận diện **10 chiếc khóa khác nhau** và phân bổ đều các lượt ghi trên khắp **10 phân vùng logic (logical partitions)** (~900 WPS cho mỗi phân vùng, nằm an toàn bên dưới ngưỡng giới hạn). Lỗi nghẽn lưu lượng (**throttling**) biến mất, độ trễ P99 hạ nhiệt về lại mức một chữ số (dưới 10ms).

**Chi phí khi đọc (The read cost):** 
Bạn phải áp dụng cơ chế **Scatter-Gather** (phân tán truy vấn - thu thập kết quả) trên toàn bộ 10 hậu tố này để lấy dữ liệu cho tenant đó. Tuy nhiên, đối với một đường ống phân tích dữ liệu thiên về ghi (**write-heavy analytics pipeline**), đây là một sự đánh đổi hoàn toàn chuẩn xác (**the right tradeoff**).

> [!NOTE]
> Đây chính xác là mẫu thiết kế chuẩn (**canonical pattern**) được chính AWS ghi nhận trong tài liệu kỹ thuật để khắc phục triệt để vấn đề hot partitions.

---

### Lời giải 2: Phương án C (Answer 2)

> [!CAUTION]
> ### C — Partition Splitting (CẠM BẪY DÀNH CHO KỸ SƯ CAO CẤP / SENIOR ENGINEER TRAP)

DynamoDB quả thực có cơ chế tự động tách phân vùng (**auto-split partitions**) — chính vì vậy phương án này nghe có vẻ rất hợp lý. 

Thế nhưng, việc phân tách này **dựa trên lưu lượng tổng thể (throughput), chứ không dựa trên số lượng giá trị khóa duy nhất (key cardinality)**. Nếu một giá trị PK duy nhất sản sinh ra 9.000 WPS, toàn bộ các lượt ghi đó **vẫn sẽ bị băm (hash) về cùng một điểm đích** sau khi phân tách. Bạn **không thể** chia cắt một giá trị khóa đơn lẻ sang hai phân mảnh vật lý khác nhau được.

Bạn sẽ thấy phân vùng được tách ra trong CloudWatch, vội vàng cho rằng sự cố đã được giải quyết xong xuôi, để rồi lại bị hệ thống cảnh báo gọi dậy réo tên chỉ 10 phút sau đó. 

> Đây là dạng câu trả lời sống sót huy hoàng trong tài liệu thiết kế (design doc) nhưng lại chết thảm trong phòng xử lý khủng hoảng (war room).

---

### Lời giải 3: Phương án B (Answer 3)

> [!WARNING]
> ### B — Jitter the writes (Thêm độ trễ ngẫu nhiên cho các lượt ghi)

**Jitter** là một mẫu thiết kế có thật và hữu ích — nó giải quyết bài toán hiệu ứng đám đông ùa vào cùng lúc (**thundering herd problem**), khi mà $N$ clients đồng loạt gửi yêu cầu tại cùng một mili-giây và tạo nên một đỉnh nhọn đột biến (**spike**). Việc phân tán các request đó trong khoảng thời gian 500ms sẽ giúp làm mịn tải xung đột biến (**smooths the burst**).

Tuy nhiên, hot partition ở đây là một lưu lượng **9.000 WPS kéo dài liên tục (sustained)**, chứ không phải là một đợt bùng phát ngắn hạn. Thêm độ trễ vào không hề làm giảm tốc độ luồng dữ liệu — DynamoDB vẫn tiếp tục phải hứng chịu 9.000 WPS đổ vào cùng một phân vùng. Bạn vừa khiến cho mọi thao tác ghi trở nên chậm chạp hơn mà chẳng thu lại được bất kỳ lợi ích nào.

---

### Lời giải 4: Phương án D (Answer 4)

> [!NOTE]
> ### D — Time-bucket the key (Gom nhóm khóa theo thời gian)

Mẫu cấu trúc `tenant_id#2026-05-21-14` là một mẫu thực tế rất phổ biến đối với dữ liệu chuỗi thời gian (**time-series data**) — nó giữ kích thước trên mỗi bucket ở mức kiểm soát được và hỗ trợ cơ chế hết hạn TTL (Time-To-Live) hiệu quả.

Thế nhưng, tại bất kỳ một giờ nhất định nào, bạn **vẫn chỉ có duy nhất một partition key** đang phải gánh toàn bộ 9.000 WPS cho tenant đó. Bạn thực chất chỉ đang đổi tên từ một **hot partition** thành một **hot time bucket**. Vẫn là vấn đề cũ, chỉ khoác lên một cái tên mới. Chưa kể giờ đây các tác vụ đọc (**reads**) của bạn còn phải khổ sở truy vấn qua 24 PK khác nhau chỉ để lấy dữ liệu của một ngày duy nhất.

---

### Bảng tổng kết so sánh các phương án:

| Phương án | Bản chất cơ chế | Tác động tới Hot Partition (9K WPS) | Kết luận |
| :--- | :--- | :--- | :--- |
| **A. Write Sharding** | Gắn hậu tố ngẫu nhiên `#0..#9` để phân tán hash | Chia nhỏ 9K WPS thành 10 luồng ~900 WPS vào 10 partition vật lý | **CHÍNH XÁC (The Right Answer)** |
| **B. Jitter writes** | Delay ngẫu nhiên 0–500ms ở producer | Không đổi; tải sustained 9K WPS vẫn nã vào 1 partition | **SAI (Chỉ làm tăng độ trễ vô ích)** |
| **C. Partition Splitting**| Tăng WCU để hệ thống tự auto-split | Hash của 1 PK duy nhất vẫn trỏ về đúng 1 shard vật lý | **SAI (Cạm bẫy Senior Engineer)** |
| **D. Time-bucket key** | Đổi PK thành `tenant_id#YYYY-MM-DD-HH` | Trong mỗi 1 giờ, 1 PK duy nhất vẫn phải gánh trọn 9K WPS | **SAI (Bình mới rượu cũ, đọc phức tạp)** |


---

[← Ngày trước](day-15-fast-has-the-user-seen-this-checks.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-17-backpressure-on-an-overwhelmed-consumer.md)
