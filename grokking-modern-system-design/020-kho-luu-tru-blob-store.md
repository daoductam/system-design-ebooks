# 020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)

[← Bài trước](019-gioi-han-tan-suat-rate-limiter.md) | [Mục lục](README.md) | [Bài tiếp theo →](021-tim-kiem-phan-tan-distributed-search.md)

---


# Thiết Kế Hệ Thống: Kho Lưu Trữ Đối Tượng Lớn (System Design: A Blob Store)

Làm quen với kho lưu trữ đối tượng lớn (blob store) và chuẩn bị sẵn sàng để thiết kế hệ thống này.

**Chúng ta sẽ tìm hiểu các nội dung sau:**
* Kho lưu trữ đối tượng lớn (blob store) là gì?
* Tại sao chúng ta sử dụng blob store?
* Chúng ta thiết kế một hệ thống blob store như thế nào?

---

### Kho lưu trữ đối tượng lớn (Blob store) là gì?

**Blob store** (Binary Large Object store - Kho lưu trữ đối tượng nhị phân lớn) là một giải pháp lưu trữ dành cho **dữ liệu phi cấu trúc (unstructured data)**. Chúng ta có thể lưu trữ hình ảnh, âm thanh, video, mã thực thi nhị phân (binary executable codes) hoặc các mục đa phương tiện (multimedia) khác trong một blob store. 

Mọi loại dữ liệu đều được lưu trữ dưới dạng một **blob**. Hệ thống tuân theo mô hình tổ chức dữ liệu phẳng (flat data organization pattern), nơi không tồn tại cấu trúc phân cấp (hierarchies), tức là không có thư mục (directories), thư mục con (sub-directories), v.v.

Phần lớn, nó được sử dụng bởi các ứng dụng có yêu cầu nghiệp vụ đặc thù mang tên **ghi một lần, đọc nhiều lần - WORM (Write Once, Read Many)**, quy định rằng dữ liệu chỉ có thể được ghi một lần duy nhất và không ai có thể chỉnh sửa nó. Tương tự như trong Microsoft Azure, các blob được tạo một lần và đọc nhiều lần. Ngoài ra, các blob này không thể bị xóa cho đến khi hết một khoảng thời gian được chỉ định, và chúng cũng không thể bị sửa đổi nhằm bảo vệ các dữ liệu quan trọng.

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p001_00.png)
*Hình minh họa: Một blob store lưu trữ và truyền phát trực tuyến (streaming) các tệp tin phi cấu trúc kích thước lớn như âm thanh, video, hình ảnh và tài liệu.*

> [!NOTE]
> Không nhất thiết tất cả các ứng dụng đều phải có yêu cầu WORM này. Tuy nhiên, chúng ta giả định rằng các blob một khi đã được ghi thì không thể sửa đổi (immutable). Thay vì sửa đổi, chúng ta có thể tải lên một phiên bản mới (new version) của blob nếu cần thiết.

---

### Tại sao chúng ta sử dụng blob store?

Blob store là một thành phần trọng yếu của nhiều ứng dụng xử lý dữ liệu quy mô lớn (data-intensive applications), chẳng hạn như YouTube, Netflix, Facebook, v.v. Bảng dưới đây hiển thị giải pháp lưu trữ blob được sử dụng bởi một số ứng dụng nổi tiếng nhất:

| Hệ thống (System) | Kho lưu trữ Blob (Blob Store) |
| :--- | :--- |
| **Netflix** | Amazon S3 |
| **YouTube** | Google Cloud Storage |
| **Facebook** | Tectonic |

Các ứng dụng này tạo ra một lượng khổng lồ dữ liệu phi cấu trúc mỗi ngày. Chúng đòi hỏi một giải pháp lưu trữ có khả năng mở rộng dễ dàng (**easily scalable**), đáng tin cậy (**reliable**), và có tính sẵn sàng cao (**highly available**), để có thể lưu trữ các tệp phương tiện truyền thông dung lượng lớn. 

Do lượng dữ liệu liên tục tăng lên, các ứng dụng này cần lưu trữ số lượng blob gần như không giới hạn. Theo một số ước tính, YouTube cần thêm hơn một petabyte dung lượng lưu trữ mỗi ngày. 

Trong một hệ thống như YouTube, một video được lưu trữ ở nhiều độ phân giải khác nhau. Ngoài ra, video ở tất cả các độ phân giải đều được nhân bản (**replicated**) nhiều lần qua các trung tâm dữ liệu (**data centers**) và khu vực (**regions**) khác nhau vì mục đích đảm bảo tính sẵn sàng (**availability**). Đó là lý do tại sao tổng dung lượng lưu trữ cần thiết cho mỗi video không bằng kích thước ban đầu của video được tải lên.

---

### Chúng ta thiết kế một hệ thống blob store như thế nào?

Chúng tôi đã chia việc thiết kế blob store thành năm bài học và một bài kiểm tra ngắn (quiz):

1. **Yêu cầu (Requirements):** Trong bài học này, chúng ta xác định các yêu cầu chức năng (functional requirements) và phi chức năng (non-functional requirements) của một blob store. Chúng ta cũng ước tính tài nguyên (resource estimation) cần thiết cho hệ thống blob store.
2. **Thiết kế (Design):** Bài học này cung cấp thiết kế tổng thể cấp cao (high-level design), thiết kế API (API design) và thiết kế chi tiết (detailed design) của blob store, đồng thời giải thích chi tiết toàn bộ các thành phần và quy trình hoạt động (workflow).
3. **Các cân nhắc thiết kế (Design considerations):** Trong bài học này, chúng ta thảo luận về một số khía cạnh quan trọng của thiết kế. Ví dụ: lược đồ cơ sở dữ liệu (database schema), chiến lược phân vùng dữ liệu (partitioning strategy), lập chỉ mục blob (blob indexing), phân trang (pagination) và cơ chế nhân bản (replication).
4. **Đánh giá (Evaluation):** Trong bài học này, chúng ta đánh giá blob store dựa trên các yêu cầu đã đề ra ban đầu.
5. **Kiểm tra kiến thức (Quiz):** Trong bài học này, chúng ta đánh giá mức độ hiểu biết về thiết kế blob store.

Hãy bắt đầu với các yêu cầu của hệ thống blob store.

---

# Yêu Cầu Thiết Kế Kho Lưu Trữ Đối Tượng Lớn (Requirements of a Blob Store's Design)

Xác định các yêu cầu và thực hiện các ước tính tài nguyên cho blob store.

**Chúng ta sẽ tìm hiểu các nội dung sau:**
* Các yêu cầu (Requirements)
  * Yêu cầu chức năng (Functional requirements)
  * Yêu cầu phi chức năng (Non-functional requirements)
* Ước tính tài nguyên (Resource estimation)
  * Ước tính số lượng máy chủ (Number of servers estimation)
  * Ước tính dung lượng lưu trữ (Storage estimation)
  * Ước tính băng thông (Bandwidth estimation)
* Các khối xây dựng (Building blocks) chúng ta sẽ sử dụng

---

## Các Yêu Cầu (Requirements)

Hãy cùng tìm hiểu các yêu cầu chức năng và phi chức năng dưới đây:

### 1. Yêu cầu chức năng (Functional requirements)

Dưới đây là các yêu cầu chức năng cho thiết kế của một blob store:

* **Tạo một thùng chứa (Create a container):** Người dùng có thể tạo các thùng chứa (**containers**) để gom nhóm các blob. Ví dụ: nếu một ứng dụng muốn lưu trữ dữ liệu riêng cho từng người dùng, nó phải có khả năng lưu trữ các blob của các tài khoản người dùng khác nhau trong các container khác nhau. Ngoài ra, một người dùng có thể muốn gom nhóm các blob video và tách biệt chúng khỏi nhóm các blob hình ảnh. Một người dùng blob store duy nhất có thể tạo nhiều container, và mỗi container có thể chứa nhiều blob, như được minh họa dưới đây. Để đơn giản hóa, chúng ta giả định rằng không thể tạo một container bên trong một container khác (không có nested container).

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p005_00.png)
*Hình minh họa: Nhiều container liên kết với một tài khoản lưu trữ duy nhất, và nhiều blob bên trong một container duy nhất.*

```text
Tài khoản (Account)
    └── Thùng chứa (Container)
            └── Đối tượng (Blob)

Educative
    ├── movies
    │     └── mov1.avi
    └── pictures
          ├── img1.jpg
          └── img2.jpg
```

* **Ghi dữ liệu (Put data):** Blob store phải cho phép người dùng tải lên (upload) các blob vào các container đã tạo.
* **Đọc/Lấy dữ liệu (Get data):** Hệ thống phải tạo ra một đường dẫn định danh URL cho blob đã tải lên, để người dùng có thể truy cập blob đó sau này thông qua URL này.
* **Xóa dữ liệu (Delete data):** Người dùng có thể xóa một blob. Nếu người dùng muốn giữ lại dữ liệu trong một khoảng thời gian xác định (thời gian lưu giữ - retention time), hệ thống của chúng ta phải hỗ trợ chức năng này.
* **Liệt kê danh sách blob (List blobs):** Người dùng có thể lấy danh sách các blob bên trong một container cụ thể.
* **Xóa một thùng chứa (Delete a container):** Người dùng có thể xóa một container cùng toàn bộ các blob bên trong nó.
* **Liệt kê danh sách thùng chứa (List containers):** Hệ thống phải cho phép người dùng liệt kê tất cả các container thuộc về một tài khoản cụ thể.

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p005_01.png)
*Hình minh họa: Các yêu cầu chức năng của một blob store (Functional requirements of a blob store).*

---

### 2. Yêu cầu phi chức năng (Non-functional requirements)

Dưới đây là các yêu cầu phi chức năng của hệ thống blob store:

* **Tính sẵn sàng cao (Availability):** Hệ thống của chúng ta phải đạt tính sẵn sàng cao (**highly available**).
* **Độ bền vững dữ liệu (Durability):** Dữ liệu một khi đã được tải lên không được phép bị mất mát, trừ khi người dùng chủ động thực hiện thao tác xóa dữ liệu đó một cách rõ ràng.
* **Khả năng mở rộng (Scalability):** Hệ thống phải có khả năng xử lý và quản lý hàng tỷ blob.
* **Thông lượng (Throughput):** Để truyền tải hàng gigabyte dữ liệu, chúng ta phải đảm bảo thông lượng truyền dữ liệu cao (**high data throughput**).
* **Độ tin cậy và khả năng chịu lỗi (Reliability & Fault Tolerance):** Vì các sự cố hỏng hóc (failures) là điều hiển nhiên thường xảy ra trong các hệ thống phân tán, thiết kế của chúng ta phải có khả năng phát hiện lỗi và phục hồi kịp thời.
* **Tính nhất quán (Consistency):** Hệ thống phải đạt mức nhất quán mạnh (**strongly consistent**). Các người dùng khác nhau phải nhìn thấy cùng một trạng thái/khung nhìn (view) đồng nhất của một blob.

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p005_02.png)
*Hình minh họa: Các yêu cầu phi chức năng của một kho lưu trữ blob (The non-functional requirements of a blob store).*

---

## Ước Tính Tài Nguyên (Resource Estimation)

Hãy cùng ước tính tổng số lượng máy chủ (**servers**), dung lượng lưu trữ (**storage**), và băng thông (**bandwidth**) cần thiết cho một hệ thống lưu trữ blob. 

Vì các blob có thể chứa tất cả các loại dữ liệu, việc liệt kê tất cả các dạng dữ liệu đó trong quá trình ước tính là không thực tế. Do đó, chúng ta sẽ lấy **YouTube** làm ví dụ điển hình—nơi lưu trữ các video và hình thu nhỏ (thumbnails) trên blob store. Hơn nữa, chúng ta sẽ đưa ra các giả định sau để hoàn thành các tính toán ước tính của mình:

### Các giả định (Assumptions):
* Số lượng người dùng hoạt động hàng ngày (**DAU - Daily Active Users**) thực hiện tải lên hoặc xem video là: **5 triệu (5,000,000)**.
* Số lượng yêu cầu trên mỗi giây (**RPS - Requests Per Second**) mà một máy chủ blob store đơn lẻ có thể xử lý là: **500 RPS**.
* Kích thước trung bình của một video là: **50 MB**.
* Kích thước trung bình của một ảnh thu nhỏ (thumbnail) là: **20 KB**.
* Số lượng video được tải lên mỗi ngày là: **250,000 video**.

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p005_03.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p006_00.png)

