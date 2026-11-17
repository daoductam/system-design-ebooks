# 021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)

[← Bài trước](020-kho-luu-tru-blob-store.md) | [Mục lục](README.md) | [Bài tiếp theo →](022-ghi-log-phan-tan-distributed-logging.md)

---


# Thiết Kế Hệ Thống: Công Cụ Tìm Kiếm Phân Tán (System Design: The Distributed Search)

Tìm hiểu cách thức hoạt động của một hệ thống tìm kiếm (Search System) và nắm bắt kế hoạch cấp cao (high-level plan) để thiết kế một hệ thống tìm kiếm phân tán (Distributed Search System).

**Nội dung sẽ bao gồm:**
* Tại sao chúng ta cần một hệ thống tìm kiếm?
* Hệ thống tìm kiếm là gì?
* Chúng ta sẽ thiết kế một hệ thống tìm kiếm phân tán như thế nào?

---

### Tại sao chúng ta cần một hệ thống tìm kiếm?

Ngày nay, chúng ta thấy một thanh tìm kiếm (search bar) trên hầu hết mọi trang web. Chúng ta sử dụng thanh tìm kiếm đó để chọn lọc ra nội dung liên quan từ một lượng nội dung khổng lồ có sẵn trên trang web đó. Một thanh tìm kiếm cho phép chúng ta nhanh chóng tìm thấy những gì mình đang tìm. Ví dụ: có rất nhiều khóa học trên trang web Educative. Nếu không có tính năng tìm kiếm, người dùng sẽ phải cuộn qua nhiều trang và đọc tên của từng khóa học để tìm được khóa học họ cần.

Hãy lấy một ví dụ khác. Có hàng tỷ video được tải lên và lưu trữ trên YouTube. Hãy tưởng tượng nếu YouTube không cung cấp cho chúng ta một thanh tìm kiếm. Làm thế nào để chúng ta tìm thấy một video cụ thể trong số hàng triệu video đã được đăng tải trên YouTube qua nhiều năm? Sẽ mất hàng tháng trời để duyệt qua tất cả các video đó và tìm ra video chúng ta cần. Người dùng sẽ thấy vô cùng khó khăn để tìm thấy thứ họ muốn chỉ bằng cách cuộn chuột xem qua lại.

Internet hiện có hàng tỷ trang web. Mỗi trang web lại có nhiều trang con (web pages) và có vô số nội dung trên từng trang này. Với một lượng nội dung khổng lồ như vậy, Internet trên thực tế sẽ trở nên vô dụng nếu không có các công cụ tìm kiếm (search engines), và người dùng sẽ bị lạc trong một biển dữ liệu không liên quan. Các công cụ tìm kiếm về bản chất là các bộ lọc cho lượng dữ liệu khổng lồ này. Chúng cho phép người dùng nhanh chóng thu thập thông tin thực sự được quan tâm mà không cần phải sàng lọc qua quá nhiều trang web không cần thiết.

Đằng sau mỗi thanh tìm kiếm là cả một **hệ thống tìm kiếm (search system)**.

---

### Hệ thống tìm kiếm là gì?

Một hệ thống tìm kiếm là một hệ thống tiếp nhận đầu vào văn bản, gọi là **truy vấn tìm kiếm (search query)**, từ người dùng và trả về nội dung liên quan trong vài giây hoặc ít hơn. Có ba thành phần chính của một hệ thống tìm kiếm, cụ thể là:

1. **Bộ thu thập dữ liệu (Crawler):** Thu thập nội dung và tạo các tài liệu (documents).
2. **Bộ đánh chỉ mục (Indexer):** Xây dựng một chỉ mục có thể tìm kiếm được (searchable index).
3. **Bộ tìm kiếm (Searcher):** Phản hồi các truy vấn tìm kiếm bằng cách thực thi truy vấn đó trên chỉ mục được tạo bởi bộ đánh chỉ mục (indexer).

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p002_00.png)

> [!NOTE]
> Chúng ta có một chương riêng biệt dành riêng cho việc giải thích thành phần bộ thu thập dữ liệu (crawler). Trong chương này, chúng ta sẽ tập trung vào phần **đánh chỉ mục (indexing)**.

---

### Chúng ta sẽ thiết kế một hệ thống tìm kiếm phân tán như thế nào?

Chúng tôi chia thiết kế của hệ thống tìm kiếm phân tán thành năm bài học:

1. **Yêu cầu (Requirements):** Trong bài học này, chúng ta liệt kê các yêu cầu chức năng (functional requirements) và phi chức năng (non-functional requirements) của một hệ thống tìm kiếm phân tán. Chúng ta cũng ước lượng tài nguyên hệ thống như máy chủ (servers), dung lượng lưu trữ (storage), và băng thông (bandwidth) cần thiết để phục vụ một lượng truy vấn nhất định.
2. **Đánh chỉ mục (Indexing):** Bài học này cung cấp kiến thức nền tảng về quy trình đánh chỉ mục thông qua một ví dụ cụ thể. Sau khi thảo luận về việc lập chỉ mục, chúng ta cũng sẽ xem xét kiến trúc tập trung (centralized architecture) của các hệ thống tìm kiếm phân tán.
3. **Thiết kế ban đầu (Initial design):** Bài học này bao gồm thiết kế cấp cao (high-level design) của hệ thống, giao diện lập trình ứng dụng (API), cùng các chi tiết về quy trình lập chỉ mục và tìm kiếm.
4. **Thiết kế hoàn thiện (Final design):** Trong bài học này, chúng ta đánh giá thiết kế trước đó và cải tiến lại để hệ thống có khả năng mở rộng (scalable) tốt hơn.
5. **Đánh giá (Evaluation):** Bài học này giải thích cách hệ thống tìm kiếm phân tán mà chúng ta thiết kế đáp ứng các yêu cầu đã đặt ra như thế nào.

Hãy bắt đầu bằng việc tìm hiểu các yêu cầu thiết kế một hệ thống tìm kiếm phân tán.

---

# Yêu Cầu Thiết Kế Hệ Thống Tìm Kiếm Phân Tán (Requirements of a Distributed Search System's Design)

Hãy xác định các yêu cầu của một hệ thống tìm kiếm phân tán và phác thảo các tài nguyên mà chúng ta cần.

**Nội dung sẽ bao gồm:**
* Yêu cầu (Requirements)
  * Yêu cầu chức năng (Functional requirements)
  * Yêu cầu phi chức năng (Non-functional requirements)
* Ước lượng tài nguyên (Resource estimation)
  * Ước lượng số lượng máy chủ (Number of servers estimation)
  * Ước lượng dung lượng lưu trữ (Storage estimation)
  * Ước lượng băng thông (Bandwidth estimation)
* Các khối xây dựng (Building blocks) sẽ sử dụng

---

## Yêu cầu (Requirements)

Hãy cùng tìm hiểu các yêu cầu chức năng và phi chức năng của một hệ thống tìm kiếm phân tán.

### Yêu cầu chức năng (Functional requirements)
Dưới đây là yêu cầu chức năng của hệ thống tìm kiếm phân tán:
* **Tìm kiếm (Search):** Người dùng phải nhận được nội dung liên quan dựa trên các truy vấn tìm kiếm của họ.

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p004_00.png)

### Yêu cầu phi chức năng (Non-functional requirements)
Dưới đây là các yêu cầu phi chức năng của hệ thống tìm kiếm phân tán:
* **Tính sẵn sàng cao (Availability):** Hệ thống phải có độ sẵn sàng cao đối với người dùng (Highly Available).
* **Khả năng mở rộng (Scalability):** Hệ thống phải có khả năng mở rộng quy mô cùng với sự gia tăng của khối lượng dữ liệu. Nói cách khác, hệ thống phải có khả năng đánh chỉ mục một lượng dữ liệu rất lớn.
* **Tìm kiếm nhanh trên dữ liệu lớn (Fast search on big data):** Người dùng phải nhận được kết quả nhanh chóng (độ trễ thấp - Low Latency), bất kể lượng nội dung họ đang tìm kiếm lớn đến mức nào.
* **Giảm thiểu chi phí (Reduced cost):** Tổng chi phí xây dựng và vận hành hệ thống tìm kiếm phải ở mức thấp nhất có thể.

---

## Ước lượng tài nguyên (Resource estimation)

Hãy ước lượng tổng số lượng máy chủ (servers), dung lượng lưu trữ (storage) và băng thông (bandwidth) theo yêu cầu của hệ thống tìm kiếm phân tán. Chúng ta sẽ tính toán các con số này dựa trên ví dụ về tính năng tìm kiếm của YouTube.

### Ước lượng số lượng máy chủ (Number of servers estimation)

Để ước lượng số lượng máy chủ, chúng ta cần biết có bao nhiêu người dùng hoạt động hàng ngày (Daily Active Users - DAU) đang sử dụng tính năng tìm kiếm trên YouTube và một máy chủ đơn lẻ của chúng ta có thể xử lý bao nhiêu yêu cầu mỗi giây (Requests Per Second - RPS). Chúng ta giả định các con số như sau:
* Số lượng người dùng hoạt động hàng ngày sử dụng tính năng tìm kiếm: **3 triệu (3,000,000)**.
* Số lượng yêu cầu mà một máy chủ đơn lẻ có thể xử lý: **1,000 RPS**.

Số lượng máy chủ cần thiết được tính theo công thức:

$$\text{Số lượng máy chủ} = \frac{\text{Số lượng người dùng hoạt động}}{\text{Số truy vấn xử lý trên mỗi máy chủ}} = \frac{3,000,000}{1,000} = 3,000 \text{ máy chủ (3K servers)}$$

Nếu 3 triệu người dùng đang tìm kiếm đồng thời, 3 triệu yêu cầu tìm kiếm sẽ được tạo ra tại cùng một thời điểm. Một máy chủ đơn lẻ xử lý 1,000 yêu cầu cùng một lúc. Lấy 3 triệu chia cho 1,000, chúng ta cần **3,000 máy chủ**.

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p005_00.png)

---

### Ước lượng dung lượng lưu trữ (Storage estimation)

Dữ liệu đặc tả (metadata) của mỗi video được lưu trữ trong một tài liệu JSON riêng biệt. Mỗi tài liệu được định danh duy nhất bởi `video_id`. Metadata này chứa tiêu đề video (title), phần mô tả (description), tên kênh (channel name) và bản ghi phụ đề (transcript). Chúng ta giả định các con số sau đây để ước lượng dung lượng lưu trữ cần thiết nhằm đánh chỉ mục cho một video:
* Kích thước của một tài liệu JSON: **200 KB**.
* Số lượng từ khóa hoặc khóa (terms/keys) duy nhất được trích xuất từ một tài liệu JSON: **1,000 terms**.
* Dung lượng lưu trữ cần thiết để thêm một từ khóa vào bảng chỉ mục (index table): **100 Bytes**.

Công thức sau đây được sử dụng để tính toán dung lượng lưu trữ cần thiết nhằm đánh chỉ mục cho một video:

