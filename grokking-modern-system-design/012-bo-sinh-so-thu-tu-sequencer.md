# 012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)

[← Bài trước](011-mang-phan-phoi-noi-dung-cdn.md) | [Mục lục](README.md) | [Bài tiếp theo →](013-giam-sat-phan-tan-distributed-monitoring.md)

---


# Thiết Kế Hệ Thống: Bộ Sinh Số Thứ Tự Toàn Cục (System Design: Sequencer)

Tìm hiểu các nguyên lý cơ bản trong thiết kế một bộ sinh số thứ tự toàn cục (Sequencer).

Chúng ta sẽ bao quát các nội dung sau:
* Động lực thiết kế (Motivation)
* Làm thế nào để thiết kế một bộ sinh số thứ tự (How do we design a sequencer?)

---

## Động Lực Thiết Kế (Motivation)

Trong một hệ thống phân tán quy mô lớn (large distributed system), có thể có hàng triệu sự kiện (events) diễn ra mỗi giây. Bình luận vào một bài đăng trên Facebook, chia sẻ một Tweet trên Twitter, hay đăng một bức ảnh lên Instagram chỉ là một vài ví dụ điển hình cho các sự kiện như vậy. Chúng ta cần một cơ chế để phân biệt các sự kiện này với nhau. Một trong những cơ chế đó là gán các định danh duy nhất trên toàn cục (**Globally Unique IDs**) cho từng sự kiện.

Gán khóa chính (**Primary Key**) cho một bản ghi trong cơ sở dữ liệu (Database) là một trường hợp sử dụng (use case) phổ biến khác của định danh duy nhất (Unique ID). Thông thường, tính năng tự động tăng (**Auto-increment**) trong cơ sở dữ liệu đáp ứng tốt yêu cầu này. Tuy nhiên, tính năng đó sẽ không hoạt động đối với một cơ sở dữ liệu phân tán (**Distributed Database**), nơi mà các nút (nodes) khác nhau sinh mã định danh một cách hoàn toàn độc lập. Đối với trường hợp này, chúng ta cần một bộ sinh ID duy nhất đóng vai trò làm khóa chính trong môi trường phân tán — ví dụ: một bảng được phân mảnh theo chiều ngang (**Horizontally-sharded table**).

Một ID duy nhất giúp chúng ta theo dõi và nhận diện luồng thực thi của một sự kiện trong các tệp nhật ký (logs), rất hữu ích cho quá trình gỡ lỗi (**Debugging**). Một ví dụ thực tế về việc sử dụng Unique ID là hệ thống phân tích và theo dõi hiệu năng đầu-cuối (**End-to-end performance tracing and analysis system**) Canopy của Facebook. Canopy sử dụng `TraceID` để định danh duy nhất một sự kiện xuyên suốt đường dẫn thực thi (**Execution path**), vốn có thể phải gọi tới hàng trăm dịch vụ vi mô (**Microservices**) để đáp ứng một yêu cầu duy nhất từ người dùng.

---

### Gán TraceID Duy Nhất Cho Từng Sự Kiện (Assigning a unique TraceID to each event)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p002_00.png)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p002_01.png)

> **Luồng xử lý minh họa:**
> * Chia sẻ bài đăng Facebook (Sự kiện A - `event A`) / Tải lên video (Sự kiện B - `event B`).
> * Luồng ID và Trace được chuyển qua bộ sinh Trace ID (**Trace ID generator**): sinh `[Trace ID for event A]` và `[Trace ID for event B]`.
> * Đưa vào lưu trữ (**Storage**), chia sẻ (**Share**), đăng lên dòng thời gian (**Post on timeline**).

---

## Làm Thế Nào Để Thiết Kế Một Bộ Sinh Số Thứ Tự? (How do we design a sequencer?)

Chúng tôi chia thiết kế toàn diện của bộ sinh số thứ tự thành hai bài học sau:

1. **Thiết kế Bộ Sinh ID Duy Nhất (Design of a Unique ID Generator):** Sau khi liệt kê các yêu cầu thiết kế, chúng ta sẽ thảo luận về ba phương pháp tạo ID duy nhất: sử dụng UUID, sử dụng cơ sở dữ liệu (Database), và sử dụng bộ xử lý dải số (Range Handler).
2. **ID Duy Nhất Có Tính Quan Hệ Nhân Quả (Unique IDs with Causality):** Trong bài học này, chúng ta sẽ kết hợp thêm yếu tố thời gian vào quá trình tạo ID và giải thích quy trình dựa trên việc xem xét mối quan hệ nhân quả (**Causality**).

> [!NOTE]
> Các ID duy nhất đóng vai trò vô cùng quan trọng trong việc định danh các sự kiện và đối tượng bên trong một hệ thống phân tán. Tuy nhiên, việc thiết kế một bộ sinh ID duy nhất trong môi trường phân tán là một bài toán đầy thách thức. Trong phần tiếp theo, chúng ta hãy cùng xem xét các yêu cầu kỹ thuật đối với một hệ thống sinh ID duy nhất phân tán.

---

## Thiết Kế Bộ Sinh ID Duy Nhất (Design of a Unique ID Generator)

Tìm hiểu cách thiết kế một hệ thống sinh định danh duy nhất.

Chúng ta sẽ bao quát các nội dung sau:
* Các yêu cầu đối với định danh duy nhất (Requirements for unique identifiers)
* Giải pháp thứ nhất: UUID (First solution: UUID)
  * Nhược điểm (Cons)
* Giải pháp thứ hai: Sử dụng cơ sở dữ liệu (Second solution: using a database)
  * Ưu điểm (Pros)
  * Nhược điểm (Cons)
* Giải pháp thứ ba: Sử dụng bộ xử lý dải số (Third solution: using a range handler)
  * Ưu điểm (Pros)
  * Nhược điểm (Cons)

Trong phần trước, chúng ta đã thấy sự cần thiết của các định danh duy nhất cho nhiều trường hợp sử dụng, chẳng hạn như xác định đối tượng (ví dụ: các đoạn Tweet, video được tải lên, v.v.) và theo dõi luồng thực thi trong một mạng lưới dịch vụ phức tạp. Bây giờ, chúng ta sẽ chuẩn hóa các yêu cầu đối với một định danh duy nhất và thảo luận về ba thiết kế cải tiến dần để đáp ứng các yêu cầu đó.

---

### Các Yêu Cầu Đối Với Định Danh Duy Nhất (Requirements for unique identifiers)

Các yêu cầu cho hệ thống của chúng ta như sau:

* **Tính duy nhất (Uniqueness):** Chúng ta cần gán các mã định danh duy nhất cho các sự kiện khác nhau nhằm mục đích nhận dạng.
* **Khả năng mở rộng (Scalability):** Hệ thống tạo ID phải có khả năng sinh ít nhất một tỷ (**1 billion**) ID duy nhất mỗi ngày.
* **Tính sẵn sàng cao (High Availability):** Vì có vô số sự kiện xảy ra ngay cả ở cấp độ nano giây (nanoseconds), hệ thống của chúng ta phải sinh được ID cho tất cả các sự kiện xảy ra.
* **ID số 64-bit (64-bit numeric ID):** Chúng ta giới hạn độ dài của ID ở mức 64 bits vì kích thước bit này là đủ dùng cho rất nhiều năm trong tương lai. Hãy cùng tính toán số năm trước khi dải ID của chúng ta bị tràn và quay vòng lại từ đầu (**Wrap around**):

$$\text{Tổng số lượng số khả dụng} = 2^{64} = 1.8446744 \times 10^{19}$$

$$\text{Số lượng sự kiện ước tính mỗi ngày} = 1 \text{ tỷ} = 10^9$$

$$\text{Số lượng sự kiện mỗi năm} = 365 \text{ tỷ} = 365 \times 10^9$$

$$\text{Số năm để dùng hết toàn bộ dải định danh} = \frac{2^{64}}{365 \times 10^9} = 50,539,024.8595 \text{ năm}$$

> [!TIP]
> Dựa trên các phép tính toán trên, độ dài **64 bits** là hoàn toàn đủ đáp ứng cho một Unique ID trong nhiều triệu năm.

Hãy cùng đi sâu vào các giải pháp khả thi cho bài toán nêu trên.

---

## Giải Pháp Thứ Nhất: UUID (First solution: UUID)

Một giải pháp đơn giản ban đầu (**Straw man solution**) cho thiết kế của chúng ta là sử dụng **UUID** (*Universally Unique Identifiers* - Định danh duy nhất toàn cầu). Đây là một số có độ dài 128-bit và có dạng thập lục phân (hexadecimal) như sau:

$$\text{123e4567e89b12d3a456426614174000}$$

Nó cung cấp cho chúng ta khoảng $10^{38}$ số. UUID có nhiều phiên bản khác nhau. Chúng ta lựa chọn **phiên bản 4 (Version 4)**, phiên bản sinh số giả ngẫu nhiên (**Pseudorandom number**).

Mỗi máy chủ (Server) có thể tự sinh ID của riêng mình và gán ID đó cho sự kiện tương ứng. Không cần bất kỳ sự điều phối tập trung nào (**No coordination is needed**) đối với UUID vì nó hoàn toàn độc lập với máy chủ. Việc mở rộng quy mô tăng lên hoặc giảm xuống (**Scaling up and down**) rất dễ dàng với UUID, và hệ thống này cũng đạt tính sẵn sàng cao (**High Availability**). Hơn nữa, nó có xác suất xung đột (**Collision probability**) cực kỳ thấp. 

Thiết kế cho phương pháp tiếp cận này được mô tả dưới đây:

### Tạo Unique ID Sử Dụng Phương Pháp UUID (Generating a unique ID using the UUID approach)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p005_00.png)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p005_01.png)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p005_02.png)

> **Kiến trúc luồng xử lý:**
> * Máy khách (**Clients**) $\rightarrow$ Bộ cân bằng tải (**Load Balancer**) $\rightarrow$ Các máy chủ Web (**Web servers**).
> * Mỗi Web server tự thực thi thao tác tạo ID (**Generate ID**) độc lập: ví dụ sinh ra UUID `123e4567e89b12d3a456426614174000`.

---

### Điểm Cần Suy Ngẫm (Point to Ponder)

> [!NOTE]
> **Câu hỏi trắc nghiệm:** (Chọn tất cả các đáp án đúng) Những ưu điểm của việc sử dụng phương pháp UUID là gì?

---

### Nhược Điểm (Cons)

* **Ảnh hưởng hiệu năng chỉ mục:** Việc sử dụng các số 128-bit làm khóa chính (**Primary Keys**) khiến cho việc đánh chỉ mục khóa chính (**Primary-key Indexing**) chậm hơn, dẫn đến tốc độ thêm mới dữ liệu (**Inserts**) bị chậm.
* **Định dạng dữ liệu không tối ưu:** Một giải pháp tình thế là diễn giải ID dưới dạng chuỗi hexa (Hex string) thay vì dạng số. Tuy nhiên, các định danh không phải dạng số (Non-numeric identifiers) có thể không phù hợp cho nhiều trường hợp sử dụng.
* **Kích thước không đạt chuẩn yêu cầu:** ID này không có kích thước 64-bit như mục tiêu thiết kế ban đầu.
* **Rủi ro trùng lặp về mặt lý thuyết:** Có khả năng xảy ra trùng lặp (**Duplication**). Mặc dù xác suất này là cực kỳ nhỏ, chúng ta không thể khẳng định UUID mang tính duy nhất một cách tất định (**Deterministically unique**).
* **Không đảm bảo thứ tự thời gian:** Thêm vào đó, các UUID được cấp cho máy khách theo thời gian có thể không có tính tăng đơn điệu (**Monotonically increasing**).

