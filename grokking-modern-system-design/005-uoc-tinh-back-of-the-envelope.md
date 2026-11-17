# 005 - Kỹ Năng Ước Tính Đại Khái (Back-of-the-envelope Calculations)

[← Bài trước](004-dac-tinh-phi-chuc-nang.md) | [Mục lục](README.md) | [Bài tiếp theo →](006-gioi-thieu-building-blocks.md)

---


# Đặt Các Con Số Ước Tính Đại Khái (Back-of-the-envelope Numbers) Vào Đúng Bối Cảnh Thực Tế

Học cách sử dụng các con số phù hợp trong các phép tính toán ước tính đại khái (*back-of-the-envelope calculations*).

---

### Chúng ta sẽ tìm hiểu các nội dung sau:
* Tại sao chúng ta lại sử dụng các phép tính ước tính đại khái (*back-of-the-envelope calculations*)?
* Các loại máy chủ trong trung tâm dữ liệu (*Types of data center servers*)
  * Máy chủ web (*Web servers*)
  * Máy chủ ứng dụng (*Application servers*)
  * Máy chủ lưu trữ (*Storage servers*)
* Các con số tiêu chuẩn cần ghi nhớ (*Standard numbers to remember*)
* Ước tính số lượng yêu cầu (*Requests estimation*)

---

## Tại sao chúng ta lại sử dụng các phép tính ước tính đại khái (Back-of-the-envelope Calculations)?

Một hệ thống phân tán (*Distributed System*) bao gồm các nút tính toán (*compute nodes*) được kết nối với nhau thông qua mạng (*network*). Có rất nhiều loại nút tính toán sẵn có khác nhau và chúng có thể được liên kết theo vô số phương thức đa dạng. Các phép tính ước tính đại khái (*back-of-the-envelope calculations*) giúp chúng ta tạm gác lại những chi tiết vụn vặt, tiểu tiết của hệ thống (ít nhất là ở cấp độ thiết kế kiến trúc) để tập trung vào các khía cạnh quan trọng hơn.

Một số ví dụ về phép tính ước tính đại khái có thể kể đến:
* **Số lượng kết nối TCP đồng thời (*concurrent TCP connections*)** mà một máy chủ có thể hỗ trợ.
* **Số lượng yêu cầu mỗi giây (*Requests Per Second - RPS*)** mà một máy chủ web (*web server*), cơ sở dữ liệu (*database server*), hoặc bộ nhớ đệm (*cache server*) có thể xử lý.
* **Yêu cầu về dung lượng lưu trữ (*storage requirements*)** của một dịch vụ.

Việc chọn lựa một con số phi thực tế cho các phép tính toán này có thể dẫn đến một thiết kế kiến trúc sai lầm nghiêm trọng. Do chúng ta cần có những ước tính chuẩn xác trong nhiều bài toán thiết kế hệ thống, chúng ta sẽ thảo luận chi tiết toàn bộ các khái niệm liên quan trong bài học này. Các khái niệm này bao gồm:
* Các loại máy chủ trong trung tâm dữ liệu (*data center*).
* Độ trễ truy cập thực tế (*realistic access latencies*) của các thành phần phần cứng khác nhau.
* Ước tính chỉ số RPS mà một máy chủ có thể gánh tải.
* Các ví dụ về ước tính băng thông (*bandwidth*), số lượng máy chủ (*servers*), và dung lượng lưu trữ (*storage estimation*).

---

## Các loại máy chủ trong trung tâm dữ liệu (Types of Data Center Servers)

Các trung tâm dữ liệu (*data centers*) không sử dụng một loại máy chủ duy nhất. Các giải pháp doanh nghiệp thường tận dụng phần cứng thương mại đại trà (*commodity hardware*) nhằm tối ưu hóa chi phí và phát triển các giải pháp có khả năng mở rộng quy mô linh hoạt (*scalable solutions*). Dưới đây, chúng ta sẽ phân tích các loại máy chủ thường được triển khai bên trong một trung tâm dữ liệu để xử lý các khối lượng công việc (*workloads*) khác nhau.

Ước tính mức tài nguyên cần thiết ở các tầng: máy chủ web (*web server*), máy chủ ứng dụng (*application server*), và máy chủ lưu trữ (*storage server*). Trục Y biểu thị mức tài nguyên theo các cấp độ phân loại: Thấp (*Low*), Trung bình (*Medium*), và Cao (*High*):

![005 - Kỹ Năng Ước Tính Đại Khái (Back-of-the-envelope Calculations)](images/topic_005_p002_00.png)

![005 - Kỹ Năng Ước Tính Đại Khái (Back-of-the-envelope Calculations)](images/topic_005_p002_01.png)

![005 - Kỹ Năng Ước Tính Đại Khái (Back-of-the-envelope Calculations)](images/topic_005_p002_02.png)

---

### Máy chủ Web (Web Servers)

Để phục vụ khả năng mở rộng (*scalability*), các máy chủ web (*web servers*) được tách rời độc lập (*decoupled*) khỏi các máy chủ ứng dụng (*application servers*). Máy chủ web là điểm tiếp xúc đầu tiên (*first point of contact*) của lưu lượng truy cập sau các bộ cân bằng tải (*load balancers*). Các trung tâm dữ liệu sở hữu những tủ rack chứa đầy các máy chủ web, chuyên trách xử lý các lệnh gọi API (*API calls*) từ phía máy khách (*clients*).

Tùy thuộc vào dịch vụ được cung cấp, tài nguyên bộ nhớ RAM và dung lượng lưu trữ trên các máy chủ web có thể ở mức từ nhỏ đến trung bình (*small to medium*). Tuy nhiên, các máy chủ này đòi hỏi tài nguyên tính toán xử lý (*computational resources*) rất tốt. 