$$\text{Tổng dung lượng / video} = \text{Dung lượng / tài liệu} + (\text{Số từ khóa / tài liệu} \times \text{Dung lượng / từ khóa})$$

$$\text{Tổng dung lượng / video} = 200\text{ KB} + (1,000 \times 100\text{ Bytes}) = 200\text{ KB} + 100,000\text{ Bytes} \approx 200\text{ KB} + 100\text{ KB} = 300\text{ KB}$$

#### Bảng tổng dung lượng lưu trữ cần thiết để đánh chỉ mục một video trên YouTube
| Dung lượng mỗi tài liệu JSON (KB) | Số lượng từ khóa mỗi tài liệu | Dung lượng mỗi từ khóa (Bytes) | Tổng dung lượng mỗi video (KB) |
| :--- | :--- | :--- | :--- |
| 200 | 1000 | 100 | 300 |

Ở bảng trên, chúng ta tính dung lượng lưu trữ cần thiết để đánh chỉ mục một video là **300 KB**. Giả sử rằng trung bình số lượng video được tải lên mỗi ngày trên YouTube là **6,000 video**, hãy tính tổng dung lượng lưu trữ cần thiết để đánh chỉ mục các video được tải lên mỗi ngày. Công thức tính như sau:

$$\text{Tổng dung lượng / ngày} = \text{Số lượng video / ngày} \times \text{Tổng dung lượng / video}$$

$$\text{Tổng dung lượng / ngày} = 6,000 \times 300\text{ KB} = 1,800,000\text{ KB} = 1.8\text{ GB}$$

#### Bảng tổng dung lượng lưu trữ cần thiết để đánh chỉ mục video mỗi ngày trên YouTube
| Số lượng video mỗi ngày | Tổng dung lượng mỗi video (KB) | Tổng dung lượng mỗi ngày (GB) |
| :--- | :--- | :--- |
| 6000 | 300 | 1.8 |

Tổng dung lượng lưu trữ cần thiết để lập chỉ mục cho 6,000 video tải lên mỗi ngày trên YouTube là **1.8 GB**. Yêu cầu lưu trữ này chỉ là ước tính dành riêng cho YouTube. Nhu cầu lưu trữ sẽ tăng lên đáng kể nếu chúng ta cung cấp hệ thống tìm kiếm phân tán dưới dạng một dịch vụ cho nhiều bên thuê (Multi-tenant Distributed Search as a Service).

> [!IMPORTANT]
> **Tóm tắt yêu cầu lưu trữ:**
> Tổng dung lượng lưu trữ cần thiết của hệ thống tìm kiếm phân tán cho các video được tải lên YouTube mỗi ngày $= \mathbf{1.8\text{ GB/ngày}}$.

---

### Ước lượng băng thông (Bandwidth estimation)

Dữ liệu được truyền tải qua lại giữa người dùng và máy chủ trên mỗi yêu cầu tìm kiếm. Chúng ta sẽ ước lượng băng thông cần thiết cho lưu lượng đến (incoming traffic) vào máy chủ và lưu lượng đi (outgoing traffic) từ máy chủ.

Công thức tính băng thông yêu cầu:

$$\text{Tổng băng thông} = \text{Tổng số yêu cầu mỗi giây} \times \text{Kích thước yêu cầu/phản hồi}$$

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p006_00.png)

#### 1. Lưu lượng đến (Incoming traffic)
Để ước lượng băng thông lưu lượng truy cập đến, chúng ta giả định các thông số sau:
* Số lượng yêu cầu tìm kiếm mỗi ngày: **150 triệu (150,000,000)**.
* Kích thước của một truy vấn tìm kiếm (search query size): **100 Bytes**.

Số yêu cầu mỗi giây (RPS):

$$\text{Số yêu cầu mỗi giây} = \frac{150,000,000}{24 \times 3600\text{ giây}} \approx 1,736.11\text{ req/s}$$

Áp dụng công thức tính băng thông cho lưu lượng đến:

$$\text{Băng thông đến} = 1,736.11 \times 100\text{ Bytes} = 173,611\text{ Bytes/s} \approx \frac{173,611 \times 8}{1,000,000}\text{ Mb/s} \approx 1.39\text{ Mb/s}$$

#### Bảng băng thông cần thiết cho các truy vấn tìm kiếm gửi đến mỗi giây
| Số yêu cầu mỗi giây (req/s) | Kích thước truy vấn (Bytes) | Băng thông (Mb/s) |
| :--- | :--- | :--- |
| 1736.11 | 100 | 1.39 |

---

#### 2. Lưu lượng đi (Outgoing traffic)
Lưu lượng đi là phản hồi (response) mà máy chủ trả về cho người dùng tương ứng với yêu cầu tìm kiếm. Chúng ta giả định rằng số lượng video được gợi ý cho một truy vấn tìm kiếm là **80 video**, và một mục gợi ý có kích thước là **50 Bytes**. Danh sách gợi ý bao gồm một danh sách có thứ tự các `video_id`.

Để ước lượng băng thông lưu lượng gửi đi, chúng ta giả định các thông số sau:
* Số lượng yêu cầu tìm kiếm mỗi ngày: **150 triệu**.
* Kích thước phản hồi (Response size): $80 \times 50\text{ Bytes} = \mathbf{4,000\text{ Bytes}}$.

Áp dụng công thức tính băng thông cho lưu lượng đi:

$$\text{Băng thông đi} = 1,736.11 \times 4,000\text{ Bytes} = 6,944,440\text{ Bytes/s} \approx \frac{6,944,440 \times 8}{1,000,000}\text{ Mb/s} \approx 55.56\text{ Mb/s}$$

#### Bảng băng thông cần thiết cho lưu lượng phản hồi gửi đi mỗi giây
| Số yêu cầu mỗi giây (req/s) | Kích thước phản hồi (Bytes) | Băng thông (Mb/s) |
| :--- | :--- | :--- |
| 1736.11 | 4000 | 55.56 |

---

# Thiết Kế Hệ Thống: Công Cụ Tìm Kiếm Phân Tán (The Distributed Search)

---

## Trang 7

**Quay lại (Back)** | **Đánh dấu hoàn thành (Mark As Completed)** | **Tiếp theo (Next)**

### Lập chỉ mục trong Tìm kiếm Phân tán (Indexing in a Distributed Search)

#### Tổng hợp các yêu cầu băng thông (Bandwidth Requirements) của hệ thống tìm kiếm video

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p007_10.png)

* **Băng thông lưu lượng đến (Incoming traffic bandwidth):** `1.39 Mbps`  
* **+**  
* **Băng thông lưu lượng đi (Outgoing traffic bandwidth):** `55.56 Mbps`  
* **=**  
* **Tổng băng thông (Total bandwidth):** `56.95 Mbps`

> [!NOTE]  
> Các yêu cầu về băng thông là tương đối khiêm tốn vì chúng ta đang giả định kết quả trả về ở dạng văn bản (text results). Nhiều dịch vụ tìm kiếm có thể trả về các hình ảnh thu nhỏ (thumbnails) kích thước nhỏ cùng các tệp đa phương tiện (media) khác nhằm nâng cao trải nghiệm trang tìm kiếm. Nhu cầu băng thông trên mỗi trang được chủ đích giữ ở mức thấp để dịch vụ có thể cung cấp kết quả gần với thời gian thực (near real-time) đến máy khách (client).

---

### Các khối xây dựng (Building blocks) sẽ sử dụng

Chúng ta cần một hệ thống lưu trữ phân tán (**Distributed Storage**) trong thiết kế của mình. Do đó, chúng ta có thể sử dụng kho lưu trữ đối tượng nhị phân (**Blob Store**)—một khối xây dựng (building block) đã được thảo luận trước đó—để lưu trữ dữ liệu cần lập chỉ mục cũng như lưu trữ chính bản thân bộ chỉ mục (index). Chúng ta sẽ sử dụng thuật ngữ chung là **"Lưu trữ phân tán" (Distributed Storage)** thay vì thuật ngữ cụ thể **"Kho lưu trữ blob" (Blob Store)**.

* **Lưu trữ phân tán (Distributed storage):** Kho lưu trữ Blob (Blob store)

Để tóm lược lại, chúng ta đã giải thích các yêu cầu của hệ thống tìm kiếm là gì. Chúng ta đã thực hiện các ước tính tài nguyên (resource estimations). Và cuối cùng, chúng ta đã đề cập đến khối xây dựng (building block) sẽ được sử dụng trong bản thiết kế hệ thống tìm kiếm phân tán của mình.

**Chuyển sang bài học tiếp theo (Go to next lesson)**: `Ctrl + >`

---

## Trang 8

# Lập Chỉ Mục trong Tìm Kiếm Phân Tán (Indexing in a Distributed Search)

Tìm hiểu về việc lập chỉ mục (**Indexing**) và ứng dụng của nó trong một công cụ tìm kiếm phân tán (**Distributed Search**).

### Chúng ta sẽ tìm hiểu các nội dung sau:
* **Lập chỉ mục (Indexing)**
* **Xây dựng một bộ chỉ mục có khả năng tìm kiếm (Build a searchable index)**
* **Chỉ mục đảo (Inverted index)**
* **Tìm kiếm từ một chỉ mục đảo (Searching from an inverted index)**
* **Các yếu tố trong thiết kế chỉ mục (Factors of index design)**
* **Lập chỉ mục trên một hệ thống tập trung (Indexing on a centralized system)**

Đầu tiên, chúng ta sẽ mô tả việc lập chỉ mục (**Indexing**) là gì, sau đó chúng ta sẽ tiến tới việc phân tán các chỉ mục (**Distributing Indexes**) trên nhiều nút (nodes).

---

### Lập chỉ mục (Indexing)

**Lập chỉ mục (Indexing)** là quá trình tổ chức và xử lý dữ liệu được thực hiện nhằm hỗ trợ việc truy xuất thông tin một cách nhanh chóng và chính xác.

---

### Xây dựng một bộ chỉ mục có khả năng tìm kiếm (Build a searchable index)

Cách đơn giản nhất để xây dựng một bộ chỉ mục có thể tìm kiếm được là gán một định danh duy nhất (**Unique ID**) cho mỗi tài liệu và lưu trữ nó trong một bảng cơ sở dữ liệu, như được minh họa trong bảng dưới đây. Cột đầu tiên trong bảng là ID của văn bản và cột thứ hai chứa nội dung văn bản từ mỗi tài liệu.

---

## Trang 9

### Bảng Chỉ mục Tài liệu Đơn giản (Simple Document Index)

| ID | Nội dung tài liệu (Document Content) |
| :--- | :--- |
| **1** | Elasticsearch is the distributed and analytics engine that is based on REST APIs. |
| **2** | Elasticsearch is a Lucene library-based search engine. |
| **3** | Elasticsearch is a distributed search and analytics engine built on Apache Lucene. |

Kích thước của bảng đưa ra ở trên sẽ biến thiên phụ thuộc vào số lượng tài liệu mà chúng ta có cũng như dung lượng kích thước của các tài liệu đó. Bảng trên chỉ là một ví dụ minh họa, và nội dung từ mỗi tài liệu chỉ bao gồm một hoặc hai câu. 