---

# Thiết kế Hệ thống: Bộ Sinh Số Thứ Tự Toàn Cục (System Design: Sequencer / Unique ID Generator)

---

### Các yêu cầu được đáp ứng khi sử dụng UUID (Requirements Filled with UUID)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p007_03.png)

| Tiêu chí | Sử dụng UUID (Using UUID) |
| :--- | :---: |
| **Tính duy nhất (Unique)** | ✅ |
| **Khả năng mở rộng (Scalable)** | ✅ |
| **Tính sẵn sàng cao (Available)** | ✅ |
| **Mã định danh số 64-bit (64-bit numeric ID)** | ❌ |

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p007_04.png)

---

## Giải pháp thứ hai: Sử dụng Cơ sở dữ liệu (Second solution: using a database)

Hãy thử mô phỏng lại tính năng tự động tăng (**auto-increment**) của một cơ sở dữ liệu. Hãy cân nhắc một cơ sở dữ liệu trung tâm (**central database**) chịu trách nhiệm cung cấp ID hiện tại và sau đó tăng giá trị này lên một đơn vị. Chúng ta có thể sử dụng ID hiện tại làm mã định danh duy nhất cho các sự kiện của mình.

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p007_06.png)

### Sử dụng cơ sở dữ liệu trung tâm để sinh ID duy nhất (Using a central database to generate unique IDs)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p007_07.png)

* **Cơ sở dữ liệu trung tâm (Central database)**
  * `. . .`
  * **Máy chủ 1 (Server 1):** Yêu cầu ID duy nhất (Request unique ID) $\rightarrow$ Trả về ID duy nhất (Return unique ID)
  * **Máy chủ 2 (Server 2):** Yêu cầu ID duy nhất (Request unique ID) $\rightarrow$ Trả về ID duy nhất (Return unique ID)
  * **Máy chủ 3 (Server 3):** Yêu cầu ID duy nhất (Request unique ID) $\rightarrow$ Trả về ID duy nhất (Return unique ID)
  * **Máy chủ N (Server N):** Yêu cầu ID duy nhất (Request unique ID) $\rightarrow$ Trả về ID duy nhất (Return unique ID)

---

### Điểm cần suy ngẫm (Point to Ponder)

> [!IMPORTANT]
> **Câu hỏi (Question):**
> Vấn đề tiềm ẩn khi sử dụng một cơ sở dữ liệu trung tâm là gì?

<details>
<summary><b>Ẩn câu trả lời (Hide Answer)</b></summary>

Thiết kế này tiềm ẩn một vấn đề rất lớn: **Điểm lỗi đơn lẻ (Single Point of Failure - SPOF)**.  
Việc phụ thuộc vào một cơ sở dữ liệu duy nhất có thể ảnh hưởng nghiêm trọng đến toàn bộ hệ thống. Toàn bộ hệ thống sẽ ngừng hoạt động nếu cơ sở dữ liệu trung tâm này gặp sự cố (**goes down**).
</details>

---

Để giải quyết vấn đề điểm lỗi đơn lẻ (**SPOF**), chúng ta sửa đổi tính năng tự động tăng truyền thống (vốn tăng từng đơn vị một). Thay vì tăng một đơn vị, hãy dựa vào một giá trị $m$, trong đó $m$ bằng tổng số lượng máy chủ cơ sở dữ liệu (**database servers**) mà chúng ta có.

Mỗi máy chủ sinh một ID, và ID tiếp theo sẽ cộng thêm $m$ vào giá trị trước đó. Phương pháp này có khả năng mở rộng (**scalable**) và ngăn chặn việc trùng lặp ID. 

Hình ảnh sau đây minh họa trực quan cách một ID duy nhất được sinh ra bằng cơ sở dữ liệu:

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p008_01.png)

* $\text{NewID} = 1$
* $\text{NewID} = 2$
* $\text{NewID} = 3$
* Số lượng thành viên trong nhóm (**Members in the group**) $(m) = 3$
* **Máy chủ cơ sở dữ liệu (Database servers):** A, B, C
* **Máy chủ Web (Web servers)**
  * **Máy chủ dữ liệu A (Dataserver A):** $\text{PrevID} = \text{Null}$, $\text{NewID} = 1$
  * **Máy chủ dữ liệu B (Dataserver B):** $\text{PrevID} = \text{Null}$, $\text{NewID} = 2$
  * **Máy chủ dữ liệu C (Dataserver C):** $\text{PrevID} = \text{Null}$, $\text{NewID} = 3$

### Sinh ID sử dụng giá trị của m (Generating IDs using the value of m)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p008_04.png)

* **1 trên 2 (1 of 2)**

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p009_00.png)

* $\text{NewID} = 4$
* $\text{NewID} = 5$
* $\text{NewID} = 6$
* Số lượng thành viên trong nhóm (**Members in the group**) $(m) = 3$
* Công thức: $\text{NewID} = \text{PrevID} + 3$
* **Máy chủ cơ sở dữ liệu (Database servers):** A, B, C
* **Máy chủ Web (Web servers)**
  * **Máy chủ dữ liệu A (Dataserver A):** $\text{PrevID} = 1$, $\text{NewID} = 4$
  * **Máy chủ dữ liệu B (Dataserver B):** $\text{PrevID} = 2$, $\text{NewID} = 5$
  * **Máy chủ dữ liệu C (Dataserver C):** $\text{PrevID} = 3$, $\text{NewID} = 6$

### Sinh ID sử dụng giá trị của m (Generating IDs using the value of m)
* **2 trên 2 (2 of 2)**

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p009_01.png)

---

### Ưu điểm (Pros)
* Hướng tiếp cận này có khả năng mở rộng (**scalable**). Chúng ta có thể bổ sung thêm máy chủ và giá trị của $m$ sẽ được cập nhật tương ứng.

### Nhược điểm (Cons)
* Mặc dù phương pháp này có khả năng mở rộng ở một mức độ nhất định, nhưng rất khó để mở rộng quy mô trên nhiều trung tâm dữ liệu (**multiple data centers**).
* Tác vụ thêm hoặc xóa một máy chủ có thể dẫn đến việc trùng lặp ID (**duplicate IDs**).
* **Ví dụ:** Giả sử $m = 3$, và máy chủ A sinh các ID duy nhất là 1, 4 và 7. Máy chủ B sinh các ID là 2, 5 và 8, trong khi máy chủ C sinh các ID là 3, 6 và 9. Máy chủ B gặp sự cố ngừng hoạt động (**downtime**). Khi đó, giá trị $m$ được cập nhật thành 2.

Máy chủ A sinh 9 là ID duy nhất tiếp theo của nó, nhưng ID này đã được sinh ra trước đó bởi máy chủ C. Do đó, các ID không còn duy nhất nữa.

Bảng dưới đây nêu bật những hạn chế trong giải pháp của chúng ta. Một hệ thống sinh ID duy nhất không được phép là một điểm lỗi đơn lẻ (**Single Point of Failure - SPOF**). Nó phải có khả năng mở rộng (**Scalability**) và tính sẵn sàng cao (**High Availability**).

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p010_00.png)

### Bảng so sánh các yêu cầu được đáp ứng giữa UUID và Cơ sở dữ liệu (Requirements Filled by UUID versus Using a Database)

| Tiêu chí | Sử dụng UUID (Using UUID) | Sử dụng Cơ sở dữ liệu (Using a database) |
| :--- | :---: | :---: |
| **Tính duy nhất (Unique)** | ✅ | ❌ |
| **Khả năng mở rộng (Scalable)** | ✅ | ❌ |
| **Tính sẵn sàng cao (Available)** | ✅ | ❌ |
| **Mã định danh số 64-bit (64-bit numeric ID)** | ❌ | ✅ |

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p010_02.png)

---

## Giải pháp thứ ba: Sử dụng bộ quản lý dải ID (Third solution: using a range handler)

Hãy thử khắc phục các vấn đề đã được xác định ở các phương pháp trước. Chúng ta có thể sử dụng các dải số (**ranges**) trong một máy chủ trung tâm. Giả sử chúng ta có nhiều dải số từ 1 đến 2 tỷ, chẳng hạn như từ 1 đến 1.000.000; từ 1.000.001 đến 2.000.000; và cứ thế tiếp tục. Trong trường hợp như vậy, một microservice trung tâm có thể cung cấp một dải số cho một máy chủ khi có yêu cầu.

Bất kỳ máy chủ nào cũng có thể đăng ký nhận một dải số (**claim a range**) khi nó cần lần đầu tiên hoặc khi nó đã dùng hết dải số hiện tại. Giả sử một máy chủ đã có một dải số, giờ đây nó sẽ lưu giữ giá trị bắt đầu của dải số trong một biến cục bộ (**local variable**). Bất cứ khi nào có yêu cầu cấp phát ID, nó sẽ cung cấp giá trị của biến cục bộ đó cho bên gửi yêu cầu và tăng giá trị này lên một đơn vị.

> [!NOTE]
> **Ví dụ luồng hoạt động:**  
> Giả sử Máy chủ 1 đăng ký nhận dải số từ **300.001 đến 400.000**. Sau khi đăng ký dải này:
> 1. ID người dùng **300.001** được gán cho yêu cầu đầu tiên.
> 2. Máy chủ sau đó trả về **300.002** cho người dùng tiếp theo, tăng dần vị trí hiện tại của nó trong dải.
> 3. Quá trình này tiếp tục cho đến khi ID người dùng **400.000** được máy chủ phát hành.
> 4. Máy chủ ứng dụng sau đó sẽ truy vấn máy chủ trung tâm để lấy dải khả dụng tiếp theo và lặp lại quy trình này.

Cách tiếp cận này giải quyết triệt để vấn đề trùng lặp ID người dùng. Mỗi máy chủ ứng dụng có thể phản hồi các yêu cầu một cách đồng thời (**concurrently**). Chúng ta có thể thêm một bộ cân bằng tải (**Load Balancer**) phía trên một nhóm máy chủ để giảm tải áp lực từ các yêu cầu.

Chúng ta sử dụng một microservice gọi là **range handler** (bộ quản lý dải ID) có nhiệm vụ theo dõi và ghi nhận toàn bộ các dải số đã được cấp phát và các dải số còn trống (**available ranges**). Trạng thái của từng dải số sẽ xác định xem dải số đó có khả dụng hay không. Trạng thái này — tức là máy chủ nào đang được gán dải số nào — có thể được lưu trữ trên một hệ thống lưu trữ có cơ chế nhân bản dữ liệu (**replicated storage**).