---

### Số Lượng Yêu Cầu Đọc (Read Requests)
* Số lượng yêu cầu đọc của một người dùng đơn lẻ mỗi ngày là **20**.

---

### Ước Tính Số Lượng Máy Chủ (Number of Servers Estimation)

Từ các giả định ban đầu, chúng ta sử dụng số lượng người dùng hoạt động hàng ngày (**DAU - Daily Active Users**) và số lượng truy vấn mà một máy chủ lưu trữ blob (**Blob Store Server**) có thể xử lý mỗi giây (**QPS - Queries Per Second**). Số lượng máy chủ mà chúng ta cần được tính toán bằng công thức dưới đây:

$$\text{Số lượng máy chủ} = \frac{\text{Số lượng người dùng hoạt động hàng ngày (DAU)}}{\text{Số truy vấn xử lý trên mỗi máy chủ (Queries handled per server)}} = \mathbf{10.000\text{ máy chủ (servers)}}$$

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p007_00.png)

> **Số lượng máy chủ cần thiết cho một hệ thống blob store chuyên dụng để lưu trữ dữ liệu YouTube:**
> **10.000 máy chủ (servers)**

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p007_01.png)

---

### Ước Tính Dung Lượng Lưu Trữ (Storage Estimation)

Xem xét các giả định đã nêu ở trên, chúng ta sử dụng công thức dưới đây để tính toán tổng dung lượng lưu trữ mà YouTube yêu cầu trong một ngày:

$$\text{Tổng dung lượng lưu trữ/ngày} = \text{Số video/ngày} \times (\text{Dung lượng lưu trữ/video} + \text{Dung lượng lưu trữ/thumbnail})$$

Đưa các số liệu trên vào công thức, ta có kết quả là **12,51 TB/ngày**. Đây là dung lượng lưu trữ xấp xỉ mà YouTube cần mỗi ngày để lưu giữ một bản sao duy nhất (**single copy**) của video được tải lên ở một độ phân giải duy nhất.

$$= \mathbf{12,51\text{ TB/ngày}}$$

#### Bảng: Tổng dung lượng lưu trữ cần thiết để lưu trữ Video và Thumbnail tải lên mỗi ngày trên YouTube

| Số video mỗi ngày (No. of videos per day) | Dung lượng mỗi video (MB) (Storage per video) | Dung lượng mỗi thumbnail (KB) (Storage per thumbnail) | Tổng dung lượng mỗi ngày (TB) (Total storage per day) |
| :--- | :--- | :--- | :--- |
| **250.000** | **50** | **20** | **12,51** |

---

### Ước Tính Băng Thông (Bandwidth Estimation)

Hãy cùng ước tính băng thông (**Bandwidth**) cần thiết để tải dữ liệu lên (**upload**) và lấy dữ liệu từ (**retrieval/download**) kho lưu trữ blob store.

#### 1. Lưu lượng tải lên / Lưu lượng vào (Incoming Traffic)
Để ước tính băng thông cần thiết cho lưu lượng chiều vào, chúng ta xem xét tổng dữ liệu được tải lên mỗi ngày, điều này gián tiếp đồng nghĩa với tổng dung lượng lưu trữ cần thiết mỗi ngày mà chúng ta đã tính toán ở trên. Lượng dữ liệu được truyền tới các máy chủ mỗi giây có thể được tính theo công thức sau:

$$\text{Tổng băng thông chiều vào} = \frac{\text{Tổng dung lượng lưu trữ/ngày (Total storage/day)}}{24 \times 60 \times 60}$$

#### Bảng: Băng thông cần thiết cho việc tải Video lên YouTube

| Tổng dung lượng lưu trữ mỗi ngày (TB) | Số giây trong một ngày | Băng thông (Gb/s) |
| :--- | :--- | :--- |
| **12,51** | **86.400** | **1,16** |

#### 2. Lưu lượng tải xuống / Lưu lượng ra (Outgoing Traffic)
Vì kho lưu trữ blob store là một hệ thống thiên về đọc (**Read-Intensive Store**), phần lớn băng thông sẽ dành cho lưu lượng chiều ra (**Outgoing Traffic**). Xem xét các giả định đã đề cập ở trên, chúng ta tính toán băng thông cần thiết cho lưu lượng ra bằng công thức sau:

$$\text{Tổng băng thông chiều ra} = \frac{\text{Số người dùng hoạt động/ngày} \times \text{Số yêu cầu/người dùng/ngày} \times \text{Tổng kích thước dữ liệu}}{\text{Số giây trong một ngày}}$$

#### Bảng: Băng thông cần thiết cho việc tải/xem Video trên YouTube

| Số người dùng hoạt động mỗi ngày | Số yêu cầu trên mỗi người dùng | Kích thước dữ liệu (MB) | Băng thông yêu cầu (Gb/s) |
| :--- | :--- | :--- | :--- |
| **5.000.000** | **20** | **50** | **462,96** |

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p009_00.png)

#### Tổng kết yêu cầu băng thông của hệ thống Blob Store (chỉ tính riêng cho Video YouTube)
* **Băng thông lưu lượng vào (Incoming traffic bandwidth):** `1,16 Gbps`
* **Băng thông lưu lượng ra (Outgoing traffic bandwidth):** `462,96 Gbps`
* **Tổng băng thông (Total Bandwidth):** $1,16\text{ Gbps} + 462,96\text{ Gbps} = \mathbf{464,12\text{ Gbps}}$

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p009_01.png)

---

### Các Thành Phần Khối Dựng Cơ Bản Sẽ Sử Dụng (Building Blocks We Will Use)

Chúng ta sử dụng các khối dựng (**Building Blocks**) sau trong thiết kế hệ thống blob store:

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p009_02.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p009_03.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p009_04.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p009_05.png)

* **Bộ giới hạn tốc độ (Rate Limiter):** Cần thiết để kiểm soát tương tác của người dùng với hệ thống nhằm chống quá tải hoặc tấn công lạm dụng.
* **Bộ cân bằng tải (Load Balancer):** Cần thiết để phân phối tải yêu cầu đồng đều lên các máy chủ khác nhau.
* **Cơ sở dữ liệu (Database):** Được sử dụng để lưu trữ thông tin siêu dữ liệu (**Metadata**) cho các blob.
* **Hệ thống giám sát (Monitoring):** Cần thiết để kiểm tra các thiết bị lưu trữ và dung lượng khả dụng trên chúng nhằm bổ sung tài nguyên lưu trữ kịp thời khi cần.

Trong phần này, chúng ta đã thảo luận về các yêu cầu (**Requirements**) và ước tính tài nguyên (**Estimations**) của hệ thống blob store. Chúng ta sẽ tiến hành thiết kế hệ thống blob store ở bài tiếp theo, bám sát các yêu cầu đã vạch ra.

---

## Thiết Kế Hệ Thống Kho Lưu Trữ Đối Tượng Lớn (Design of a Blob Store)

Tìm hiểu cách tích hợp các yêu cầu cụ thể vào thiết kế của một kho lưu trữ blob store.

**Nội dung sẽ bao gồm:**
* Thiết kế mức tổng quan (High-level design)
* Thiết kế giao diện lập trình ứng dụng (API design)
* Thiết kế chi tiết (Detailed design)
* Các thành phần hệ thống (Components)
* Luồng thực thi (Workflow)

---

### Thiết Kế Mức Tổng Quan (High-Level Design)

Hãy cùng xác định và kết nối các thành phần của hệ thống blob store. Ở mức tổng quan, các thành phần bao gồm: các **Client**, **Front-End Server**, và **Ổ đĩa lưu trữ (Storage Disks)**.

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p011_00.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p011_01.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p011_02.png)

> **Thiết kế tổng quan của một Blob Store:**
> `Clients` $\rightarrow$ `Front-end server` $\rightarrow$ `Storage disks`

Các yêu cầu từ phía client được tiếp nhận tại các **Front-End Server** để xử lý. Các Front-End Server sẽ lưu trữ blob của client lên các **ổ đĩa lưu trữ (Storage Disks)** gắn liền với chúng.

---

### Thiết Kế API (API Design)

Hãy xem xét thiết kế API của hệ thống blob store. Tất cả các hàm bên dưới chỉ có thể được thực thi bởi người dùng đã đăng ký và xác thực danh tính hợp lệ (**Authenticated User**). Để ngắn gọn, chúng ta không đưa các chức năng đăng ký và xác thực người dùng vào đây.

#### 1. Tạo thùng chứa (Create Container)
Thao tác `createContainer` tạo một container mới dưới tài khoản đang đăng nhập đã phát sinh yêu cầu này.

```text
createContainer(containerName)
```

| Tham số (Parameter) | Mô tả (Description) |
| :--- | :--- |
| `containerName` | Đây là tên của container. Tên này phải là duy nhất (**unique**) trong phạm vi một tài khoản lưu trữ (Storage Account). |

#### 2. Tải lên Blob (Upload Blobs)
Dữ liệu của client được lưu trữ dưới dạng các byte (**Bytes**) trong kho lưu trữ blob. Dữ liệu có thể được đưa vào một container bằng lời gọi hàm sau:

```text
putBlob(containerPath, blobName, data)
```

| Tham số (Parameter) | Mô tả (Description) |
| :--- | :--- |
| `containerPath` | Đây là đường dẫn của container nơi chúng ta tải blob lên. Nó bao gồm mã định danh của container (`containerID`). |
| `blobName` | Đây là tên của blob. Tên này phải là duy nhất trong một container, hoặc hệ thống sẽ gán cho blob được tải lên sau một số hiệu phiên bản (**version number**). |
| `data` | Đây là tệp tin (**file**) mà người dùng muốn tải lên kho lưu trữ blob store. |

> [!NOTE]
> **Lưu ý:** Định nghĩa API này chỉ là một cách thức logic để diễn giải nhu cầu chức năng. Trong triển khai thực tế, chúng ta có thể sử dụng cơ chế truyền phát dữ liệu nhiều bước (**Multistep Streaming Call**) nếu kích thước dữ liệu lớn.

---

rất lớn (*very large*).

### Tải xuống Blob (*Download blobs*)
Các blob được định danh bằng tên hoặc ID duy nhất của chúng (*unique name or ID*).

```text
getBlob(blobPath)
```

| Tham số (*Parameter*) | Mô tả (*Description*) |
| :--- | :--- |
| `blobPath` | Đây là đường dẫn đầy đủ (*fully qualified path*) của dữ liệu hoặc tệp tin, bao gồm cả định danh duy nhất của nó. |

---

### Xóa Blob (*Delete blob*)
Thao tác `deleteBlob` đánh dấu blob được chỉ định để xóa. Blob thực tế sẽ được dọn dẹp và xóa bỏ vật lý trong quá trình thu gom rác (*garbage collection*).

```text
deleteBlob(blobPath)
```

| Tham số (*Parameter*) | Mô tả (*Description*) |
| :--- | :--- |
| `blobPath` | Đây là đường dẫn của blob mà người dùng muốn xóa. |

---

### Liệt kê các Blob (*List blobs*)
Thao tác `listBlobs` trả về danh sách các blob nằm dưới container hoặc đường dẫn được chỉ định.

```text
listBlobs(containerPath)
```

| Tham số (*Parameter*) | Mô tả (*Description*) |
| :--- | :--- |
| `containerPath` | Đây là đường dẫn đến container mà người dùng muốn lấy danh sách các blob. |

---

### Xóa Container (*Delete container*)
Thao tác `deleteContainer` đánh dấu container được chỉ định để xóa. Container cùng bất kỳ blob nào bên trong nó sẽ được xóa sau đó trong quá trình thu gom rác (*garbage collection*).

```text
deleteContainer(containerPath)
```

| Tham số (*Parameter*) | Mô tả (*Description*) |
| :--- | :--- |
| `containerPath` | Đây là đường dẫn đến container mà người dùng muốn xóa. |

---

### Liệt kê các Container (*List containers*)
Thao tác `listContainers` trả về danh sách các container thuộc tài khoản lưu trữ blob (*blob store account*) của người dùng được chỉ định.

```text
listContainers(accountID)
```