Với một ví dụ thực tế ngoài đời thực, nội dung của mỗi tài liệu trong bảng có thể dài nhiều trang. Điều này sẽ khiến bảng dữ liệu của chúng ta trở nên vô cùng lớn. Việc chạy một truy vấn tìm kiếm (search query) trên bộ chỉ mục mức tài liệu (document-level index) đưa ra ở trên không phải là một tiến trình nhanh chóng. Với mỗi yêu cầu tìm kiếm, chúng ta phải duyệt qua (traverse) toàn bộ các tài liệu và đếm số lần xuất hiện của chuỗi tìm kiếm trong từng tài liệu.

> [!NOTE]  
> Đối với tìm kiếm mờ (**Fuzzy Search**), chúng ta còn phải thực hiện các truy vấn khớp mẫu (**Pattern-Matching Queries**) khác nhau. Nhiều chuỗi trong các tài liệu sẽ khớp theo một mức độ nào đó với chuỗi được tìm kiếm. 
> 1. Đầu tiên, chúng ta phải tìm các chuỗi ứng viên duy nhất bằng cách duyệt qua tất cả các tài liệu. 
> 2. Sau đó, chúng ta phải chọn lọc ra chuỗi khớp xấp xỉ nhất trong số các chuỗi này. 
> 3. Chúng ta cũng phải tìm tần suất xuất hiện của chuỗi khớp nhất đó trong từng tài liệu. 
> 
> Điều này đồng nghĩa với việc mỗi truy vấn tìm kiếm sẽ tiêu tốn một lượng thời gian rất lớn.

Thời gian phản hồi (**Response Time**) cho một truy vấn tìm kiếm phụ thuộc vào một vài yếu tố sau:

---

## Trang 10

* **Chiến lược tổ chức dữ liệu** trong cơ sở dữ liệu.
* **Kích thước (Dung lượng)** của dữ liệu.
* **Tốc độ xử lý của CPU và dung lượng bộ nhớ RAM** của cỗ máy được sử dụng để xây dựng chỉ mục và xử lý truy vấn tìm kiếm.

Việc thực thi các truy vấn tìm kiếm trên hàng tỷ tài liệu vốn được lập chỉ mục ở cấp độ tài liệu (document-level indexed) sẽ là một tiến trình chậm chạp, có thể mất nhiều phút, thậm chí là hàng giờ đồng hồ.

Hãy cùng xem xét một kỹ thuật tổ chức và xử lý dữ liệu khác giúp giảm thiểu thời gian tìm kiếm.

---

### Chỉ mục đảo (Inverted index)

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p007_11.png)

Một **Chỉ mục đảo (Inverted Index)** là một cấu trúc dữ liệu tương tự như bảng băm (**HashMap-like data structure**) áp dụng ma trận tài liệu - từ khóa (**Document-Term Matrix**). Thay vì lưu trữ toàn bộ tài liệu nguyên vẹn như ban đầu, nó tiến hành tách các tài liệu thành từng từ riêng lẻ. 

Sau bước này, ma trận tài liệu - từ khóa sẽ xác định các từ duy nhất (unique words) và loại bỏ các từ xuất hiện phổ biến thường gặp như *"to", "they", "the", "is",* v.v. Những từ xuất hiện thường xuyên như vậy được gọi là các từ dừng/từ tố (**Terms**). Ma trận tài liệu - từ khóa duy trì một bộ chỉ mục ở cấp độ từ tố (term-level index) thông qua việc nhận diện các từ duy nhất này và xóa bỏ các từ tố không cần thiết.

Đối với mỗi từ tố (**Term**), bộ chỉ mục sẽ tính toán và thu thập các thông tin sau:
* Danh sách các tài liệu mà từ tố đó xuất hiện.
* Tần suất xuất hiện của từ tố trong từng tài liệu.
* Vị trí của từ tố trong từng tài liệu.

---

## Trang 11

### Bảng Chỉ mục Đảo (Inverted Index)

| Từ tố (Term) | Ánh xạ (Mapping)<br>`( [doc], [freq], [[loc]] )` |
| :--- | :--- |
| **elasticsearch** | `( [1, 2, 3], [1, 1, 1], [[1], [1], [1]] )` |
| **distributed** | `( [1, 3], [1, 1], [[4], [4]] )` |
| **restful** | `( [1], [1], [[5]] )` |
| **search** | `( [1, 2, 3], [1, 1, 1], [[6], [4], [5]] )` |
| **analytics** | `( [1, 3], [1, 1], [[8], [7]] )` |
| **engine** | `( [1, 2, 3], [1, 1, 1], [[9], [5], [8]] )` |
| **heart** | `( [1], [1], [[12]] )` |
| **elastic** | `( [1], [1], [[15]] )` |
| **stack** | `( [1], [1], [[16]] )` |
| **lucene** | `( [2, 3], [1, 1], [[9], [12]] )` |
| **library** | `( [2], [1], [[10]] )` |
| **Apache** | `( [3], [1], [[11]] )` |

Trong bảng phía trên, cột **"Term"** chứa tất cả các từ tố duy nhất được trích xuất từ toàn bộ các tài liệu. Mỗi mục nhập trong cột **"Mapping"** bao gồm ba danh sách:
1. **Một danh sách các tài liệu (`[doc]`)** mà trong đó từ tố xuất hiện.
2. **Một danh sách đếm tần suất (`[freq]`)** xuất hiện của từ tố trong từng tài liệu tương ứng.
3. **Một danh sách hai chiều (`[[loc]]`)** xác định chính xác vị trí của từ tố trong từng tài liệu. Một từ tố có thể xuất hiện nhiều lần trong một tài liệu đơn lẻ, đó chính là lý do vì sao một danh sách hai chiều được sử dụng ở đây.

---

## Trang 12

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p007_12.png)

> [!NOTE]  
> Thay vì các danh sách (lists), các ánh xạ (mappings) cũng có thể tồn tại dưới dạng các bộ dữ liệu (**Tuples**)—chẳng hạn như `doc`, `freq`, và `loc`.

Chỉ mục đảo (**Inverted Index**) là một trong những cơ chế chỉ mục phổ biến nhất được sử dụng trong việc truy xuất tài liệu (**Document Retrieval**). Nó cho phép triển khai hiệu quả các thuật toán tìm kiếm boolean (boolean), tìm kiếm boolean mở rộng (extended boolean), tìm kiếm theo độ tiệm cận/khoảng cách (proximity), xếp hạng mức độ liên quan (relevance) cùng nhiều loại thuật toán tìm kiếm khác.

#### Ưu điểm của việc sử dụng chỉ mục đảo (Advantages of using an inverted index)
* Một chỉ mục đảo hỗ trợ tối đa cho các tác vụ tìm kiếm toàn văn (**Full-Text Search**).
* Một chỉ mục đảo giảm thiểu đáng kể thời gian đếm số lần xuất hiện của một từ trong từng tài liệu tại thời điểm chạy (**Run time**) bởi vì chúng ta đã có sẵn các ánh xạ (mappings) được tạo trước đối với từng từ tố.

#### Nhược điểm của việc sử dụng chỉ mục đảo (Disadvantages of using an inverted index)
* **Tổn hao dung lượng lưu trữ (Storage overhead):** Cần thêm tài nguyên lưu trữ để duy trì bộ chỉ mục đảo song song cùng với các tài liệu gốc. Tuy nhiên, đổi lại chúng ta giảm thiểu được thời gian tìm kiếm.
* **Chi phí bảo trì / cập nhật (Maintenance costs - Processing):** Chi phí xử lý phát sinh khi thêm mới, cập nhật, hoặc xóa một tài liệu. 
  * Để **thêm một tài liệu**, chúng ta phải trích xuất các từ tố từ tài liệu đó. Sau đó, với mỗi từ tố được trích xuất, chúng ta phải thêm một hàng mới vào chỉ mục đảo hoặc cập nhật hàng đã tồn tại nếu từ tố đó đã có mục nhập từ trước. 
  * Tương tự, để **xóa một tài liệu**, chúng ta phải tiến hành xử lý để tìm các mục nhập trong chỉ mục đảo cho các từ tố thuộc tài liệu bị xóa và cập nhật lại chỉ mục đảo tương ứng.

---

### Tìm kiếm từ một chỉ mục đảo (Searching from an inverted index)

Xét một hệ thống có các ánh xạ (mappings) sau đây khi chúng ta thực hiện tìm kiếm cụm từ **“search engine”**:

---

### --- Trang 13 ---

| Thuật ngữ (*Term*) | Ánh xạ (*Mapping*) |
| :--- | :--- |
| **search** | `( [1, 2, 3], [1, 1, 1], [[6], [4], [5]] )` |
| **engine** | `( [1, 2, 3], [1, 1, 1], [[9], [5], [8]] )` |

Cả hai từ này đều được tìm thấy trong các tài liệu (*documents*) 1, 2 và 3. Cả hai từ đều xuất hiện một lần trong mỗi tài liệu.
- Từ **“search”** nằm ở vị trí số 6 trong tài liệu 1, vị trí số 4 trong tài liệu 2, và vị trí số 5 trong tài liệu 3.
- Từ **“engine”** nằm ở vị trí số 9 trong tài liệu 1, vị trí số 5 trong tài liệu 2, và vị trí số 8 trong tài liệu 3.

Một thuật ngữ đơn lẻ có thể xuất hiện trong hàng triệu tài liệu. Do đó, danh sách các tài liệu trả về cho một truy vấn tìm kiếm (*search query*) có thể sẽ rất dài.

> [!NOTE]
> **Câu hỏi (*Question*):** Liệu kỹ thuật này có hoạt động hiệu quả khi có quá nhiều tài liệu được tìm thấy khớp với một thuật ngữ đơn lẻ hay không?
> 
> **Ẩn câu trả lời (*Hide Answer*):**
> Việc trả về tất cả các tài liệu tìm thấy khả năng cao là sẽ không khả thi. Thay vào đó, chúng ta nên sắp xếp (*sort*) chúng dựa trên mức độ liên quan (*relevance*) đối với truy vấn tìm kiếm. Các kết quả hàng đầu (*top results*) nên được trả về cho người dùng thay vì trả về toàn bộ tài liệu.

#### Các yếu tố trong thiết kế chỉ mục (*Factors of index design*)

---

### --- Trang 14 ---

Dưới đây là một số yếu tố mà chúng ta cần lưu ý khi thiết kế một chỉ mục (*index*):