Microservice này có thể trở thành một điểm lỗi đơn lẻ (**SPOF**), nhưng một máy chủ dự phòng chịu lỗi (**failover server**) sẽ đóng vai trò cứu trợ trong trường hợp đó. Máy chủ failover sẽ đảm nhận việc phân phối các dải số khi máy chủ chính gặp sự cố. Chúng ta hoàn toàn có thể khôi phục lại trạng thái của các dải số khả dụng và không khả dụng từ điểm kiểm tra mới nhất (**latest checkpoint**) của kho lưu trữ nhân bản (**replicated store**).

---

### Thiết kế của microservice quản lý dải ID (Design of the range handler microservice)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p011_00.png)

* **Khách hàng (Clients)**
* **Bộ cân bằng tải (Load balancer)**
* **Máy chủ ứng dụng (Application servers)**
* **Microservice quản lý dải ID (Range handler microservice):** duy trì và quản lý các dải khả dụng (maintaining the available ranges)
* **Các máy chủ (Servers)**

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p011_01.png)

---

### Ưu điểm (Pros)
* Hệ thống này có khả năng mở rộng (**scalable**), tính sẵn sàng cao (**available**), và sinh ra các ID người dùng hoàn toàn không bị trùng lặp.
* Hơn nữa, chúng ta có thể duy trì dải số này trong định dạng **64-bit kiểu số (numeric)**.

### Nhược điểm (Cons)
* Chúng ta sẽ bị mất một dải số đáng kể khi một máy chủ gặp sự cố tắt đột ngột (**dies**) và chỉ có thể cấp phát một dải số mới khi máy chủ đó hoạt động trở lại. 
* Chúng ta có thể khắc phục nhược điểm này bằng cách cấp phát các dải số ngắn hơn cho các máy chủ, mặc dù các dải số vẫn cần đủ lớn để phục vụ việc sinh mã định danh trong một khoảng thời gian nhất định.

---

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p011_02.png)

* **Quay lại (Back):** Thiết kế Hệ thống: Bộ Sinh Số Thứ Tự Toàn Cục (System Design: Sequencer)
* **Đánh dấu Đã hoàn thành (Mark As Completed)**
* **Tiếp theo (Next):** ID Duy nhất có Tính Nhân quả (Unique IDs with Causality)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p011_03.png)

---

Bảng sau đây tổng kết những gì mà hướng tiếp cận này đáp ứng cho chúng ta:

### Các yêu cầu được đáp ứng bởi Ba tùy chọn này (Requirements Filled by These Three Options)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p012_00.png)

| Tiêu chí | Sử dụng UUID (Using UUID) | Sử dụng Cơ sở dữ liệu (Using a database) | Sử dụng Bộ quản lý dải ID (Using a range handler) |
| :--- | :---: | :---: | :---: |
| **Tính duy nhất (Unique)** | ✅ | ❌ | ✅ |
| **Khả năng mở rộng (Scalable)** | ✅ | ❌ | ✅ |
| **Tính sẵn sàng cao (Available)** | ✅ | ❌ | ✅ |
| **Mã định danh số 64-bit (64-bit numeric ID)** | ❌ | ✅ | ✅ |

---

Chúng ta đã phát triển một giải pháp cung cấp ID duy nhất, có thể gán cho nhiều sự kiện khác nhau và thậm chí dùng làm khóa chính (**primary key**). 

Nhưng điều gì sẽ xảy ra nếu chúng ta bổ sung thêm một yêu cầu: **ID cũng phải có khả năng sắp xếp theo thời gian (time sortable)**?

---

# Định danh Duy nhất kèm Quan hệ Nhân quả (Unique IDs with Causality)

Tìm hiểu cách sử dụng thời gian để tạo định danh duy nhất (unique ID) đồng thời duy trì quan hệ nhân quả (causality) giữa các sự kiện.

### Chúng ta sẽ tìm hiểu các nội dung sau:
* **Quan hệ nhân quả (Causality)**
* **Sử dụng nhãn thời gian UNIX (Use UNIX time stamps)**
  * Ưu điểm (Pros)
  * Nhược điểm (Cons)
* **Twitter Snowflake**
  * Ưu điểm (Pros)
  * Nhược điểm (Cons)
* **Sử dụng đồng hồ logic (Using logical clocks)**
  * Đồng hồ Lamport (Lamport clocks)
  * Đồng hồ vector (Vector clocks)
* **TrueTime API**
  * Ưu điểm (Pros)
  * Nhược điểm (Cons)
* **Tổng kết (Summary)**

---

## Quan hệ nhân quả (Causality)

Trong bài học trước, chúng ta đã tạo các ID duy nhất (unique IDs) để phân biệt giữa các sự kiện khác nhau. Bên cạnh việc có các định danh duy nhất cho các sự kiện, chúng ta cũng quan tâm đến việc xác định trình tự (sequence) của các sự kiện này. 

Hãy xem xét một ví dụ trong đó Peter và John là hai người dùng Twitter:
* John đăng một bình luận (**sự kiện A** - event A).
* Peter trả lời bình luận của John (**sự kiện B** - event B). 

Sự kiện B phụ thuộc vào sự kiện A và không thể xảy ra trước sự kiện A. Ở đây, các sự kiện này **không đồng thời (nonconcurrent)**.

Chúng ta cũng có thể có các **sự kiện đồng thời (concurrent events)** — nghĩa là hai sự kiện diễn ra độc lập với nhau. Ví dụ: nếu Peter và John bình luận trên hai Tweet khác nhau, thì không có quan hệ "xảy ra trước" (happened-before relationship) hoặc quan hệ nhân quả (causality) nào giữa chúng. Việc xác định sự phụ thuộc của một sự kiện này vào sự kiện khác là điều cốt yếu, nhưng điều này không áp dụng trong trường hợp các sự kiện đồng thời.

> [!NOTE]
> Kịch bản được mô tả ở trên cũng có thể được xử lý bằng cách gán một ID duy nhất và mã hóa sự phụ thuộc của các sự kiện bằng đồ thị xã hội (social graph). Chúng ta cũng có thể sử dụng một cấu trúc dữ liệu thời gian riêng biệt kết hợp với một ID duy nhất đơn giản. Tuy nhiên, chúng ta muốn một ID duy nhất phải đảm nhiệm **nhiệm vụ kép (double duty)** — vừa cung cấp khả năng định danh duy nhất, vừa hỗ trợ duy trì quan hệ nhân quả (causality) của các sự kiện.

---

### Trực quan hóa các sự kiện đồng thời và không đồng thời (Visualization of concurrent and nonconcurrent events)

#### Các sự kiện không đồng thời (Nonconcurrent events)

* **Slide 1/5:**
  * **TA1** (`@ta1`): *"Here is our first post"* (11:44 AM · Jan 20, 2022 · 5 Likes · Twitter for iPhone)

* **Slide 2/5:**
  * John viết một bình luận (*John writes a comment*): Nhập phản hồi ("tweet your reply" / "Reply").

* **Slide 3/5:**
  * John đã thêm một bình luận (*John added a comment*): 
  * Bài đăng của **TA1** hiển thị thêm bình luận: *"Comment from john"* (5 Likes, 1 Reply).