| Tham số (*Parameter*) | Mô tả (*Description*) |
| :--- | :--- |
| `accountID` | Đây là ID của người dùng muốn liệt kê các container của họ. |

> [!NOTE]
> Các API dùng để truy xuất blob cung cấp siêu dữ liệu (*metadata*) bao gồm kích thước (*size*), số phiên bản (*version number*), đặc quyền truy cập (*access privileges*), tên (*name*), v.v.

---

## Thiết kế chi tiết (*Detailed design*)

Chúng ta bắt đầu phần này bằng việc xác định các thành phần cốt lõi cần thiết để hoàn thiện thiết kế kho lưu trữ blob (*blob store*). Sau đó, chúng ta sẽ xem xét cách các thành phần này kết nối với nhau để đáp ứng các yêu cầu chức năng (*functional requirements*).

### Các thành phần (*Components*)
Dưới đây là danh sách các thành phần được sử dụng trong thiết kế kho lưu trữ blob:

- **Client**: Đây là người dùng hoặc chương trình thực hiện bất kỳ chức năng API nào đã được chỉ định.
- **Bộ giới hạn tốc độ (*Rate limiter*)**: Bộ giới hạn tốc độ hạn chế số lượng yêu cầu dựa trên gói đăng ký (*subscription*) của người dùng hoặc giới hạn số lượng yêu cầu từ cùng một địa chỉ IP tại cùng một thời điểm. Nó không cho phép người dùng vượt quá giới hạn định trước.
- **Bộ cân bằng tải (*Load balancer*)**: Bộ cân bằng tải phân phối lưu lượng mạng đến giữa một nhóm máy chủ. Nó cũng được sử dụng để điều hướng lại các yêu cầu đến các khu vực (*regions*) khác nhau tùy thuộc vào vị trí của người dùng, các trung tâm dữ liệu (*data centers*) khác nhau trong cùng một khu vực, hoặc các máy chủ khác nhau trong cùng một trung tâm dữ liệu. Cân bằng tải DNS (*DNS load balancing*) có thể được sử dụng để định tuyến lại các yêu cầu giữa các khu vực khác nhau dựa trên vị trí địa lý của người dùng.
- **Các máy chủ Front-end (*Front-end servers*)**: Các máy chủ front-end chuyển tiếp các yêu cầu thêm hoặc xóa dữ liệu của người dùng đến các máy chủ lưu trữ (*storage servers*) phù hợp.
- **Các nút dữ liệu (*Data nodes*)**: Các nút dữ liệu chứa dữ liệu blob thực tế. Chúng cũng có thể chỉ chứa một phần dữ liệu của blob. Các blob được chia thành các mảnh nhỏ có kích thước cố định gọi là các khối dữ liệu (*chunks*). Một nút dữ liệu có thể chứa tất cả các chunk của một blob hoặc ít nhất là một vài chunk trong số đó.
- **Nút quản lý (*Manager node*)**: Nút quản lý là thành phần trung tâm quản lý tất cả các nút dữ liệu. Nó lưu trữ thông tin về đường dẫn lưu trữ và các đặc quyền truy cập (*access privileges*) của các blob. Có hai loại đặc quyền truy cập: riêng tư (*private*) và công khai (*public*). Đặc quyền truy cập riêng tư có nghĩa là blob chỉ có thể được truy cập bởi tài khoản sở hữu blob đó. Đặc quyền truy cập công khai có nghĩa là bất kỳ ai cũng có thể truy cập blob đó.

> [!NOTE]
> Mỗi nút dữ liệu trong cụm (*cluster*) định kỳ gửi một tín hiệu nhịp tim (*heartbeat*) và một báo cáo chunk (*chunk report*) đến nút quản lý. Sự hiện diện của nhịp tim cho biết nút dữ liệu vẫn đang hoạt động bình thường (*operational*). Một báo cáo chunk sẽ liệt kê tất cả các chunk hiện có trên một nút dữ liệu.
> 
> Nếu một nút dữ liệu không gửi được nhịp tim, nút quản lý sẽ coi nút đó đã chết (*dead node*) và sau đó xử lý các yêu cầu của người dùng trên các nút bản sao (*replica nodes*). Nút quản lý duy trì một nhật ký các thao tác đang chờ xử lý (*log of pending operations*) để thực thi phát lại (*replayed*) trên nút dữ liệu đã chết khi nó phục hồi trở lại.

- **Kho lưu trữ siêu dữ liệu (*Metadata storage*)**: Kho lưu trữ siêu dữ liệu là một cơ sở dữ liệu phân tán (*distributed database*) được nút quản lý sử dụng để lưu trữ tất cả siêu dữ liệu (*metadata*). Siêu dữ liệu bao gồm: siêu dữ liệu tài khoản (*account metadata*), siêu dữ liệu container (*container metadata*), và siêu dữ liệu blob (*blob metadata*).
  - **Siêu dữ liệu tài khoản (*Account metadata*)**: Chứa thông tin tài khoản của từng người dùng và các container do từng tài khoản nắm giữ.
  - **Siêu dữ liệu container (*Container metadata*)**: Bao gồm danh sách các blob nằm trong mỗi container.
  - **Siêu dữ liệu blob (*Blob metadata*)**: Bao gồm thông tin vị trí nơi mỗi blob được lưu trữ. Siêu dữ liệu blob sẽ được thảo luận chi tiết trong bài học tiếp theo.
- **Dịch vụ giám sát (*Monitoring service*)**: Dịch vụ giám sát theo dõi tình trạng của các nút dữ liệu và nút quản lý. Nó cảnh báo cho quản trị viên trong trường hợp xảy ra lỗi đĩa cứng (*disk failures*) cần có sự can thiệp của con người. Nó cũng thu thập thông tin về tổng dung lượng khả dụng còn lại trên các ổ đĩa để cảnh báo quản trị viên bổ sung thêm ổ đĩa.
- **Quản trị viên (*Administrator*)**: Quản trị viên chịu trách nhiệm xử lý các thông báo từ các dịch vụ giám sát và tiến hành kiểm tra định kỳ toàn bộ dịch vụ để đảm bảo độ tin cậy (*reliability*).

Kiến trúc về cách các thành phần này kết nối với nhau được thể hiện trong sơ đồ dưới đây:

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p016_00.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p016_01.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p016_02.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p016_03.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p016_04.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p016_05.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p016_06.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p016_07.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p017_00.png)

*Hình: Thiết kế chi tiết của một kho lưu trữ blob (Detailed design of a blob store)*

---

## Luồng công việc (*Workflow*)

Chúng ta mô tả luồng công việc dựa trên các thao tác cơ bản có thể thực hiện trên một kho lưu trữ blob. Giả định rằng người dùng đã đăng nhập thành công và một container đã được tạo sẵn. Một ID duy nhất (*unique ID*) được gán cho từng người dùng và từng container. Người dùng thực hiện các thao tác sau bên trong một container cụ thể:

### Ghi một blob (*Write a blob*)

1. **Client tạo yêu cầu tải lên blob (*upload blob request*)**: Nếu yêu cầu của client vượt qua bộ giới hạn tốc độ (*rate limiter*) thành công, bộ cân bằng tải (*load balancer*) sẽ chuyển tiếp yêu cầu của client đến một trong các máy chủ front-end. Máy chủ front-end sau đó gửi yêu cầu đến nút quản lý (*manager node*) để hỏi danh sách các nút dữ liệu (*data nodes*) mà nó cần liên hệ để lưu trữ blob.
2. **Nút quản lý gán ID duy nhất và chia nhỏ blob**: Nút quản lý gán cho blob một ID duy nhất bằng hệ thống tạo ID duy nhất (*unique ID generator system*). Sau đó, nó chia blob có kích thước lớn thành các chunk nhỏ hơn có kích thước cố định và chỉ định cho mỗi chunk một nút dữ liệu nơi chunk đó cuối cùng sẽ được lưu trữ. Nút quản lý xác định lượng không gian lưu trữ còn trống trên các nút dữ liệu bằng hệ thống quản lý dung lượng trống (*free-space management system*).
3. **Ghi các chunk dữ liệu**: Sau khi xác định được ánh xạ giữa các chunk và các nút dữ liệu (*mapping of chunks to data nodes*), các máy chủ front-end sẽ ghi các chunk vào các nút dữ liệu được chỉ định.
4. **Nhân bản chunk (*Chunk replication*)**: Chúng ta nhân bản (*replicate*) từng chunk nhằm mục đích dự phòng dữ liệu (*redundancy*). Mọi quyết định liên quan đến việc nhân bản chunk đều được thực hiện tại nút quản lý. Do đó, nút quản lý cũng phân bổ không gian lưu trữ và các nút dữ liệu để lưu các bản sao (*replicas*).
5. **Lưu trữ siêu dữ liệu**: Nút quản lý lưu siêu dữ liệu blob vào kho lưu trữ siêu dữ liệu (*metadata storage*). Chúng ta sẽ thảo luận chi tiết về lược đồ siêu dữ liệu (*metadata schema*) của blob trong bài học tiếp theo.
6. **Trả về đường dẫn blob**: Sau khi ghi blob thành công, đường dẫn đầy đủ (*fully qualified path*) của blob sẽ được trả về cho client. Đường dẫn này bao gồm ID người dùng (*user ID*), ID container (*container ID*) nơi người dùng thêm blob, ID blob (*blob ID*), và cấp độ truy cập (*access level*) của blob.

---

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p017_01.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p017_02.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p017_03.png)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p017_04.png)

---

> [!TIP]
> ### Vấn đề cần suy ngẫm (*Point to Ponder*)
> **Câu hỏi:** Nút quản lý (*manager node*) sẽ làm gì nếu một người dùng ghi đồng thời (*concurrently writes*) hai blob có cùng tên vào bên trong cùng một container?
> 
> **Lời giải:** Nút quản lý sẽ tuần tự hóa (*serializes*) các thao tác đó và gán một số phiên bản (*version number*) cho blob được tải lên sau.

---

### Đọc một blob (*Reading a blob*)

1. Khi yêu cầu đọc một blob gửi đến máy chủ front-end, nó sẽ yêu cầu nút quản lý cung cấp siêu dữ liệu (*metadata*) của blob đó.
2. Nút quản lý trước tiên kiểm tra xem blob đó là riêng tư (*private*) hay công khai (*public*) dựa trên đường dẫn của blob, và xác thực xem chúng ta có được phép truyền/tải blob đó hay không (*authorized to transfer*).
3. Sau khi xác thực quyền truy cập blob, nút quản lý tìm kiếm các chunk của blob đó trong kho siêu dữ liệu và tra cứu thông tin ánh xạ của chúng tới các nút dữ liệu tương ứng. Nút quản lý trả về thông tin các chunk và ánh xạ của chúng (danh sách các nút dữ liệu) về cho client.
4. Client sau đó trực tiếp đọc dữ liệu chunk từ các nút dữ liệu (*data nodes*).

> [!NOTE]
> Thông tin siêu dữ liệu phục vụ việc đọc blob được lưu vào bộ nhớ đệm (*cached*) tại máy client, nhờ đó lần tiếp theo client muốn đọc cùng một blob, chúng ta sẽ không phải tạo thêm tải lên nút quản lý (*burden the manager node*). Thêm vào đó, thao tác đọc của client ở lần tiếp theo sẽ nhanh hơn rất nhiều.

---

### **--- Trang 19 ---**

#### **Điểm cần suy ngẫm (Point to Ponder)**

##### **Câu hỏi (Question)**
Giả sử nút quản lý (*manager node*) di chuyển dữ liệu từ một nút dữ liệu (*data node*) này sang một nút dữ liệu khác do sự cố ổ đĩa sắp xảy ra. Người dùng lúc này sẽ có thông tin lỗi thời (*stale information*) nếu họ sử dụng siêu dữ liệu đã được lưu trong bộ nhớ đệm (*cached metadata*) để truy cập dữ liệu. Chúng ta xử lý các tình huống như vậy như thế nào?

##### **Ẩn câu trả lời (Hide Answer)**
Trong những trường hợp như vậy, các lệnh gọi từ phía máy khách (*client calls*) sẽ thất bại. Sau đó, máy khách (*client*) sẽ xóa bộ nhớ đệm (*flush cache*) và nạp thông tin siêu dữ liệu (*metadata*) mới từ nút quản lý (*manager node*).