- **Kích thước của chỉ mục (*Size of the index*):** Cần bao nhiêu bộ nhớ máy tính và RAM để lưu giữ chỉ mục. Chúng ta giữ chỉ mục trong RAM nhằm hỗ trợ độ trễ thấp (*low latency*) cho việc tìm kiếm.
- **Tốc độ tìm kiếm (*Search speed*):** Tốc độ tìm kiếm một từ từ một chỉ mục đảo (*inverted index*) nhanh đến mức nào.
- **Bảo trì chỉ mục (*Maintenance of the index*):** Mức độ hiệu quả khi cập nhật chỉ mục nếu chúng ta thêm hoặc xóa một tài liệu.
- **Khả năng chịu lỗi (*Fault tolerance*):** Tầm quan trọng sống còn của việc dịch vụ phải duy trì độ tin cậy (*reliable*). Việc xử lý sự cố hỏng hóc chỉ mục (*index corruption*), hỗ trợ cô lập dữ liệu không hợp lệ (*invalid data isolation*), đối phó với sự cố phần cứng bị lỗi (*defective hardware*), phân vùng dữ liệu (*partitioning*), và sao chép nhân bản (*replication*) đều là các vấn đề cần xem xét ở đây.
- **Khả năng thích ứng / chống chịu (*Resilience*):** Khả năng chống chịu của hệ thống trước những đối tượng cố tình thao túng hệ thống (*game the system*) và phòng ngừa các thủ thuật tối ưu hóa công cụ tìm kiếm (SEO - *search engine optimization schemes*), bởi vì chúng ta chỉ trả về một số lượng nhỏ các kết quả có liên quan cho mỗi lượt tìm kiếm.

Dựa trên các yếu tố thiết kế được liệt kê ở trên, hãy cùng xem xét một số vấn đề khi xây dựng chỉ mục trên một hệ thống tập trung (*centralized system*).

#### Đánh chỉ mục trên một hệ thống tập trung (*Indexing on a centralized system*)

Trong một hệ thống tìm kiếm tập trung, tất cả các thành phần của hệ thống tìm kiếm đều chạy trên một nút (*node*) đơn lẻ có năng lực tính toán khá mạnh. Kiến trúc của một hệ thống tìm kiếm tập trung được thể hiện trong hình minh họa sau:

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p014_00.png)

*Kiến trúc của một hệ thống tìm kiếm tập trung:*
- **Documents to index** *(Tài liệu cần đánh chỉ mục)* $\rightarrow$ **Single server** *(Máy chủ đơn lẻ)*:
  - **Indexing process (batch)** *(Tiến trình đánh chỉ mục - xử lý theo lô)* $\rightarrow$ **Binary file containing inverted index** *(Tệp nhị phân chứa chỉ mục đảo)*.
  - **Query processing** *(Xử lý truy vấn)*: Tiếp nhận **Textual query** *(Truy vấn dạng văn bản)* $\rightarrow$ Đọc tệp nhị phân $\rightarrow$ Trả về **Query result (suggestions)** *(Kết quả truy vấn / gợi ý)*.

Tiến trình đánh chỉ mục (*indexing process*) nhận các tài liệu làm đầu vào và chuyển đổi chúng thành một chỉ mục đảo (*inverted index*), được lưu trữ dưới dạng một tệp nhị phân (*binary file*).

Tiến trình xử lý truy vấn (*query processing*) hoặc tiến trình tìm kiếm sẽ thông dịch tệp nhị phân đó.

---

### --- Trang 15 ---

Nó chứa chỉ mục đảo. Nó cũng tính toán giao điểm (*intersection*) của các danh sách đảo (*inverted lists*) cho một truy vấn nhất định để trả về kết quả tìm kiếm cho truy vấn đó.

Dưới đây là những vấn đề đi kèm với kiến trúc của hệ thống tìm kiếm tập trung:
- **SPOF (*Single Point of Failure* - Điểm lỗi đơn lẻ)**
- **Quá tải máy chủ (*Server overload*)**
- **Kích thước chỉ mục lớn (*Large size of the index*)**

- **SPOF:** Một hệ thống tập trung là một điểm lỗi đơn lẻ. Nếu nó bị sập (*dead*), không có thao tác tìm kiếm nào có thể được thực hiện.
- **Quá tải máy chủ (*Server overload*):** Nếu có quá nhiều người dùng thực hiện các truy vấn và các truy vấn đó phức tạp, điều này sẽ gây áp lực nặng nề lên máy chủ (nút).
- **Kích thước chỉ mục lớn (*Large size of the index*):** Kích thước của chỉ mục đảo tăng lên cùng với số lượng tài liệu, đặt ra các yêu cầu tài nguyên rất lớn đối với một máy chủ đơn lẻ. Hệ thống máy tính càng lớn, chi phí và độ phức tạp trong việc quản lý nó càng cao.

> [!NOTE]
> Với một hệ thống phân tán (*distributed system*), các hệ thống máy tính chi phí thấp (*commodity hardware*) được tận dụng, mang lại hiệu quả cao về mặt chi phí tổng thể.

Một chỉ mục đảo cần phải được nạp vào bộ nhớ chính (*main memory / RAM*) khi thêm một tài liệu hoặc khi thực thi một truy vấn tìm kiếm. Một phần lớn của chỉ mục đảo phải nằm vừa vặn trong RAM của máy tính để đảm bảo hiệu năng.

Theo số liệu phân tích của Google vào năm 2022, có hàng trăm tỷ trang web với tổng kích thước rơi vào khoảng 100 petabytes. Nếu chúng ta xây dựng một hệ thống tìm kiếm cho toàn bộ mạng toàn cầu (*World Wide Web*), kích thước chỉ mục đảo cũng sẽ lên tới hàng petabytes. Điều này đồng nghĩa với việc chúng ta phải nạp hàng petabytes dữ liệu vào RAM. Việc tiếp tục nâng cấp tài nguyên cho một cỗ máy đơn lẻ (*vertical scaling*) để đánh chỉ mục một tỷ trang là điều phi thực tế và kém hiệu quả so với việc chuyển đổi sang một hệ thống phân tán (*distributed system*) và tận dụng sức mạnh của việc xử lý song song (*parallelization*). Chạy một truy vấn tìm kiếm trên một chỉ mục đảo đơn lẻ, khổng lồ sẽ dẫn đến thời gian phản hồi (*response time*) chậm chạp.

---

### --- Trang 16 ---

[Quay lại] **Yêu cầu của một hệ thống tìm kiếm phân tán... (*Requirements of a Distributed Searc…*)**  
[Đánh dấu đã hoàn thành]  
[Tiếp theo] **Thiết kế một hệ thống tìm kiếm phân tán (*Design of a Distributed Search*)**

> [!TIP]
> Tìm kiếm một cuốn sách từ một kệ sách chứa 100 cuốn sách sẽ dễ hơn nhiều so với việc tìm một cuốn sách từ một kệ sách chứa một triệu cuốn. Thời gian tìm kiếm tăng dần theo khối lượng dữ liệu mà chúng ta tìm kiếm trên đó.

Các cuộc tấn công nhắm vào hệ thống chỉ mục tập trung có thể để lại tác động nặng nề hơn so với các cuộc tấn công vào hệ thống chỉ mục phân tán. Hơn nữa, xác suất xảy ra các điểm nghẽn cổ chai (*bottlenecks* - vốn có thể xuất hiện ở băng thông máy chủ hoặc RAM) cũng thấp hơn nhiều trong một chỉ mục phân tán.

Trong bài học này, chúng ta đã tìm hiểu về việc đánh chỉ mục và xem xét các vấn đề của việc đánh chỉ mục trên một hệ thống tập trung. Bài học tiếp theo sẽ giới thiệu giải pháp phân tán cho bài toán đánh chỉ mục.

---

### --- Trang 17 ---

### Thiết kế một hệ thống tìm kiếm phân tán (*Design of a Distributed Search*)

Nắm bắt tổng quan về thiết kế của một hệ thống tìm kiếm phân tán có khả năng xử lý số lượng lớn các truy vấn mỗi giây (QPS - *Queries Per Second*).

**Nội dung sẽ bao gồm:**
- Thiết kế tổng thể (*High-level design*)
- Thiết kế API (*API design*)
- Thảo luận chi tiết (*Detailed discussion*)
- Đánh chỉ mục và tìm kiếm phân tán (*Distributed indexing and searching*)
- Sao chép nhân bản (*Replication*)
- Hệ số nhân bản và phân phối bản sao (*Replication factor and replica distribution*)
- Tổng kết (*Summary*)

#### Thiết kế tổng thể (*High-level design*)

Hãy cùng phác thảo thiết kế tổng thể của một hệ thống tìm kiếm phân tán trước khi đi sâu vào thảo luận chi tiết. Hệ thống như vậy bao gồm hai giai đoạn (*two phases*), như được mô tả trong hình minh họa dưới đây:
1. **Giai đoạn ngoại tuyến (*Offline phase*):** Bao gồm việc thu thập dữ liệu (*data crawling*) và đánh chỉ mục (*indexing*), trong đó người dùng không cần phải thực hiện bất kỳ thao tác nào.
2. **Giai đoạn trực tuyến (*Online phase*):** Bao gồm việc tìm kiếm các kết quả tương ứng với truy vấn tìm kiếm từ người dùng.

---

### --- Trang 18 ---

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p018_00.png)

*Thiết kế tổng thể của một hệ thống tìm kiếm phân tán (*High-level design of a distributed search system*):*

- **Giai đoạn ngoại tuyến (*Offline*):**
  1. **Crawler** *(Bộ thu thập dữ liệu)* thu thập dữ liệu $\rightarrow$ Lưu **Documents** *(Tài liệu)* vào **Distributed storage** *(Lưu trữ phân tán)*.
  2. **Indexer** *(Bộ đánh chỉ mục)* lấy dữ liệu từ **Distributed storage** $\rightarrow$ Sử dụng **Distributed data processing system (MapReduce)** *(Hệ thống xử lý dữ liệu phân tán)* để đánh chỉ mục song song.
  3. Kết quả đánh chỉ mục (dạng bảng **Term - Mapping**) được ghi lại vào **Distributed storage** dưới dạng **Index** *(Chỉ mục)*.

- **Giai đoạn trực tuyến (*Online*):**
  4. Người dùng gửi **Search query** *(Truy vấn tìm kiếm)* đến **Searcher** *(Bộ tìm kiếm)*.
  5. **Searcher** đọc **Index** từ **Distributed storage**, thực hiện tra cứu/tính toán ánh xạ và trả về **Search results** *(Kết quả tìm kiếm)* cho người dùng.

Chi tiết hoạt động của các thành phần:
- **Crawler (*Bộ thu thập dữ liệu*):** Thu thập nội dung từ tài nguyên đích. Ví dụ: nếu chúng ta xây dựng tính năng tìm kiếm cho ứng dụng YouTube, crawler sẽ thu thập dữ liệu qua tất cả các video trên YouTube và trích xuất nội dung văn bản cho từng video. Nội dung có thể là tiêu đề video, phần mô tả, tên kênh, hoặc thậm chí là các chú thích (*annotations*) của video nhằm kích hoạt khả năng tìm kiếm thông minh không chỉ dựa trên tiêu đề và mô tả mà còn dựa trên chính nội dung của video đó. Crawler định dạng nội dung đã trích xuất của mỗi video thành một tài liệu JSON (*JSON document*) và lưu trữ các tài liệu JSON này vào kho lưu trữ phân tán (*distributed storage*).
- **Indexer (*Bộ đánh chỉ mục*):** Lấy các tài liệu từ kho lưu trữ phân tán và đánh chỉ mục các tài liệu này bằng MapReduce - chạy trên một cụm phân tán gồm các máy tính phần cứng thông dụng (*distributed cluster of commodity machines*). Indexer sử dụng một hệ thống xử lý dữ liệu phân tán như MapReduce để xây dựng chỉ mục song song và phân tán. Bảng chỉ mục sau khi được xây dựng sẽ được lưu trữ vào kho lưu trữ phân tán.
- **Distributed storage (*Lưu trữ phân tán*):** Được sử dụng để lưu trữ các tài liệu (*documents*) và chỉ mục (*index*).
- **Searcher (*Bộ tìm kiếm*):** Người dùng nhập chuỗi tìm kiếm chứa nhiều từ vào... *(văn bản tiếp tục ở trang sau)*