* **Slide 4/5:**
  * Peter trả lời bình luận của John (*Peter replies to John's comment*): 
  * Dưới bình luận *"Comment from john"*, hiển thị phản hồi của Peter (2 phút trước, 2 tương tác, 1 like).

---

#### Các sự kiện đồng thời (Concurrent events)

* **Slide 5/5:**
  * **TA2** (`@ta2`): *"Here is our second post"* (11:44 AM · Jan 20, 2022 · 5 Likes · Twitter for iPhone) $\rightarrow$ **John thêm bình luận vào bài đăng của TA2** (*John adds comment on TA2's post*).
  * **TA3** (`@ta3`): *"Here is our third post"* (11:44 AM · Jan 20, 2022 · 5 Likes · Twitter for iPhone) $\rightarrow$ **Peter thêm bình luận vào bài đăng của TA3** (*Peter adds comment on TA3's post*).
  * Hai sự kiện này diễn ra độc lập, không có quan hệ nhân quả trực tiếp với nhau.

---

Một số ứng dụng yêu cầu các sự kiện vừa phải có định danh duy nhất vừa phải mang theo bất kỳ thông tin nhân quả (causality information) liên quan nào. Một ví dụ tiêu biểu là việc gán định danh cho các thao tác ghi đồng thời (concurrent writes) của một khóa (key) vào một kho lưu trữ dạng key-value (key-value store) để triển khai chiến lược **ghi sau cùng sẽ thắng (Last-Write-Wins - LWW)**.

Chúng ta có thể sử dụng **đồng hồ logic (logical clocks)** hoặc **đồng hồ vật lý (physical clocks)** để suy luận quan hệ nhân quả. Một số hệ thống có thêm các yêu cầu bổ sung trong đó quan hệ nhân quả của các định danh sự kiện phải ánh xạ chính xác với **thời gian thực tế trên đồng hồ treo tường (wall-clock time)**. Một ví dụ về điều này là một ứng dụng tài chính phải tuân thủ các quy định **MiFID của Châu Âu**. MiFID yêu cầu đồng hồ phải có độ lệch trong phạm vi **100 micro giây (100 microseconds)** so với chuẩn Giờ Phối hợp Quốc tế (**UTC**) để phát hiện các bất thường trong các giao dịch thị trường có khối lượng lớn / tốc độ cao (high-volume/high-speed market trades).

> [!NOTE]
> Có rất nhiều điểm tinh vi và phức tạp liên quan đến đồng hồ logic hoặc đồng hồ vật lý. Chúng ta có thể tham khảo phần nội dung bên dưới có tiêu đề “Thời gian trong một Hệ thống Phân tán” (*Time in a Distributed System*) để ôn lại các khái niệm về thời gian.

Chúng ta sử dụng thời gian để xác định trình tự các sự kiện trong cuộc sống hàng ngày. Ví dụ: nếu Sam tắm lúc 6:00 sáng và ăn sáng lúc 7:00 sáng, chúng ta có thể xác định rằng Sam đã tắm trước khi ăn sáng dựa vào nhãn thời gian (timestamps) của từng sự kiện. Do đó, nhãn thời gian có thể được sử dụng để duy trì quan hệ nhân quả.

---

### Phần ôn tập tùy chọn: Thời gian trong một Hệ thống Phân tán (Optional Revision: Time in a Distributed System)

---

## Sử dụng nhãn thời gian UNIX (Use UNIX time stamps)

Nhãn thời gian UNIX (UNIX timestamps) có độ chi tiết (granularity) đến cấp **mili-giây (millisecond)** và có thể được sử dụng để phân biệt các sự kiện khác nhau. 

Chúng ta thiết lập một máy chủ tạo ID (ID-generating server) có khả năng tạo ra một ID trong một mili-giây. Mọi yêu cầu tạo ID duy nhất đều được định tuyến (routed) đến máy chủ đó; máy chủ này sẽ lấy nhãn thời gian hiện tại và trả về một ID duy nhất. Khả năng tạo một ID theo từng mili-giây cho phép chúng ta sinh ra **1.000 định danh mỗi giây (1,000 IDs/second)**.

Điều này có nghĩa là chúng ta có thể tạo ra số lượng ID trong một ngày là:

$$24\text{ (giờ)} \times 60\text{ (phút/giờ)} \times 60\text{ (giây/phút)} \times 1000\text{ (ID/giây)} = 86.400.000\text{ IDs}$$

Con số này là **ít hơn 1 tỷ ID mỗi ngày (less than a billion per day)**.

> [!NOTE]
> Kết nối tới terminal bên dưới để xem nhãn thời gian UNIX tính bằng mili-giây.

```text
Terminal 1
Terminal
Click to Connect...
```

Hệ thống của chúng ta hoạt động tốt đối với việc tạo ID, nhưng nó đặt ra một vấn đề cốt tử: **Máy chủ tạo ID là một điểm lỗi đơn lẻ (Single Point of Failure - SPOF)**, và chúng ta bắt buộc phải xử lý vấn đề này.

Để giải quyết vấn đề SPOF, chúng ta có thể bổ sung thêm nhiều máy chủ. Mỗi máy chủ sẽ tạo ra một ID duy nhất cho mỗi mili-giây. Để đảm bảo toàn bộ định danh là duy nhất trên toàn hệ thống (globally unique across the system), chúng ta **gắn thêm định danh máy chủ (server ID)** vào cùng với nhãn thời gian UNIX. Sau đó, chúng ta thêm một bộ cân bằng tải (**Load Balancer**) để phân phối lưu lượng truy cập (traffic) một cách hiệu quả hơn. Thiết kế của một bộ tạo ID duy nhất sử dụng nhãn thời gian UNIX được minh họa bên dưới:

---

# 012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)

---

## --- Trang 19 ---

### Sử Dụng Dấu Thời Gian Làm Định Danh (Using the timestamp as an ID)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p019_00.png)

```
. . .
Tập hợp các máy chủ (Set of servers)
├── Server 1
├── Server 2
├── Server 3
└── Server N

Yêu cầu ID duy nhất (Request unique ID) ──► Load Balancer ──► Server 1..N
Trả về ID duy nhất (Return unique ID)   ◄── Load Balancer ◄── Server 1..N
```

#### Ưu điểm (Pros)
Phương pháp này đơn giản, có khả năng mở rộng (**Scalable**), và dễ dàng triển khai. Nó cũng cho phép nhiều máy chủ xử lý các yêu cầu đồng thời (**Concurrent requests**).

#### Nhược điểm (Cons)
Đối với hai sự kiện xảy ra đồng thời (**Concurrent events**), cùng một dấu thời gian (**Timestamp**) sẽ được trả về và cùng một ID có thể bị gán cho cả hai sự kiện đó. Theo cách này, các ID sẽ không còn đảm bảo tính duy nhất (**Unique**) nữa.

---

## --- Trang 20 ---

### Bảng Đối Chiếu Các Yêu Cầu Được Đáp Ứng Bởi Từng Phương Pháp (Requirements Fulfilled by Each Approach)

| Phương pháp tiếp cận | Duy nhất (Unique) | Khả năng mở rộng (Scalable) | Tính sẵn sàng cao (Available) | Định danh dạng số 64-bit (64-bit numeric ID) |
| :--- | :---: | :---: | :---: | :---: |
| **Sử dụng UUID (Using UUID)** | Có | Có | Có | Không |
| **Sử dụng cơ sở dữ liệu (Using a database)** | Có | Không | Không | Có |
| **Sử dụng bộ quản lý dải số (Using a range handler)** | Có | Có | Có | Có |
| **Sử dụng dấu thời gian UNIX (Using UNIX timestamps)** | Yếu (Weak) | Có | Có | Có |

---

### Twitter Snowflake

Hãy thử tối ưu hóa việc sử dụng thời gian một cách hiệu quả. Chúng ta có thể trích một số bit trong tổng số 64 bit mục tiêu để lưu trữ thời gian và các bit còn lại dùng cho các thông tin khác. Dưới đây là sơ đồ tổng quan về việc phân chia bit:

#### Tổng Quan Về Cách Phân Chia Các Bit Trong Twitter Snowflake (Overview of the division of bits in Twitter Snowflake)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p019_01.png)

```
0   0000000000   0000000000   0000000000   0000000000   0   0000000000   0000000000   00
│   └─────────────────────────┬────────────────────────┘   └────┬─────┘   └─────┬────┘
│                         41 bit                               10 bit        12 bit
1 bit dấu              Dấu thời gian                        Worker ID       Số thứ tự
(Sign bit)         (2^41 định danh khả dụng)                              (Sequence)
```

- **Thời gian cạn kiệt dải giá trị (Time to range depletion):**
  $$\frac{2^{41} \text{ định danh}}{365 \text{ (ngày/năm)} \times 24 \text{ (giờ/ngày)} \times 60 \text{ (phút/giờ)} \times 60 \text{ (giây/phút)} \times 1000 \text{ (định danh/giây)}} \approx 69 \text{ Năm}$$

- **Số lượng mã định danh máy chủ (Count of worker IDs):** $2^{10} = 1024$
- **Số lượng tổ hợp số thứ tự (Count of sequence number combinations):** $2^{12} = 4096$

Chi tiết giải thích về việc phân chia các bit như sau:

- **Bit dấu (Sign bit):** Một bit đơn lẻ được chỉ định làm bit dấu, và giá trị của nó sẽ luôn luôn bằng $0$. Điều này giúp toàn bộ số luôn là số dương. Việc này đảm bảo rằng bất kỳ môi trường lập trình nào sử dụng các mã định danh này đều thông dịch chúng dưới dạng số nguyên dương (**Positive integers**).
- **Dấu thời gian (Timestamp):** $41$ bit được phân bổ để lưu mili-giây (milliseconds). Mốc thời gian gốc (**Epoch**) mặc định của Twitter Snowflake sẽ được sử dụng.

---

## --- Trang 21 ---

Giá trị của nó là `1288834974657`, tương đương với ngày **04 tháng 11 năm 2010, lúc 01:42:54 UTC**. Chúng ta có thể khởi tạo mốc thời gian gốc riêng khi hệ thống của chúng ta được triển khai, ví dụ: lấy ngày 01 tháng 01 năm 2022 vào lúc 12 giờ đêm (00:00:00) làm điểm bắt đầu từ số 0 cho Epoch của chúng ta. 

Thời gian tối đa để cạn kiệt dải giá trị này được tính toán dưới đây:

$$\text{Thời gian cạn kiệt dải giá trị} = \frac{2^{41} \text{ định danh}}{365 \text{ (ngày/năm)} \times 24 \text{ (giờ/ngày)} \times 60 \text{ (phút/giờ)} \times 60 \text{ (giây/phút)} \times 1000 \text{ (định danh/giây)}} \approx 69 \text{ năm}$$

Các phép tính trên cho thấy chúng ta có **69 năm** trước khi cần một thuật toán mới để tạo ID. Như chúng ta đã thấy trước đây, nếu chúng ta chỉ có thể tạo ra $1.000$ mã định danh mỗi giây, chúng ta sẽ không thể đạt được mục tiêu $1$ tỷ mã định danh mỗi ngày. Tuy nhiên, hiện tại với đề xuất Snowflake, chúng ta có lượng định danh dồi dào khả dụng khi kết hợp sử dụng Worker ID và số thứ tự cục bộ của máy (**Machine local sequence numbers**).

- **Mã định danh máy chủ (Worker number):** Worker number chiếm $10$ bit. Nó cung cấp cho chúng ta $2^{10} = 1024$ Worker ID. Máy chủ tạo ra ID duy nhất cho các sự kiện của nó sẽ gắn kèm ID này.
- **Số thứ tự (Sequence number):** Sequence number chiếm $12$ bit. Cứ mỗi ID được tạo ra trên máy chủ, số thứ tự sẽ được tăng dần lên một đơn vị. Nó cung cấp cho chúng ta $2^{12} = 4096$ số thứ tự duy nhất. Chúng ta sẽ đặt lại (reset) nó về $0$ khi đạt đến $4096$. Con số này bổ sung một tầng bảo vệ để tránh sự trùng lặp (**Avoid duplication**).

Các slide dưới đây minh họa quá trình chuyển đổi từ dấu thời gian (**Timestamp**) sang giờ UTC:

---

## --- Trang 22 ---

### Slide 1 of 5: Tổng Quan Về Cách Phân Chia Các Bit (Overview of the division of bits)
```
0   0010100100   0011111110   1010011000   1100011011 1   0000001010   0000000000   01
│   └─────────────────────────┬────────────────────────┘   └────┬─────┘   └─────┬────┘
1-bit sign                 41-bit timestamp                  10-bit workerID  12-bit Sequence
```
- **Thời gian cạn kiệt dải giá trị (Time to range depletion):** $\approx 69 \text{ Năm}$
- **Số lượng mã Worker ID (Count of worker IDs):** $2^{10} = 1024$
- **Số lượng tổ hợp Sequence number (Count of sequence number combinations):** $2^{12} = 4096$

---

### Slide 2 of 5: Chuyển Đổi Thời Gian Sang UTC (Convert the time to UTC)
```
0   0010100100   0011111110   1010011000   1100011011 1   0000001010   0000000000   01
    └─────────────────────────┬────────────────────────┘
                       41 bit timestamp
```

---

## --- Trang 23 ---

### Slide 3 of 5: Chuyển Đổi Các Bit Sang Hệ Thập Phân (Convert the bits to decimal)
```
0   0010100100   0011111110   1010011000   1100011011 1   0000001010   0000000000   01
    └─────────────────────────┬────────────────────────┘
                      352721356343 sang thập phân (to decimal)
```

---

### Slide 4 of 5: Chuyển Đổi Giá Trị Thập Phân Sang Epoch (Convert the decimal to epoch)
```
0   0010100100   0011111110   1010011000   1100011011 1   0000001010   0000000000   01
    └─────────────────────────┬────────────────────────┘
                      352721356343 sang thập phân (to decimal)
                   + Twitter epoch 1288834974657
                   = 1641556331000
```

---

## --- Trang 24 ---

### Slide 5 of 5: Chuyển Đổi Mili-giây Sang UTC (Convert milliseconds to UTC)
```
0   0010100100   0011111110   1010011000   1100011011 1   0000001010   0000000000   01
    └─────────────────────────┬────────────────────────┘
                      352721356343 sang thập phân (to decimal)
                   + Twitter epoch 1288834974657
                   = 1641556331000
                   = Jan 07 2022 11:52:11 UTC (Sang thời gian UTC)
```

---

### Ưu điểm (Pros)
Twitter Snowflake sử dụng dấu thời gian (**Timestamp**) làm thành phần đầu tiên. Do đó, các ID này có thể sắp xếp theo thứ tự thời gian (**Time sortable**). Bộ tạo ID này cũng có tính sẵn sàng cao (**Highly available**).

### Nhược điểm (Cons)
Các ID được tạo trong khoảng thời gian chết (**Dead period**) là một vấn đề. Khoảng thời gian chết là khi không có yêu cầu tạo ID nào được gửi đến máy chủ. Những ID này sẽ bị lãng phí vì chúng chiếm dụng không gian định danh (**Identifier space**). Dải giá trị duy nhất khả dụng sẽ bị cạn kiệt sớm hơn dự kiến và tạo ra các khoảng trống (**Gaps**) trong tập hợp ID người dùng toàn cục của chúng ta.

---

### Điểm Cần Suy Ngẫm (Point to Ponder)

---

### --- Trang 25 ---

#### **Câu hỏi (Question)**
Bạn có thể tìm thấy một nhược điểm (shortcoming) khác trong thiết kế được hiển thị ở trên không?

#### **Ẩn câu trả lời (Hide Answer)**
Đồng hồ vật lý (physical clocks) là không đáng tin cậy. Đối với những loại đồng hồ như vậy, sai số có thể lên tới 17 giây mỗi ngày. Nếu chúng ta đo lường thời gian bằng cách sử dụng các đồng hồ này trên một máy chủ, thời gian sẽ bị trôi dạt (drifts away).

Nếu xét trên một máy chủ đơn lẻ (single server), chúng ta sẽ không bị ảnh hưởng bởi hiện tượng trôi dạt thời gian (time drift) này vì tất cả các giao dịch (transactions) đều được xử lý trên cùng một máy chủ. Nhưng trong một môi trường phân tán (distributed environment), các đồng hồ sẽ không thể duy trì trạng thái đồng bộ với nhau.

Do tính chất không đáng tin cậy của việc đo lường thời gian chính xác, bất kể chúng ta có đồng bộ hóa các đồng hồ này với nhau hoặc với các đồng hồ khác bằng các phương pháp đo lường chính xác thường xuyên đến mức nào đi nữa, vẫn sẽ luôn có độ lệch (skew) giữa các đồng hồ khác nhau tham gia vào một hệ thống phân tán (distributed system).

Một điểm yếu khác của hệ thống này là sự phụ thuộc vào thời gian. Giao thức NTP (Network Time Protocol) có thể ảnh hưởng đến hoạt động của hệ thống này. Nếu đồng hồ trên một trong các máy chủ bị trôi 2 giây về phía tương lai, các máy chủ khác sẽ bị chậm hơn 2 giây. Đồng hồ NTP nhận biết được điều đó và tiến hành hiệu chuẩn lại (recalibrates) đồng hồ của nó. Khi đó, tất cả các máy chủ sẽ được căn chỉnh đồng bộ lại. Tuy nhiên, trong quá trình trôi dạt (drifting process) đó, các định danh (IDs) có thể đã được sinh ra cho một thời điểm thậm chí còn chưa diễn ra, và bây giờ chúng ta sẽ có một cặp sự kiện có thể không đồng thời (nonconcurrent events) nhưng lại mang cùng một nhãn thời gian (timestamp). Cuối cùng, tính nhân quả (causality) của các sự kiện của chúng ta sẽ không được duy trì.

> [!NOTE]
> **Ghi chú (Note):** Giao thức NTP (Network Time Protocol) là một giao thức mạng dùng để đồng bộ hóa đồng hồ giữa các hệ thống máy tính qua các mạng dữ liệu chuyển mạch gói (packet-switched) với độ trễ biến thiên (variable-latency data networks). Mục tiêu của NTP là đồng bộ hóa tất cả các máy tính tham gia trong phạm vi vài mili-giây so với Giờ phối hợp quốc tế (Coordinated Universal Time - UTC). Nó giúp giảm thiểu ảnh hưởng của độ trễ mạng biến thiên (variable network latency).

---

### --- Trang 26 ---

Việc có được thời gian chính xác vẫn tiếp tục là một vấn đề nan giải. Chúng ta có thể đọc đồng hồ thời gian trong ngày (time-of-day clock) của một cỗ máy với độ phân giải micro-giây hoặc thậm chí nano-giây. Dù có phép đo độ chi tiết cao (fine-grained measurement) này, các rủi ro từ NTP vẫn tồn tại. Vì chúng ta không thể dựa vào đồng hồ vật lý (physical clocks), hãy đưa đồng hồ logic (logical clocks) vào sử dụng.

Bảng dưới đây cung cấp một cái nhìn tổng quan về các yêu cầu đã được đáp ứng bằng các phương pháp tiếp cận thiết kế khác nhau:

#### **Các yêu cầu được đáp ứng bởi từng phương pháp tiếp cận (Requirements Fulfilled by Each Approach)**

| Phương pháp tiếp cận (Approach) | Tính duy nhất (Unique) | Khả năng mở rộng (Scalable) | Tính sẵn sàng (Available) | Định danh số 64-bit (64-bit numeric ID) |
| :--- | :---: | :---: | :---: | :---: |
| **Sử dụng UUID (Using UUID)** | ✔ | ✔ | ✔ | ❌ |
| **Sử dụng cơ sở dữ liệu (Using a database)** | ✔ | ❌ | ❌ | ✔ |
| **Sử dụng bộ xử lý dải (Using a range handler)** | ✔ | ✔ | ✔ | ✔ |
| **Sử dụng nhãn thời gian UNIX (Using UNIX time stamps)** | ❌ | ❌ | ✔ | ✔ |
| **Sử dụng Twitter Snowflake (Using Twitter Snowflake)** | ✔ | ✔ | ✔ | ✔ (yếu - weak) |
| **Sử dụng đồng hồ logic (Using logical clocks)** | ✔ | ✔ | ✔ | ✔ |

Chúng ta có thể tận dụng đồng hồ logic (logical clocks) (như đồng hồ Lamport và đồng hồ vector - vector clocks), vốn cần các định danh tăng đơn điệu (monotonically increasing identifiers) cho các sự kiện.

#### **Đồng hồ Lamport (Lamport clocks)**
Trong đồng hồ Lamport, mỗi nút (node) sở hữu một bộ đếm (counter) riêng của nó. Tất cả các nút trong hệ thống đều được trang bị một bộ đếm số học bắt đầu từ giá trị 0 khi được kích hoạt lần đầu tiên. Trước khi thực thi một sự kiện, bộ đếm số học sẽ được tăng thêm 1 đơn vị. Thông điệp (message) gửi từ sự kiện này đến một nút khác sẽ mang theo giá trị bộ đếm đó. Khi nút kia nhận được thông điệp, trước tiên nó sẽ cập nhật đồng hồ logic của mình bằng cách lấy giá trị cực đại (maximum) giữa

---

### --- Trang 27 ---

giá trị đồng hồ hiện tại của nó với giá trị được gửi kèm trong thông điệp, sau đó mới thực thi thông điệp.

Đồng hồ Lamport cung cấp một thứ tự bộ phận duy nhất (unique partial ordering) cho các sự kiện bằng cách sử dụng quan hệ xảy ra trước (happened-before relationship). Chúng ta cũng có thể đạt được một thứ tự toàn phần (total ordering) của các sự kiện bằng cách gắn thêm các định danh nút/tiến trình duy nhất (unique node/process identifiers), mặc dù thứ tự như vậy không phải là duy nhất và sẽ thay đổi tùy theo cách gán các định danh nút khác nhau. Tuy nhiên, chúng ta cần lưu ý rằng đồng hồ Lamport không cho phép chúng ta suy luận ra tính nhân quả (causality) ở cấp độ toàn cục (global level). Điều này có nghĩa là chúng ta không thể đơn thuần so sánh hai giá trị đồng hồ trên bất kỳ máy chủ nào để suy luận ra quan hệ xảy ra trước (happened-before relationship). Đồng hồ vector (Vector clocks) khắc phục được nhược điểm này.

#### **Đồng hồ Vector (Vector clocks)**
Đồng hồ vector duy trì lịch sử nhân quả (causal history)—nghĩa là toàn bộ thông tin về các mối quan hệ xảy ra trước (happened-before relationships) của các sự kiện. Do đó, chúng ta phải chọn một cấu trúc dữ liệu (data structure) hiệu quả để lưu trữ lịch sử nhân quả của từng sự kiện.

Hãy xem xét thiết kế được trình bày bên dưới. Chúng ta sẽ tạo ra ID của mình bằng cách ghép nối (concatenating) các thông tin liên quan, tương tự như Twitter Snowflake, với cách phân chia như sau:
* **Bit dấu (Sign bit):** Một bit đơn lẻ được gán làm bit dấu, và giá trị của nó sẽ luôn luôn bằng 0.
* **Đồng hồ vector (Vector clock):** Phần này chiếm 53 bits và chứa các bộ đếm (counters) của từng nút.
* **Số thứ tự máy trạm (Worker number):** Phần này chiếm 10 bits. Nó cung cấp cho chúng ta $2^{10} = 1.024$ ID máy trạm (worker IDs).

Các slide tiếp theo giải thích quy trình sinh ID duy nhất (unique ID generation) sử dụng đồng hồ vector, trong đó các nút A, B và C cùng nằm trong một trung tâm dữ liệu (data center).

> [!NOTE]
> **Ghi chú (Note):** Trong các slide sau, chúng tôi chưa chuyển đổi dữ liệu sang dạng bit để người đọc dễ hiểu hơn. Mẫu định dạng (pattern) mà chúng ta sẽ sử dụng cho ID duy nhất là:
> `[vector-clock][worker-id]`

---

### --- Trang 28 ---

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p028_00.png)

* **Node A**: $C = [0, 0, 0]$
* **Node B**: $C = [0, 0, 0]$
* **Node C**: $C = [0, 0, 0]$

> Hiện tại không có sự kiện nào đang được xử lý (No event is currently in progress)

*Slide 1 / 14 (1 of 14)*

---

### --- Trang 29 ---

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p029_00.png)

* **Node A**: $C = [1, 0, 0]$
* **Node B**: $C = [0, 0, 0]$
* **Node C**: $C = [0, 0, 0]$

* Sự kiện: **A1**
* Giá trị vector: `[1, 0, 0]`
* **ID duy nhất cho A1 (Unique ID for A1):** `[1,0,0][A]`

*Slide 2 / 14 (2 of 14)*

---

### --- Trang 30 ---

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p030_00.png)