#### **Xóa một Blob (Deleting a blob)**
Khi nhận được yêu cầu xóa blob, nút quản lý (*manager node*) sẽ đánh dấu blob đó là đã xóa trong siêu dữ liệu (*metadata*), và sau đó giải phóng dung lượng bằng bộ thu gom rác (*garbage collector*). Chúng ta sẽ tìm hiểu thêm về các bộ thu gom rác (*garbage collectors*) trong bài học tiếp theo.

#### **Điểm cần suy ngẫm (Point to Ponder)**

##### **Câu hỏi (Question)**
Nút quản lý (*manager node*) có thể bị coi là điểm hỏng duy nhất (*single point of failure - SPOF*) hay không? Nếu có, thì chúng ta có thể đối phó với vấn đề này như thế nào?

---

### **--- Trang 20 ---**

**Quay lại (Back)**  
Yêu cầu Thiết kế của một Blob Store (*Requirements of a Blob Store's Design…*)  
**Đánh dấu đã hoàn thành (Mark As Completed)**  
**Tiếp theo (Next)**  
Các cân nhắc thiết kế của một Blob Store (*Design Considerations of a Blob Store*)

##### **Ẩn câu trả lời (Hide Answer)**
Có, bởi vì nút quản lý (*manager node*) là điểm trung tâm của một kho lưu trữ blob (*blob store*) và là một điểm hỏng duy nhất (*single point of failure - SPOF*). Do đó, chúng ta phải có một máy chủ sao lưu (*backup server*) hoặc máy chủ bóng (*shadow server*) để thay thế cho nút quản lý (*manager node*).

Kỹ thuật mà chúng ta sử dụng cho việc này được gọi là tạo điểm kiểm tra (*checkpointing*), nghĩa là chúng ta chụp nhanh dữ liệu (*take snapshots*) tại các khoảng thời gian khác nhau. Một bản chụp nhanh (*snapshot*) sẽ ghi lại trạng thái (*state*), dữ liệu (*data*), cấu hình phần cứng (*hardware configuration*) của nút quản lý (*manager node*) đang chạy, cùng các thông điệp đang trong quá trình truyền tải (*messages in transit*) giữa nút quản lý (*manager node*) và các nút dữ liệu (*data nodes*). Kỹ thuật này duy trì nhật ký hoạt động (*operation log*) trong một vùng lưu trữ bên ngoài hoặc kho lưu trữ bản chụp nhanh (*snapshot repository*). Nếu nút quản lý (*manager node*) gặp sự cố, một hệ thống tự động hoặc quản trị viên sẽ sử dụng bản chụp nhanh (*snapshot*) đó để khởi động lại nút quản lý (*manager node*) từ trạng thái mà nó bị lỗi và phát lại nhật ký hoạt động (*replay the operation log*).

Trong bài học tiếp theo, chúng ta sẽ thảo luận về các cân nhắc thiết kế (*design considerations*) của một kho lưu trữ blob (*blob store*).

---

### **--- Trang 21 ---**

## **Các Cân nhắc Thiết kế của một Blob Store (Design Considerations of a Blob Store)**

Tìm hiểu thêm thông tin chi tiết về các khía cạnh thiết kế khác nhau của kho lưu trữ blob (*blob store*).

**Chúng ta sẽ đề cập đến các nội dung sau:**
* Giới thiệu (*Introduction*)
* Siêu dữ liệu của blob (*Blob metadata*)
* Phân vùng dữ liệu (*Partition data*)
* Lập chỉ mục blob (*Blob indexing*)
* Phân trang để liệt kê danh sách (*Pagination for listing*)
* Sao chép dữ liệu (*Replication*)
  * Sao chép đồng bộ trong cụm lưu trữ (*Synchronous replication within a storage cluster*)
  * Sao chép bất đồng bộ giữa các trung tâm dữ liệu và khu vực (*Asynchronous replication across data centers and regions*)
* Thu gom rác khi xóa một blob (*Garbage collection while deleting a blob*)
* Truyền phát một tệp (*Stream a file*)
* Lưu bộ nhớ đệm cho kho lưu trữ blob (*Cache the blob store*)

### **Giới thiệu (Introduction)**
Mặc dù chúng ta đã thảo luận chi tiết về thiết kế của hệ thống lưu trữ blob (*blob store system*) và các thành phần chính của nó trong bài học trước, nhưng vẫn còn một số câu hỏi thú vị cần được giải đáp. Ví dụ: làm thế nào để chúng ta lưu trữ các blob lớn? Chúng ta lưu trữ chúng trên cùng một đĩa, trên cùng một máy, hay chúng ta chia các blob đó thành các khối (*chunks*)? Cần tạo bao nhiêu bản sao (*replicas*) của một blob để đảm bảo độ tin cậy (*reliability*) và tính sẵn sàng (*availability*)? Làm thế nào để chúng ta tìm kiếm và truy xuất các blob một cách nhanh chóng? Đây chỉ là một vài câu hỏi có thể nảy sinh.

Bài học này giải quyết những mối quan tâm thiết kế quan trọng này. Bảng dưới đây tóm tắt các mục tiêu của bài học này.

---

### **--- Trang 22 ---**

### **Tóm tắt bài học (Summary of the Lesson)**

| Phần (Section) | Mục đích (Purpose) |
| :--- | :--- |
| **Siêu dữ liệu của blob (*Blob metadata*)** | Đây là siêu dữ liệu được duy trì nhằm đảm bảo việc lưu trữ và truy xuất các blob một cách hiệu quả. |
| **Phân vùng (*Partitioning*)** | Phần này xác định cách các blob được phân vùng giữa các nút dữ liệu (*data nodes*) khác nhau. |
| **Lập chỉ mục blob (*Blob indexing*)** | Phần này chỉ cho chúng ta cách tìm kiếm các blob một cách hiệu quả. |
| **Phân trang (*Pagination*)** | Phần này dạy chúng ta cách hình thành một phương pháp truy xuất một số lượng blob giới hạn nhằm đảm bảo cải thiện khả năng đọc và thời gian tải (*loading time*). |
| **Sao chép dữ liệu (*Replication*)** | Phần này dạy chúng ta cách sao chép các blob và cho biết chúng ta nên duy trì bao nhiêu bản sao để cải thiện tính sẵn sàng (*availability*). |
| **Thu gom rác (*Garbage collection*)** | Phần này dạy chúng ta cách xóa các blob mà không làm suy giảm hiệu năng (*performance*). |
| **Truyền phát (*Streaming*)** | Phần này dạy chúng ta cách truyền phát các tệp lớn theo từng khối (*chunk-by-chunk*) để tạo điều kiện thuận lợi cho tính tương tác của người dùng. |
| **Bộ nhớ đệm (*Caching*)** | Phần này chỉ ra cách cải thiện thời gian phản hồi (*response time / latency*) và thông lượng (*throughput*). |

Trước khi trả lời các câu hỏi được liệt kê ở trên, chúng ta hãy xem cách tạo ra các tầng trừu tượng (*layers of abstraction*) cho người dùng nhằm che giấu sự phức tạp nội bộ của một kho lưu trữ blob (*blob store*). Các tầng trừu tượng này cũng giúp chúng ta đưa ra các quyết định liên quan đến thiết kế.

**Có ba tầng trừu tượng (layers of abstractions):**
1. **Tài khoản người dùng (*User account*):** Người dùng được định danh duy nhất ở tầng này thông qua `account_ID` của họ. Các blob do người dùng tải lên được duy trì trong các vùng chứa (*containers*) của họ.
2. **Vùng chứa (*Container*):** Mỗi người dùng có một tập hợp các vùng chứa mà tất cả đều được định danh duy nhất bằng một `container_ID`. Các vùng chứa này chứa các blob.
3. **Blob:** Tầng này chứa thông tin về các blob được định danh duy nhất bằng `blob_ID` của chúng. Tầng này duy trì thông tin về siêu dữ liệu (*metadata*) của các blob, điều này tối quan trọng để đạt được tính sẵn sàng (*availability*) và độ tin cậy (*reliability*) của hệ thống.

---

### **--- Trang 23 ---**

Chúng ta có thể đưa ra các quyết định định tuyến (*routing*), lưu trữ (*storage*) và phân mảnh (*sharding*) dựa trên cơ sở các tầng này. Bảng dưới đây tóm tắt các tầng này.

### **Thông tin phân tầng (Layered Information)**

| Cấp độ (Level) | Định danh duy nhất bởi (Uniquely identified by) | Thông tin (Information) | Phân mảnh / Sharding (Sh...) |
| :--- | :--- | :--- | :--- |
| **Tài khoản kho lưu trữ blob của người dùng (*User’s blob store account*)** | `account_ID` | Danh sách các giá trị `container_ID` (*list of containers_ID values*) | theo tài khoản (*account*) |
| **Vùng chứa (*Container*)** | `container_ID` | Danh sách các giá trị `blob_ID` (*List of blob_ID values*) | theo vùng chứa (*container*) |
| **Blob** | `blob_ID` | {danh sách các khối, thông tin khối: ID các nút dữ liệu,..} (*{list of chunks, chunkInfo: data node ID's,.. }*) | theo blob |

> [!NOTE]
> **Lưu ý:** Chúng ta tạo các ID duy nhất cho tài khoản người dùng, vùng chứa và blob bằng cách sử dụng một bộ tạo ID duy nhất (*unique ID generator*).

Bên cạnh việc lưu trữ dữ liệu blob thực tế, chúng ta phải duy trì một số siêu dữ liệu (*metadata*) để quản lý việc lưu trữ blob. Hãy xem dữ liệu đó là gì.

### **Siêu dữ liệu của blob (Blob metadata)**
Khi người dùng tải lên một blob, nó được chia nhỏ thành các khối kích thước nhỏ (*small-sized chunks*) nhằm có thể hỗ trợ việc lưu trữ các tệp lớn không thể vừa vặn trong một vị trí liền kề, trong một nút dữ liệu (*data node*), hoặc trong một khối (*block*) của một đĩa gắn liền với nút dữ liệu đó. Các khối (*chunks*) của một blob đơn lẻ sau đó được lưu trữ trên các nút dữ liệu (*data nodes*) khác nhau có sẵn đủ dung lượng lưu trữ để chứa các khối này. Có hàng tỷ blob được giữ trong bộ lưu trữ. Nút quản lý (*manager node*) phải lưu trữ tất cả thông tin về các khối của blob và nơi chúng được lưu trữ, để nó có thể truy xuất các khối đó khi có thao tác đọc (*reads*). Nút quản lý (*manager node*) gán một ID cho mỗi khối (*chunk*).

Thông tin về một blob bao gồm các ID của khối (*chunk IDs*) và tên của nút dữ liệu được gán...

---

### **--- Trang 24 ---**

...cho mỗi khối (*chunk*). Chúng ta chia các blob thành các khối có kích thước bằng nhau (*equal-sized chunks*). Các khối được sao chép (*replicated*) để cho phép chúng xử lý sự cố khi nút dữ liệu gặp lỗi (*data node failure*). Do đó, chúng ta cũng lưu trữ các ID của bản sao (*replica IDs*) cho mỗi khối. Chúng ta có quyền truy cập vào tất cả thông tin liên quan đến từng blob này.

Giả sử chúng ta có một blob dung lượng 128 MB, và chúng ta chia nó thành hai khối, mỗi khối 64 MB. Siêu dữ liệu (*metadata*) cho blob này được hiển thị trong bảng sau:

### **Siêu dữ liệu Blob (Blob Metadata)**

| Khối (Chunk) | ID Nút dữ liệu (Datanode ID) | ID Bản sao 1 (Replica 1 ID) | ID Bản sao 2 (Replica 2 ID) | ID Bản sao 3 (Replica 3 ID) |
| :---: | :---: | :---: | :---: | :---: |
| **1** | `d1b1` | `r1b1` | `r2b1` | `r3b1` |
| **2** | `d1b2` | `r1b2` | `r2b2` | `r3b2` |

> [!NOTE]
> **Lưu ý:** Với tư cách là những nhà thiết kế kiến trúc (*designers*), chúng ta cần chọn một kích thước hợp lý cho khối dữ liệu của blob (*blob data chunk*). Chúng ta có thể quyết định giữ kích thước khối đã chọn cố định cho toàn bộ kho lưu trữ blob (*blob store*) (nghĩa là chúng ta không muốn cho phép các ứng dụng sử dụng các kích thước khối khác nhau cho các tệp khác nhau nhằm giảm độ phức tạp trong việc triển khai của chúng ta).
> 
> * **Nếu chọn kích thước khối quá nhỏ**, nó sẽ làm tăng kích thước siêu dữ liệu (*metadata size*) (thường tính trên mỗi khối), điều này không có lợi cho thiết kế dựa trên một nút quản lý đơn lẻ (*single manager-based design*) của chúng ta.
> * **Nếu chọn kích thước khối quá lớn**, các đĩa vật lý bên dưới có thể không ghi được dữ liệu tại các vị trí liền kề, và chúng ta có thể nhận được hiệu năng đọc/ghi (*read/write performance*) thấp hơn.
> 
> Do đó, chúng ta cần đưa ra một kích thước khối hợp lý nhằm vừa đáp ứng nhu cầu của các ứng dụng, vừa có thể mang lại hiệu năng tốt từ phần cứng bên dưới. Có nhiều biến số có thể tác động đến hiệu năng đọc/ghi, chẳng hạn như kích thước khối (*chunk size*), loại lưu trữ bên dưới (đĩa quay cơ học - *rotating disks* hoặc đĩa flash - *flash disk*), đặc tính khối lượng công việc (*workload characteristics*: đọc/ghi tuần tự - *sequential read/write* hoặc đọc/ghi ngẫu nhiên - *random read/write*, toàn bộ khối dữ liệu - *full data block* so với các thao tác đọc/ghi truyền phát - *streaming read/write operations*), v.v. Giả sử chúng ta đang sử dụng đĩa quay cơ học (*rotating disks*), nơi mà một cung từ (*sector*) là một đơn vị đọc và ghi, thì...

---

### Quản Lý Phân Khối (Chunk) & Bản Sao (Replica)

...rất có lợi khi thiết lập kích thước phân khối (*chunk size*) là một bội số nguyên của kích thước cung từ (*sector size*).

Chúng tôi duy trì ba bản sao (*three replicas*) cho mỗi khối dữ liệu (*block*). Khi ghi một đối tượng nhị phân lớn (*blob*), nút quản lý (*manager node*) sẽ xác định dữ liệu và các nút bản sao (*replica nodes*) thông qua hệ thống quản lý dung lượng trống (*free space management system*) của nó. Bên cạnh việc xử lý sự cố lỗi nút dữ liệu (*data node failure*), các nút bản sao còn được sử dụng để phục vụ các yêu cầu đọc/ghi (*read/write requests*), giúp nút sơ cấp (*primary node*) không bị quá tải (*overloaded*).

Trong ví dụ trên, kích thước blob là một bội số của chunk size, do đó manager node có thể xác định chính xác số lượng Byte cần đọc cho mỗi chunk.

> [!NOTE]
> **Điểm cần suy ngẫm (Point to Ponder)**
> 
> **Câu hỏi (Question):** Điều gì sẽ xảy ra nếu kích thước blob không phải là bội số của chunk size đã cấu hình? Làm thế nào manager node biết được cần đọc bao nhiêu Byte cho phân khối cuối cùng (*last chunk*)?
> 
> **Ẩn/Hiện câu trả lời (Hide Answer):**  
> Nếu kích thước blob không phải là bội số của chunk size, chunk cuối cùng sẽ không được chứa đầy.  
> Manager node cũng lưu giữ kích thước của từng blob để xác định số lượng Byte cần đọc cho chunk cuối cùng đó.

---

### Phân Vùng Dữ Liệu (Partition Data)

Chúng ta đã thảo luận về các tầng trừu tượng (*levels of abstraction*) khác nhau trong một kho lưu trữ đối tượng (*blob store*)—tầng tài khoản (*account layer*), tầng vùng chứa (*container layer*), và tầng đối tượng (*blob layer*). Có hàng tỷ blob được lưu trữ và truy xuất đọc. Có một số lượng rất lớn các nút dữ liệu (*data nodes*) mà chúng ta dùng để lưu trữ các blob này. Nếu chúng ta phải tìm kiếm các data node chứa các blob cụ thể trên toàn bộ tập hợp tất cả data nodes, đó sẽ là một quy trình vô cùng chậm chạp. 

Thay vào đó, chúng ta có thể gom nhóm các data node lại và gọi mỗi nhóm là một **phân vùng (*partition*)**. Chúng ta duy trì một bảng ánh xạ phân vùng (*partition map table*) chứa danh sách tất cả các blob trong mỗi partition. Nếu chúng ta phân phối các blob vào các partition khác nhau mà độc lập với mã định danh vùng chứa (*container ID*) và mã định danh tài khoản (*account ID*) của chúng, chúng ta sẽ gặp phải một vấn đề, như được minh họa trong hình ảnh sau:

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p027_00.png)

#### Hàng Tỷ Blob (Billions of blobs)
**Đường dẫn Blob (*Blob Path*):**  
`(user_ID/container_ID/blob_ID/accessType)`
* `A001/001c908/001c908b001/public`
* `A002/002c003/002c003b009/private`
* `B213/213c007/213c0067b005/private`

#### Phân Vùng Theo Dải Dựa Trên Blob ID (*Range partitioning based on blob IDs*)

| Người Dùng (*User*) | Mã Blob (*Blob_ID*) | Phân Vùng (*Partition*) |
| :--- | :--- | :--- |
| **Alice** | `[b001, b080, b043, b051]` | `[p1, p2, p1, p2]` |
| **Bob** | `[b007, b032, b092]` | `[p1, p1, p2]` |

* **Phân Vùng 1 (*Partition 1: b001–b050*)**: chứa `b001` (Alice), `b007` (Bob), `b032` (Bob), `b043` (Alice).
* **Phân Vùng 2 (*Partition 2: b051–b100*)**: chứa `b051` (Alice), `b080` (Alice), `b092` (Bob).

> [!WARNING]
> **Vấn đề (*Problem*):** Để tìm các blob thuộc về Alice, chúng ta phải tra cứu trên cả hai partition (`p1` và `p2`). Chúng ta cũng phải thực hiện cùng một quy trình tốn kém này để tìm các blob của Bob.

Việc phân vùng chỉ dựa trên các Blob ID gây ra một số vấn đề nhất định. Ví dụ: các blob thuộc cùng một container hoặc một account cụ thể có thể nằm rải rác ở các partition khác nhau, điều này làm tăng đáng kể chi phí phụ trội (*overhead*) khi đọc hoặc liệt kê (*listing*) danh sách các blob liên kết với một account hay một container cụ thể.

Để khắc phục vấn đề nêu trên, chúng ta có thể phân vùng các blob dựa trên **đường dẫn đầy đủ (*complete path*)** của blob. Khóa phân vùng (*partition key*) ở đây là sự kết hợp của:
$$\text{Partition Key} = \text{Account ID} + \text{Container ID} + \text{Blob ID}$$

Cơ chế này giúp định vị tập trung (*co-locating*) các blob của cùng một người dùng trên cùng một máy chủ phân vùng (*partition server*), từ đó gia tăng đáng kể hiệu năng (*performance*).

> [!NOTE]
> Các ánh xạ phân vùng (*partition mappings*) được duy trì bởi manager node, và các ánh xạ này được lưu trữ trong hệ thống lưu trữ siêu dữ liệu phân tán (*distributed metadata storage*).

---

### Đánh Chỉ Mục Blob (Blob Indexing)

Việc tìm kiếm các blob cụ thể giữa một biển blob khổng lồ ngày càng trở nên khó khăn và tiêu tốn nhiều thời gian khi số lượng blob được tải lên hệ thống lưu trữ tăng vọt. **Chỉ mục blob (*blob index*)** giải quyết bài toán quản lý và truy vấn blob này.

Để nạp dữ liệu cho blob index, chúng ta định nghĩa các thuộc tính thẻ khóa-giá trị (*key-value tag attributes*) trên các blob trong quá trình tải blob lên (*upload*). Chúng ta sử dụng nhiều thẻ (*tags*), chẳng hạn như: tên container (*container name*), tên blob (*blob name*), ngày giờ upload (*upload date and time*), cùng các phân loại khác như blob hình ảnh hoặc video, v.v.

Như được minh họa dưới đây, một công cụ đánh chỉ mục blob (*blob indexing engine*) sẽ đọc các thẻ mới, lập chỉ mục chúng và hiển thị chúng ra một chỉ mục blob có thể tìm kiếm được (*searchable blob index*):

```
[blob 1, blob 2, ..., blob n]
   │
   ├─► (Upload blob 2 kèm thẻ: { container name: C1, blob name: blob 2, category: image })
   │          │
   │          ▼
   │   [Indexing engine] ──(blob 2 path, tags)──► [Blob index]
   │                                                    ▲
   └─► (Truy vấn tìm kiếm: LIST blobs WHERE category=='image') ──┘
```

Chúng ta có thể phân loại blob cũng như sắp xếp (*sort*) blob bằng cách sử dụng cơ chế đánh chỉ mục. Hãy xem cách chúng ta ứng dụng chỉ mục trong kỹ thuật phân trang (*pagination*).

---

### Phân Trang Khi Liệt Kê (Pagination for Listing)

Liệt kê (*listing*) là việc trả về một danh sách các blob cho người dùng, phụ thuộc vào tiền tố (*prefix*) do người dùng nhập vào. Một tiền tố (*prefix*) là một ký tự hoặc chuỗi ký tự dùng để lọc và trả về các blob có tên bắt đầu bằng chính ký tự hoặc chuỗi ký tự đó.

Người dùng có thể muốn liệt kê tất cả các blob liên kết với một tài khoản cụ thể, tất cả các blob hiện diện bên trong một vùng chứa cụ thể, hoặc họ có thể muốn liệt kê một số blob công khai (*public blobs*) dựa trên một prefix. 

Vấn đề đặt ra là danh sách này có thể rất dài. Chúng ta không thể trả về toàn bộ danh sách cho người dùng chỉ trong một lần duy nhất. Vì vậy, chúng ta phải trả về danh sách các blob theo từng phần (*in parts*).

Giả sử một người dùng muốn lấy danh sách các blob liên kết với tài khoản của họ và có tổng cộng 2.000 blob thuộc tài khoản đó. Việc tìm kiếm, trả về và tải quá nhiều blob cùng một lúc sẽ làm suy giảm nghiêm trọng hiệu năng (*performance*). Đây chính là lúc **phân trang (*paging / pagination*)** trở nên tối quan trọng. Chúng ta có thể trả về 5 kết quả đầu tiên và cung cấp cho người dùng một nút "Next". Với mỗi lần nhấp vào nút "Next", hệ thống sẽ trả về 5 kết quả tiếp theo. Kỹ thuật này được gọi là **phân trang (*pagination*)**.

```
Request: listBlobs (accountID)
----------------------------------
 container1/foo.png
 container1/cat.jpg
 container2/table.json
 container3/myVideo.mp4
 container3/lecture1.ppt
----------------------------------
 [Previous]             [Next]
```

Các chủ sở hữu ứng dụng (*application owners*) thiết lập số lượng kết quả trả về dựa trên các yếu tố sau:
1. Khoảng thời gian họ ước tính người dùng chấp nhận chờ đợi cho một phản hồi truy vấn (*query response*).
2. Số lượng kết quả họ có thể trả về trong khoảng thời gian đó. *(Chúng tôi đưa ra con số 5 kết quả trên mỗi trang chỉ là một con số rất nhỏ dùng cho mục đích trực quan hóa minh họa).*

> [!NOTE]
> **Điểm cần suy ngẫm (Point to Ponder)**
> 
> **Câu hỏi (Question):** Làm thế nào để chúng ta quyết định 5 blob nào sẽ được trả về đầu tiên trong tổng số 2.000 blob?
> 
> **Ẩn/Hiện câu trả lời (Hide Answer):**  
> Tại đây, chúng ta tận dụng chỉ mục (*indexing*) để sắp xếp và phân loại các blob. Chúng ta phải thực hiện điều này từ trước, ngay tại thời điểm lưu trữ các blob. Nếu không, việc này sẽ trở thành một thách thức lớn tại thời điểm phải trả danh sách về cho người dùng. Có thể có hàng triệu hoặc hàng tỷ blob và chúng ta không thể sắp xếp chúng một cách nhanh chóng ngay khi nhận được yêu cầu liệt kê (*list request*).

Đối với kỹ thuật phân trang, chúng ta cần một **thẻ tiếp tục (*continuation token*)** đóng vai trò là điểm bắt đầu cho phần danh sách sẽ được trả về kế tiếp. *Continuation token* là một chuỗi mã (*string token*) được đính kèm trong phản hồi của một truy vấn nếu tổng số kết quả được truy vấn vượt quá số lượng kết quả tối đa mà chúng ta có thể trả về cùng một lúc. Do đó, nó đóng vai trò như một con trỏ (*pointer*), cho phép truy vấn kế tiếp tiếp tục chính xác tại vị trí mà chúng ta đã dừng lại trước đó.

---

### Sao Chép Dữ Liệu (Replication)

Quá trình sao chép (*replication*) được thực hiện ở hai cấp độ nhằm hỗ trợ Tính Sẵn Sàng Cao (*High Availability*) và Tính Nhất Quán Mạnh (*Strong Consistency*):
* Để giữ cho dữ liệu đạt tính nhất quán mạnh (*strongly consistent*), chúng ta **sao chép đồng bộ (*synchronously replicate*)** dữ liệu giữa các nút được dùng để phục vụ các yêu cầu đọc, ngay sau khi thực hiện thao tác ghi (*write operation*).
* Để đạt được tính sẵn sàng cao (*availability*), chúng ta có thể **sao chép dữ liệu đến các vùng (*regions*) hoặc các trung tâm dữ liệu (*data centers*) khác nhau** sau khi hoàn tất thao tác ghi. Chúng ta sẽ không phục vụ yêu cầu đọc từ trung tâm dữ liệu hoặc khu vực khác cho đến khi dữ liệu được sao chép hoàn tất tới đó.

Hai cấp độ sao chép bao gồm:
1. **Sao chép đồng bộ trong phạm vi một cụm lưu trữ (*Synchronous replication within a storage cluster*)**.
2. **Sao chép bất đồng bộ giữa các trung tâm dữ liệu và các vùng (*Asynchronous replication across data centers and regions*)**.

---

#### 1. Sao Chép Đồng Bộ Trong Cụm Lưu Trữ (Synchronous Replication within a Storage Cluster)

Một cụm lưu trữ (*storage cluster*) được cấu thành từ $N$ tủ rack chứa các nút lưu trữ (*storage nodes*), mỗi tủ rack được cấu hình như một miền chịu lỗi (*fault domain*) độc lập với hạ tầng mạng (*networking*) và nguồn điện (*power*) dự phòng.

Chúng tôi bảo đảm rằng mọi dữ liệu được ghi vào một storage cluster đều được duy trì bền bỉ (*durable*) bên trong chính storage cluster đó. Manager node duy trì đầy đủ các bản sao dữ liệu (*data replicas*) phân bổ trên các nút thuộc các miền chịu lỗi (*fault domains*) riêng biệt nhằm đảm bảo độ bền vững dữ liệu (*data durability*) bên trong cụm kể cả khi xảy ra sự cố hỏng đĩa cứng (*disk failure*), hỏng nút (*node failure*) hoặc sập toàn bộ tủ rack (*rack failure*).

> [!IMPORTANT]
> Quá trình sao chép nội cụm (*intra-cluster replication*) này được thực hiện trực tiếp trên luồng xử lý then chốt (*critical path*) của các yêu cầu ghi từ máy khách (*client's write requests*).

Tín hiệu thành công (*success*) chỉ có thể được trả về cho client sau khi một thao tác ghi đã được sao chép đồng bộ thành công bên trong storage cluster đó. Cơ chế này cho phép thực hiện các thao tác ghi nhanh chóng bởi vì:
* Chúng ta sao chép dữ liệu bên trong một storage cluster nơi tất cả các nút đều nằm gần nhau về mặt vật lý, từ đó giảm thiểu độ trễ (*latency*).
* Chúng ta sử dụng kỹ thuật sao chép dữ liệu song song (*in-lined data copying*), tận dụng các đường truyền mạng dự phòng để sao chép dữ liệu tới tất cả các bản sao song song cùng một lúc.

Kỹ thuật sao chép này giúp duy trì tính nhất quán dữ liệu (*data consistency*) và tính sẵn sàng (*availability*) bên trong cụm lưu trữ.

---

#### 2. Sao Chép Bất Đồng Bộ Giữa Các Trung Tâm Dữ Liệu và Khu Vực (Asynchronous Replication across Data Centers and Regions)

Các trung tâm dữ liệu (*data centers*) của hệ thống blob store hiện diện ở nhiều khu vực (*regions*) khác nhau—ví dụ: Châu Á - Thái Bình Dương (Asia-Pacific), Châu Âu (Europe), Miền Đông Hoa Kỳ (Eastern US), và nhiều nơi khác.

Trong mỗi region, chúng ta thiết lập nhiều hơn một data center đặt tại các vị trí địa lý khác nhau; nhờ vậy, nếu một data center gặp sự cố ngừng hoạt động (*goes down*), chúng ta luôn có các data center khác trong cùng region sẵn sàng tiếp quản và phục vụ các yêu cầu của người dùng.

Có tối thiểu ba trung tâm dữ liệu (*minimum of three data centers*) bên trong mỗi khu vực, mỗi trung tâm được đặt cách nhau nhiều dặm (*miles*) để phòng ngừa và bảo vệ hệ thống trước các thảm họa cục bộ như hỏa hoạn, lũ lụt, v.v.

---

# THIẾT KẾ HỆ THỐNG LƯU TRỮ ĐỐI TƯỢNG (BLOB STORE)

---

### [Trang 31]

Số lượng bản sao của một blob được gọi là **hệ số nhân bản** (*replication factor*). Phần lớn các trường hợp, hệ số nhân bản bằng **3** là đã đủ đáp ứng yêu cầu.

Đây là các khu vực (*regions*) và các vùng khả dụng (*availability zones*). Màu vàng đậm đại diện cho dữ liệu sơ cấp (*primary data*) và màu vàng nhạt là các bản sao (*replicas*).

* **Trung tâm dữ liệu 1** (*Data center 1*)
* **Trung tâm dữ liệu n** (*Data center n*)
* **Trung tâm dữ liệu 2** (*Data center 2*)
* **Châu Á - Thái Bình Dương (Mumbai)** (*Asia-Pacific (Mumbai)*)
* **Trung tâm dữ liệu 1** (*Data center 1*)
* **Trung tâm dữ liệu n** (*Data center n*)
* **Trung tâm dữ liệu 2** (*Data center 2*)
* **Trung tâm dữ liệu 1** (*Data center 1*)
* **Trung tâm dữ liệu n** (*Data center n*)
* **Trung tâm dữ liệu 2** (*Data center 2*)
* **Bản chính** (*Primary*)
* **Bản sao** (*Replica*)
* **Châu Âu (Paris)** (*Europe (Paris)*)
* **Đông Hoa Kỳ (Bắc Virginia)** (*Eastern US (N. Virginia)*)

Chúng ta duy trì **4 bản sao** của một blob:
1. **Bản sao cục bộ (Local copy):** Được đặt bên trong trung tâm dữ liệu (*data center*) thuộc khu vực sơ cấp (*primary region*) nhằm phòng ngừa sự cố hỏng tủ rack máy chủ (*server rack failure*) và hỏng ổ đĩa cứng (*drive failures*).
2. **Bản sao thứ hai:** Được đặt tại một trung tâm dữ liệu khác nằm trong cùng một khu vực (*same region*) nhằm bảo vệ hệ thống trước các thảm họa như hỏa hoạn hoặc ngập lụt tại trung tâm dữ liệu.
3. **Bản sao thứ ba (và thứ tư):** Được đặt tại trung tâm dữ liệu thuộc một khu vực địa lý khác (*different region*) để phòng chống các thảm họa quy mô toàn vùng (*regional disasters*).

---

### Thu dọn rác khi xóa một Blob (*Garbage collection while deleting a blob*)

Do các phân đoạn blob (*blob chunks*) được phân tán tại nhiều nút dữ liệu (*data nodes*) khác nhau, việc thực hiện xóa đồng thời từ nhiều nút phân tán sẽ tiêu tốn thời gian, và việc bắt phía máy khách (*client*) phải treo kết nối chờ đợi cho tới khi tiến trình đó hoàn tất không phải là một giải pháp khả thi. 

Nhằm tối ưu hóa độ trễ thời gian thực (*real-time latency optimization*), chúng ta không thực sự xóa blob ra khỏi kho lưu trữ blob (*blob store*) ngay khi nhận được yêu cầu xóa (*delete request*). Thay vào đó, chúng ta chỉ đánh dấu blob đó là **"DELETED"** (Đã xóa) trong siêu dữ liệu (*metadata*) để người dùng không thể truy cập được nữa. Blob vật lý sẽ được xóa bỏ sau đó, sau khi hệ thống đã gửi phản hồi thành công cho yêu cầu xóa của người dùng.

> [!NOTE]
> Việc đánh dấu blob là đã xóa nhưng chưa thực sự giải phóng trên đĩa cứng ngay tại thời điểm đó sẽ gây ra tình trạng **bất nhất siêu dữ liệu nội bộ** (*internal metadata inconsistencies*). Điều này có nghĩa là các tài nguyên tiếp tục chiếm dụng không gian lưu trữ mà đáng lẽ ra phải được giải phóng.

Tuy nhiên, các bất nhất siêu dữ liệu này **hoàn toàn không gây ảnh hưởng gì tới người dùng**. Ví dụ:

---

### [Trang 32]

Đối với một blob đã được đánh dấu là xóa trong metadata, chúng ta vẫn còn giữ các bản ghi đại diện cho các chunk của blob đó trong metadata. Các nút dữ liệu (*data nodes*) vẫn đang nắm giữ các chunk vật lý của blob đó. 

Do đó, chúng ta triển khai một dịch vụ chuyên trách gọi là **Trình thu dọn rác** (*Garbage Collector*) để dọn dẹp các điểm bất nhất siêu dữ liệu này sau. Việc xóa bỏ một blob về sau sẽ giải phóng toàn bộ các chunk liên kết với blob đó. 

> [!IMPORTANT]
> Sẽ tồn tại một khoảng thời gian trễ đáng kể (*appreciable time delay*) tính từ thời điểm blob bị người dùng xóa cho đến khi dung lượng trống trong kho lưu trữ blob tăng lên tương ứng. Chúng ta chấp nhận độ trễ thời gian này, bởi vì đổi lại, hệ thống mang lại lợi ích phản hồi thời gian thực cực nhanh (*real-time fast response*) đối với yêu cầu xóa blob của người dùng.

Toàn bộ quy trình xóa được minh họa qua các bước tuần tự dưới đây:

---

#### Bước 1 / 10
* **Disk 1**: Đang chứa 3 blob: `b020`, `b903`, `b883`.
* **Metadata - Thông tin Ổ đĩa (Disk Info):**
  * `Disk_ID: 1` | `List of blobs: [b020, b903, b883]`
* **Metadata - Thông tin Blob (Blob Info):**
  * `Blob_ID: b020` | `Location: Disk 1`
  * `Blob_ID: b903` | `Location: Disk 1`
  * `Blob_ID: b883` | `Location: Disk 1`
* **Tổng dung lượng lưu trữ (Total storage):** `6 GB`
* **Người dùng (User) | Xóa blob (Delete blob) | Garbage collector**

> **Mô tả:** Ba blob được tải lên kho lưu trữ blob. Ổ đĩa 1 (*Disk 1*) đang lưu trữ toàn bộ cả ba blob này.  
> *(1 of 10)*

---

### [Trang 33]

#### Bước 2 / 10
* **Disk 1**: Đang chứa `b020`, `b903`, `b883`.
* **Metadata - Thông tin Ổ đĩa (Disk Info):**
  * `Disk_ID: 1` | `List of blobs: [b020, b903, b883]`
* **Metadata - Thông tin Blob (Blob Info):**
  * `Blob_ID: b020` | `Location: Disk 1`
  * `Blob_ID: b903` | `Location: Disk 1`
  * `Blob_ID: b883` | `Location: Disk 1`
* **Tổng dung lượng lưu trữ:** `6 GB`
* **Yêu cầu xóa:** `b903` từ Người dùng (*User*).

> **Mô tả:** Một người dùng gửi yêu cầu xóa blob có định danh là `b903`.  
> *(2 of 10)*

---

#### Bước 3 / 10
* **Disk 1**: Đang chứa `b020`, `b903`, `b883`.
* **Metadata - Thông tin Ổ đĩa (Disk Info):**
  * `Disk_ID: 1` | `List of blobs: [b020, b903, b883]`
* **Metadata - Thông tin Blob (Blob Info):**
  * `Blob_ID: b020` | `Location: Disk 1`
  * `Blob_ID: b903` | `Location: Disk 1`
  * `Blob_ID: b883` | `Location: Disk 1`
* **Tổng dung lượng lưu trữ:** `6 GB`
* **Hành động:** Delete Blob API tra cứu vào Bảng Blob (*Blob Table*) để chuẩn bị xóa `b903`.

> **Mô tả:** Giao diện lập trình ứng dụng Xóa Blob (*Delete Blob API*) tra cứu vào Bảng Blob (*Blob Table*) để xóa `b903`.  
> *(3 of 10)*

---

### [Trang 34]

#### Bước 4 / 10
* **Disk 1**: Đang chứa `b020`, `b903`, `b883`.
* **Metadata - Thông tin Ổ đĩa (Disk Info):**
  * `Disk_ID: 1` | `List of blobs: [b020, b903, b883]`
* **Metadata - Thông tin Blob (Blob Info):**
  * `Blob_ID: b020` | `Location: Disk 1`
  * `Blob_ID: b883` | `Location: Disk 1`
  * *(Bản ghi `b903 Disk 1` đã được gỡ khỏi bảng và chuyển sang bộ thu dọn rác)*
* **Tổng dung lượng lưu trữ:** `6 GB`
* **Garbage Collector:** Tiếp nhận thông tin `b903 Disk 1`.

> **Mô tả:** Bản ghi cho blob `b903` bị xóa khỏi Bảng Blob (*Blob Table*) để không ai có thể truy cập blob này được nữa. Trình thu dọn rác (*Garbage collector*) tiến hành thu nhận bản ghi của blob này.  
> *(4 of 10)*

---

#### Bước 5 / 10
* **Disk 1**: Đang chứa `b020`, `b903`, `b883`.
* **Metadata - Thông tin Ổ đĩa (Disk Info):**
  * `Disk_ID: 1` | `List of blobs: [b020, b903, b883]`
* **Metadata - Thông tin Blob (Blob Info):**
  * `Blob_ID: b020` | `Location: Disk 1`
  * `Blob_ID: b883` | `Location: Disk 1`
* **Tổng dung lượng lưu trữ:** `6 GB`
* **Trạng thái:** `b903 Disk 1 - deleted` (đã đánh dấu xóa).
* **Tín hiệu xác nhận:** Gửi gói xác nhận (*acknowledgment - ACK*) ngược lại cho Delete Blob API.

> **Mô tả:** Sau khi đánh dấu blob là đã xóa, một thông điệp xác nhận (*acknowledgment*) được gửi về cho Delete Blob API.  
> *(5 of 10)*

---

### [Trang 35]

#### Bước 6 / 10
* **Disk 1**: Đang chứa `b020`, `b903`, `b883`.
* **Metadata - Thông tin Ổ đĩa (Disk Info):**
  * `Disk_ID: 1` | `List of blobs: [b020, b903, b883]`
* **Metadata - Thông tin Blob (Blob Info):**
  * `Blob_ID: b020` | `Location: Disk 1`
  * `Blob_ID: b883` | `Location: Disk 1`
* **Tổng dung lượng lưu trữ:** `6 GB`
* **Trạng thái:** `b903 Disk 1 - deleted`.
* **Phản hồi:** Trả về cho Người dùng (*User*).

> **Mô tả:** Delete Blob API phản hồi nhanh chóng cho người dùng thông báo rằng blob đã được xóa thành công.  
> *(6 of 10)*

---

#### Bước 7 / 10
* **Disk 1**: Đang chứa `b020`, `b903`, `b883`.
  * *Disk 1 thông báo:* **"Tôi đang có ba blob!"** (*"I have three blobs!"*)
* **Metadata - Thông tin Ổ đĩa (Disk Info):**
  * `Disk_ID: 1` | `List of blobs: [b020, b903, b883]`
* **Metadata - Thông tin Blob (Blob Info):**
  * `Blob_ID: b020` | `Location: Disk 1`
  * `Blob_ID: b883` | `Location: Disk 1`
  * *Metadata ghi nhận:* **"Chỉ có hai blob trên Disk 1!"** (*"Two blobs on Disk 1!"*)
* **Tổng dung lượng lưu trữ:** `6 GB`
* **Trình thu dọn rác (Garbage collector):** Đang giữ `b903 Disk 1`.

> **Mô tả:** Yêu cầu của người dùng đã được xử lý nhanh chóng, nhưng hiện tại đang tồn tại sự bất nhất siêu dữ liệu (*metadata inconsistencies*). Sau đó, trình thu dọn rác (*garbage collector*) sẽ dọn dẹp những điểm bất nhất này.  
> *(7 of 10)*

---

### [Trang 36]

#### Bước 8 / 10
* **Disk 1**: 
  * Đang chứa `b020`, `b883`.
  * Đang thực hiện: **Giải phóng không gian lưu trữ đã chiếm dụng cho b903** (*free space occupied for b903*).
  * *Disk 1 thông báo:* **"Tôi đang có ba blob!"** (*"I have three blobs!"*)
* **Metadata - Thông tin Ổ đĩa (Disk Info):**
  * `Disk_ID: 1` | `List of blobs: [b020, b903, b883]`
* **Metadata - Thông tin Blob (Blob Info):**
  * `Blob_ID: b020` | `Location: Disk 1`
  * `Blob_ID: b883` | `Location: Disk 1`
  * *Metadata:* **"Có hai blob trên Disk 1!"** (*"Two blobs on Disk 1!"*)
* **Tổng dung lượng lưu trữ:** `6 GB`
* **Garbage Collector:** Thực hiện xóa các Byte vật lý của `b903` trên Ổ đĩa 1 (*Disk 1*).

> **Mô tả:** Trình thu dọn rác (*garbage collector*) tiến hành xóa các Byte dữ liệu đã ghi của `b903` khỏi Ổ đĩa 1 (*Disk 1*).  
> *(8 of 10)*

---

#### Bước 9 / 10
* **Disk 1**: Đang chứa `b020`, `b883`.
  * *Disk 1:* Chuẩn bị cập nhật danh sách blob thực tế.
* **Metadata - Thông tin Ổ đĩa (Disk Info):**
  * `Disk_ID: 1` | `List of blobs: [b020, b903, b883]` *(Đang chuẩn bị nhận bản cập nhật)*
* **Metadata - Thông tin Blob (Blob Info):**
  * `Blob_ID: b020` | `Location: Disk 1`
  * `Blob_ID: b883` | `Location: Disk 1`
  * *Metadata:* **"Có hai blob trên Disk 1!"** (*"Two blobs on Disk 1!"*)
* **Tổng dung lượng lưu trữ:** `6 GB`
* **Garbage Collector**

> **Mô tả:** Một tiến trình của nút dữ liệu (*data node process*) chạy trực tiếp trên ổ đĩa sẽ cập nhật cho nút siêu dữ liệu (*metadata node*) về danh sách blob mới nhất mà nó đang thực tế lưu trữ.  
> *(9 of 10)*

---

# Thiết Kế Kho Lưu Trữ Đối Tượng Lớn (Design of a Blob Store)

### Dọn Dẹp Rác và Đồng Bộ Trạng Thái (Garbage Collection & State Reconciliation)

| Bảng Thông Tin Ổ Đĩa (Disk Info) | |
| :--- | :--- |
| **Mã ổ đĩa (Disk_ID)** | **Danh sách các blob (List of blobs)** |
| 1 | `[b020, b883]` |

| Bảng Thông Tin Blob (Blob Info) | |
| :--- | :--- |
| **Mã Blob (Blob_ID)** | **Vị trí lưu trữ (Location)** |
| `b020` | Disk 1 |
| `b883` | Disk 1 |

* **Tổng dung lượng lưu trữ (Total storage):** 6 GB
* **Dữ liệu đặc tả (Metadata)**
* **Người dùng (User):** Yêu cầu xóa blob (`Delete blob`)
* **Bộ dọn rác (Garbage collector):** *"Có hai blob trên Disk 1! (Two blobs on Disk 1!)"*
* **Disk 1:** *"Tôi đang chứa hai blob! (I have two blobs!)"*
* **Nút metadata (The metadata node):** Cập nhật bảng `Disk Info`. Tình trạng bất đồng bộ dữ liệu (inconsistencies) đã được loại bỏ hoàn toàn.
* **Tiến trình:** Bước 10 / 10

---

### Truyền Phát Một Tệp Tin (Stream a File)

Để truyền phát một tệp tin (stream a file), chúng ta cần xác định lượng dữ liệu tính theo Byte được phép đọc trong mỗi lần truy vấn. 

Giả sử mỗi lần chúng ta đọc $X$ Bytes:
* Lần đầu tiên, ta đọc $X$ Bytes đầu tiên bắt đầu từ Byte thứ 0 (từ $0$ đến $X - 1$).
* Lần tiếp theo, ta đọc tiếp $X$ Bytes kế tiếp (từ $X$ đến $2X - 1$).

> [!NOTE]
> **Điểm Cần Suy Ngẫm (Point to Ponder)**
> 
> **Câu hỏi (Question):** Làm thế nào để hệ thống biết được những Byte nào đã được đọc trước đó và những Byte nào cần phải đọc tiếp theo?
> 
> **Ẩn/Hiện câu trả lời (Hide/Show Answer):**
> Chúng ta có thể sử dụng một giá trị độ lệch (**offset**) để theo dõi chỉ mục Byte mà từ đó hệ thống cần tiếp tục đọc lại.

---

### Bộ Nhớ Đệm Cho Kho Lưu Trữ Blob (Cache the Blob Store)

Quá trình lưu bộ nhớ đệm (caching) có thể diễn ra ở nhiều tầng kiến trúc khác nhau. Dưới đây là một số ví dụ điển hình:

* **Metadata của các chunk (khối dữ liệu) thuộc blob:** Được lưu đệm ở phía máy khách (client-side) ngay trong lần đọc đầu tiên. Khi đó, client có thể truy cập trực tiếp tới các nút dữ liệu (**data nodes**) mà không cần giao tiếp lại với nút quản lý (**manager node**) khi muốn đọc cùng một blob ở lần thứ hai.
* **Tại các máy chủ tiền tuyến (front-end servers):** Chúng ta lưu đệm bản đồ phân vùng (**partition map**) và sử dụng nó để xác định máy chủ phân vùng (**partition server**) nào sẽ tiếp nhận và xử lý từng yêu cầu được chuyển tiếp đến.
* **Các chunk được truy cập thường xuyên (frequently accessed chunks):** Được lưu đệm trực tiếp tại nút quản lý (**manager node**), giúp quá trình truyền phát các đối tượng lớn (streaming large objects) diễn ra với hiệu năng cao, đồng thời giảm thiểu đáng kể các thao tác vào/ra ổ đĩa vật lý (**disk I/O**).

> [!NOTE]
> **Lưu ý:** Việc tạo bộ nhớ đệm cho kho lưu trữ blob thường được thực hiện thông qua mạng phân phối nội dung (**CDN - Content Delivery Network**). Dịch vụ Azure Blob Storage lưu đệm các blob có quyền truy cập công khai vào mạng Azure CDN cho đến khi giá trị thời gian sống (**TTL - Time-To-Live**) của blob đó hết hạn. Máy chủ gốc (origin server) sẽ xác định giá trị TTL này, và CDN sẽ nhận biết nó thông qua tiêu đề `Cache-Control` trong phản hồi HTTP từ máy chủ gốc.

Chúng ta đã xem xét toàn bộ các yếu tố thiết kế cần cân nhắc khi xây dựng một hệ thống lưu trữ blob. Bây giờ, chúng ta sẽ tiến hành đánh giá chi tiết thiết kế đã đề xuất.

---

# Đánh Giá Thiết Kế Của Kho Lưu Trữ Blob (Evaluation of a Blob Store's Design)

Xem xét cách thức thiết kế kho lưu trữ blob của chúng ta đáp ứng đầy đủ các yêu cầu hệ thống đề ra.

**Nội dung bao gồm:**
* Tính sẵn sàng (**Availability**)
* Độ bền vững dữ liệu (**Durability**)
* Khả năng mở rộng (**Scalability**)
* Băng thông / Thông lượng (**Throughput**)
* Độ tin cậy (**Reliability**)
* Tính nhất quán (**Consistency**)
* Kết luận (**Conclusion**)

Hãy cùng đánh giá chi tiết cách thiết kế giúp chúng ta đạt được các mục tiêu kỹ thuật này:

---

### Tính Sẵn Sàng (Availability)

Thành phần nhân bản dữ liệu (**replication**) trong thiết kế đóng vai trò quyết định đảm bảo tính sẵn sàng cao (**High Availability**) cho toàn hệ thống:

* **Đối với các yêu cầu đọc (Read Requests):** Chúng ta duy trì bốn bản sao (**4 replicas**) cho mỗi blob. Nhờ có các bản sao này, hệ thống có thể phân phối đều tải lưu lượng truy vấn (**load balancing**). Nếu một nút gặp sự cố (**node failure**), nút bản sao khác có thể lập tức phục vụ yêu cầu thay thế.
* **Chiến lược đặt bản sao (Replica Placement Strategy):** Có khả năng chống chịu việc hỏng hóc toàn bộ một trung tâm dữ liệu (**data center failure**), thậm chí ứng phó được tình trạng mất kết nối hoặc tê liệt toàn bộ một vùng địa lý (**region unavailability**) do thiên tai, thảm họa.
* **Dịch vụ giám sát (Monitoring Service):** Đảm bảo luôn có đủ số lượng bản sao khả dụng tại bất kỳ thời điểm nào. Hệ thống sẽ chủ động tạo bản sao dữ liệu kịp thời nếu số lượng bản sao bị lỗi vượt quá một ngưỡng (**threshold**) quy định.
* **Đối với các yêu cầu ghi (Write Requests):** Dữ liệu được nhân bản bên trong cụm (cluster) theo cơ chế chịu lỗi (**fault-tolerant**) và nhanh chóng phản hồi kết quả về cho người dùng, đảm bảo tính sẵn sàng tối đa cho các tác vụ ghi.
* **Đối với nút quản lý (Manager Node):** Để duy trì tính sẵn sàng của manager node, chúng ta liên tục lưu bản sao lưu dự phòng trạng thái (**state backup**) của nó. Trong trường hợp nút quản lý gặp sự cố, một phiên bản (instance) mới của nút quản lý sẽ được khởi tạo ngay lập tức từ trạng thái đã lưu trữ trước đó.

---

### Độ Bền Vững Dữ Liệu (Durability)

Các dịch vụ nhân bản (**replication**) và giám sát (**monitoring**) kết hợp cùng nhau để bảo đảm độ bền vững dữ liệu tuyệt đối:

* Dữ liệu một khi đã tải lên thành công sẽ được nhân bản đồng bộ (**synchronously replicated**) bên trong cụm lưu trữ. Nếu xảy ra mất mát dữ liệu tại một nút, chúng ta hoàn toàn có thể khôi phục lại dữ liệu từ các nút khác.
* Dịch vụ giám sát liên tục theo dõi tình trạng của các ổ đĩa lưu trữ. Nếu phát hiện bất kỳ ổ đĩa nào bị hỏng, dịch vụ giám sát sẽ phát cảnh báo đến các quản trị viên để thay thế ổ đĩa, đồng thời gửi thông điệp đến nút quản lý để sao chép toàn bộ nội dung trên ổ đĩa lỗi sang một ổ đĩa khả dụng khác hoặc một ổ đĩa mới vừa được bổ sung. Sau đó, nút quản lý sẽ cập nhật lại bảng ánh xạ (**mapping table**) tương ứng.

#### Các Cam Kết Do Kho Lưu Trữ Blob Cung Cấp (Guarantees provided by the blob store)

* Băng thông / Thông lượng (**Throughput**)
* Khả năng mở rộng (**Scalability**)
* Độ tin cậy (**Reliability**)
* Tính sẵn sàng (**Availability**)
* Tính nhất quán (**Consistency**)
* Độ bền vững (**Durability**)

![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p041_00.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p041_01.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p041_02.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p041_03.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p041_04.png)
![020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](images/topic_020_p041_05.png)

---

### Khả Năng Mở Rộng (Scalability)

Chiến lược phân vùng (**partitioning**) và chia nhỏ các blob thành các chunk (khối) có kích thước nhỏ giúp hệ thống có thể mở rộng quy mô phục vụ hàng tỷ yêu cầu truy xuất blob:

* Các blob được phân vùng thành các dải phạm vi riêng biệt (**ranges**) và được phục vụ bởi các máy chủ phân vùng (**partition servers**) khác nhau.
* Các bảng ánh xạ phân vùng (**partition mappings**) xác định rõ ràng máy chủ phân vùng nào sẽ chịu trách nhiệm phục vụ yêu cầu cho dải blob cụ thể nào.
* Cơ chế phân vùng cũng tự động cân bằng tải (**automatic load balancing**) giữa các máy chủ phân vùng nhằm đáp ứng linh hoạt nhu cầu lưu lượng truy cập của các blob.
* Hệ thống có khả năng **mở rộng theo chiều ngang (horizontally scalable)** đối với tầng lưu trữ. Bất cứ khi nào phát sinh nhu cầu dung lượng, chúng ta chỉ cần bổ sung thêm các nút dữ liệu (**data nodes**).
* Tuy nhiên, ở một ngưỡng quy mô nhất định, nút quản lý (**manager node**) có thể trở thành điểm nghẽn cổ chai (**bottleneck**). Một nút quản lý đơn lẻ có thể xử lý khoảng **10.000 truy vấn mỗi giây (10,000 QPS - Queries Per Second)**.

> [!NOTE]
> **Điểm Cần Suy Ngẫm (Point to Ponder)**
> 
> **Câu hỏi (Question):** Làm thế nào để chúng ta có thể tiếp tục mở rộng quy mô khi máy chủ quản lý chạm ngưỡng giới hạn hiệu năng và chúng ta không thể tăng thêm năng lực tính toán của nó bằng phương pháp mở rộng theo chiều dọc (**vertical scaling**)?
> 
> **Ẩn/Hiện câu trả lời (Hide/Show Answer):**
> Chúng ta có thể tạo ra hai phiên bản hệ thống độc lập (**independent instances**). Mỗi phiên bản sẽ sở hữu một nút quản lý riêng biệt cùng một tập hợp các nút dữ liệu đi kèm. Việc triển khai các hệ thống có kiến trúc tương tự như thiết kế của chúng ta đã được chứng minh thực tế là có thể mở rộng lên đến quy mô **vài petabyte (PB)**. Do đó, việc khởi tạo thêm các phiên bản bổ sung sẽ giúp chúng ta tiếp tục mở rộng quy mô hệ thống.
> 
> Tuy nhiên, để mở rộng quy mô sâu hơn nữa bên trong cùng một phiên bản đơn lẻ, chúng ta sẽ cần đến một thiết kế mới phức tạp hơn rất nhiều.

---

### Băng Thông / Thông Lượng (Throughput)

* Chúng ta lưu trữ các chunk của cùng một blob trên nhiều nút dữ liệu (**data nodes**) khác nhau, giúp phân tán các yêu cầu truy xuất của một blob ra nhiều máy chủ vật lý.
* Việc nạp song song các chunk (**parallel fetching of chunks**) từ nhiều nút dữ liệu giúp hệ thống đạt được **băng thông cực lớn (high throughput)**.
* Thêm vào đó, việc thiết lập bộ nhớ đệm (**caching**) đa tầng — từ phía máy khách (**client-side**), các máy chủ tiền tuyến (**front-end servers**) cho đến nút quản lý (**manager node**) — giúp cải thiện vượt bậc thông lượng của toàn hệ thống và giảm thiểu tối đa độ trễ (**latency**).

---

### Độ Tin Cậy (Reliability)

*(Nội dung tiếp tục ở các phần sau...)*

---

### --- Trang 43 ---

Chúng tôi đạt được **độ tin cậy** (*reliability*) thông qua các kỹ thuật giám sát (*monitoring techniques*). Ví dụ, giao thức nhịp tim (**heartbeat protocol**) liên tục cập nhật trạng thái của các nút dữ liệu (**data nodes**) cho nút quản lý (**manager node**). Điều này cho phép nút quản lý chỉ yêu cầu dữ liệu từ các nút đáng tin cậy. Hơn nữa, nó thực hiện các biện pháp phòng ngừa cần thiết nhằm đảm bảo dịch vụ luôn đáng tin cậy. Chẳng hạn, sự cố lỗi của một nút (*node failure*) sẽ kích hoạt nút quản lý yêu cầu một nút bản sao bổ sung (**additional replica node**).

Các dịch vụ giám sát (*monitoring services*) cũng gửi cảnh báo đến các quản trị viên (*administrators*) để thay thế phần cứng bị lỗi như ổ đĩa hỏng (*failed disks*) hoặc các liên kết mạng/thiết bị chuyển mạch bị đứt gãy (*broken network links or switches*). Để đảm bảo dịch vụ hoạt động tin cậy, nút quản lý sẽ theo dõi dung lượng trống còn lại trên ổ đĩa. Nếu dung lượng khả dụng còn lại chạm tới một ngưỡng nhất định (*certain threshold*), một cảnh báo sẽ được gửi tới các quản trị viên để bổ sung các ổ đĩa mới.

#### Tính nhất quán (Consistency)

Chúng tôi sao chép đồng bộ (**synchronously replicate**) các khối dữ liệu trên đĩa (*disk data blocks*) bên trong một cụm lưu trữ (**storage cluster**) ngay khi có yêu cầu ghi (**write request**), giúp dữ liệu đạt được **tính nhất quán mạnh** (**strongly consistent**) bên trong cụm lưu trữ đó. Quá trình này được thực hiện trực tiếp trên luồng xử lý quan trọng của người dùng (**user’s critical path**). Chúng tôi phục vụ các yêu cầu đọc (**read requests**) tiếp theo đối với dữ liệu này từ chính cụm lưu trữ đó cho đến khi chúng tôi chưa sao chép dữ liệu này sang một trung tâm dữ liệu (**data center**) khác và/hoặc trên các cụm lưu trữ khác.

> [!NOTE]  
> Sau khi phản hồi yêu cầu ghi và hoàn tất việc sao chép dữ liệu bên trong cụm lưu trữ, chúng tôi tiến hành **sao chép bất đồng bộ** (**asynchronously replicate**) các blob tới các trung tâm dữ liệu đặt ở xa hoặc ở các khu vực khác (**regions**) nhằm đảm bảo **tính sẵn sàng** (**High Availability**).

#### Kết luận (Conclusion)

Chúng ta đã thấy rằng kho lưu trữ blob (**blob store**) được thiết kế để lưu trữ dữ liệu phi cấu trúc (*unstructured data*) và có kích thước lớn. Một kho lưu trữ blob giúp các ứng dụng lưu trữ hình ảnh, video, âm thanh, v.v. Ngày nay, nó được sử dụng bởi rất nhiều ứng dụng lớn như YouTube, Facebook, Instagram, Twitter và nhiều nền tảng khác. Chúng tôi đã thiết kế một hệ thống nơi người dùng có thể thực hiện chức năng cơ bản của một kho lưu trữ blob. Cuối cùng, chúng tôi đã đánh giá thiết kế của mình dựa trên các **yêu cầu phi chức năng** (**non-functional requirements**).

---

### --- Trang 44 ---

* **Quay lại (Back):** Các cân nhắc thiết kế của một kho lưu trữ Blob (*Design Considerations of a Blob Store*)
* **Đánh dấu đã hoàn thành (Mark As Completed)**
* **Tiếp theo (Next):** Bài trắc nghiệm về Thiết kế của Kho lưu trữ Blob (*Quiz on the Blob Store's Design*)


---

[← Bài trước](019-gioi-han-tan-suat-rate-limiter.md) | [Mục lục](README.md) | [Bài tiếp theo →](021-tim-kiem-phan-tan-distributed-search.md)