---

# HỆ THỐNG TÌM KIẾM PHÂN TÁN (DISTRIBUTED SEARCH SYSTEM)

---

### Thanh tìm kiếm (Search Bar)
Bộ tìm kiếm (**Searcher**) tiến hành phân tích cú pháp (parse) chuỗi tìm kiếm, tra cứu các ánh xạ từ chỉ mục (**Index**) được lưu trữ trong hệ thống lưu trữ phân tán (**Distributed Storage**), và trả về các kết quả khớp nhất cho người dùng. Bộ tìm kiếm có khả năng ánh xạ thông minh các từ viết sai chính tả trong chuỗi tìm kiếm về các từ vựng gần nhất trong từ điển (**Vocabulary words**). Nó cũng tìm kiếm các tài liệu chứa tất cả các từ khóa và thực hiện xếp hạng (**Ranking**) chúng.

---

### Thiết kế API (API Design)

Vì người dùng chỉ gửi các yêu cầu dưới dạng một chuỗi văn bản (string), thiết kế API khá đơn giản.

**Tìm kiếm (Search):** Hàm tìm kiếm được thực thi khi người dùng truy vấn hệ thống để tìm kiếm một nội dung nào đó.

```
search(query)
```

| Tham số (Parameter) | Mô tả (Description) |
| :--- | :--- |
| `query` | Đây là truy vấn dạng văn bản do người dùng nhập vào thanh tìm kiếm, dựa vào đó nội dung phù hợp sẽ được tìm thấy. |

---

### Thảo luận chi tiết (Detailed Discussion)

Vì bộ đánh chỉ mục (**Indexer**) là thành phần cốt lõi trong một hệ thống tìm kiếm, chúng ta đã thảo luận về kỹ thuật đánh chỉ mục cũng như các vấn đề liên quan đến việc đánh chỉ mục tập trung (**Centralized Indexing**) ở bài học trước. Trong bài học này, chúng ta sẽ xem xét một giải pháp phân tán (**Distributed Solution**) cho việc đánh chỉ mục và tìm kiếm.

---

### Đánh chỉ mục và Tìm kiếm phân tán (Distributed Indexing and Searching)

Hãy xem cách chúng ta có thể phát triển một hệ thống đánh chỉ mục và tìm kiếm phân tán. Chúng ta hiểu rằng đầu vào của một hệ thống đánh chỉ mục là các tài liệu được tạo ra trong quá trình thu thập dữ liệu web (**Web Crawling**). Để xây dựng một chỉ mục theo phương thức phân tán, chúng ta sử dụng một lượng lớn các máy tính chi phí thấp (các node) và phân vùng (**Partition**) hoặc chia nhỏ các tài liệu dựa trên tài nguyên sẵn có của chúng. Tất cả các node đều được kết nối với nhau. Một nhóm các node được gọi là một cụm (**Cluster**).

> [!TIP]
> **Mẹo triển khai (Tip):**  
> Để thực hiện đánh chỉ mục phân tán, các máy tính trong cụm thường sở hữu bộ vi xử lý x86 lõi kép chạy Linux, với bộ nhớ RAM từ 2–4 GB trên mỗi máy. Không nhất thiết tất cả các máy phải có cùng cấu hình phần cứng, tuy nhiên hiệu năng của chúng nên tương đương nhau ở mức độ nhất định. Khung làm việc **MapReduce** đủ thông minh để phân bổ khối lượng công việc nhiều hơn cho các máy mạnh hơn.

Chúng ta sử dụng vô số các node nhỏ phục vụ cho việc đánh chỉ mục nhằm đạt được hiệu quả về mặt chi phí (**Cost Efficiency**). Quá trình này đòi hỏi chúng ta phải phân vùng (**Partition**) hoặc chia tách dữ liệu đầu vào (các tài liệu) giữa các node này. Tuy nhiên, một câu hỏi then chốt cần được giải quyết: **Làm thế nào để chúng ta thực hiện việc phân vùng này?**

Hai kỹ thuật phổ biến nhất được sử dụng để phân vùng dữ liệu (**Data Partitioning**) trong đánh chỉ mục phân tán bao gồm:

1. **Phân vùng theo tài liệu (Document Partitioning):** Trong phân vùng theo tài liệu, toàn bộ các tài liệu được thu thập bởi trình thu thập web (**Web Crawler**) được phân chia thành các tập hợp con tài liệu. Mỗi node sau đó sẽ thực hiện đánh chỉ mục trên tập hợp con tài liệu được chỉ định cho nó.
2. **Phân vùng theo thuật ngữ (Term Partitioning):** Từ điển gồm tất cả các thuật ngữ (terms) được phân chia thành các tập hợp con, với mỗi tập hợp con cư trú tại một node duy nhất. Ví dụ: một tập hợp con tài liệu chứa thuật ngữ *"search"* sẽ được xử lý và đánh chỉ mục bởi một node cụ thể.

---

### Các kiểu phân vùng dữ liệu trong tìm kiếm phân tán (Types of Data Partitioning in a Distributed Search)

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p021_00.png)

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p021_01.png)

Trong **Phân vùng theo thuật ngữ (Term Partitioning)**, một truy vấn tìm kiếm sẽ được gửi đến các node tương ứng với các thuật ngữ trong truy vấn. Điều này mang lại mức độ đồng thời (**Concurrency**) cao hơn vì một luồng các truy vấn tìm kiếm với các thuật ngữ khác nhau sẽ được phục vụ bởi các node khác nhau. Tuy nhiên, phân vùng theo thuật ngữ lại là một bài toán rất phức tạp trong thực tế. Các truy vấn đa từ (multiword queries) đòi hỏi phải truyền các danh sách ánh xạ (**Mapping Lists**) dài giữa các nhóm node để thực hiện hợp nhất (**Merging**), điều này có thể gây tốn kém chi phí tài nguyên mạng vượt quá lợi ích mang lại từ việc tăng tính đồng thời.

Trong **Phân vùng theo tài liệu (Document Partitioning)**, mỗi truy vấn được phân phối tới tất cả các node, và kết quả từ các node này được hợp nhất lại trước khi hiển thị cho người dùng. Phương pháp phân vùng này đòi hỏi ít giao tiếp giữa các node (**Inter-node Communication**) hơn. Trong thiết kế của chúng ta, chúng ta sử dụng **Document Partitioning**.

Tuân theo phương pháp phân vùng theo tài liệu, hãy cùng xem xét một thiết kế phân tán cho việc xây dựng chỉ mục và truy vấn, như được minh họa ở sơ đồ bên dưới. Chúng ta sử dụng một cụm gồm nhiều node chi phí thấp và một bộ quản lý cụm (**Cluster Manager**). Bộ quản lý cụm sử dụng mô hình lập trình **MapReduce** để song song hóa quá trình tính toán chỉ mục trên từng phân vùng. MapReduce có thể xử lý các tập dữ liệu lớn hơn đáng kể mà một máy chủ lớn đơn lẻ rất khó có thể đảm đương.

---

### Đánh chỉ mục và Tìm kiếm phân tán song song trên nhiều node trong cụm máy chủ thương mại (Commodity Machines)

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p022_00.png)

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p022_01.png)

Hệ thống được mô tả ở trên hoạt động như sau:

#### Quá trình đánh chỉ mục (Indexing)
* Chúng ta đã có một tập hợp tài liệu được thu thập từ trước bởi trình thu thập dữ liệu (**Crawler**).
* Bộ quản lý cụm (**Cluster Manager**) chia tách tập tài liệu đầu vào thành $N$ phân vùng (**Partitions**), trong đó $N = 3$ như trong hình minh họa ở trên. Kích thước của mỗi phân vùng do bộ quản lý cụm quyết định dựa trên quy mô dữ liệu, năng lực tính toán, giới hạn bộ nhớ (**Memory Limits**), và số lượng node hiện có trong cụm.
* Không phải tất cả các node đều luôn khả dụng vì nhiều lý do khác nhau. Bộ quản lý cụm giám sát trạng thái hoạt động (**Health Check**) của từng node thông qua tín hiệu nhịp tim định kỳ (**Periodic Heartbeats**).
* Để gán một tài liệu vào một trong $N$ phân vùng, một hàm băm (**Hashing Function**) có thể được sử dụng.
* Sau khi tạo các phân vùng, bộ quản lý cụm sẽ chạy các thuật toán đánh chỉ mục cho tất cả $N$ phân vùng đồng thời trên $N$ node trong cụm. Mỗi tiến trình đánh chỉ mục tạo ra một chỉ mục đảo ngược thu nhỏ (**Tiny Inverted Index**), được lưu trữ trên bộ nhớ cục bộ (**Local Storage**) của chính node đó. Bằng cách này, chúng ta tạo ra $N$ chỉ mục đảo ngược nhỏ thay vì một chỉ mục đảo ngược khổng lồ.

#### Quá trình tìm kiếm (Searching)
* Trong giai đoạn tìm kiếm, khi một truy vấn của người dùng gửi đến, chúng ta thực hiện các tìm kiếm song song (**Parallel Searches**) trên từng chỉ mục đảo ngược thu nhỏ được lưu trữ trên ổ đĩa cục bộ của các node, tạo ra $N$ truy vấn con.
* Kết quả tìm kiếm từ mỗi chỉ mục đảo ngược nhỏ là một danh sách ánh xạ (**Mapping List**) tương ứng với thuật ngữ được truy vấn (giả định truy vấn của người dùng là một từ/thuật ngữ đơn). Bộ hợp nhất (**Merger**) sẽ tổng hợp các danh sách ánh xạ này.
* Sau khi tập hợp các danh sách ánh xạ, bộ hợp nhất tiến hành sắp xếp danh sách tài liệu từ danh sách ánh xạ tổng hợp dựa trên tần suất xuất hiện của thuật ngữ (**Term Frequency**) trong mỗi tài liệu.
* Danh sách tài liệu đã được sắp xếp sẽ được trả về cho người dùng dưới dạng kết quả tìm kiếm. Các tài liệu được hiển thị theo thứ tự sắp xếp (tăng dần/mức độ phù hợp) tới người dùng.

