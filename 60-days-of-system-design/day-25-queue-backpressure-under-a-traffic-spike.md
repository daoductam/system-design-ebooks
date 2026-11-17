# Ngày 25: Queue Backpressure Under a Traffic Spike

[← Ngày trước](day-24-paginating-large-result-sets-efficiently.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-26-write-path-cache-consistency.md)

---


# NGÀY 25 · THIẾT KẾ HỆ THỐNG (DAY 25 · SYSTEM DESIGN)

## Áp lực ngược lên hàng đợi khi lưu lượng tăng đột biến (Queue Backpressure Under a Traffic Spike)

![Sơ đồ kiến trúc hàng đợi khi chịu áp lực ngược](images/page_103_00.png)

### Tình huống thực tế (Scenario)
Dịch vụ xử lý đơn hàng (*order processing service*) của bạn đang chạy trên **Amazon SQS** (*Simple Queue Service*).

* **Tải thông thường (Normal load):** 200 đơn hàng/phút (`200 orders/min`). Các tiến trình tiêu thụ dữ liệu (*consumers*) vẫn bắt kịp tốc độ này rất tốt.
* **Thời điểm sự kiện:** Ngày hội mua sắm **Black Friday** ập đến. Các tiến trình phát sinh dữ liệu (*producers*) bắt đầu đẩy tới **4.000 đơn hàng/phút** (`4,000 orders/min`). 
* **Hậu quả tức thì:** 
  * Độ sâu hàng đợi (*queue depth*) tăng vọt lên **80.000 thông điệp** (`80,000 messages`) chỉ trong vòng 20 phút.
  * Cơ sở dữ liệu hạ nguồn (*downstream DB*) của bạn đang chạm mức **95% CPU**.
  * Các consumers đang bị tụt lại phía sau xa dần và bạn đang phải chứng kiến hàng đợi phình to ra theo thời gian thực (*real time*).

Bạn cần phải xử lý tình trạng áp lực ngược (**backpressure**) này. **Bạn sẽ làm gì?**

---

### Các phương án lựa chọn (Options)

* **A)** Mở rộng quy mô người tiêu thụ theo chiều ngang (**Scale consumers horizontally**) — bổ sung thêm các hàm **AWS Lambda** / tiến trình worker trên **EC2** để ngốn hết lượng hàng đợi tồn đọng (*backlog*) nhanh hơn.
* **B)** Thiết lập thời gian ẩn thông điệp (**Visibility Timeout**) và định tuyến các thông điệp lỗi sang một hàng đợi chứa thư rác/thông điệp lỗi (**Dead-Letter Queue - DLQ**) nhằm phòng vệ trước các thông điệp độc hại (**Poison Pills**).
* **C)** Giới hạn tốc độ của bên phát sinh dữ liệu ngay tại nguồn (**Rate-limit producers at the source**) — sử dụng thuật toán thùng chứa thẻ (**Token Bucket**) hoặc cửa sổ trượt (**Sliding Window**) để áp mức trần tốc độ đẩy thông điệp vào hàng đợi.
* **D)** Chuyển sang sử dụng hàng đợi trễ **SQS Delay Queues** — trì hoãn khả năng hiển thị của thông điệp (*defer message visibility*) để dàn trải thời gian phân phối và giảm áp lực lên các consumers.

---

## NGÀY 25 · ĐÁP ÁN & GIẢI THÍCH CHI TIẾT (DAY 25 · ANSWERS & EXPLANATIONS)

![Phân tích chi tiết giải pháp xử lý Backpressure](images/page_104_00.png)

### Câu trả lời 1 (Answer 1)

### ✓ ĐÁP ÁN ĐÚNG: C

#### Tại sao phương án C chiến thắng, và tại sao nó không phá hỏng trải nghiệm người dùng (UX)

Hàng đợi tăng lên bởi vì phía phát sinh dữ liệu (*producer*) đang thắng trong cuộc đua tốc độ: **4.000 thông điệp nạp vào, chỉ có 200 thông điệp được xử lý xong**. Bạn có thể mở rộng quy mô (*scale*) các consumers cả ngày lẫn đêm thì khoảng cách chênh lệch đó cũng không thể tự thu hẹp được, đặc biệt là khi cơ sở dữ liệu (*database*) hạ nguồn vốn dĩ **đã chạm mốc 95% CPU**.