* **Node A**: $C = [1, 0, 0]$
* **Node B**: $C = [0, 0, 0]$
* **Node C**: $C = [0, 0, 1]$

* Sự kiện tại Node A: **A1** mang vector `[1, 0, 0]`
* Sự kiện tại Node C: **C1** mang vector `[0, 0, 1]`
* **ID duy nhất cho C1 (Unique ID for C1):** `[0,0,1][C]`

*Slide 3 / 14 (3 of 14)*

---

# 012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)
## Cơ Chế Đồng Hồ Vector (Vector Clocks) & Định Danh Phân Tán (Distributed Unique ID)

---

### --- Trang 31 ---

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p031_00.png)

#### Trạng Thái Các Node (Node States) & Vector Clock:
* **Nút A (Node A):** $C = [1, 0, 0]$
* **Nút B (Node B):** $C = [1, 1, 0]$
* **Nút C (Node C):** $C = [0, 0, 1]$

#### Danh Sách Sự Kiện Đã Ghi Nhận (Recorded Events):
* **Sự kiện A1 (Event A1):** $[1, 0, 0]$
* **Sự kiện B1 (Event B1):** $[1, 1, 0]$
* **Sự kiện C1 (Event C1):** $[0, 0, 1]$

#### Định Danh Duy Nhất Được Tạo (Generated Unique ID):
* **Mã định danh duy nhất cho B1 (Unique ID for B1):** `[1, 1, 0][B]`