> [!NOTE]
> **Ghi chú (Note):**  
> Chúng ta đã thiết kế một hệ thống tìm kiếm áp dụng kiến trúc phân tán và song song hóa cả quá trình đánh chỉ mục lẫn tìm kiếm. Điều này giúp chúng ta xử lý được các tập dữ liệu khổng lồ bằng cách chia nhỏ để thao tác trên các phân vùng tài liệu nhỏ hơn. Cần lưu ý rằng cả hai tác vụ tìm kiếm và đánh chỉ mục đều được thực thi trên cùng một node. Chúng ta gọi khái niệm này là **Đồng vị trí (Colocation)**.

Thiết kế đề xuất trên hoạt động hiệu quả, và chúng ta có thể sao chép (**Replicate**) mô hình này trên toàn cầu tại nhiều trung tâm dữ liệu (**Data Centers**) khác nhau để phục vụ toàn bộ người dùng. Do đó, chúng ta có thể đạt được các lợi thế sau:
* Thiết kế của chúng ta sẽ không gặp phải điểm lỗi đơn lẻ (**Single Point of Failure - SPOF**).
* Độ trễ (**Latency**) cho toàn bộ người dùng sẽ luôn ở mức thấp.
* Việc bảo trì và nâng cấp tại từng trung tâm dữ liệu riêng lẻ trở nên khả thi mà không gián đoạn hệ thống.
* Khả năng mở rộng (**Scalability**) của hệ thống (phục vụ nhiều người dùng hơn trên mỗi giây) được cải thiện rõ rệt.

---

### Cơ chế sao chép (Replication)

Chúng ta tạo các bản sao (**Replicas**) cho các node đánh chỉ mục vốn chịu trách nhiệm tạo chỉ mục đảo ngược cho các phân vùng được phân công. Với các bản sao này, chúng ta có thể phản hồi một truy vấn từ nhiều tập hợp node khác nhau. 

Ý tưởng tổng thể rất trực quan: Chúng ta tiếp tục sử dụng kiến trúc tương tự như trước, nhưng thay vì chỉ có một nhóm node duy nhất, chúng ta có $R$ nhóm node để trả lời các truy vấn của người dùng, trong đó $R$ là số lượng bản sao (**Number of Replicas**). Số lượng bản sao có thể mở rộng (**Expand**) hoặc thu hẹp (**Shrink**) linh hoạt dựa trên lưu lượng yêu cầu, và mỗi nhóm node đều chứa đầy đủ tất cả các phân vùng cần thiết để trả lời mọi truy vấn.

Mỗi nhóm node được lưu trữ trên các vùng khả dụng (**Availability Zones - AZ**) khác nhau nhằm mang lại hiệu năng cao hơn và đảm bảo tính sẵn sàng cao (**High Availability**) của hệ thống trong trường hợp xảy ra sự cố sập toàn bộ trung tâm dữ liệu.

> [!NOTE]
> **Ghi chú (Note):**  
> Thành phần cân bằng tải (**Load Balancer**) là bắt buộc để điều phối, phân bổ đồng đều các truy vấn giữa các nhóm node khác nhau và thực hiện thử lại (**Retry**) khi có bất kỳ lỗi nào phát sinh.

---

### Hệ số sao chép và Phân phối bản sao (Replication Factor and Replica Distribution)

Thông thường, một hệ số sao chép (**Replication Factor**) bằng 3 là đủ. Hệ số sao chép bằng 3 đồng nghĩa với việc có 3 node cùng lưu trữ chung một phân vùng và tạo chỉ mục cho phân vùng đó. Một trong ba node sẽ đóng vai trò là node chính (**Primary Node**), trong khi hai node còn lại là các bản sao (**Replicas**). Mỗi node này tạo chỉ mục theo cùng một thứ tự để hội tụ về cùng một trạng thái (**Converge on the same state**).

Để minh họa, hãy chia nhỏ dữ liệu (tập hợp tài liệu) thành 4 phân vùng. Vì hệ số sao chép là 3, nên một phân vùng sẽ được lưu trữ bởi 3 node. Chúng ta giả định rằng có 2 vùng khả dụng ($\text{AZ}_1$ và $\text{AZ}_2$). Tại mỗi vùng khả dụng, chúng ta có 2 node. Mỗi node chỉ đóng vai trò là Primary cho duy nhất một phân vùng (Ví dụ: Node 1 trong $\text{AZ}_1$ là Primary Node cho phân vùng $P_1$). 

Ba bản sao (màu hồng, màu xanh lam và màu tím) của một phân vùng được chia sẻ giữa hai thực thể $\text{AZ}$ sao cho hai bản sao nằm ở một zone và bản sao thứ ba nằm ở zone còn lại. Ba màu sắc đại diện cho ba bản sao của từng phân vùng. Ví dụ, điều này đúng với phân vùng $P_4$:
* Bản sao thứ nhất, biểu diễn bằng **màu hồng**, được đặt tại Node 2 của $\text{AZ}_2$.
* Bản sao thứ hai, biểu diễn bằng **màu xanh lam**, được đặt tại Node 1 của $\text{AZ}_2$.
* Bản sao thứ ba, biểu diễn bằng **màu tím**, được đặt tại Node 2 của $\text{AZ}_1$.

Mỗi nhóm trong hình minh họa bao gồm một bản sao từ tất cả 4 phân vùng ($P_1, P_2, P_3, P_4$).

---

### Phân phối Bản sao (Replica Distribution): Mỗi Node chứa một Phân vùng Chính (Primary Partition) và hai Bản sao (Replicas)

```
AZ1 (Vùng sẵn sàng 1)
Node 1          Node 2
P1              P2
P3              P4
P1              P2
P3              P1
P3              P4

AZ2 (Vùng sẵn sàng 2)
Node 1          Node 2
P1              P2
P4              P2
P3              P4

Primary         Primary         Primary
Nhóm 1 (Group 1) Nhóm 2 (Group 2) Nhóm 3 (Group 3)
Các phân vùng (Partitions)
```

Trong hình minh họa trên, bản sao chính (**primary replica**) cho **P1** được biểu thị bằng màu tím đậm, bản sao chính cho **P2** được biểu thị bằng màu xanh lam đậm, và bản sao chính cho **P3** cùng **P4** được biểu thị bằng màu hồng đậm.

Sau khi đã hoàn thành việc sao chép dữ liệu (**replication**), hãy cùng xem cách thức quá trình lập chỉ mục (**indexing**) và tìm kiếm (**searching**) được thực thi trên các bản sao này.

#### Lập chỉ mục với các bản sao (Indexing with replicas)
Từ sơ đồ trên, chúng ta giả định rằng mỗi phân vùng (**partition**) sẽ được chuyển tiếp (**forwarded**) đến từng bản sao (**replica**) để thực hiện tính toán chỉ mục (**index computation**). Hãy xét ví dụ khi chúng ta muốn lập chỉ mục cho phân vùng **P1**. Điều này có nghĩa là cùng một phân vùng đó sẽ được chuyển tiếp đến toàn bộ ba bản sao trên cả hai vùng sẵn sàng (**Availability Zones - AZ**). Do đó, mỗi node sẽ tính toán chỉ mục đồng thời (**simultaneously**) và đạt đến cùng một trạng thái.

Ưu điểm của chiến lược này là thao tác lập chỉ mục (**indexing operation**) sẽ không bị gián đoạn hay ảnh hưởng nếu node chính (**primary node**) gặp sự cố (**failover / node failure**).

#### Tìm kiếm với các bản sao (Searching with replicas)
Chúng ta có ba bản sao cho chỉ mục của mỗi phân vùng. Bộ cân bằng tải (**Load Balancer**) sẽ chọn một trong ba bản sao của từng phân vùng để thực thi truy vấn (**query**). Việc tăng số lượng bản sao giúp cải thiện khả năng mở rộng (**Scalability**) và độ sẵn sàng cao (**High Availability**) của hệ thống. Giờ đây, hệ thống có thể xử lý số lượng truy vấn gấp ba lần trong cùng một khoảng thời gian.

---

### Tóm tắt (Summary)
Trong bài học này, chúng ta đã học cách xử lý khối lượng dữ liệu lớn và lượng truy vấn khổng lồ bằng các chiến lược sau:
- **Lập chỉ mục và tìm kiếm song song (Parallel indexing and searching)**, trong đó cả hai tiến trình này được đặt chung trên cùng một node (**colocated**).
- **Sao chép từng phân vùng (Replicating each partition)**, đồng nghĩa với việc chúng ta cũng sao chép cả tiến trình lập chỉ mục và tìm kiếm.

Chúng ta đã thiết kế thành công một hệ thống có khả năng mở rộng với các thao tác đọc (**read - search**) và ghi (**write - indexing**) cùng nằm trên một node (**colocated**). Tuy nhiên, phương pháp mở rộng quy mô này lại mang lại một số hạn chế. Chúng ta sẽ cùng xem xét các nhược điểm này và giải pháp khắc phục trong bài học tiếp theo.

---

## Mở rộng Quy mô Tìm kiếm và Lập chỉ mục (Scaling Search and Indexing)

Tìm hiểu phương pháp hiệu quả để mở rộng quy mô lập chỉ mục (**indexing**) và tìm kiếm (**search**) trong một hệ thống tìm kiếm.

**Nội dung bao gồm:**
- Các vấn đề với thiết kế đề xuất (Problems with the proposed design)
- Giải pháp (Solution)
- Tách biệt lập chỉ mục và tìm kiếm (Separate the indexing and search)
- Giải thích chi tiết về lập chỉ mục (Indexing explained)
- Tóm tắt (Summary)

---

### Các vấn đề với thiết kế đề xuất (Problems with the proposed design)

Mặc dù thiết kế được đề xuất trong bài học trước có vẻ hợp lý, nhưng nó vẫn tồn tại một số nhược điểm nghiêm trọng. Chúng ta sẽ thảo luận các nhược điểm này dưới đây:

1. **Đặt chung tiến trình lập chỉ mục và tìm kiếm (Colocated indexing and searching):** Chúng ta đã tạo ra một hệ thống đặt chung (**colocates**) cả việc lập chỉ mục và tìm kiếm trên cùng một node. Mặc dù nhìn qua có vẻ là cách sử dụng tài nguyên hiệu quả, nhưng nó cũng có những mặt trái. Cả tìm kiếm và lập chỉ mục đều là các tác vụ tiêu tốn nhiều tài nguyên (**resource-intensive operations**). Hai hoạt động này cạnh tranh và tác động tiêu cực đến hiệu năng (**performance**) của nhau. Ngoài ra, thiết kế đặt chung này không thể mở rộng quy mô hiệu quả khi khối lượng thao tác lập chỉ mục và tìm kiếm thay đổi biến thiên theo thời gian. Việc đặt cả hai thao tác này trên cùng một máy có thể dẫn đến sự mất cân bằng tải và gây ra các vấn đề về khả năng mở rộng (**scalability issues**).