Giải pháp khắc phục nằm ở **thượng nguồn (upstream)**. Hãy giới hạn tốc độ (*Rate-limit*) bên producer bằng thuật toán **Token Bucket** hoặc **Sliding Window**. Trong hệ sinh thái **AWS**, đó có thể là:
* Các gói sử dụng của **API Gateway** (*API Gateway usage plans*),
* Mức đồng quy dành riêng của Lambda (**Lambda reserved concurrency**),
* Hoặc các lớp phần mềm trung gian điều tiết (**throttle middleware**) bên trong chính dịch vụ.

Khi đó:
1. Độ sâu hàng đợi (*queue depth*) sẽ ổn định trở lại.
2. Các consumers bắt kịp tiến độ theo nhịp độ tự nhiên của chúng.
3. Cơ sở dữ liệu hạ nguồn không còn bị "nung nóng" ở ngưỡng tới hạn nữa.

> [!TIP]
> **Mô hình tư duy cốt lõi (Mental Model):** 
> *Hãy vặn nhỏ vòi nước lại, thay vì chỉ chăm chăm mở rộng lỗ thoát nước.* *(Slow the tap, don't just widen the drain).*

---

#### Chi tiết quan trọng mà sơ đồ thường lướt qua: "Producer" không phải là người dùng cuối của bạn!

Trong hầu hết các hệ thống thực tế chuẩn kiến trúc phân rã (*decoupled*):
1. Người dùng gửi một đơn hàng (**submit order**).
2. Đơn hàng được ghi nhận vào Database và người dùng nhận ngay phản hồi thành công (**success response**).
3. Một tiến trình xử lý tách biệt sau đó sẽ đọc các sự kiện này (thông qua cơ chế thăm dò - **polling** hoặc lắng nghe thay đổi dữ liệu - **CDC - Change Data Capture**) rồi mới bắn chúng vào hàng đợi **SQS**.

Chính **bộ phát sự kiện (emitter) đó mới là producer mà bạn cần điều tiết (throttle)**.

Do đó, việc áp đặt **Rate-limiting** này không bao giờ chạm đến tiến trình thanh toán (*checkout*) của khách hàng:
* Người dùng **đã nhận được phản hồi xác nhận (ACK)** từ thao tác ghi trước đó rồi.
* Bạn chỉ đang khống chế trần tốc độ luân chuyển các sự kiện đi vào hàng đợi, chứ không hề giới hạn tốc độ đặt hàng của người dùng.
* Trải nghiệm người dùng (**UX**) hoàn toàn nguyên vẹn; chỉ có hàng đợi là ngừng việc vượt quá khả năng xử lý của consumers.

> [!NOTE]
> **Bản chất thực sự của Áp lực ngược (Backpressure):** 
> Đó là khi **hệ thống hạ nguồn (downstream) phát tín hiệu yêu cầu hệ thống thượng nguồn (upstream) phải chạy chậm lại**. 
> Độ sâu hàng đợi (*queue depth*) chính là tín hiệu đó. Và việc bạn cần làm là **phản ứng với tín hiệu đó ngay tại thượng nguồn**.

---

### Câu trả lời 2 (Answer 2)

#### Tại sao A là câu trả lời bẫy (Scale consumers):

Đây là câu trả lời mang tính bản năng, và nó đủ thuyết phục để đánh lừa cả những kỹ sư cấp cao (**Senior Engineers**).

Đúng là việc có thêm nhiều consumers đồng nghĩa với việc gia tăng thông lượng (*throughput*). Nhưng làm như vậy là bạn đang **đối xử với một vấn đề lệch pha về tốc độ (rate mismatch) như thể nó là một vấn đề về dung lượng phần cứng (capacity problem)**.

Nếu producer luôn luôn có thể tạo ra dữ liệu nhanh hơn tốc độ mà consumers có thể xử lý — và vào ngày Black Friday thì chắc chắn nó làm được điều đó — bạn đang lao vào một cuộc chạy đua vũ trang không bao giờ thắng:
* Bạn khởi chạy thêm gấp **10 lần hàm Lambda**,
* Bạn đâm sầm vào giới hạn thông lượng ghi (**write throughput limits**) của **DynamoDB**,
* Bạn dập nát vùng kết nối (**RDS connection pool**) của cơ sở dữ liệu quan hệ,
* Và kết quả là: **Hàng đợi vẫn tiếp tục phình to**, chỉ là với tốc độ chậm hơn một chút, trong khi hóa đơn chi phí hạ tầng (*infrastructure bill*) của bạn đã tăng lên gấp đôi.

> [!WARNING]
> Mở rộng quy mô người tiêu thụ (**Consumer scaling**) chỉ phát huy tác dụng khi nút thắt cổ chai của bạn nằm ở **năng lực tính toán (compute)**. Nó hoàn toàn vô tác dụng khi vấn đề xuất phát từ **tốc độ phát sinh không giới hạn của producer (unbounded producer rate)**.

---

### Câu trả lời 3 (Answer 3)

#### Tại sao B sai (Visibility timeout + DLQ):

Đây là cơ chế **xử lý sự cố (failure handling)**, hoàn toàn không phải là giải pháp xử lý áp lực ngược (**backpressure**).

* **Hàng đợi Dead-Letter Queue (DLQ):** Dùng để hứng các thông điệp độc hại (**Poison Pills**) — tức là những thông điệp liên tục bị lỗi trong quá trình xử lý và nếu không tách ra thì sẽ lặp lại vô tận trong hệ thống (*infinite loop*).
* **Thời gian ẩn thông điệp (Visibility Timeout):** Dùng để kiểm soát khoảng thời gian một thông điệp sẽ tạm thời biến mất/vô hình sau khi một consumer tiếp nhận nó (nhằm ngăn chặn việc bị xử lý trùng lặp - *double-processing*).

Cả hai cơ chế này **không hề làm chậm producer lại**, cũng **không làm giảm đà tăng trưởng độ sâu của hàng đợi**.

Việc nhầm lẫn giữa áp lực ngược (**backpressure**) với cơ chế thử lại/xử lý lỗi (**retry/error handling**) là một trong những hiểu lầm kiến trúc phổ biến nhất thường thấy. Hai cơ chế này giải quyết hai bài toán hoàn toàn khác biệt nhau.

---

### Câu trả lời 4 (Answer 4)

#### Tại sao D sai (SQS delay queues):

Hàng đợi trễ (**Delay queues**) chỉ trì hoãn **khả năng nhìn thấy của thông điệp (message visibility)**, chứ không hề trì hoãn việc **tạo ra thông điệp (message creation)**. 

* Producer của bạn vẫn miệt mài đẩy **4.000 thông điệp/phút**.
* Các thông điệp này sẽ âm thầm dồn ứ lại trong trạng thái vô hình.
* Khi khoảng thời gian trễ kết thúc, chúng sẽ đồng loạt hiện ra cùng một lúc thành từng đợt bùng nổ dữ liệu lớn (*bursts*).

Bạn không hề làm giảm áp lực ngược (**backpressure**) — bạn chỉ đang **hoãn cái sự quá tải đó lại một chút và làm cho đồ thị phân phối lưu lượng trở nên giật cục, nhọn hoắt hơn** (*spikier*).

> [!CAUTION]
> Làm như vậy chẳng khác nào việc **lấy nắp đậy một bồn rửa bát đang ngập tràn nước lại rồi tự dối lòng rằng sự cố đã được sửa xong**. Trong khi thực tế: **Nước vẫn đang không ngừng dâng cao...**

---

### Bảng tóm tắt so sánh kiến trúc (Architectural Comparison Matrix)

| Giải pháp | Bản chất kỹ thuật | Giải quyết được Backpressure? | Tác động lên Downstream DB (95% CPU) | Đánh giá kiến trúc |
| :--- | :--- | :---: | :--- | :--- |
| **A) Scale Consumers** | Mở rộng tầng Compute | ❌ Không | Đè bẹp hoàn toàn Connection Pool & IOPS | **Bẫy tư duy**: Biến lệch pha tốc độ thành nghẽn DB và lãng phí chi phí hạ tầng. |
| **B) Visibility Timeout + DLQ** | Error Handling & Poison Pill Isolation | ❌ Không | Không ảnh hưởng đến tải | **Sai mục đích**: Nhầm lẫn giữa xử lý lỗi/retry với điều tiết tải. |
| **C) Rate-limit Producers (Đáp án đúng)** | Traffic Shaping thượng nguồn (*Token Bucket / Sliding Window*) | ✅ **Có** | Giải phóng tải CPU, cho phép DB hạ nhiệt | **Tối ưu nhất**: Cắt ngọn cơn bão tải tại nguồn, duy trì trọn vẹn UX nhờ mô hình Decoupled Architecture. |
| **D) Delay Queues** | Defer Message Visibility | ❌ Không | Tạo ra hiện tượng giật tải (*traffic bursts*) ngay khi hết delay | **Nguy hiểm**: Chỉ giấu dòng nước ngập bằng cách đậy nắp, làm spike tải nặng nề hơn. |


---

[← Ngày trước](day-24-paginating-large-result-sets-efficiently.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-26-write-path-cache-consistency.md)