> [!NOTE]
> **Tiến trình:** 4 / 14 (4 of 14)

---

### --- Trang 32 ---

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p032_00.png)

#### Trạng Thái Các Node (Node States) & Vector Clock:
* **Nút A (Node A):** $C = [1, 0, 0]$
* **Nút B (Node B):** $C = [1, 1, 0]$
* **Nút C (Node C):** $C = [0, 0, 1]$

#### Danh Sách Sự Kiện Hiện Tại (Current Events):
* **A1:** $[1, 0, 0]$
* **B1:** $[1, 1, 0]$
* **C1:** $[0, 0, 1]$

#### Trạng Thái Cấp Phát Định Danh (ID Assignment Status):
* **Không có mã định danh mới nào cần được cấp phát (No new ID needs to be assigned)**

> [!NOTE]
> **Tiến trình:** 5 / 14 (5 of 14)

---

### --- Trang 33 ---

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p033_00.png)

#### Trạng Thái Các Node (Node States) & Vector Clock:
* **Nút A (Node A):** $C = [1, 0, 0]$
* **Nút B (Node B):** $C = [1, 1, 0]$
* **Nút C (Node C):** $C = [0, 0, 2]$ *(Node C tăng biến đếm cục bộ / local counter)*

#### Danh Sách Sự Kiện Hiện Tại (Current Events):
* **A1:** $[1, 0, 0]$
* **B1:** $[1, 1, 0]$
* **C1:** $[0, 0, 1]$
* **C2:** $[0, 0, 2]$

#### Định Danh Duy Nhất Được Tạo (Generated Unique ID):
* **Mã định danh duy nhất cho C2 (Unique ID for C2):** `[0, 0, 2][C]`

> [!NOTE]
> **Tiến trình:** 6 / 14 (6 of 14)

---

### --- Trang 34 ---

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p034_00.png)

#### Trạng Thái Các Node (Node States) & Vector Clock:
* **Nút A (Node A):** $C = [1, 0, 0]$
* **Nút B (Node B):** $C = [1, 2, 0]$ *(Node B tăng biến đếm cục bộ / local counter)*
* **Nút C (Node C):** $C = [0, 0, 2]$

#### Danh Sách Sự Kiện Hiện Tại (Current Events):
* **A1:** $[1, 0, 0]$
* **B1:** $[1, 1, 0]$
* **B2:** $[1, 2, 0]$
* **C1:** $[0, 0, 1]$
* **C2:** $[0, 0, 2]$

#### Định Danh Duy Nhất Được Tạo (Generated Unique ID):
* **Mã định danh duy nhất cho B2 (Unique ID for B2):** `[1, 2, 0][B]`

> [!NOTE]
> **Tiến trình:** 7 / 14 (7 of 14)

---

### --- Trang 35 ---

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p035_00.png)

#### Trạng Thái Các Node (Node States) & Vector Clock:
* **Nút A (Node A):** $C = [2, 0, 0]$ *(Node A tăng biến đếm cục bộ / local counter)*
* **Nút B (Node B):** $C = [1, 2, 0]$
* **Nút C (Node C):** $C = [0, 0, 2]$

#### Danh Sách Sự Kiện Hiện Tại (Current Events):
* **A1:** $[1, 0, 0]$
* **A2:** $[2, 0, 0]$
* **B1:** $[1, 1, 0]$
* **B2:** $[1, 2, 0]$
* **C1:** $[0, 0, 1]$
* **C2:** $[0, 0, 2]$

#### Định Danh Duy Nhất Được Tạo (Generated Unique ID):
* **Mã định danh duy nhất cho A2 (Unique ID for A2):** `[2, 0, 0][A]`

> [!NOTE]
> **Tiến trình:** 8 / 14 (8 of 14)

---

### --- Trang 36 ---

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p036_00.png)

#### Trạng Thái Các Node (Node States) & Vector Clock:
* **Nút A (Node A):** $C = [2, 0, 0]$
* **Nút B (Node B):** $C = [1, 2, 0]$
* **Nút C (Node C):** $C = [0, 0, 3]$ *(Node C tiếp tục tăng biến đếm cục bộ / local counter)*

#### Danh Sách Sự Kiện Hiện Tại (Current Events):
* **A1:** $[1, 0, 0]$
* **A2:** $[2, 0, 0]$
* **B1:** $[1, 1, 0]$
* **B2:** $[1, 2, 0]$
* **C1:** $[0, 0, 1]$
* **C2:** $[0, 0, 2]$
* **C3:** $[0, 0, 3]$

#### Định Danh Duy Nhất Được Tạo (Generated Unique ID):
* **Mã định danh duy nhất cho C3 (Unique ID for C3):** `[0, 0, 3][C]`

> [!NOTE]
> **Tiến trình:** 9 / 14 (9 of 14)

---

# 012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)

---

## Minh họa Thuật toán Đồng hồ Vector (Vector Clocks) (Tiếp theo)

### Bước 10: Trạng thái Hệ thống sau khi Đồng bộ
Không có định danh (ID) mới nào cần được gán tại thời điểm này. Trạng thái vector clock nội bộ của từng node sau các biến cố trước đó được duy trì.

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p037_00.png)

* **Node A**: $C = [2, 0, 0]$
  * Biến cố $A_1$: $[1, 0, 0]$
  * Biến cố $A_2$: $[2, 0, 0]$
* **Node B**: $C = [1, 2, 0]$
  * Biến cố $B_1$: $[1, 1, 0]$
  * Biến cố $B_2$: $[1, 2, 0]$
* **Node C**: $C = [0, 0, 3]$
  * Biến cố $C_1$: $[0, 0, 1]$
  * Biến cố $C_2$: $[0, 0, 2]$
  * Biến cố $C_3$: $[0, 0, 3]$

> **Không có ID mới nào cần được gán (No new ID needs to be assigned)**  
> *(Trang 10 / 14)*

---

### Bước 11: Biến cố $C_4$ xuất hiện tại Node C
Giả sử Node C nhận được thông tin/thông điệp từ Node B (khi đó mang trạng thái $[1, 1, 0]$) và phát sinh biến cố nội bộ tiếp theo: phần tử vị trí của Node C tăng thêm 1 thành 4, đồng thời hợp nhất tri thức từ Node B.

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p038_00.png)

* **Node A**: $C = [2, 0, 0]$
  * $A_1$: $[1, 0, 0]$
  * $A_2$: $[2, 0, 0]$
* **Node B**: $C = [1, 2, 0]$
  * $B_1$: $[1, 1, 0]$
  * $B_2$: $[1, 2, 0]$
* **Node C**: $C = [1, 1, 4]$
  * $C_1$: $[0, 0, 1]$
  * $C_2$: $[0, 0, 2]$
  * $C_3$: $[0, 0, 3]$
  * $C_4$: $[1, 1, 4]$

> **Định danh duy nhất cho $C_4$ (Unique ID for $C_4$):** `[1, 1, 4][C]`  
> *(Trang 11 / 14)*

---

### Bước 12: Biến cố $C_5$ xuất hiện tại Node C
Node C tiếp tục sinh ra biến cố nội bộ $C_5$. Giá trị bộ đếm cục bộ của Node C tăng từ 4 lên 5.

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p039_00.png)

* **Node A**: $C = [2, 0, 0]$
  * $A_1$: $[1, 0, 0]$
  * $A_2$: $[2, 0, 0]$
* **Node B**: $C = [1, 2, 0]$
  * $B_1$: $[1, 1, 0]$
  * $B_2$: $[1, 2, 0]$
* **Node C**: $C = [1, 1, 5]$
  * $C_1$: $[0, 0, 1]$
  * $C_2$: $[0, 0, 2]$
  * $C_3$: $[0, 0, 3]$
  * $C_4$: $[1, 1, 4]$
  * $C_5$: $[1, 1, 5]$

> **Định danh duy nhất cho $C_5$ (Unique ID for $C_5$):** `[1, 1, 5][C]`  
> *(Trang 12 / 14)*

---

### Bước 13: Biến cố $A_3$ xuất hiện tại Node A
Node A nhận thông điệp mang thông tin trạng thái từ Node C ($[1, 1, 5]$). Node A cập nhật vector clock bằng cách lấy giá trị cực đại từng thành phần $\max(C_A[i], C_{msg}[i])$ và tăng giá trị counter của chính mình ($Node\ A$) lên:
$$\max([2, 0, 0], [1, 1, 5]) = [2, 1, 5] \xrightarrow{+1 \text{ cho Node A}} [3, 1, 5]$$

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p040_00.png)

* **Node A**: $C = [3, 1, 5]$
  * $A_1$: $[1, 0, 0]$
  * $A_2$: $[2, 0, 0]$
  * $A_3$: $[3, 1, 5]$
* **Node B**: $C = [1, 2, 0]$
  * $B_1$: $[1, 1, 0]$
  * $B_2$: $[1, 2, 0]$
* **Node C**: $C = [1, 1, 5]$
  * $C_1$: $[0, 0, 1]$
  * $C_2$: $[0, 0, 2]$
  * $C_3$: $[0, 0, 3]$
  * $C_4$: $[1, 1, 4]$
  * $C_5$: $[1, 1, 5]$

> **Định danh duy nhất cho $A_3$ (Unique ID for $A_3$):** `[3, 1, 5][A]`  
> *(Trang 13 / 14)*

---

### Bước 14: Trạng thái Kết thúc của Kịch bản
Không có ID mới nào cần được gán tại thời điểm này.

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p041_00.png)

* **Node A**: $C = [3, 1, 5]$
  * $A_1$: $[1, 0, 0]$
  * $A_2$: $[2, 0, 0]$
  * $A_3$: $[3, 1, 5]$
* **Node B**: $C = [1, 2, 0]$
  * $B_1$: $[1, 1, 0]$
  * $B_2$: $[1, 2, 0]$
* **Node C**: $C = [1, 1, 5]$
  * $C_1$: $[0, 0, 1]$
  * $C_2$: $[0, 0, 2]$
  * $C_3$: $[0, 0, 3]$
  * $C_4$: $[1, 1, 4]$
  * $C_5$: $[1, 1, 5]$

> **Không có ID mới nào cần được gán (No new ID needs to be assigned)**  
> *(Trang 14 / 14)*

---

### Đánh giá Thuật toán Đồng hồ Vector (Vector Clocks)

Cách tiếp cận của chúng ta với đồng hồ vector hoạt động hiệu quả. Tuy nhiên, để nắm bắt đầy đủ quan hệ nhân quả (Causality), một vector clock phải có kích thước tối thiểu là $n$ phần tử, tương ứng với $n$ node tham gia vào hệ thống. 

Do đó, khi tổng số lượng node tham gia trở nên khổng lồ, vector clocks đòi hỏi một dung lượng lưu trữ (Storage) rất lớn. Một số hệ thống ngày nay, chẳng hạn như các ứng dụng web, coi mỗi trình duyệt (Browser) là một client của hệ thống. Thông tin như vậy làm tăng độ dài của ID lên đáng kể, khiến ID trở nên khó xử lý, lưu trữ, sử dụng và mở rộng (Scale).