2. **Tính toán lại chỉ mục (Index recomputation):** Chúng ta đang giả định rằng mỗi bản sao (**replica**) sẽ tính toán chỉ mục một cách riêng lẻ độc lập, điều này dẫn đến việc sử dụng tài nguyên kém hiệu quả. Hơn nữa, việc tính toán chỉ mục là một tác vụ tiêu tốn cực kỳ nhiều tài nguyên với hàng trăm giai đoạn xử lý theo đường ống (**pipelined operations**). Do đó, việc tính toán lại cùng một chỉ mục trên các bản sao khác nhau đòi hỏi các cỗ máy phần cứng mạnh mẽ. Thay vào đó, cách tiếp cận hợp lý hơn là chỉ tính toán chỉ mục một lần duy nhất rồi sao chép (**replicate**) nó qua các vùng sẵn sàng (**Availability Zones**).

---

Vì những lý do then chốt này, chúng ta sẽ xem xét một phương pháp thay thế cho việc lập chỉ mục và tìm kiếm phân tán.

### Giải pháp (Solution)

Thay vì tính toán lại chỉ mục trên từng bản sao, chúng ta chỉ tính toán chỉ mục đảo (**inverted index**) duy nhất trên node chính (**primary node**). Tiếp theo, chúng ta truyền chỉ mục đảo này (dưới dạng tệp nhị phân / binary blob) sang các bản sao (**replicas**). Lợi ích cốt lõi của phương pháp này là tránh lãng phí dung lượng CPU và bộ nhớ (RAM) bị nhân bản cho việc lập chỉ mục trên các bản sao.

> [!NOTE]
> **Điểm cần suy ngẫm (Point to Ponder)**
> 
> **Câu hỏi:** Nhược điểm của giải pháp đề xuất ở trên là gì?
> 
> **Trả lời:**
> - Vì chỉ mục đảo sẽ được truyền tới các bản sao, điều này sẽ tạo ra độ trễ truyền tải (**transmission latency**) để sao chép tệp chỉ mục đảo, do kích thước của tệp chỉ mục có thể rất lớn.
> - Khi node chính tiếp nhận các thao tác lập chỉ mục mới, tệp chỉ mục đảo sẽ thay đổi. Mỗi bản sao cần phải kéo (**fetch**) phiên bản mới nhất của tệp về sau khi số lượng thao tác lập chỉ mục đạt đến một ngưỡng quy định nhất định.

---

### Tách biệt lập chỉ mục và tìm kiếm (Separate the indexing and search)

Với sự phát triển vượt bậc của công nghệ mạng và ảo hóa, điện toán đám mây (**cloud computing**) đã trở thành một công nghệ thành công và phổ biến. Trong môi trường công nghệ này, chúng ta có thể tiếp cận lượng băng thông khổng lồ (lên tới 100 Gbps) và hệ thống lưu trữ phân tán có khả năng mở rộng cao (**scalable distributed storage**).

Những tiến bộ này cho phép tạo ra sự phân tách mạnh mẽ (**strong separation**) giữa việc lập chỉ mục và tìm kiếm mà không phải gánh chịu hậu quả tiêu cực của độ trễ lập chỉ mục (**indexing latency**). Nhờ sự cô lập tài nguyên này, quá trình lập chỉ mục sẽ không ảnh hưởng đến khả năng mở rộng của tìm kiếm và ngược lại. Đồng thời, thay vì tính toán lại chỉ mục trên các node bản sao gây lãng phí tài nguyên, chúng ta chỉ cần sao chép các tệp chỉ mục (**index files**).

Chúng ta sẽ áp dụng các công nghệ này để tái thiết kế hệ thống tìm kiếm và lập chỉ mục phân tán. Có ba thành phần tham gia vào thiết kế hệ thống tìm kiếm này:
1. **Indexer (Bộ lập chỉ mục):** Bao gồm một nhóm các node để tính toán chỉ mục.
2. **Distributed Storage (Bộ lưu trữ phân tán):** Hệ thống này được sử dụng để lưu trữ các phân vùng (**partitions**) và chỉ mục đã được tính toán.
3. **Searcher (Bộ tìm kiếm):** Bao gồm nhiều node để thực thi tác vụ tìm kiếm.

Hình minh họa dưới đây mô tả quá trình tạo và truyền chỉ mục đảo giữa một node Indexer và một node Searcher:

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p029_00.png)

*Các chỉ mục được tạo ra bởi các node Indexer sẽ được lưu trữ trên bộ lưu trữ phân tán, và các node tham gia vào quá trình tìm kiếm sẽ đọc các chỉ mục từ bộ lưu trữ phân tán để tạo kết quả cho truy vấn của người dùng.*

- **Tiến trình lập chỉ mục (Indexing process):** Node lập chỉ mục (Indexing node) $\rightarrow$ Tải chỉ mục lên (Upload index) $\rightarrow$ Bộ lưu trữ phân tán (Distributed storage) (có Chỉ mục cục bộ - Local index tùy chọn).
- **Tiến trình tìm kiếm (Search process):** Bộ lưu trữ phân tán (Distributed storage) $\rightarrow$ Tải chỉ mục về (Download index) $\rightarrow$ Node tìm kiếm (Searching node) (sở hữu Chỉ mục cục bộ - Local index).

---

Trong hình minh họa trên, chỉ có một node đơn lẻ được hiển thị cho mỗi thao tác lập chỉ mục và tìm kiếm. Nhưng trên thực tế, sẽ có $N$ node trong giai đoạn lập chỉ mục, mỗi node phụ trách một phân vùng (tập hợp tài liệu) để tạo ra các chỉ mục đảo.

Chỉ mục đảo được lưu dưới dạng các tệp nhị phân (**binary blob files**) trên bộ nhớ cục bộ (**local storage**) của các node. Việc lưu trữ đệm (**caching**) các tệp blob này sẽ giúp cải thiện hiệu năng. Các tệp nhị phân này cũng được đẩy lên một bộ lưu trữ phân tán (**distributed storage**). Trong trường hợp xảy ra sự cố hỏng hóc phần cứng (**hardware failure**), một máy tính Searcher hoặc Indexer mới sẽ được bổ sung vào cụm, và một bản sao chép dữ liệu sẽ được truy xuất phục hồi từ bộ lưu trữ phân tán.

Khi quá trình tải lên (**upload**) hoàn tất, các node Searcher sẽ tải các tệp chỉ mục này về. Tùy thuộc vào hành vi tìm kiếm của người dùng, các node tìm kiếm sẽ duy trì một bộ nhớ đệm (**cache**) chứa các truy vấn thường gặp và phục vụ dữ liệu trực tiếp từ bộ nhớ RAM. Truy vấn tìm kiếm của người dùng sẽ được phân phát (**scattered/extended**) đến tất cả các node tìm kiếm; mỗi node này sẽ tạo phản hồi dựa trên các chỉ mục tương ứng của chúng. Một node tổng hợp (**merger node**) ở tầng máy chủ giao diện (**front-end servers**) sẽ gom (**aggregate/combine**) toàn bộ các kết quả tìm kiếm và hiển thị cho người dùng.

Tiến trình lập chỉ mục sẽ xử lý các tài liệu mới ngay khi chúng sẵn sàng. Đồng thời, các node tìm kiếm sẽ lấy về các chỉ mục đã cập nhật để cung cấp kết quả tìm kiếm tối ưu nhất.

---

### Giải thích chi tiết về lập chỉ mục (Indexing explained)

Cho đến thời điểm hiện tại, chúng ta đã giải thích cách phát triển một thiết kế có khả năng mở rộng cao (**highly scalable**) và hiệu năng vượt trội (**performant**) bằng cách sử dụng các node chi phí thấp. Tuy nhiên, chúng ta vẫn chưa đi sâu vào cấu trúc bên trong (**internals**) của các node lập chỉ mục. Trong phần này, chúng ta sẽ tìm hiểu cách thức lập chỉ mục được thực thi bằng mô hình phân tán **MapReduce** và khung xử lý song song (**parallel processing framework**).

Khung xử lý MapReduce được triển khai với sự hỗ trợ của một **Trình quản lý cụm (Cluster Manager)** và một tập hợp các **node công nhân (Worker nodes)** được phân loại thành **Mappers** và **Reducers**. Đúng như tên gọi của nó, MapReduce bao gồm hai pha:
1. **Pha Map (The Map phase)**
2. **Pha Giảm / Thu gom (The Reduction phase)**

Ngoài ra, đầu vào của MapReduce là một tập hợp các phân vùng (**partitions**) hoặc tập hợp tài liệu, trong khi đầu ra của nó là một chỉ mục đảo tổng hợp hoàn chỉnh (**aggregated inverted index**).

Hãy cùng tìm hiểu mục đích của các thành phần trên:
- **Cluster manager (Trình quản lý cụm):** Trình quản lý khởi tạo tiến trình bằng cách phân phối một tập hợp các phân vùng cho các Mapper. Khi các Mapper hoàn thành tác vụ, Cluster Manager sẽ phân phối đầu ra của các Mapper cho các Reducer.
- **Mappers:** Thành phần này chịu trách nhiệm trích xuất (**extracts**) và lọc (**filters**) các thuật ngữ / từ khóa (**terms**) từ các phân vùng tài liệu.

---

### Quá trình Xử lý MapReduce cho Chỉ mục Ngược (Inverted Index)

...được chỉ định cho nó bởi **Cluster Manager** (trình quản lý cụm). Các máy này xuất ra các chỉ mục ngược (inverted indexes) song song, đóng vai trò là đầu vào (input) cho các **Reducers**.

- **Reducers**: Reducer kết hợp các ánh xạ (mappings) cho các thuật ngữ (terms) khác nhau để tạo ra một chỉ mục tổng hợp (summarized index).

**Cluster Manager** đảm bảo rằng tất cả các worker nodes đều được khai thác hiệu quả trong cụm. MapReduce được xây dựng để vận hành tốt ngay cả khi xảy ra lỗi cục bộ/từng phần (**Partial Failures** / **Fault Tolerance**). Nếu một node bị lỗi (fail), hệ thống sẽ lập lịch lại công việc đó trên một node khác (**reschedule**).

> [!NOTE]
> Lưu ý rằng các Reducers không thể bắt đầu chừng nào các Mappers vẫn đang hoạt động. Điều này có nghĩa là Cluster Manager có thể tái sử dụng cùng một node vừa làm **Mapper** vừa làm **Reducer**.

Các slide dưới đây mô tả một mô hình thiết lập đơn giản hóa về cách MapReduce có thể được sử dụng để tạo ra một chỉ mục ngược (inverted index):

---

#### Minh họa từng bước quy trình MapReduce

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p031_00.png)
*Hình 1/5: Cluster Manager và các phân vùng tài liệu (document partitions).*

---

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p031_01.png)
![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p032_00.png)

**Giai đoạn Map (Map phase):**
- **Assign map**: Giai đoạn Map bắt đầu và Cluster Manager phân phối các phân vùng tài liệu (document partitions) cho các node đang rảnh (idle nodes) trong cluster. Chúng ta gọi các node này là **Mappers**.

*(Trình tự 2/5)*

---

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p032_01.png)
![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p032_02.png)
![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p033_00.png)