Ví dụ, Facebook từng sử dụng máy chủ web trang bị **32 GB RAM** và **500 GB dung lượng lưu trữ**. Nhưng để đáp ứng nhu cầu tính toán cao cấp (*high-end computational needs*), họ đã hợp tác với Intel để chế tạo một bộ vi xử lý tùy chỉnh **16 lõi (16-core)**.

> [!NOTE]  
> Nhiều con số được trích dẫn trong bài học này được thu thập từ tài liệu thiết kế trung tâm dữ liệu mà Facebook đã công bố mã nguồn mở vào năm 2011. Do sự suy giảm tốc độ tăng trưởng hiệu năng từ định luật Moore (*Moore's law*) vào khoảng năm 2004, các con số này hiện vẫn giữ nguyên giá trị thực tế và không bị lạc hậu.

---

### Máy chủ Ứng dụng (Application Servers)

Máy chủ ứng dụng (*application servers*) chịu trách nhiệm thực thi phần mềm ứng dụng lõi và toàn bộ logic nghiệp vụ (*business logic*). Sự khác biệt giữa máy chủ web và máy chủ ứng dụng đôi khi khá mong manh (*somewhat fuzzy*). 

* **Máy chủ ứng dụng** chủ yếu tạo và cung cấp nội dung động (*dynamic content*).
* **Máy chủ web** chủ yếu phục vụ nội dung tĩnh (*static content*) cho máy khách (phần lớn là các trình duyệt web).

Máy chủ ứng dụng đòi hỏi tài nguyên tính toán và lưu trữ rất lớn. Tài nguyên lưu trữ có thể bao gồm bộ nhớ khả biến (*volatile memory* - như RAM) và bộ nhớ bất biến (*non-volatile storage* - như ổ cứng). Facebook từng sử dụng các máy chủ ứng dụng có dung lượng **RAM lên đến 256 GB** cùng hai loại hình lưu trữ: đĩa từ quay truyền thống (*traditional rotating disks - HDD*) và ổ nhớ thể rắn (*flash - SSD*), với tổng dung lượng lên đến **6.5 TB**.

---

### Máy chủ Lưu trữ (Storage Servers)

Cùng với sự bùng nổ mạnh mẽ của lượng người dùng Internet, khối lượng dữ liệu được lưu trữ bởi các dịch vụ khổng lồ đã tăng lên gấp bội. Ngoài ra, nhiều dạng dữ liệu khác nhau hiện đang được phân bổ trên các đơn vị lưu trữ chuyên biệt. 

Chẳng hạn, **YouTube** sử dụng các kho lưu trữ dữ liệu (*datastores*) sau:
1. **Lưu trữ Blob (*Blob storage*)**: Dùng cho các tệp video đã được mã hóa (*encoded videos*).
2. **Kho lưu trữ hàng đợi xử lý tạm thời (*Temporary processing queue storage*)**: Có khả năng chứa hàng trăm giờ nội dung video được tải lên YouTube hàng ngày đang chờ xử lý.
3. **Kho lưu trữ chuyên dụng Bigtable**: Dùng để lưu trữ một số lượng khổng lồ hình ảnh thu nhỏ (*thumbnails*) của các video.
4. **Hệ quản trị cơ sở dữ liệu quan hệ (*Relational Database Management System - RDBMS*)**: Dùng cho siêu dữ liệu (*metadata*) của người dùng và video (bình luận, lượt thích, kênh người dùng, v.v.).

Các kho dữ liệu khác vẫn được sử dụng cho việc phân tích dữ liệu chuyên sâu (*analytics*) — ví dụ như hệ thống tệp phân tán **Hadoop HDFS**.

Máy chủ lưu trữ chủ yếu bao gồm các hệ thống quản trị dữ liệu có cấu trúc (*structured - ví dụ SQL*) và phi cấu trúc (*non-structured - NoSQL*).

Quay trở lại ví dụ của Facebook, chúng ta biết rằng họ đã triển khai các máy chủ có dung lượng lưu trữ lên tới **120 TB**. Với số lượng máy chủ vận hành đồ sộ, Facebook có khả năng chứa đến hàng exabyte dữ liệu. Một exabyte tương đương $10^{18}$ Bytes. Theo quy ước chuẩn, chúng ta đo lường dung lượng lưu trữ và băng thông mạng (*network bandwidth*) theo hệ thập phân (cơ số 10 - *base 10*), chứ không phải hệ nhị phân (cơ số 2 - *base 2*). Mặc dù có dung lượng ổ đĩa lớn, bộ nhớ RAM của các máy chủ lưu trữ này thường chỉ dừng ở mức **32 GB**.

> [!NOTE]  
> Các loại máy chủ được mô tả ở trên không phải là những loại duy nhất có mặt trong một trung tâm dữ liệu. Các tổ chức còn cần nhiều máy chủ phục vụ các dịch vụ hạ tầng khác như: cấu hình (*configuration*), giám sát (*monitoring*), cân bằng tải (*load balancing*), phân tích số liệu (*analytics*), tính cước/kế toán (*accounting*), bộ nhớ đệm (*caching*), v.v.

Các con số được Facebook công bố mã nguồn mở trước đây hiện tại có phần đã cũ. Bảng dưới đây thể hiện thông số kỹ thuật tiêu chuẩn của một máy chủ có thể tìm thấy trong các trung tâm dữ liệu ngày nay:

#### Thông Số Kỹ Thuật Máy Chủ Tiêu Chuẩn (Typical Server Specifications)

| Thành phần (*Component*) | Số lượng / Cấu hình (*Count*) |
| :--- | :--- |
| **Số lượng socket cắm CPU (*Number of sockets*)** | 2 |
| **Bộ vi xử lý (*Processor*)** | Intel Xeon X2686 |
| **Số lượng lõi (*Number of cores*)** | 36 cores (72 luồng phần cứng - *hardware threads*) |
| **Bộ nhớ RAM** | 256 GB |
| **Bộ nhớ đệm L3 (*Cache L3*)** | 45 MB |
| **Dung lượng lưu trữ (*Storage capacity*)** | 15 TB |

> [!NOTE]  
> Luồng phần cứng (*hardware threads*) ban đầu được gọi là công nghệ đa luồng đồng thời (*Simultaneous Multithreading - SMT*). Về sau, Intel đã đổi tên thương mại thành công nghệ siêu phân luồng (*Hyper-Threading*).

Các thông số nêu trên được lấy cảm hứng từ cấu hình máy chủ vật lý chuyên dụng (*bare-metal server*) của Amazon. Tuy nhiên, trên thực tế vẫn có những cỗ máy mạnh hơn hoặc yếu hơn, hỗ trợ dung lượng RAM cao hơn nhiều (lên đến **8 TB**), dung lượng ổ đĩa lớn hơn (lên đến **24 ổ đĩa với tối đa 20 TB mỗi ổ**, số liệu khoảng năm 2021), và bộ nhớ đệm CPU (*cache memory*) lớn hơn (lên đến **120 MB**).

---

## Các Con Số Tiêu Chuẩn Cần Ghi Nhớ (Standard Numbers to Remember)

Rất nhiều công sức và nguồn lực được đổ vào khâu lập kế hoạch và triển khai một dịch vụ. Tuy nhiên, nếu thiếu kiến thức nền tảng về loại khối lượng công việc (*workloads*) mà máy móc có thể đáp ứng, việc hoạch định này là bất khả thi. 

Độ trễ (*Latencies*) đóng vai trò tối quan trọng trong việc quyết định khối lượng tải mà một máy chủ có thể chịu đựng. Bảng dưới đây mô tả một số con số then chốt mà các kỹ sư thiết kế hệ thống (*System Designers*) bắt buộc phải nắm vững để tiến hành ước tính tài nguyên chính xác:

#### Độ Trễ Quan Trọng (Important Latencies)

| Thành phần thao tác (*Component*) | Thời gian thực thi (*Time*) |
| :--- | :--- |
| **Tham chiếu bộ nhớ đệm L1 (*L1 cache reference*)** | 0.9 ns (nanô giây) |
| **Tham chiếu bộ nhớ đệm L2 (*L2 cache reference*)** | 2.8 ns |
| **Tham chiếu bộ nhớ đệm L3 (*L3 cache reference*)** | 12.9 ns |
| **Tham chiếu bộ nhớ chính - RAM (*Main memory reference*)** | 100 ns |
| **Nén 1 KB dữ liệu bằng Snzip (*Compress 1KB with Snzip*)** | 3,000 ns (3 µs - micro giây) |
| **Đọc tuần tự 1 MB từ bộ nhớ RAM (*Read 1 MB sequentially from memory*)** | 9,000 ns (9 µs) |
| **Đọc tuần tự 1 MB từ ổ SSD (*Read 1 MB sequentially from SSD*)** | 200,000 ns (200 µs) |
| **Thời gian khứ hồi mạng trong cùng một trung tâm dữ liệu (*Round trip within same datacenter*)** | 500,000 ns (500 µs) |
| **Đọc tuần tự 1 MB từ ổ SSD tốc độ cao (~1 GB/s) (*Read 1 MB sequentially from SSD with speed ~1GB/sec SSD*)** | 1,000,000 ns (1 ms - mili giây) |
| **Tìm kiếm vị trí trên đĩa từ (*Disk seek*)** | 4,000,000 ns (4 ms) |
| **Đọc tuần tự 1 MB từ đĩa cứng HDD (*Read 1 MB sequentially from disk*)** | 2,000,000 ns (2 ms) |
| **Gửi gói tin từ San Francisco đến New York (*Send packet SF->NYC*)** | 71,000,000 ns (71 ms) |

Bên cạnh các chỉ số độ trễ được liệt kê ở trên, còn có các con số về thông lượng (*Throughput*) được đo bằng số lượng truy vấn mỗi giây (**Queries Per Second - QPS**) mà một máy chủ kho lưu trữ dữ liệu đơn lẻ (*single-server datastore*) điển hình có thể đảm đương.

---

# Các Tỷ Suất Quan Trọng (Important Rates)

| Thành phần lưu trữ | QPS xử lý (QPS handled) |
| :--- | :--- |
| QPS được xử lý bởi MySQL | 1,000 |
| QPS được xử lý bởi key-value store | 10,000 |
| QPS được xử lý bởi cache server | 100,000 – 1,000,000 (1M) |

Các con số trên là ước tính xấp xỉ và biến thiên rất lớn phụ thuộc vào nhiều yếu tố như: loại truy vấn (truy vấn điểm - point query và truy vấn dải - range query), thông số kỹ thuật của phần cứng (machine specifications), thiết kế của cơ sở dữ liệu (database design), cơ chế đánh chỉ mục (indexing), v.v.

---

## Ước Tính Yêu Cầu (Requests Estimation)

Phần này thảo luận về số lượng yêu cầu (requests) mà một máy chủ điển hình có thể xử lý trong một giây. Bên trong một máy chủ, tài nguyên là hữu hạn, và tùy thuộc vào loại yêu cầu của client, các tài nguyên khác nhau có thể trở thành điểm nghẽn cổ chai (bottleneck). Hãy cùng tìm hiểu hai loại yêu cầu sau:

- **Các yêu cầu giới hạn bởi CPU (CPU-bound requests):** Đây là loại yêu cầu mà yếu tố giới hạn chính là tài nguyên CPU.
- **Các yêu cầu giới hạn bởi bộ nhớ (Memory-bound requests):** Đây là loại yêu cầu bị giới hạn bởi dung lượng bộ nhớ (RAM) của máy chủ.

Hãy ước tính xấp xỉ chỉ số RPS (Requests Per Second) cho từng loại yêu cầu. Tuy nhiên, trước khi thực hiện, chúng ta cần đưa ra các giả định sau:
- Máy chủ của chúng ta có các thông số kỹ thuật của một máy chủ điển hình (typical server) như đã định nghĩa ở bảng trước (72 CPU threads, 256 GB RAM).
- Hệ điều hành (Operating System) và các tiến trình phụ trợ (auxiliary processes) khác đã tiêu tốn tổng cộng **16 GB RAM**.
- Mỗi worker tiêu tốn **300 MB dung lượng RAM** để hoàn thành một yêu cầu.
- Để đơn giản hóa, chúng ta giả định rằng CPU lấy dữ liệu trực tiếp từ RAM. Do đó, hệ thống bộ nhớ đệm (caching system) đảm bảo rằng toàn bộ nội dung cần thiết đều sẵn sàng để phục vụ mà không cần phải truy xuất xuống tầng lưu trữ thứ cấp (storage layer/disk).
- Mỗi yêu cầu giới hạn bởi CPU (CPU-bound request) mất **200 mili-giây (ms)**, trong khi mỗi yêu cầu giới hạn bởi bộ nhớ (memory-bound request) mất **50 mili-giây (ms)** để hoàn thành.

Bây giờ, hãy thực hiện tính toán cho từng loại yêu cầu:

### 1. Giới hạn bởi CPU (CPU-bound)
Công thức đơn giản dùng để tính toán RPS cho các yêu cầu giới hạn bởi CPU là:

$$\text{RPS}_{\text{CPU}} = \text{Num}_{\text{CPU}} \times \frac{1}{\text{Task}_{\text{time}}}$$

Trong phép tính này, chúng ta sử dụng các thuật ngữ:
- $\text{RPS}_{\text{CPU}}$: RPS giới hạn bởi CPU (CPU-bound RPS).
- $\text{Num}_{\text{CPU}}$: Số lượng luồng CPU (Number of CPU threads), hay còn gọi là các luồng phần cứng (hardware threads).
- $\text{Task}_{\text{time}}$: Thời gian cần thiết để mỗi tác vụ hoàn thành (The time each task takes to complete).

Khi đó:
$$\text{RPS}_{\text{CPU}} = 72 \times \frac{1}{200\text{ ms}} = 360\text{ RPS}$$

**Cơ sở lý giải:** Chúng ta có thể hình dung một giây như một chiếc hộp lớn và tính toán xem có bao nhiêu chiếc hộp nhỏ (tác vụ - tasks) có thể đặt vừa vặn bên trong chiếc hộp lớn đó — nghĩa là số lượng tác vụ có thể được hoàn thành trong một giây bởi một số lượng CPU nhất định. Do đó, số lượng CPU/luồng càng cao sẽ mang lại chỉ số RPS càng lớn.

---

### 2. Các yêu cầu giới hạn bởi bộ nhớ (Memory-bound requests)
Đối với các yêu cầu giới hạn bởi bộ nhớ, chúng ta sử dụng công thức sau:

$$\text{RPS}_{\text{memory}} = \frac{\text{RAM}_{\text{size}}}{\text{Worker}_{\text{memory}}} \times \frac{1}{\text{Task}_{\text{time}}}$$

Trong phép tính này, chúng ta sử dụng các thuật ngữ:
- $\text{RPS}_{\text{memory}}$: RPS giới hạn bởi bộ nhớ (Memory-bound RPS).
- $\text{RAM}_{\text{size}}$: Tổng dung lượng RAM khả dụng (Total size of RAM).
- $\text{Worker}_{\text{memory}}$: Lượng bộ nhớ RAM của một worker quản lý một yêu cầu (A worker in memory that manages a request).

Khi đó (với dung lượng RAM khả dụng là $256\text{ GB} - 16\text{ GB} = 240\text{ GB}$):
$$\text{RPS}_{\text{memory}} = \frac{240\text{ GB}}{300\text{ MB}} \times \frac{1}{50\text{ ms}} = 800 \times 20 = 16,000\text{ RPS}$$

Tiếp tục phép loại suy chiếc hộp từ phần giải thích các tiến trình giới hạn bởi CPU: ở đây, trước tiên chúng ta tính toán số lượng hộp hiện có (máy chủ có thể chứa được bao nhiêu tiến trình memory-bound đồng thời), sau đó tính toán xem chúng ta có thể đặt vừa bao nhiêu chiếc hộp nhỏ (tác vụ) vào từng chiếc hộp lớn hơn đó.

---

### Tổng hợp thông lượng hệ thống (Combined Throughput)
Một dịch vụ thường tiếp nhận cả hai loại yêu cầu: giới hạn bởi CPU (CPU-bound) và giới hạn bởi bộ nhớ (memory-bound).

Xét trường hợp một nửa số yêu cầu là CPU-bound và một nửa còn lại là memory-bound, chúng ta có thể xử lý tổng cộng:

$$\text{Total RPS} = \frac{360}{2} + \frac{16,000}{2} = 180 + 8,000 = 8,180 \approx 8,000\text{ RPS}$$

Các tính toán ở trên chỉ mang tính chất xấp xỉ nhằm xây dựng sự thấu hiểu về các yếu tố cơ bản liên quan đến việc ước tính RPS. Trong thực tế, rất nhiều yếu tố khác sẽ cùng tác động:
- Ví dụ, độ trễ (latency) phát sinh khi thực hiện tìm kiếm trên đĩa (disk seek) trong trường hợp dữ liệu không có sẵn trong RAM.
- Hoặc nếu yêu cầu được chuyển tiếp đến máy chủ cơ sở dữ liệu (database server), độ trễ sẽ bao gồm cả độ trễ xử lý của database và độ trễ mạng (network latency).
- Thêm vào đó, loại truy vấn cũng đóng vai trò quan trọng.
- Dĩ nhiên, các sự cố (faults), lỗi trong mã nguồn (bugs in code), lỗi sập nút (node failures), mất điện (power outages), gián đoạn mạng (network disruptions) và nhiều vấn đề khác đều là những yếu tố tất yếu xảy ra.

Vào một ngày thông thường, nhiều loại yêu cầu khác nhau sẽ ập đến. Một máy chủ cấu hình mạnh chỉ chuyên phục vụ nội dung tĩnh (static content) từ RAM có thể xử lý lên tới **500k RPS**. Ở chiều ngược lại, các tác vụ tính toán nặng (computational-intensive tasks) như xử lý hình ảnh (image processing) có thể chỉ cho phép tối đa **50 RPS**.

> [!NOTE]
> Trong thực tế, ước tính năng lực hệ thống (capacity estimation) là một bài toán khó, và các tổ chức phải học hỏi, hoàn thiện nó qua nhiều năm. Một hệ thống giám sát (monitoring system) sẽ liên tục theo dõi tất cả các thành phần trong hạ tầng để đưa ra những cảnh báo sớm về tình trạng quá tải máy chủ (overloading servers).

---

## Các Ví Dụ Về Ước Tính Tài Nguyên (Examples of Resource Estimation)

Hãy thử sức với một số con số ước tính nhanh (back-of-the-envelope numbers).

Chúng ta sẽ bao gồm các nội dung sau:
- Giới thiệu (Introduction)
- Số lượng máy chủ yêu cầu (Number of servers required)
- Yêu cầu về lưu trữ (Storage requirements)
- Yêu cầu về băng thông (Bandwidth requirements)

### Giới thiệu (Introduction)
Sau khi đã thiết lập nền tảng cho việc ước tính tài nguyên, hãy vận dụng kiến thức nền tảng để ước tính các tài nguyên như máy chủ (servers), bộ lưu trữ (storage) và băng thông (bandwidth). Dưới đây, chúng ta xem xét một kịch bản và một dịch vụ cụ thể, đưa ra các giả định, và dựa trên những giả định đó, tiến hành ước tính. Hãy bắt đầu ngay!

---

### Số Lượng Máy Chủ Yêu Cầu (Number of Servers Required)

Hãy đưa ra các giả định sau về một dịch vụ tương tự như Twitter (Twitter-like service):

**Các giả định (Assumptions):**
- Có **500 triệu (500M)** người dùng hoạt động hàng ngày (Daily Active Users - DAU).
- Một người dùng trung bình thực hiện **20 yêu cầu mỗi ngày (20 requests/day)**.
- Nhắc lại rằng một máy chủ đơn lẻ có thể xử lý **8,000 RPS**.

#### Bảng Ước Tính Số Lượng Máy Chủ (Estimating the Number of Servers)

| Tham số | Giá trị |
| :--- | :--- |
| Người dùng hoạt động hàng ngày (DAU) | **500 M** |
| Số yêu cầu trung bình / ngày | **20** |
| **Tổng số yêu cầu / ngày** | **10 Tỷ (Billion)** |
| **Tổng số yêu cầu / giây** | **115 K** |
| **Tổng số máy chủ yêu cầu** | **15** |

#### Chi tiết tính toán:
- **Tổng số yêu cầu mỗi giây (Total requests per second):**
  $$\text{Requests per second} = \frac{500\text{M} \times 20}{86,400\text{ giây}} \approx 115\text{K requests/sec}$$
  Đây chính là chỉ số RPS yêu cầu cho toàn hệ thống của chúng ta.

- **Về số lượng máy chủ (Number of servers):**
  $$\text{Số máy chủ} = \frac{\text{Số lượng Requests/sec}}{\text{RPS của một server}} \approx \frac{115\text{K}}{8\text{K}} \approx 15\text{ máy chủ}$$
  để xử lý toàn bộ các yêu cầu.

---

> [!WARNING]
> Trên thực tế, con số ở trên có vẻ **không chính xác**. Nếu chúng ta chỉ cần **15 máy chủ thông thường (commodity servers)** để phục vụ 500 triệu người dùng hàng ngày, thì tại sao các dịch vụ lớn lại phải sử dụng tới **hàng triệu máy chủ** trong một trung tâm dữ liệu (data center)?

Lý do cốt lõi cho điều này là chỉ số RPS chưa đủ để ước tính số lượng máy chủ cần thiết để cung cấp một dịch vụ hoàn chỉnh. Hơn nữa, chúng ta đã đưa ra một số giả định ngầm trong các phép tính bên trên:
1. Một trong những giả định đó là: một yêu cầu chỉ do duy nhất một máy chủ xử lý. Trong thực tế, các yêu cầu đi qua các máy chủ web (web servers), các máy chủ này tương tác với các máy chủ ứng dụng (application servers), rồi các máy chủ ứng dụng lại tiếp tục yêu cầu dữ liệu từ các máy chủ lưu trữ (storage servers). 
2. Mỗi máy chủ có thể mất một khoảng thời gian khác nhau để xử lý từng yêu cầu.
3. Hơn nữa, mỗi yêu cầu có thể được xử lý khác nhau tùy thuộc vào trạng thái của trung tâm dữ liệu, ứng dụng và chính bản thân yêu cầu đó. Hãy nhớ rằng chúng ta có rất nhiều loại máy chủ đa dạng phục vụ các dịch vụ khác nhau bên trong một data center.

---

### Chúng ta đã đúc kết được rằng:
1. **Việc tìm ra các ước tính năng lực (capacity estimations) chính xác là một thách thức** do có nhiều yếu tố tác động — ví dụ: mỗi dịch vụ được thiết kế khác nhau, có quy tắc phân nhánh xử lý (fan-out rules) và phần cứng khác nhau, trách nhiệm của các máy chủ thay đổi theo thời gian, v.v.
2. **Ở cấp độ thiết kế (design level), việc ước tính sơ bộ (coarse-grained estimation) là hoàn toàn phù hợp** vì mục đích chính là đưa ra các cận trên hợp lý (reasonable upper bounds) cho các tài nguyên cần thiết. Chúng ta cũng có thể sử dụng các phương pháp nâng cao từ lý thuyết hàng đợi (queuing theory) và nghiên cứu vận trù học (operations research) để đưa ra các ước tính tốt hơn. Tuy nhiên, một buổi phỏng vấn hay giai đoạn thiết kế ban đầu không phải là thời điểm thích hợp để sử dụng chiến lược phức tạp như vậy. Các hệ thống thực tế sử dụng nhiều phương pháp khác nhau (tính toán nhanh trên phong bì - back-of-the-envelope calculations, mô phỏng - simulations, xây dựng nguyên mẫu thử nghiệm - prototyping, và giám sát - monitoring) để cải thiện dần dần các ước tính ban đầu (vốn có thể còn sơ sài).

Do đó, chúng ta tính xấp xỉ số lượng máy chủ bằng cách mô tả có bao nhiêu client mà một máy chủ có thể xử lý trong một ngày nhất định:

$$\text{Số lượng máy chủ} = \frac{\text{Số lượng người dùng hoạt động hàng ngày (DAU)}}{\text{RPS của một máy chủ}}$$

Để có một ước tính xấp xỉ tốt hơn, hãy sử dụng hai giả định sau:
1. Chúng ta giả định rằng mỗi người dùng hoạt động hàng ngày (DAU) của dịch vụ chỉ gửi duy nhất **một yêu cầu mỗi ngày (1 request/day)**:
   $$\text{Số lượng máy chủ} = \frac{\text{Số lượng người dùng hoạt động hàng ngày (1)}}{\text{RPS của một máy chủ}} = \frac{\text{Số lượng yêu cầu/ngày}}{\text{RPS của một máy chủ}}$$
2. Chúng ta giả định rằng có một giây cụ thể trong ngày mà toàn bộ yêu cầu của tất cả người dùng đồng loạt đổ về dịch vụ cùng một lúc. Chúng ta sử dụng giả định này để tính toán ước tính năng lực cho trường hợp tải đỉnh (peak load). Để thực hiện tốt hơn, chúng ta sẽ cần đến các phân phối yêu cầu và phản hồi (request and response distributions), những dữ liệu có thể thu thập được ở cấp độ xây dựng nguyên mẫu thử nghiệm (prototyping level). Chúng ta có thể giả định rằng các phân phối này tuân theo một dạng phân phối xác suất cụ thể,...

---

### Ước Tính Số Lượng Máy Chủ (Number of Servers Estimation)

Ví dụ như phân phối Poisson (Poisson distribution). Bằng cách sử dụng **DAU (Daily Active Users - Người dùng hoạt động hàng ngày)** làm giá trị đại diện (proxy) cho tải đỉnh (peak load) trong một giây cụ thể, chúng ta đã tránh được những khó khăn trong việc tìm tỷ lệ đến (arrival rates) của các yêu cầu (requests) và phản hồi (responses).

Do đó, DAU khi ấy sẽ trở thành số lượng yêu cầu mỗi giây (requests per second - RPS). Chúng ta đã có chỉ số RPS cho một máy chủ (server); vì vậy, phương trình (1) trở thành:

$$\text{Số lượng máy chủ} = \frac{\text{Số lượng yêu cầu / giây}}{\text{RPS của máy chủ}}$$

Bằng cách điền các giá trị vào phương trình trên, chúng ta thu được số lượng máy chủ như sau:

$$= \frac{\text{Số lượng yêu cầu / giây}}{\text{RPS của máy chủ}} = \frac{500\text{ M}}{8000} = 62.500$$

![005 - Kỹ Năng Ước Tính Đại Khái (Back-of-the-envelope Calculations)](images/topic_005_p013_00.png)

* **Số lượng máy chủ cần thiết cho một dịch vụ tương tự Twitter:** $62.500\text{ máy chủ}$

> [!NOTE]
> **Ghi chú:** Các phép tính của chúng ta dựa trên một phép xấp xỉ (approximation) có thể không cung cấp một cận chặt (tight bound) về số lượng máy chủ, nhưng nó vẫn là một con số thực tế. Do đó, chúng ta sử dụng cách tiếp cận này trong việc ước tính số lượng máy chủ cho các bài toán thiết kế hệ thống. Một cách không chính thức (informally), phương trình nêu trên giả định rằng một máy chủ có thể xử lý $8.000$ người dùng mỗi giây. Chúng tôi cũng sẽ sử dụng tham chiếu này trong phần còn lại của khóa học.

---

### Yêu Cầu Về Lưu Trữ (Storage Requirements)

Trong phần này, chúng ta sẽ cố gắng hiểu cách thực hiện ước tính dung lượng lưu trữ bằng cách lấy ví dụ về Twitter. Chúng ta ước tính dung lượng lưu trữ cần thiết của Twitter cho các tweet mới trong một năm. Để bắt đầu, hãy đưa ra các giả định sau:

* Chúng ta có tổng cộng **250 triệu (250 M) người dùng hoạt động hàng ngày (Daily Active Users - DAU)**.
* Mỗi người dùng đăng **3 tweet** mỗi ngày.
* **10%** số lượng tweet có chứa hình ảnh, trong khi **5%** số lượng tweet có chứa video. Bất kỳ tweet nào chứa video sẽ không chứa hình ảnh và ngược lại.
* Giả định rằng trung bình một hình ảnh có kích thước **200 KB** và một video có kích thước **3 MB**.
* Văn bản của tweet (tweet text) cùng siêu dữ liệu (metadata) của nó yêu cầu tổng cộng **250 Bytes** dung lượng lưu trữ trong cơ sở dữ liệu (database).

Khi đó, dung lượng lưu trữ sau đây sẽ được yêu cầu:

#### Bảng Ước Tính Yêu Cầu Lưu Trữ (Estimating Storage Requirements)

| Hạng mục | Giá trị | Đơn vị |
| :--- | :--- | :--- |
| **Người dùng hoạt động hàng ngày (Daily active users - DAU)** | $250$ | $\text{M}$ |
| **Số tweet mỗi ngày (Daily tweets)** | $3$ | |
| **Tổng số yêu cầu / ngày (Total requests / day)** | $750$ | $\text{M}$ |
| **Dung lượng lưu trữ yêu cầu cho mỗi tweet (Storage required per tweet)** | $250$ | $\text{B}$ |
| **Dung lượng lưu trữ yêu cầu cho mỗi hình ảnh (Storage required per image)** | $200$ | $\text{KB}$ |
| **Dung lượng lưu trữ yêu cầu cho mỗi video (Storage required per video)** | $3$ | $\text{MB}$ |
| **Dung lượng lưu trữ cho văn bản tweets (Storage for tweets)** | $187.5$ | $\text{GB}$ |
| **Dung lượng lưu trữ cho hình ảnh (Storage for images)** | $15$ | $\text{TB}$ |
| **Dung lượng lưu trữ cho video (Storage for videos)** | $112.5$ | $\text{TB}$ |
| **Tổng dung lượng lưu trữ (Total storage)** | $128$ | $\text{TB}$ |

---

#### Chi Tiết Phép Tính (Hide Calculations)

* **Tổng số tweet:**
  $$250\text{ M} \times 3 = 750 \times 10^6\text{ tweet mỗi ngày.}$$

* **Dung lượng lưu trữ yêu cầu cho tweets trong một ngày:**
  $$750 \times 10^6 \times 250\text{ B} = 187.5\text{ GB}$$

* **Dung lượng lưu trữ yêu cầu cho 10% hình ảnh trong một ngày:**
  $$\frac{750 \times 10^6 \times 10}{100} \times 200 \times 10^3\text{ B} = 15\text{ TB}$$

* **Dung lượng lưu trữ yêu cầu cho 5% nội dung video trong một ngày:**
  $$\frac{750 \times 10^6 \times 5}{100} \times 3 \times 10^6\text{ B} = 112.5\text{ TB}$$

* **Tổng dung lượng lưu trữ yêu cầu cho một ngày:**
  $$0.1875\text{ TB} + 15\text{ TB} + 112.5\text{ TB} \approx 128\text{ TB}$$

* **Dung lượng lưu trữ yêu cầu cho một năm:**
  $$365 \times 128\text{ TB} = 46.72\text{ PB}$$

![005 - Kỹ Năng Ước Tính Đại Khái (Back-of-the-envelope Calculations)](images/topic_005_p016_00.png)

$$\text{Tổng dung lượng lưu trữ mà Twitter yêu cầu trong một năm} = \text{Lưu trữ / ngày } (128\text{ TB}) \times \text{Số ngày / năm } (365) = \text{Lưu trữ / năm } (46.72\text{ PB})$$

---

### Yêu Cầu Về Băng Thông (Bandwidth Requirements)

Để ước tính các yêu cầu về băng thông (bandwidth requirements) cho một dịch vụ, chúng ta thực hiện theo các bước sau:

1. Ước tính lượng dữ liệu đầu vào (incoming data) hàng ngày gửi tới dịch vụ.
2. Ước tính lượng dữ liệu đầu ra (outgoing data) hàng ngày từ dịch vụ.
3. Ước tính băng thông theo đơn vị **Gbps (gigabits per second)** bằng cách chia lượng dữ liệu đầu vào và đầu ra cho số giây trong một ngày.

#### Lưu Lượng Dữ Liệu Đầu Vào (Incoming traffic):
Hãy tiếp tục từ ví dụ trước về Twitter với yêu cầu $128\text{ TB}$ lưu trữ mỗi ngày. Do đó, lưu lượng đầu vào cần phải hỗ trợ mức băng thông mỗi giây như sau:

$$\frac{128 \times 10^{12} \times 8}{86400} \approx 12\text{ Gbps}$$

> [!NOTE]
> **Ghi chú:** Chúng ta nhân với $8$ để chuyển đổi từ **Bytes (B)** sang **bits (b)** vì băng thông được đo bằng đơn vị **bits per second (bps)**.

#### Lưu Lượng Dữ Liệu Đầu Ra (Outgoing traffic):
Giả sử rằng một người dùng xem trung bình **50 tweet** trong một ngày. Xét cùng tỷ lệ $5\%$ đối với video và $10\%$ đối với hình ảnh: trong số $50$ tweet đó, sẽ có $2.5$ tweet chứa nội dung video và $5$ tweet chứa hình ảnh. Với giả định có **250 triệu (250 M)** người dùng hoạt động hàng ngày, chúng ta đi đến các ước tính sau:

---

#### Bảng Ước Tính Yêu Cầu Băng Thông (Estimating Bandwidth Requirements)

| Hạng mục | Giá trị | Đơn vị |
| :--- | :--- | :--- |
| **Người dùng hoạt động hàng ngày (Daily active users - DAU)** | $250$ | $\text{M}$ |
| **Số tweet xem mỗi ngày (Daily tweets viewed)** | $50$ | mỗi người dùng (per user) |
| **Số tweet xem / giây (Tweets viewed / second)** | $145$ | $\text{K}$ |
| **Băng thông yêu cầu cho tweets (Bandwidth required for tweets)** | $0.3$ | $\text{Gbps}$ |
| **Băng thông yêu cầu cho hình ảnh (Bandwidth required for images)** | $23.2$ | $\text{Gbps}$ |
| **Băng thông yêu cầu cho video (Bandwidth required for videos)** | $174$ | $\text{Gbps}$ |
| **Tổng băng thông (Total bandwidth)** | $197.5$ | $\text{Gbps}$ |

---

# 005 - Kỹ Năng Ước Tính Đại Khái (Back-of-the-envelope Calculations)

[Quay lại (Back)] | **Đưa các con số ước tính đại khái vào thực tế… (Put Back-of-the-envelope Numbers …)** | [Đánh dấu đã hoàn thành (Mark As Completed)] | [Tiếp theo (Next): Giới thiệu về các khối kiến trúc cơ bản cho M… (Introduction to Building Blocks for M…)]

---

### [Ẩn các phép tính (Hide Calculations)]

* **Số lượng tweet được xem mỗi ngày:**
  $$250\text{ triệu người dùng} \times 50\text{ tweets} = 12.5\text{ tỷ (billion) tweets được xem mỗi ngày}$$

* **Số lượt xem tweet mỗi giây (Tweets viewed per second):**
  $$\frac{12.5\times 10^9}{86400\text{ giây}} \approx 145 \times 10^3\text{ tweets/giây (tweets per second)}$$

* **Băng thông phục vụ tweet văn bản (Bandwidth for tweet):**
  $$145 \times 10^3 \times 250\text{ bytes} \times 8\text{ bits} \approx 0.3\text{ Gbps}$$
  *(Mỗi tweet tương đương $250\text{ bytes}$).*

* **Băng thông cho 10% tweet có chứa hình ảnh trong một giây (Bandwidth of 10 percent images in tweets in a second):**
  $$145 \times 10^3 \times \frac{10}{100} \times 200 \times 10^3\text{ bytes} \times 8\text{ bits} = 23.2\text{ Gbps}$$

* **Băng thông cho 5% tweet chứa video trong một giây (Bandwidth for 5 percent video tweets in a second):**
  $$145 \times 10^3 \times \frac{5}{100} \times 3 \times 10^6\text{ bytes} \times 8\text{ bits} = 174\text{ Gbps}$$

* **Tổng lưu lượng gửi ra ngoài (Total outgoing traffic) cần thiết sẽ bằng:**
  $$0.3 + 23.2 + 174 \approx 197.5\text{ Gbps}$$

---

![005 - Kỹ Năng Ước Tính Đại Khái (Back-of-the-envelope Calculations)](images/topic_005_p019_00.png)

> [!IMPORTANT]
> **Tổng kết nhu cầu băng thông:**
> Twitter sẽ cần tổng cộng **$12\text{ Gbps}$** lưu lượng đi vào (**incoming traffic / Ingress bandwidth**) và **$197.5\text{ Gbps}$** lưu lượng đi ra (**outgoing traffic / Egress bandwidth**), giả định rằng nội dung được tải lên không qua nén. 
> 
> **Tổng nhu cầu băng thông (Total bandwidth requirements):**
> $$12\text{ Gbps} + 197.5\text{ Gbps} = 209.5\text{ Gbps}$$

---

### Tổng lượng băng thông yêu cầu bởi Twitter (The total bandwidth required by Twitter)

| Thành phần lưu lượng (Traffic Component) | Băng thông (Bandwidth) |
| :--- | :--- |
| **Băng thông đi ra (Outgoing bandwidth / Egress)** | $197.5\text{ Gbps}$ |
| **Băng thông đi vào (Incoming bandwidth / Ingress)** | $+ 12\text{ Gbps}$ |
| **Tổng cộng (Total)** | **$= 209.5\text{ Gbps}$** |

![005 - Kỹ Năng Ước Tính Đại Khái (Back-of-the-envelope Calculations)](images/topic_005_p019_01.png)

---


---

[← Bài trước](004-dac-tinh-phi-chuc-nang.md) | [Mục lục](README.md) | [Bài tiếp theo →](006-gioi-thieu-building-blocks.md)