> [!WARNING]
> **Hạn chế về Khả năng Mở rộng (Scalability Bottleneck):**  
> Khi kích thước cụm tăng lên hoặc khi xem mỗi client là một thực thể độc lập ($n \to \infty$), chi phí truyền tải metadata qua mạng (Network Overhead) và không gian lưu trữ của Vector Clock sẽ bùng nổ theo cấp số $O(n)$, khiến việc ứng dụng vào các hệ thống quy mô lớn gặp trở ngại nghiêm trọng.

---

## Tổng kết: Các Yêu cầu Kỹ thuật được Đáp ứng bởi Từng Giải pháp (Requirements Fulfilled by Each Approach)

Bảng đối chiếu toàn diện giữa các kiến trúc sinh định danh duy nhất phân tán dựa trên các tiêu chí: **Duy nhất (Unique)**, **Khả năng mở rộng (Scalable)**, **Độ sẵn sàng (Available)**, và **Định danh số 64-bit (64-bit numeric ID)**:

| Phương pháp Tiếp cận (Approach) | Duy nhất (Unique) | Khả năng mở rộng (Scalable) | Độ sẵn sàng (Available) | Định danh số 64-bit (64-bit numeric ID) |
| :--- | :---: | :---: | :---: | :---: |
| **Sử dụng UUID (Using UUID)** | ✔ | ✔ | ✔ | ❌ |
| **Sử dụng Cơ sở dữ liệu (Using a database)** | ✔ | ❌ | ❌ | ✔ |
| **Sử dụng Bộ xử lý dải (Using a range handler)** | ✔ | ✔ | ✔ | ✔ |
| **Sử dụng Nhãn thời gian UNIX (Using UNIX timestamps)** | ❌ *(Yếu - weak)* | ✔ | ✔ | ✔ |
| **Sử dụng Twitter Snowflake (Using Twitter Snowflake)** | ✔ | ✔ | ✔ | ✔ |
| **Sử dụng Đồng hồ Vector (Using vector clocks)** | ✔ | ❌ *(Yếu - weak)* | ✔ | ❌ *(Có thể vượt quá 64-bit - can exceed)* |

---

## Điểm Cần Suy Ngẫm (Point to Ponder)

> [!IMPORTANT]
> ### Câu hỏi (Question)
> **Liệu một đồng hồ toàn cục (Global Clock) có thể giúp giải quyết bài toán của chúng ta hay không?**  
> *(Would a global clock help solve our problem?)*

---

# Thiết Kế Hệ Thống: Bộ Sinh Số Thứ Tự Toàn Cục & Đồng Hồ Toàn Cục (TrueTime API)

### Ẩn Câu Trả Lời (Hide Answer)

Vì chúng ta không có một **đồng hồ toàn cục (Global Clock)**, ngay cả khi mỗi nút (node) có thể gán các **nhãn thời gian duy nhất (unique timestamps)** cho các sự kiện đang diễn ra, các nhãn thời gian này vẫn sẽ đến từ các đồng hồ vận hành ở tốc độ khác nhau (**clock drift / skew**). Điều này khiến việc so sánh chúng trở nên khó khăn hơn, và chúng cũng sẽ không đảm bảo tính duy nhất.

Tuy nhiên, nếu chúng ta sở hữu một đồng hồ toàn cục có khả năng cung cấp thời gian theo yêu cầu và luôn đạt độ chính xác tuyệt đối, chúng ta có thể duy trì **tính quan hệ nhân quả của các sự kiện (causality of events)**, cũng như tạo ra một **định danh duy nhất (Unique ID)**. Một chiếc đồng hồ như vậy sẽ mang lại giá trị vô cùng to lớn, nhưng xử lý thời gian trong các hệ thống phân tán (**distributed systems**) luôn là một bài toán cực kỳ phức tạp.

---

### Giao Diện Lập Trình TrueTime (TrueTime API)

**TrueTime API** của Google trong cơ sở dữ liệu Spanner là một lựa chọn hết sức thú vị. Thay vì trả về một mốc thời gian cụ thể duy nhất, nó báo cáo một **khoảng thời gian (time interval)**. Khi truy vấn thời gian hiện tại, chúng ta nhận về hai giá trị: giá trị sớm nhất và giá trị muộn nhất. Đây chính là các nhãn thời gian sớm nhất có thể và muộn nhất có thể:

$$[\text{earliest}, \text{latest}] = [\text{now} - \epsilon, \text{now} + \epsilon]$$

Dựa trên các tính toán về độ không chắc chắn (**uncertainty calculations**), đồng hồ biết rằng thời gian thực tế hiện tại chắc chắn nằm ở một vị trí nào đó bên trong khoảng thời gian đó. Độ rộng của khoảng thời gian này phụ thuộc vào nhiều yếu tố, trong đó có khoảng thời gian trôi qua kể từ lần cuối cùng đồng hồ thạch anh cục bộ (**local quartz clock**) được đồng bộ hóa với một nguồn đồng hồ có độ chính xác cao hơn.

Google triển khai một bộ thu tín hiệu GPS (**GPS receiver**) hoặc một **đồng hồ nguyên tử (atomic clock)** tại mỗi trung tâm dữ liệu (**Data Center - DC**), và các đồng hồ được đồng bộ hóa trong phạm vi sai số khoảng $7\text{ ms}$. Điều này cho phép Spanner giữ mức độ không chắc chắn của đồng hồ (**clock uncertainty**) ở mức tối thiểu. Độ không chắc chắn của khoảng thời gian được biểu diễn dưới dạng ký hiệu **epsilon ($\epsilon$)**.

Các slide trực quan hóa dưới đây giải thích cách thức các máy chủ quản lý thời gian gốc (**time master servers**) của TrueTime hoạt động cùng với GPS và đồng hồ nguyên tử trên nhiều trung tâm dữ liệu.

---

### Kiến Trúc Time Master Trên Các Data Center

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p044_00.png)

* **GPS time master**: Máy chủ thời gian chuẩn GPS
* **Atomic clock time master**: Máy chủ thời gian chuẩn đồng hồ nguyên tử
* **Data center 1, Data center 2, Data center N**: Trung tâm dữ liệu 1, Trung tâm dữ liệu 2, Trung tâm dữ liệu N...

> [!NOTE]
> Trong mỗi trung tâm dữ liệu, chúng ta đều có các bộ xử lý thời gian (**time handlers**). Các máy chủ **GPS timemaster** được gắn kèm các bộ thu GPS, và một số ít trong số chúng được trang bị **đồng hồ nguyên tử (atomic clocks)**.  
> *(1 trên 5)*

Các slide tiếp theo giải thích cách tính toán thời gian khi máy khách (**client**) gửi yêu cầu lấy thời gian từ TrueTime.

---

### Cơ Chế Tính Toán Epsilon ($\epsilon$) Và Trôi Dạt Đồng Hồ (Clock Drift)

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p044_01.png)

#### Các Thông Số & Công Thức Tính Toán:
* **Reference uncertainty** (Độ không chắc chắn tham chiếu): $+6\text{ ms}$
* **Trục thời gian (Time)**: $0\text{ sec}$, $30\text{ sec}$, $60\text{ sec}$, $90\text{ sec}$
* **Tốc độ trôi dạt tối đa của đồng hồ (Clock drift rate)**: $200\text{ }\mu\text{s/sec}$ (microgiây trên mỗi giây)
* **Công thức xác định thời gian hiện tại:**
  $$\text{now} = \text{reference now} + \text{local-clock offset}$$
  *(Thời gian hiện tại = Thời gian tham chiếu hiện tại + Độ lệch đồng hồ cục bộ)*
* **Công thức xác định độ không chắc chắn $\epsilon$:**
  $$\epsilon = \text{reference } \epsilon + \text{worst-case local-clock drift}$$
  *($\epsilon$ = $\epsilon$ tham chiếu + Độ trôi dạt đồng hồ cục bộ trong trường hợp xấu nhất)*

---

#### 1. Trước khi Client yêu cầu TrueTime
* Trạng thái thiết lập ban đầu trước khi phát sinh truy vấn thời gian.  
*(1 trên 7)*

#### 2. Tính toán Epsilon tại thời điểm 0 giây ($0\text{ sec}$)
* Xác định giá trị $\epsilon$ gốc tại mốc bắt đầu chu kỳ đồng bộ.  
*(2 trên 7)*

#### 3. Giả định về độ trôi dạt đồng hồ
* Chúng ta giả định rằng đồng hồ trôi dạt tối đa là **$200\text{ microsecond}$ mỗi giây ($200\text{ }\mu\text{s/sec}$)**. 
* Điều này đồng nghĩa với việc chúng ta sẽ cộng thêm xấp xỉ **$6\text{ millisecond (ms)}$** vào giá trị của epsilon ($\epsilon$) trong khoảng thời gian **$30\text{ giây}$** ($200\text{ }\mu\text{s} \times 30 = 6000\text{ }\mu\text{s} = 6\text{ ms}$).  
*(3 trên 7)*

#### 4. Tính toán Epsilon tại mốc 30 giây ($30\text{ sec}$)
* Độ không chắc chắn $\epsilon$ tích lũy thêm $+6\text{ ms}$ sau 30 giây hoạt động của đồng hồ cục bộ.  
*(4 trên 7)*

#### 5. Chu kỳ giao tiếp với Time Master
> [!IMPORTANT]
> Trong $30\text{ giây}$ tiếp theo, chúng ta giao tiếp với **time master** khi độ không chắc chắn tham chiếu được tính toán, và nó tiếp tục gia tăng với tốc độ $200\text{ microsecond}$ mỗi giây.  
> *(5 trên 7)*

#### 6. Tính toán Epsilon tại mốc 60 giây ($60\text{ sec}$)
* Tái tính toán và cập nhật giá trị epsilon $\epsilon$ tại mốc 60 giây khi chu kỳ đo lường và đồng bộ tiếp tục diễn ra.  
*(6 trên 7)*

---

# Thiết Kế Bộ Sinh Mã Định Danh Duy Nhất Toàn Cục (Design of a Unique ID Generator)

---

### Phân Tích Độ Bất Định Của Đồng Hồ (Clock Uncertainty Analysis)

```
+ 6 ms
30 sec
60 sec
90 sec
0 sec
200 µs/sec
now = reference now + local-clock offset
ε = reference ε + worst-case local-clock drift
Reference uncertainty
Time
```

Nhắc lại một lần nữa, **độ bất định tham chiếu được tính toán (computed reference uncertainty)** tăng lên với tốc độ **$200\text{ }\mu\text{s/giây}$** ($200\text{ microseconds per second}$).

**7 trên 7**

Spanner đảm bảo rằng nếu hai khoảng tin cậy (confidence intervals) không chồng lấn lên nhau (nghĩa là: $A_{earliest} < A_{latest} < B_{earliest} < B_{latest}$), thì sự kiện $B$ chắc chắn xảy ra sau sự kiện $A$.

Chúng ta tạo mã định danh duy nhất (unique ID) của mình bằng cách sử dụng các khoảng TrueTime (TrueTime intervals). Giả sử mốc thời gian sớm nhất trong khoảng là $T_E$ ($earliest$), mốc thời gian muộn nhất là $T_L$ ($latest$), và độ bất định là $\varepsilon$ ($uncertainty$). Chúng ta sử dụng $T_E$ tính theo mili-giây (milliseconds) làm **dấu thời gian (timestamp)** trong mã định danh duy nhất của mình.