Các **Mappers** trích xuất các thuật ngữ (terms) từ các tài liệu được giao và tạo ra $N$ chỉ mục ngược nhỏ hơn (**smaller inverted indices**).

*(Trình tự 3/5)*

**Dữ liệu trung gian được trích xuất:**
- `elasticsearch`: `([1, 3], [1, 1])`
- `distributed`: `([1, 3], [1, 1])`
- `Apache`: `([3], [1])`
- `elasticsearch`: `([2, 4], [1, 1])`
- `Apache`: `([11, 6], [1, 1])`
- `library`: `([2], [1])`
- `Server`: `([8, 12], [3, 2])`
- `engine`: `([6, 11], [1, 4])`
- `engine`: `([2, 7], [1, 1])`

---

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p033_01.png)
![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p033_02.png)

**Giai đoạn Reduce (Reduce phase):**
- **Assign reduce**: Giai đoạn Reduce bắt đầu, Cluster Manager xác định các node đang rảnh để chạy hàm Reduce (**Reduce function**) và gán công việc cho các **Reducers**.

*(Trình tự 4/5)*

---

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p034_00.png)
![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p034_01.png)
![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p034_02.png)

Các **Reducers** gom/kết hợp các thuật ngữ giống nhau từ các terms được chỉ định đến từ tất cả các Mappers và đưa toàn bộ các bản ghi cho mỗi thuật ngữ cùng nhau lên bộ lưu trữ phân tán (**Distributed Storage**).

*(Trình tự 5/5)*

**Kết quả tổng hợp lưu trữ:**
- `elasticsearch`: `([1, 3], [1, 1])`, `([2, 4], [1, 1])`
- `distributed`: `([1, 3], [1, 1])`
- `Apache`: `([3], [1])`, `([11, 6], [1, 1])`
- `library`: `([2], [1])`
- `Server`: `([8, 12], [3, 2])`
- `engine`: `([2, 7], [1, 1])`, `([6, 11], [1, 4])`

Để giữ cho mô hình trực quan, chúng tôi chỉ hiển thị hai chỉ số cho mỗi term trong hình minh họa trên: 
1. Danh sách các tài liệu mà term đó xuất hiện (document ID list).
2. Danh sách tần suất xuất hiện của term trong từng tài liệu (term frequency list) *(tham khảo phần Đánh chỉ mục - Indexing để biết thêm chi tiết)*.

> [!NOTE]
> Mô hình MapReduce thiết lập ở trên là phiên bản đơn giản hóa so với những gì diễn ra trong thực tế. Trong môi trường thực tế, cần một pipeline phức tạp của framework MapReduce để xử lý các vấn đề chuyên sâu của một search engine quy mô lớn. Tuy nhiên, các nguyên lý nền tảng cốt lõi hoàn toàn tương đồng với những gì chúng tôi đã trình bày ở đây.

---

### Tóm tắt (Summary)

*Quay lại: Thiết kế Công cụ Tìm kiếm Phân tán (Design of a Distributed Search)*  
*Đánh dấu Đã hoàn thành (Mark As Completed)*  
*Tiếp theo: Đánh giá Thiết kế của Công cụ Tìm kiếm Phân tán (Evaluation of a Distributed Search's …)*

Trong bài học này, chúng ta đã giải quyết hai vấn đề cốt lõi về:
1. **Khả năng mở rộng (Scalability)**: Do việc gom chung (co-locating) tác vụ indexing và searching trên cùng node gây ra.
2. **Lãng phí tài nguyên (Resource wastage)**: Do việc tính toán lại chỉ mục (index recomputation).

Giải pháp là sử dụng các node chuyên dụng (**dedicated nodes**) riêng biệt cho tác vụ **Indexing** và tác vụ **Searching**. Cả hai thao tác này đều phụ thuộc vào bộ lưu trữ phân tán (**Distributed Storage**). Hơn nữa, chúng tôi đã trình bày một mô tả đơn giản hóa về framework MapReduce nhằm song song hóa (**parallelize**) quy trình lập chỉ mục.

---

### Đánh giá Thiết kế của Công cụ Tìm kiếm Phân tán (Evaluation of a Distributed Search's Design)

Phân tích cách thiết kế của chúng ta đáp ứng các yêu cầu hệ thống.

Chúng ta sẽ bao quát các nội dung sau:
- **Độ khả dụng (Availability)**
- **Khả năng mở rộng (Scalability)**
- **Tìm kiếm nhanh trên dữ liệu lớn (Fast search on big data)**
- **Giảm thiểu chi phí (Reduced cost)**
- **Kết luận (Conclusion)**

---

#### Độ khả dụng (Availability)

Chúng ta sử dụng bộ lưu trữ phân tán (**Distributed Storage**) để lưu trữ các thành phần sau:
- Các tài liệu được thu thập (crawled) bởi bộ lập chỉ mục (**Indexer**).
- Các chỉ mục ngược (**Inverted Indexes**) được tạo ra bởi các node lập chỉ mục (**Indexing nodes**).

Dữ liệu được nhân bản (**Replicated**) qua nhiều vùng (**Regions**) trong bộ lưu trữ phân tán, giúp cho việc triển khai đa vùng (**Cross-Region Deployment**) cho cả tác vụ lập chỉ mục và tìm kiếm trở nên dễ dàng hơn. Nhóm các node lập chỉ mục và node tìm kiếm chỉ cần được nhân bản ở các vùng khả dụng (**Availability Zones - AZ**) khác nhau.

Vì vậy, chúng ta triển khai cụm (cluster) gồm các node indexing và search trên các Availability Zones khác nhau. Nhờ đó, nếu một sự cố xảy ra tại một nơi (single zone failure), chúng ta hoàn toàn có thể xử lý các yêu cầu từ một cụm khác. Việc duy trì nhiều nhóm node indexing và search giúp đạt được **High Availability** (độ khả dụng cao) cho cả hai quá trình. Hơn nữa, bên trong từng cluster, nếu một node bị chết (node failure), một node khác có thể ngay lập tức tiếp quản vị trí của nó.

> [!TIP]
> Việc lập chỉ mục (**Indexing**) được thực hiện ngoại tuyến (**Offline**), hoàn toàn nằm ngoài luồng xử lý quan trọng trực tiếp của người dùng (**User's Critical Path**). Chúng ta không cần phải sao chép các thao tác indexing một cách đồng bộ (**Synchronous Replication**). Hệ thống không bắt buộc phải phản hồi các truy vấn tìm kiếm của người dùng với dữ liệu mới nhất vừa mới được bổ sung vào chỉ mục. Do đó, chúng ta không cần phải chờ đợi quá trình sao chép (replication) chỉ mục mới hoàn tất rồi mới phản hồi truy vấn tìm kiếm. Điều này đảm bảo tính sẵn sàng tối đa (**High Availability**) của dịch vụ tìm kiếm đối với người dùng cuối.

---

# Thiết Kế Hệ Thống: Công Cụ Tìm Kiếm Phân Tán (Distributed Search)

> [!NOTE]
> **Lưu ý:** Một khi chúng ta sao chép (replicate) dữ liệu mới nhất vào tất cả các nhóm node đánh chỉ mục (indexing nodes) và các node tìm kiếm (search nodes) đã tải dữ liệu đó xuống, thì các truy vấn tìm kiếm (search queries) sẽ được thực thi trên tập dữ liệu mới nhất.

---

## Các Cam Kết Được Cung Cấp Bởi Hệ Thống Tìm Kiếm Phân Tán (Guarantees Provided by the Distributed Search)

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p037_00.png)

Hệ thống tìm kiếm phân tán (**Distributed search system**) đảm bảo các đặc tính cốt lõi sau:

* **Khả năng mở rộng (Scalability)**
* **Tính sẵn sàng (Availability)**
* **Tìm kiếm nhanh (Fast search)**
* **Giảm thiểu chi phí (Reduced cost)**

---

### Khả Năng Mở Rộng (Scalability)

Phân vùng dữ liệu (**Partitioning / Sharding**) là một thành phần thiết yếu để các hệ thống tìm kiếm có thể mở rộng quy mô (**scale**). Khi chúng ta tăng số lượng phân vùng (partitions) và bổ sung thêm các node vào các cụm đánh chỉ mục (**indexing clusters**) và cụm tìm kiếm (**search clusters**), chúng ta có thể mở rộng quy mô cả về khía cạnh đánh chỉ mục dữ liệu (**data indexing**) lẫn truy vấn dữ liệu (**querying**).

Sự cô lập mạnh mẽ (**strong isolation**) giữa tiến trình đánh chỉ mục (indexing) và tiến trình tìm kiếm (search) giúp cho việc đánh chỉ mục và tìm kiếm có thể mở rộng độc lập và linh hoạt theo nhu cầu (**scale independently and dynamically**).

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p037_01.png)

---

### Tìm Kiếm Nhanh Trên Dữ Liệu Lớn (Fast Search on Big Data)

Chúng ta tận dụng một số lượng lớn các node, trong đó mỗi node thực thi các truy vấn tìm kiếm **song song (parallel)** trên các chỉ mục đảo ngược (**inverted indices**) có kích thước nhỏ hơn. Kết quả từ mỗi node tìm kiếm sau đó sẽ được tổng hợp/hợp nhất (**merged**) lại và trả về cho người dùng.

![021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](images/topic_021_p037_02.png)

---

### Giảm Thiểu Chi Phí (Reduced Cost)

Chúng ta sử dụng các máy chủ chi phí thấp (cheaper commodity machines) để tính toán chỉ mục và thực thi tìm kiếm. Nếu một node gặp sự cố lỗi (**fails**), chúng ta không cần phải tính toán lại toàn bộ chỉ mục (complete index). Thay vào đó, chỉ một phần các tài liệu (**documents**) bị ảnh hưởng mới cần phải được đánh chỉ mục lại.

---

## Kết Luận (Conclusion)

Hệ thống tìm kiếm là một thành phần bắt buộc đối với hầu hết mọi ứng dụng hiện nay. Chúng ta đã thấy rằng việc phát triển một hệ thống tìm kiếm chỉ chạy trên một node đơn lẻ (single node) là điều bất khả thi. Chúng ta đã tận dụng một khung tính toán song song (**parallel computation framework**) cùng với các máy chủ chi phí thấp để xây dựng một hệ thống tìm kiếm đạt tính sẵn sàng cao (**available**), khả năng mở rộng linh hoạt (**scalable**), và hiệu năng vượt trội (**highly performant**).

---

> [!TIP]
> **Điều hướng tài liệu:**
> * **Trước (Back):** Mở rộng Tìm kiếm và Đánh chỉ mục (Scaling Search and Indexing)
> * **Trạng thái:** Đánh dấu hoàn thành (Mark As Completed)
> * **Tiếp theo (Next):** Thiết kế hệ thống: Hệ thống ghi log phân tán (System Design: Distributed Logging)


---

[← Bài trước](020-kho-luu-tru-blob-store.md) | [Mục lục](README.md) | [Bài tiếp theo →](022-ghi-log-phan-tan-distributed-logging.md)