#### Cấu Trúc Phân Bổ Các Bit Trong Định Danh (Bit Allocation):
* **Dấu thời gian (Timestamp):** Dấu thời gian chiếm **41 bits**. Chúng ta sử dụng $T_E$ làm dấu thời gian.
* **Độ bất định (Uncertainty):** Độ bất định chiếm **4 bits**. Do độ bất định tối đa được công bố là từ $6 \text{–} 10\text{ ms}$, chúng ta sẽ dùng 4 bit để lưu trữ giá trị này.
* **Mã định danh Worker (Worker number / Worker ID):** Thành phần này chiếm **10 bits**. Cung cấp cho chúng ta $2^{10} = 1.024$ mã định danh worker.
* **Số thứ tự (Sequence number):** Thành phần này chiếm **8 bits**. Với mỗi ID được tạo ra trên server, số thứ tự sẽ được tăng dần lên 1 đơn vị. Nó cung cấp cho chúng ta $2^8 = 256$ tổ hợp khả dĩ. Chúng ta sẽ đặt lại giá trị về 0 khi nó chạm mốc 256.

---

### Cơ Chế Sinh ID Phân Tán Bằng TrueTime

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p050_00.png)

*Node B đang tạo mã định danh duy nhất (unique ID) cho sự kiện của nó bằng cách sử dụng TrueTime.*

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p050_01.png)

```
Google Spanner
  ▲                  │
  │ Yêu cầu thời gian│ Trả về TE và TL
  │ (Requests time)  ▼
  └────────────────── Node B ───► Unique ID: TE-ε-C-00000001
Node A              Node B                Node C
```

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p050_02.png)

**Định dạng cho Mã định danh Duy nhất (Format for Unique ID):**
`[Thời gian sớm nhất (Earliest time)] - [Độ bất định (Uncertainty)] - [Mã Node (Node ID)] - [Số thứ tự (Sequence number)]`

![012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](images/topic_012_p050_03.png)

```
[Clients] ──► [Bộ cân bằng tải (Load Balancer)] ──► [Máy chủ ứng dụng (Application Servers)]
```

#### Ưu Điểm (Pros)
* **TrueTime** thỏa mãn toàn bộ các yêu cầu đặt ra.
* Chúng ta có khả năng sinh ra một mã định danh số **64-bit duy nhất trên quy mô toàn cầu (globally unique 64-bit identifier)**.
* Quan hệ nhân quả của các sự kiện (**Causality of events**) được bảo toàn.
* Phương pháp này đảm bảo tính mở rộng quy mô (**Scalable**) và tính sẵn sàng cao (**Highly Available**).

#### Nhược Điểm (Cons)
* Nếu hai khoảng thời gian bị chồng lấn (overlap), chúng ta sẽ không thể chắc chắn $A$ và $B$ xảy ra theo thứ tự nào. Rất có thể chúng là các sự kiện đồng thời (**Concurrent Events**), nhưng không thể đưa ra một sự đảm bảo chắc chắn 100%.
* Ngoài ra, Spanner cực kỳ tốn kém vì nó phải đảm bảo **tính nhất quán dữ liệu mức cao (High Database Consistency)**. Chi phí tài chính (dollar cost) của một hệ thống dạng như Spanner cũng rất cao do đòi hỏi cơ sở hạ tầng phức tạp và hệ thống giám sát chuyên sâu.

---

### Bảng So Sánh Toàn Diện Các Giải Pháp Sinh ID (Comparison Table)

Bảng cập nhật dưới đây cung cấp sự so sánh giữa các thiết kế hệ thống khác nhau dùng để sinh mã định danh duy nhất (Unique ID):

| Phương Pháp Tiếp Cận (Approach) | Duy Nhất (Unique) | Khả Năng Mở Rộng (Scalable) | Tính Sẵn Sàng (Available) | Định Danh Dạng Số 64-bit (64-bit numeric ID) |
| :--- | :---: | :---: | :---: | :---: |
| **Sử dụng UUID (Using UUID)** | Có | Có | Có | Không |
| **Sử dụng Cơ sở dữ liệu (Using a database)** | Có | Không | Không | Có |
| **Sử dụng Bộ xử lý dải (Using a range handler)** | Có | Có | Có | Có |
| **Sử dụng Dấu thời gian UNIX (Using UNIX timestamps)** | Yếu (Weak) | Có | Có | Có |
| **Sử dụng Twitter Snowflake (Using Twitter Snowflake)** | Có | Có | Có | Có |
| **Sử dụng Vector Clocks (Using vector clocks)** | Yếu (Weak) | Có | Có | Có thể vượt quá (Can exceed) |
| **Sử dụng TrueTime (Using TrueTime)** | Có | Có | Có | Có |

---

### Tổng Kết (Summary)

Chúng ta luôn muốn triệt tiêu hoàn toàn tình trạng trùng lặp mã định danh (duplicate identifiers). Hãy thử hình dung điều gì sẽ xảy ra nếu các lệnh thanh toán (payment orders) hoặc đơn đặt hàng (purchase orders) bị tạo trùng lặp.

* **UUID** chỉ cung cấp những bảo đảm mang tính xác suất (probabilistic guarantees) về việc không đụng độ khóa (non-collision).
* Để đạt được các cam kết không đụng độ mang tính tất định (deterministically non-collision), hệ thống có thể cần đến sự đồng thuận (**Consensus**) giữa các thực thể hoặc các kho lưu trữ phân tán khác nhau, cũng như phải đọc từ các kho lưu trữ đã được nhân bản (**Replicated Store**).
* Khi độ dài của khóa (key length) trở nên quá lớn, nó thường làm chậm quá trình cập nhật các bản ghi dữ liệu (tuple updates) trong cơ sở dữ liệu. Do đó, các mã định danh cần phải đủ lớn nhưng không được quá lớn.

> [!IMPORTANT]
> **Vấn đề Bảo Mật & Rò Rỉ Dữ Liệu (Security & Data Leakage):**
> Trong nhiều trường hợp, việc không ai có thể đoán được mã ID tiếp theo là một yêu cầu cực kỳ quan trọng. Nếu không, các sự cố rò rỉ dữ liệu ngoài ý muốn hoàn toàn có thể xảy ra, và đối thủ cạnh tranh của tổ chức có thể biết được có bao nhiêu đơn hàng đã được xử lý trong ngày chỉ đơn giản bằng cách quan sát các mã ID đơn hàng.
> 
> Việc chèn thêm một số lượng bit ngẫu nhiên (random numbers) vào các bit của mã định danh sẽ khiến nó trở nên khó đoán hơn, mặc dù điều này phải đánh đổi bằng một phần chi phí hiệu năng (**Performance Cost**).

* Chúng ta có thể sử dụng các bộ đếm đơn giản (**Simple Counters**) để tạo mã ID duy nhất nếu không muốn liên kết ID với yếu tố thời gian. Việc lấy dấu thời gian (**Fetching Timestamps**) chậm hơn so với các bộ đếm đơn giản, tuy nhiên giải pháp bộ đếm đòi hỏi chúng ta phải lưu trữ các ID đã sinh ra một cách bền vững (**Persistently**). Bộ đếm bắt buộc phải được lưu trữ trong cơ sở dữ liệu. 
* Lưu trữ trong DB cũng kéo theo hàng loạt vấn đề nội tại: bao gồm việc nhiều luồng ghi đồng thời (**Multiple Concurrent Writes**) có thể làm quá tải cơ sở dữ liệu, và cơ sở dữ liệu trở thành một điểm nghẽn chịu lỗi đơn độc (**Single Point of Failure - SPOF**).

> [!WARNING]
> **Vấn Đề Tạo Điểm Nóng (Hotspots) Trong Cơ Sở Dữ Liệu Phân Tán:**
> Đối với một số cơ sở dữ liệu phân tán (Distributed Databases) như Spanner, việc tạo các ID tăng dần hoặc giảm dần đơn điệu (**Monotonically Increasing/Decreasing IDs**) có thể gây tổn hại nghiêm trọng đến hệ thống.
> 
> Google đã đưa ra cảnh báo chính thức: 
> *"Trên thực tế, việc sử dụng các giá trị tăng dần (hoặc giảm dần) đơn điệu làm khóa hàng (row keys) là hành vi đi ngược lại các thực hành tối ưu (best practices) trong Spanner, bởi vì nó sẽ tạo ra các điểm nóng (hotspots) bên trong cơ sở dữ liệu, dẫn đến sự suy giảm hiệu năng nghiêm trọng."*

> [!NOTE]
> **Chi Phí Cho Thứ Tự Toàn Cục (Global Ordering):**
> Việc sắp xếp thứ tự các sự kiện trên quy mô toàn cầu (**Globally ordering events**) là một quy trình cực kỳ tốn kém. Một tính năng vốn dĩ rất nhanh và đơn giản trong cơ sở dữ liệu tập trung (mã ID tự tăng - auto-increment based ID) lại trở nên chậm chạp và phức tạp trong các hệ thống phân tán tương đương do phải đối mặt với các ràng buộc nền tảng cốt lõi (chẳng hạn như thuật toán đồng thuận - **Consensus**, vốn là bài toán vô cùng nan giải giữa các thực thể từ xa).
> 
> Ví dụ, Spanner — một cơ sở dữ liệu phân tán theo vị trí địa lý (geographically distributed database) — đã chỉ ra rằng: *"Nếu một giao dịch đọc-cập nhật (read-update transaction) trên một ô duy nhất (một cột trong một hàng đơn lẻ) có độ trễ (latency) là 10 mili-giây (ms), thì tần suất phát hành giá trị chuỗi tuần tự tối đa trên lý thuyết chỉ đạt 100 giá trị mỗi giây. Con số tối đa này áp dụng cho toàn bộ cơ sở dữ liệu, bất kể số lượng phiên bản ứng dụng client (client application instances) hay số lượng node trong cơ sở dữ liệu có là bao nhiêu. Điều này xảy ra là do một node đơn lẻ sẽ luôn chịu trách nhiệm quản lý một hàng duy nhất."*
> 
> Nếu chúng ta có thể nhượng bộ các yêu cầu về việc sắp xếp thứ tự toàn cục (**Global Orderings**) và các mã định danh không có khoảng trống (**Gapless Identifiers**), chúng ta sẽ có thể thu được nhiều mã định danh hơn trong thời gian ngắn hơn, đồng nghĩa với việc đạt được mức hiệu năng (**Performance**) vượt trội hơn rất nhiều.

---

**Điều Hướng:**
* **Quay Lại (Back):** Thiết Kế Bộ Sinh Mã Định Danh Duy Nhất Toàn Cục (Design of a Unique ID Generator)
* **Đánh Dấu Đã Hoàn Thành (Mark As Completed)**
* **Tiếp Theo (Next):** Thiết Kế Hệ Thống: Giám Sát Phân Tán (System Design: Distributed Monitoring…)


---

[← Bài trước](011-mang-phan-phoi-noi-dung-cdn.md) | [Mục lục](README.md) | [Bài tiếp theo →](013-giam-sat-phan-tan-distributed-monitoring.md)
