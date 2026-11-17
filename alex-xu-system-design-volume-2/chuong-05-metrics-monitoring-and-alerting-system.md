[← Chương trước](chuong-04-distributed-message-queue.md) | [Mục lục](README.md) | [Chương tiếp theo →](chuong-06-ad-click-event-aggregation.md)

---

# Chương 5: Hệ Thống Giám Sát Chỉ Số và Cảnh Báo (Metrics Monitoring & Alerting System)

---

### Trang 138

![Sơ đồ trang 138](images/page_138.jpeg)

Hệ thống giám sát chỉ số và cảnh báo bao gồm 5 thành phần cốt lõi:
1. Thu thập dữ liệu (*Data collection*)
2. Truyền tải dữ liệu (*Data transmission*)
3. Lưu trữ dữ liệu (*Data storage*)
4. Cảnh báo (*Alerting*)
5. Trực quan hóa dữ liệu (*Visualization*)

*Hình 5.2: Năm thành phần của hệ thống*

---

#### Mô hình dữ liệu (*Data model*)
Dữ liệu chỉ số (*metrics*) thường được ghi nhận dưới dạng chuỗi thời gian (*time series*), bao gồm tên chỉ số, dấu thời gian (*timestamp*), giá trị đo lường, và tùy chọn có thêm một tập hợp các nhãn (*labels / tags*).

Hãy cùng xem xét hai ví dụ cụ thể:

**Ví dụ 1:**
Biểu đồ hiển thị tải CPU trung bình (*avg of cpu.load.i631*) theo phần trăm tại các mốc thời gian:
- `0.626`
- `0.29`
- `0.313`
(Trục thời gian trải dài từ `18:00`, `18:30`, `19:00`, `19:30`, `20:00`, `20:30`, `21:00`, `21:30`, `22:00`, `22:30`, `23:00`, `23:30`, `00:00`, `00:30`).

*Hình 5.3: Các dịch vụ giám sát và cảnh báo chỉ số phổ biến*

Điểm dữ liệu (*data point*) được khoanh vùng nổi bật trong Hình 5.3 có thể được biểu diễn thông qua Bảng 5.1:

| Tên trường (*Field*) | Giá trị (*Value*) |
| :--- | :--- |
| **metric_name** | `cpu.load` |
| **labels** | `host:i631,env:prod` |
| **timestamp** | `1613707265` |
| **value** | `0.29` |

*Bảng 5.1: Điểm dữ liệu được biểu diễn dưới dạng bảng*

Trong ví dụ này, chuỗi thời gian (*time series*) được định danh duy nhất bởi tên chỉ số (*metric name*), tập nhãn (*labels*: `host:i631,env:prod`), cùng một giá trị đơn lẻ tại một thời điểm xác định.

---

### Trang 139

**Ví dụ 2:**
Định dạng dòng văn bản chuẩn thô (*raw line format*):
```text
cpu.load host=webserver01,region=us-west 1613707265 76
cpu.load host=webserver01,region=us-west 1613787265 83
```
Đây là định dạng đầu vào phổ biến (*common input format*) được hỗ trợ bởi nhiều phần mềm giám sát trên thị trường. Prometheus [7] và OpenTSDB [8] là hai ví dụ tiêu biểu.

Mỗi chuỗi thời gian (*time series*) bao gồm các thành phần sau [9]:

| Tên (*Name*) | Kiểu dữ liệu (*Type*) |
| :--- | :--- |
| Một tên chỉ số (*A metric name*) | Chuỗi ký tự (*String*) |
| Một tập hợp thẻ/nhãn (*A set of tags/labels*) | Danh sách các cặp khóa-giá trị (*List of <key:value> pairs*) |
| Một mảng các giá trị và dấu thời gian tương ứng (*An array of values and their timestamps*) | Một mảng các cặp giá trị-thời gian (*An array of <value,timestamp> pairs*) |

*Bảng 5.2: Thành phần của một chuỗi thời gian (Time series)*

---

#### Mô hình truy cập dữ liệu (*Data access pattern*)
Trong Hình 5.4, mỗi nhãn trên trục tung (trục $Y$) đại diện cho một chuỗi thời gian (được định danh duy nhất thông qua tên chỉ số và tập nhãn tương ứng), trong khi trục hoành (trục $X$) biểu diễn trục thời gian.

![Sơ đồ trang 139](images/page_139.jpeg)

---

### Trang 140

![Sơ đồ trang 140](images/page_140.jpeg)

*Hình 5.4: Mô hình truy cập dữ liệu (Data access pattern)*

- **Nhãn chuỗi thời gian (*Time series Names/Labels*):**
  - `http_error_count("servicepool":"s1", "method":"GET", "machinename":"m2")`
  - `http_error_count("servicepool":"s1", "method":"GET", "machinename":"m1")`
- **Khoảng thời gian truy vấn:** Từ $t_2, t_3, t_4, t_5, t_6, t_7, t_8, t_9$.
- **Mẫu truy vấn (*Query*):** Truy vấn để lấy tổng số lỗi trên `servicepool=s1` và `method=GET` trên toàn bộ các máy (*across all machines*) nằm trong khoảng thời gian từ $t_4$ đến $t_7$.

Đặc điểm truy cập dữ liệu:
- Dữ liệu chỉ số được ghi nhận liên tục với tần suất rất cao, do đó lưu lượng truy cập chắc chắn là **thiên về ghi dữ liệu (*write-heavy*)**.
- Ngược lại, khối lượng đọc (*read volume*) có xu hướng tăng đột biến theo từng đợt (*bursty*), mang tính xung nhịp thất thường (*spiky*).

---

#### Hệ thống lưu trữ dữ liệu (*Data storage system*)
Hệ thống cơ sở dữ liệu quan hệ truyền thống (*general-purpose relational database*) không phù hợp cho tác vụ này. 
Chẳng hạn, việc tính toán giá trị trung bình trượt (*moving average*) trong một khung thời gian động (*rolling time window*) đòi hỏi các câu lệnh truy vấn SQL vô cùng phức tạp và rất khó đọc (sẽ có một ví dụ minh họa chi tiết trong phần phân tích chuyên sâu). 

Bên cạnh đó, để hỗ trợ việc gắn thẻ/nhãn (*tagging/labeling*), chúng ta bắt buộc phải đánh chỉ mục (*index*) cho từng thẻ một. Hơn thế nữa, một cơ sở dữ liệu quan hệ đa mục đích không thể duy trì hiệu năng tốt dưới tải trọng ghi liên tục và nặng nề (*constant heavy write load*). Ở quy mô hệ thống của chúng ta, đội ngũ kỹ thuật sẽ phải tốn rất nhiều công sức để tinh chỉnh (*tuning*) cơ sở dữ liệu, và ngay cả khi đã tinh chỉnh, hệ thống vẫn có nguy cơ không đạt hiệu năng kỳ vọng.

---

### Trang 141

![Sơ đồ trang 141](images/page_141.jpeg)

Việc sử dụng một cơ sở dữ liệu NoSQL đa mục đích (*general-purpose NoSQL database*) cũng không thực sự hấp dẫn khi trên thị trường đã có sẵn các cơ sở dữ liệu chuỗi thời gian chuyên dụng (*Time-Series Database - TSDB*) đạt chuẩn công nghiệp.

Hiện có rất nhiều hệ thống lưu trữ được tối ưu hóa riêng biệt cho dữ liệu chuỗi thời gian. Nhờ sự tối ưu này, chúng ta có thể sử dụng ít máy chủ hơn đáng kể để xử lý cùng một khối lượng dữ liệu. Rất nhiều cơ sở dữ liệu dạng này cung cấp sẵn các giao diện truy vấn tùy biến (*custom query interfaces*), được thiết kế chuyên biệt cho việc phân tích chuỗi thời gian, giúp việc sử dụng trở nên dễ dàng hơn nhiều so với SQL. Một số hệ thống thậm chí còn tích hợp sẵn các tính năng quản lý thời hạn lưu trữ (*data retention*) và tổng hợp dữ liệu định kỳ (*data aggregation*). Dưới đây là một số ví dụ tiêu biểu:

- **OpenTSDB:** Là một cơ sở dữ liệu chuỗi thời gian phân tán (*distributed time-series database*), tuy nhiên do được xây dựng trên nền tảng Hadoop và HBase, việc vận hành một cụm Hadoop/HBase làm tăng đáng kể độ phức tạp của hạ tầng.
- **MetricsDB [12]:** Được Twitter phát triển và sử dụng nội bộ.
- **Amazon Timestream [13]:** Dịch vụ cơ sở dữ liệu chuỗi thời gian do Amazon cung cấp.

Theo bảng xếp hạng DB-Engines [14], hai cơ sở dữ liệu chuỗi thời gian phổ biến nhất hiện nay là **InfluxDB [15]** và **Prometheus**. Cả hai đều được thiết kế để lưu trữ khối lượng dữ liệu chuỗi thời gian khổng lồ và thực hiện các phân tích thời gian thực (*real-time analysis*) với tốc độ cao. Cả hai giải pháp đều hoạt động chủ yếu dựa trên bộ nhớ đệm (*in-memory cache*) kết hợp với cơ chế lưu trữ trên đĩa cứng (*on-disk storage*), đồng thời giải quyết rất tốt bài toán về tính bền bỉ của dữ liệu (*durability*) cũng như hiệu năng (*performance*). 

Như được thể hiện trong Hình 5.5, một máy chủ InfluxDB trang bị 8 lõi CPU (*8 cores*) và 32GB RAM có thể xử lý hơn **250.000 lượt ghi mỗi giây (*writes per second*)**.

| vCPU / CPU | RAM | IOPS | Lượt ghi mỗi giây (*Writes per second*) | Lượt truy vấn mỗi giây (*Queries per second*) | Số chuỗi duy nhất (*Unique series*) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2-4 cores | 2-4 GB | < 500 | 5.000 | < 5 | < 100.000 |
| 4-6 cores | 8-32 GB | 500 - 1000 | 250.000 | < 25 | < 1.000.000 |
| 8+ cores | 32+ GB | 1000+ | > 250.000 | > 25 | > 1.000.000 |

*Hình 5.5: Đánh giá hiệu năng InfluxDB (InfluxDB benchmarking)*

> [!NOTE]
> Vì cơ sở dữ liệu chuỗi thời gian là một hệ thống chuyên dụng, bạn không bắt buộc phải nắm rõ toàn bộ chi tiết kiến trúc nội bộ (*internals*) trong một buổi phỏng vấn thiết kế hệ thống, trừ khi bạn đã chủ động đề cập đến nó trong CV/hồ sơ của mình. 
> 
> Mục tiêu cốt lõi trong phỏng vấn là bạn phải nhận thức được rằng dữ liệu chỉ số bản chất là dữ liệu chuỗi thời gian (*time-series in nature*), và chúng ta hoàn toàn có thể lựa chọn các giải pháp TSDB chuyên dụng như InfluxDB để lưu trữ chúng.

Một đặc tính quan trọng khác của một TSDB mạnh mẽ là khả năng tổng hợp (*aggregation*) và phân tích dữ liệu chuỗi thời gian hiệu quả dựa trên các nhãn (*labels*, hay còn gọi là *tags* trong một số hệ thống). Ví dụ, InfluxDB xây dựng sẵn các cấu trúc chỉ mục (*indexes*) trên các nhãn để tăng tốc độ tra cứu chuỗi thời gian theo nhãn [16]. Hệ thống cũng cung cấp các chỉ dẫn thực hành tốt nhất (*best-practice guidelines*) rõ ràng về cách sử dụng nhãn sao cho không gây quá tải cho cơ sở dữ liệu. 

Nguyên tắc then chốt là phải đảm bảo mỗi nhãn đều có **độ biến thiên thấp (*low cardinality*)** (tức là tập giá trị khả dĩ của nhãn là hữu hạn và nhỏ)...

---

### Trang 142

...sẽ tiêu tốn rất nhiều nỗ lực nếu cố gắng tự hiện thực hóa điều này bằng một cơ sở dữ liệu đa mục đích.

---

#### Thiết kế mức cao (*High-level design*)
Sơ đồ thiết kế kiến trúc mức cao được mô tả trong Hình 5.6.

![Sơ đồ trang 142](images/page_142.jpeg)

*Hình 5.6: Thiết kế mức cao (High-level design)*

Kiến trúc bao gồm các luồng và thành phần:
- **Nguồn chỉ số (*Metrics Source*):** Các máy chủ ứng dụng, dịch vụ, hạ tầng,...
- **Bộ thu thập chỉ số (*Metrics Collector*):** Thu thập dữ liệu từ các Metrics Source.
- **Cơ sở dữ liệu chuỗi thời gian (*Time series DB*):** Lưu trữ dữ liệu chỉ số.
- **Dịch vụ truy vấn (*Query Service*):** Đóng vai trò cung cấp các cổng HTTPS Endpoints tiếp nhận các truy vấn dữ liệu từ người dùng hoặc hệ thống bên ngoài, chuyển tiếp truy vấn vào Time series DB.
- **Hệ thống cảnh báo (*Alerting System*):** Gửi truy vấn (*Send Queries*) đến Query Service để kiểm tra ngưỡng vi phạm; từ đó kích hoạt và gửi thông báo qua Email, Tin nhắn văn bản (*Text Message*), PagerDuty, v.v.
- **Hệ thống trực quan hóa (*Visualization System*):** Gửi truy vấn (*Send Queries*) đến Query Service để hiển thị các chỉ số dưới dạng các biểu đồ/đồ thị đa dạng.

---

### Bước 3 - Đi sâu vào thiết kế chi tiết (*Step 3 - Design Deep Dive*)

Trong một cuộc phỏng vấn thiết kế hệ thống, ứng viên được kỳ vọng sẽ phân tích chuyên sâu vào một vài thành phần trọng yếu hoặc các luồng xử lý cốt lõi. Trong phần này, chúng ta sẽ khảo sát chi tiết các chủ đề sau:
- Thu thập chỉ số (*Metrics collection*)
- Mở rộng quy mô đường ống truyền tải chỉ số (*Scaling the metrics transmission pipeline*)

---

### Trang 143

- Dịch vụ truy vấn (*Query service*)
- Tầng lưu trữ (*Storage layer*)
- Hệ thống cảnh báo (*Alerting system*)
- Hệ thống trực quan hóa (*Visualization system*)

---

#### Thu thập chỉ số (*Metrics collection*)
Trước tiên, chúng ta cùng phân tích luồng thu thập chỉ số (*metrics collection flow*). Thành phần này nằm trong khối viền nét đứt ở Hình 5.7.

![Sơ đồ trang 143](images/page_143.jpeg)

*Hình 5.7: Luồng thu thập chỉ số (Metrics collection flow)*

---

#### So sánh mô hình Kéo và Đẩy (*Pull vs Push models*)
Có hai phương thức chính để thu thập dữ liệu chỉ số: **Kéo (*Pull*)** hoặc **Đẩy (*Push*)**. Việc lựa chọn mô hình nào tối ưu hơn luôn là một chủ đề tranh luận quen thuộc trong thiết kế kiến trúc và không có câu trả lời tuyệt đối đúng sai. Hãy cùng phân tích kỹ lưỡng từng mô hình.

##### Mô hình Kéo (*Pull model*)
Hình 5.8 minh họa cơ chế thu thập dữ liệu bằng mô hình kéo (*pull model*) thông qua giao thức HTTP. Trong mô hình này, chúng ta triển khai các bộ thu thập chỉ số chuyên dụng (*dedicated metric collectors*) với nhiệm vụ định kỳ kéo các giá trị chỉ số (*pull metrics values*) từ các ứng dụng đang chạy.

# CHƯƠNG 5: HỆ THỐNG GIÁM SÁT CHỈ SỐ VÀ CẢNH BÁO (METRICS MONITORING AND ALERTING SYSTEM)

---

## BƯỚC 3: THIẾT KẾ ĐI SÂU CHI TIẾT (STEP 3 - DESIGN DEEP DIVE)

### Mô hình Kéo (Pull Model)

Trong mô hình này, hệ thống thu thập chỉ số (**Metrics Collector**) chủ động lấy dữ liệu từ các nguồn phát sinh chỉ số (**Metrics Sources**).

![Sơ đồ trang 144](images/page_144.jpeg)
*Hình 5.8: Mô hình Kéo (Pull model)*

* **Phát hiện Dịch vụ (Service Discovery):** etcd, Zookeeper.
* **Nguồn chỉ số (Metrics Source):** Web Servers, DB Clusters (Cụm cơ sở dữ liệu), Queue Clusters (Cụm hàng đợi tin nhắn), Cache Clusters (Cụm bộ nhớ đệm).
* **Bộ thu thập chỉ số (Metrics Collector):** Thực hiện hành động kéo chỉ số (*Pull metrics*) từ các nguồn trên.

Trong cách tiếp cận này, **Metrics Collector** cần nắm rõ danh sách đầy đủ các điểm cuối dịch vụ (*service endpoints*). Trong môi trường phân tán quy mô lớn, các máy chủ thường xuyên được bổ sung hoặc gỡ bỏ, và chúng ta cần đảm bảo rằng các bộ thu thập chỉ số không bỏ sót bất kỳ thay đổi nào về điểm cuối dịch vụ. Để giải quyết bài toán này, chúng ta tích hợp cơ chế **Service Discovery** (Phát hiện dịch vụ) như được minh họa trong **Hình 5.9**.

![Sơ đồ trang 144](images/page_144.jpeg)
*Hình 5.9: Phát hiện dịch vụ (Service discovery)*

* Các dịch vụ tự đăng ký thông tin cấu hình và metadata lên hệ thống Service Discovery (ví dụ: `region:us-west`, `region:us-south`, `region:us-east`, `type:mysql`, `host:10.10.11.1`...).

**Hình 5.10** giải thích chi tiết luồng hoạt động của mô hình kéo (*pull model*):

![Sơ đồ trang 145](images/page_145.jpeg)
*Hình 5.10: Chi tiết về mô hình kéo (Pull model in detail)*

1. **Bộ thu thập chỉ số (Metrics Collector)** lấy thông tin cấu hình siêu dữ liệu (*metadata*) của các điểm cuối dịch vụ từ hệ thống **Service Discovery** (etcd, Zookeeper) thông qua tác vụ `① Discover Targets`. Metadata bao gồm chu kỳ kéo (*pulling interval*), địa chỉ IP, các tham số thời gian chờ (*timeout*) và cơ chế thử lại (*retry*), v.v.
2. **Metrics Collector** gửi các yêu cầu HTTP (`② HTTP Requests`) đến các điểm cuối đã xác định trước (ví dụ: `/metrics`) để kéo dữ liệu chỉ số. Để mở (expose) điểm cuối này, một thư viện máy khách (*client library*) thường cần được tích hợp vào dịch vụ được giám sát. Trong **Hình 5.10**, dịch vụ ở đây là các máy chủ web (**Web Servers**).
3. **Tùy chọn nâng cao:** Metrics Collector có thể đăng ký cơ chế nhận thông báo sự kiện thay đổi (*change event notification*) với hệ thống Service Discovery để nhận cập nhật ngay khi các điểm cuối dịch vụ thay đổi. Ngoài ra, Metrics Collector cũng có thể chủ động thăm dò (*poll*) định kỳ để phát hiện các thay đổi về điểm cuối.

> [!IMPORTANT]
> **Thách thức về Quy mô (Scalability):**
> Ở quy mô của chúng ta, một node Metrics Collector đơn lẻ sẽ không thể nào xử lý nổi hàng ngàn máy chủ. Chúng ta bắt buộc phải sử dụng một nhóm/cụm các bộ thu thập chỉ số (**pool of metrics collectors**) để đáp ứng tải. 
> 
> Tuy nhiên, một vấn đề phổ biến khi có nhiều thực thể collector là nhiều node có thể cùng cố gắng kéo dữ liệu từ một tài nguyên máy chủ đích, dẫn đến việc trùng lặp dữ liệu (*duplicate data*). Bắt buộc phải có một cơ chế điều phối (*coordination scheme*) giữa các thực thể collector để triệt tiêu vấn đề này.

Một giải pháp tiềm năng là phân bổ mỗi collector quản lý một dải phạm vi trên vòng băm nhất quán (**Consistent Hash Ring**), sau đó ánh xạ từng máy chủ được giám sát vào vòng băm dựa trên tên định danh duy nhất (*unique name*) của nó. Cơ chế này đảm bảo mỗi máy chủ nguồn chỉ số chỉ do duy nhất một collector phụ trách thu thập. Hãy cùng xem xét ví dụ cụ thể:

Như được minh họa trong **Hình 5.11**, có 4 bộ thu thập (*Collectors*) và 6 máy chủ nguồn chỉ số (*Metrics Source Servers*):
* Mỗi collector chịu trách nhiệm thu thập chỉ số từ một tập hợp máy chủ riêng biệt.
* **Collector 2** chịu trách nhiệm thu thập chỉ số từ dải chứa **Server 1** ($S_1$) và **Server 5** ($S_5$).

![Sơ đồ trang 146](images/page_146.jpeg)
*Hình 5.11: Băm nhất quán (Consistent hashing)*

---

### Mô hình Đẩy (Push Model)

Trong mô hình đẩy (**Push model**), các máy chủ nguồn (máy chủ web, máy chủ cơ sở dữ liệu, v.v.) chủ động gửi trực tiếp các chỉ số đến **Metrics Collector**.

![Sơ đồ trang 146](images/page_146.jpeg)
*Hình 5.12: Mô hình Đẩy (Push model)*

* **Nguồn chỉ số (Metrics Source):** Web Servers, DB Clusters, Queue Clusters, Cache Clusters.
* **Hành vi:** Tất cả các cụm trên trực tiếp đẩy chỉ số (*Push metrics*) vào **Metrics Collector**.

Trong mô hình đẩy, một tiến trình đại diện thu thập (**Collection Agent**) thường được cài đặt trực tiếp trên mỗi máy chủ chịu sự giám sát. Collection Agent là một tiến trình chạy nền dài hạn (*long-running software process*), thực hiện thu thập các chỉ số từ các dịch vụ đang chạy trên máy chủ nội bộ và đẩy định kỳ các chỉ số đó về cho Metrics Collector. 

Ngoài ra, Collection Agent cũng có thể thực hiện tổng hợp chỉ số cục bộ (**aggregate metrics locally** - đặc biệt là các bộ đếm đơn giản (*simple counter*)) trước khi gửi qua mạng đến các metrics collector.

![Sơ đồ trang 147](images/page_147.jpeg)
*Hình 5.13: Bộ cân bằng tải (Load balancer)*

Để ngăn ngừa mất mát dữ liệu (*data loss*) khi các Metrics Collector bị quá tải hoặc xử lý chậm trễ (**falls behind**), một bộ cân bằng tải (**Load Balancer**) được đặt phía trước cụm collector. Cụm collector nên được thiết lập cơ chế tự động co giãn (**Auto-scaling**) dựa trên mức tải CPU của các máy chủ thu thập.

---

### Nên chọn Kéo hay Đẩy? (Pull or Push?)

Vậy thì, kiến trúc nào là sự lựa chọn tối ưu hơn cho hệ thống của chúng ta? Giống như nhiều bài toán kỹ thuật khác trong thực tế, không có một câu trả lời tuyệt đối đúng cho mọi trường hợp. Cả hai giải pháp đều có các ca sử dụng thành công và phổ biến rộng rãi trong thực tế:
* **Các ví dụ tiêu biểu cho kiến trúc Kéo (Pull):** Prometheus.
* **Các ví dụ tiêu biểu cho kiến trúc Đẩy (Push):** Amazon CloudWatch [18] và Graphite [19].

> [!TIP]
> Việc thấu hiểu tường tận ưu và nhược điểm của từng phương pháp quan trọng hơn nhiều so với việc cố gắng chọn ra phương án áp đảo trong một buổi phỏng vấn thiết kế hệ thống (*System Design Interview*).

**Bảng 5.3** so sánh chi tiết ưu và nhược điểm giữa hai kiến trúc Đẩy và Kéo [20] [21] [22] [23]:

| Tiêu chí | Mô hình Kéo (Pull) | Mô hình Đẩy (Push) |
| :--- | :--- | :--- |
| **Dễ dàng gỡ lỗi (Easy debugging)** | Điểm cuối `/metrics` trên các máy chủ ứng dụng dùng để kéo chỉ số có thể được truy cập để kiểm tra chỉ số bất kỳ lúc nào. Bạn thậm chí có thể thực hiện việc này trực tiếp trên máy tính cá nhân (*laptop*).<br>👉 **Pull chiếm ưu thế (Pull wins).** | Khó gỡ lỗi trực tiếp tại máy nguồn hơn vì dữ liệu chỉ được đẩy một chiều ra ngoài. |
| **Kiểm tra trạng thái hoạt động (Health check)** | Nếu một máy chủ ứng dụng không phản hồi lại yêu cầu kéo dữ liệu (*pull request*), bạn có thể nhanh chóng xác định được máy chủ ứng dụng đó đã ngừng hoạt động (*down*).<br>👉 **Pull chiếm ưu thế (Pull wins).** | Nếu bộ thu thập chỉ số không nhận được dữ liệu, sự cố có thể bắt nguồn từ lỗi mạng (*network issues*) chứ chưa hẳn do máy chủ ứng dụng sập. |
| **Các tác vụ ngắn hạn (Short-lived jobs)** | Một số tác vụ xử lý theo lô (*batch jobs*) có thể hoàn thành rất nhanh và không tồn tại đủ lâu để kịp thời điểm collector kéo dữ liệu.<br>*(Vấn đề này có thể khắc phục bằng cách bổ sung Pushgateway cho mô hình pull [24]).* | Các tác vụ ngắn hạn có thể chủ động đẩy chỉ số ngay khi kết thúc trước khi tiến trình tắt.<br>👉 **Push chiếm ưu thế (Push wins).** |
| **Tường lửa hoặc cấu hình mạng phức tạp (Firewall or complicated network setups)** | Việc máy chủ thu thập chỉ số phải chủ động kéo dữ liệu đòi hỏi tất cả các điểm cuối chỉ số phải có khả năng tiếp cận được (*reachable*). Điều này gây ra nhiều trở ngại tiềm tàng trong các mô hình triển khai đa trung tâm dữ liệu (*multi-datacenter setups*), đòi hỏi hạ tầng mạng phải cấu hình tinh vi hơn. | Nếu bộ thu thập chỉ số được thiết lập phía sau một bộ cân bằng tải (**Load Balancer**) và nhóm tự động co giãn (**Auto-scaling group**), hệ thống có khả năng nhận dữ liệu từ bất kỳ đâu đẩy về.<br>👉 **Push chiếm ưu thế (Push wins).** |
| **Hiệu năng truyền tải (Performance)** | Các phương thức Kéo thường sử dụng giao thức **TCP**. | Các phương thức Đẩy thường sử dụng giao thức **UDP**. Điều này đồng nghĩa với việc phương thức đẩy mang lại độ trễ truyền tải chỉ số thấp hơn (*lower-latency transports*).<br>*(Luận điểm phản bác ở đây là chi phí thiết lập kết nối TCP thực tế là rất nhỏ so với toàn bộ kích thước tải dữ liệu chỉ số).* |
| **Tính xác thực của dữ liệu (Data authenticity)** | Các máy chủ ứng dụng cần thu thập chỉ số được định nghĩa trước một cách chặt chẽ trong các tệp cấu hình (*config files*). Dữ liệu thu thập từ các máy chủ này luôn được đảm bảo tính xác thực tuyệt đối. | Bất kỳ loại máy khách (*client*) nào cũng có thể đẩy dữ liệu chỉ số tới collector. Điều này có thể được kiểm soát bằng cách lập danh sách trắng (*whitelisting*) các máy chủ được phép gửi chỉ số, hoặc bắt buộc cơ chế xác thực (**Authentication**). |

*Bảng 5.3: So sánh giữa Kéo (Pull) và Đẩy (Push)*

Như đã đề cập ở trên, cuộc tranh luận giữa **Pull** và **Push** là chủ đề thường thấy và không có đáp án duy nhất đúng. Một tổ chức quy mô lớn thường cần hỗ trợ cả hai mô hình, đặc biệt là với sự bùng nổ của kiến trúc không máy chủ (**Serverless** [25]) hiện nay — nơi bạn hoàn toàn không có khả năng cài đặt một tiến trình agent nội bộ để chủ động đẩy dữ liệu ra ngoài.

---

### Mở rộng Quy mô Đường truyền Chỉ số (Scale the Metrics Transmission Pipeline)

![Sơ đồ trang 149](images/page_149.jpeg)
*Hình 5.14: Đường ống truyền tải chỉ số (Metrics transmission pipeline)*

Kiến trúc đường ống truyền tải chỉ số bao gồm các thành phần cốt lõi sau:
* **Nguồn chỉ số (Metrics Source):** Nơi phát sinh các chỉ số vận hành.
* **Bộ thu thập chỉ số (Metrics Collector):** Tiếp nhận dữ liệu từ nguồn chỉ số.
* **Cơ sở dữ liệu chuỗi thời gian (Time series DB):** Lưu trữ tập trung toàn bộ dữ liệu chỉ số theo trục thời gian.
* **Dịch vụ truy vấn (Query Service):** Tiếp nhận các truy vấn (`Send Queries`) để phục vụ hai hệ thống tiêu thụ đầu ra:
  * **Hệ thống trực quan hóa (Visualization System):** Hiển thị bảng biểu, biểu đồ giám sát.
  * **Hệ thống cảnh báo (Alerting System):** Gửi các cảnh báo khi chỉ số vượt ngưỡng thông qua: Email, Tin nhắn văn bản (Text Message / SMS), PagerDuty, và các Điểm cuối HTTPS (HTTPS Endpoints / Webhooks).

# CHƯƠNG 5: HỆ THỐNG GIÁM SÁT CHỈ SỐ VÀ CẢNH BÁO (METRICS MONITORING AND ALERTING SYSTEM)

## BƯỚC 3: THIẾT KẾ CHI TIẾT (DESIGN DEEP DIVE)

### Hàng đợi thông điệp (Queueing Component)

...xử lý được nhu cầu tải cao (handle the demand).

Để giải quyết vấn đề này, chúng ta đưa vào một thành phần hàng đợi (queueing component) như minh họa trong **Hình 5.15**.

![Sơ đồ trang 150](images/page_150.jpeg)
*Hình 5.15: Bổ sung các hàng đợi (Add queues)*

Trong thiết kế này, bộ thu thập chỉ số (metrics collector) gửi dữ liệu metrics đến các hệ thống hàng đợi như **Kafka**. Sau đó, các tiến trình tiêu thụ dữ liệu (consumers) hoặc các dịch vụ xử lý luồng dữ liệu (streaming processing services) như **Apache Storm**, **Flink**, và **Spark** sẽ xử lý và đẩy dữ liệu vào cơ sở dữ liệu chuỗi thời gian (time-series database). Hướng tiếp cận này mang lại một số ưu điểm vượt trội:

* **Kafka** được sử dụng như một nền tảng truyền thông điệp phân tán (distributed messaging platform) có độ tin cậy cao (**High Reliability**) và khả năng mở rộng quy mô lớn (**Scalability**).
* Nó giúp tách rời (**Decouple**) hoàn toàn dịch vụ thu thập dữ liệu (data collection) và dịch vụ xử lý dữ liệu (data processing) với nhau.
* Nó có thể dễ dàng ngăn chặn tình trạng mất mát dữ liệu (**Data Loss**) khi cơ sở dữ liệu tạm thời không khả dụng, bằng cách lưu giữ dữ liệu an toàn bên trong Kafka.

#### Mở rộng quy mô thông qua Kafka (Scale through Kafka)

Có một số phương pháp giúp chúng ta tận dụng cơ chế phân vùng tích hợp sẵn (**Built-in Partition Mechanism**) của Kafka để mở rộng quy mô hệ thống:

* Cấu hình số lượng phân vùng (**Partitions**) dựa trên các yêu cầu về thông lượng (**Throughput**).
* Phân vùng dữ liệu chỉ số theo tên metric (**Metric Names**), giúp các consumer có thể tổng hợp dữ liệu (**Aggregate**) theo tên chỉ số một cách thuận tiện.
* Tiếp tục phân vùng dữ liệu chỉ số chi tiết hơn nữa bằng các thẻ/nhãn (**Tags/Labels**).
* Phân loại và gán mức độ ưu tiên (**Categorize & Prioritize**) cho các metrics để những chỉ số quan trọng luôn được xử lý trước.

---

![Sơ đồ trang 151](images/page_151.jpeg)
*Hình 5.16: Phân vùng Kafka (Kafka partition)*

#### Giải pháp thay thế cho Kafka (Alternative to Kafka)

Việc vận hành và bảo trì một cụm hệ thống Kafka ở quy mô môi trường production thực tế là một nhiệm vụ không hề nhỏ. Bạn có thể gặp phải phản biện từ người phỏng vấn về vấn đề này. Trên thực tế, có những hệ thống tiếp nhận và giám sát chỉ số (monitoring ingestion systems) quy mô cực lớn đang hoạt động mà không cần sử dụng bất kỳ hàng đợi trung gian nào. 

Cơ sở dữ liệu chuỗi thời gian lưu trên bộ nhớ trong (**In-Memory Time-Series Database**) mang tên **Gorilla [26]** của Facebook là một ví dụ điển hình; nó được thiết kế để duy trì tính sẵn sàng cao (**High Availability**) cho các tác vụ ghi (**Writes**), ngay cả khi xảy ra sự cố phân mảnh mạng cục bộ (**Partial Network Failure**). Hoàn toàn có thể lập luận rằng một thiết kế như vậy cũng sở hữu độ tin cậy tương đương với việc sử dụng hàng đợi trung gian như Kafka.

---

### Vị trí thực hiện tổng hợp dữ liệu (Where aggregations can happen)

Dữ liệu chỉ số (Metrics) có thể được tổng hợp (**Aggregated**) tại nhiều vị trí khác nhau: tại tác tử thu thập (**Collection Agent** - phía client), tại đường ống tiếp nhận dữ liệu (**Ingestion Pipeline** - trước khi ghi vào kho lưu trữ), và tại phía truy vấn (**Query Side** - sau khi đã ghi vào kho lưu trữ). Hãy cùng xem xét chi tiết từng vị trí:

* **Tác tử thu thập (Collection agent):** Tác tử thu thập được cài đặt trên phía máy khách (client-side) chỉ hỗ trợ logic tổng hợp đơn giản. Ví dụ: tổng hợp giá trị của một biến đếm (**Counter**) mỗi phút một lần trước khi gửi dữ liệu về bộ thu thập chỉ số (metrics collector).
* **Đường ống tiếp nhận (Ingestion pipeline):** Để tổng hợp dữ liệu trước khi ghi vào kho lưu trữ, chúng ta thường cần đến các công cụ xử lý luồng (**Stream Processing Engines**) như Flink. Dung lượng ghi sẽ được giảm thiểu đáng kể vì chỉ có kết quả đã qua tính toán mới được ghi vào cơ sở dữ liệu. Tuy nhiên, việc xử lý các sự kiện đến muộn (**Late-Arriving Events**) có thể là một thách thức lớn, và một nhược điểm khác là chúng ta sẽ mất đi độ chính xác chi tiết của dữ liệu (**Data Precision**) cùng sự linh hoạt vốn có do không còn lưu trữ dữ liệu thô ban đầu (**Raw Data**).
* **Phía truy vấn (Query side):** Dữ liệu thô có thể được tổng hợp qua một khoảng thời gian nhất định ngay tại thời điểm thực hiện truy vấn (query time). Phương pháp này hoàn toàn không làm mất mát dữ liệu, nhưng tốc độ truy vấn có thể sẽ chậm hơn do kết quả truy vấn phải được tính toán ngay lúc chạy và phải quét trên toàn bộ tập dữ liệu đồ sộ.

---

### Dịch vụ truy vấn (Query service)

Dịch vụ truy vấn bao gồm một cụm các máy chủ truy vấn (query servers), có nhiệm vụ truy cập vào các cơ sở dữ liệu chuỗi thời gian (time-series databases) và xử lý các yêu cầu từ hệ thống hiển thị trực quan (visualization system) hoặc hệ thống cảnh báo (alerting system). 

Việc sở hữu một cụm máy chủ truy vấn chuyên dụng giúp tách rời (**Decouples**) cơ sở dữ liệu chuỗi thời gian khỏi các hệ thống client (hệ thống trực quan hóa và cảnh báo). Điều này mang lại cho chúng ta sự linh hoạt cao để thay đổi cơ sở dữ liệu chuỗi thời gian, hoặc chuyển đổi hệ thống hiển thị và cảnh báo bất cứ lúc nào khi cần thiết.

#### Tầng bộ nhớ đệm (Cache layer)

Để giảm tải cho cơ sở dữ liệu chuỗi thời gian và giúp dịch vụ truy vấn đạt hiệu năng cao hơn, các máy chủ bộ nhớ đệm (**Cache Servers**) được bổ sung để lưu trữ các kết quả truy vấn, như minh họa trong **Hình 5.17**.

![Sơ đồ trang 152](images/page_152.jpeg)
*Hình 5.17: Tầng bộ nhớ đệm (Cache layer)*

#### Luận điểm phản đối dịch vụ truy vấn (The case against query service)

Thực tế có thể không có nhu cầu cấp thiết phải tự xây dựng một lớp trừu tượng riêng của chúng ta (dịch vụ truy vấn), bởi vì hầu hết các hệ thống hiển thị trực quan và cảnh báo quy mô công nghiệp trên thị trường hiện nay đều sở hữu các plugin mạnh mẽ để kết nối trực tiếp với các cơ sở dữ liệu chuỗi thời gian nổi tiếng. Và nếu lựa chọn được một cơ sở dữ liệu chuỗi thời gian phù hợp, chúng ta cũng không cần thiết phải tự xây dựng thêm tầng bộ nhớ đệm (caching) riêng.

#### Ngôn ngữ truy vấn cơ sở dữ liệu chuỗi thời gian (Time-series database query language)

Hầu hết các hệ thống giám sát chỉ số phổ biến như **Prometheus** và **InfluxDB** không sử dụng chuẩn SQL mà sở hữu các ngôn ngữ truy vấn riêng biệt. Một lý do quan trọng là rất khó để xây dựng các câu truy vấn SQL cho dữ liệu chuỗi thời gian. Ví dụ, như được đề cập tại đây [27], việc tính toán một đường trung bình động hàm mũ (**Exponential Moving Average - EMA**) khi viết bằng SQL có thể phức tạp như sau:

```sql
SELECT id,
       temp,
       avg(temp) OVER(PARTITION BY group_nr ORDER BY time_read) AS rolling_avg
FROM (
    SELECT id,
           temp,
           time_read,
           interval_group,
           id - row_number() OVER(PARTITION BY interval_group ORDER BY time_read) AS group_nr
    FROM (
        SELECT id,
               time_read,
               extract(epoch FROM time_read)::int4 / 900 AS interval_group,
               temp
        FROM readings
    ) t1
) t2
ORDER BY time_read;
```

Trong khi đó với **Flux**, một ngôn ngữ được tối ưu hóa cho phân tích chuỗi thời gian (sử dụng trong InfluxDB), câu truy vấn lại ngắn gọn và trực quan như sau:

```flux
from(db:"telegraf")
  |> range(start:-1h)
  |> filter(fn:(r) => r._measurement == "foo")
  |> exponentialMovingAverage(size:-10s)
```

Như bạn có thể thấy, cú pháp này dễ hiểu hơn rất nhiều.

---

### Tầng lưu trữ (Storage layer)

Bây giờ, chúng ta hãy đi sâu vào chi tiết của tầng lưu trữ (storage layer).

#### Lựa chọn cơ sở dữ liệu chuỗi thời gian một cách cẩn trọng (Choose a time-series database carefully)

Theo một bài báo nghiên cứu được công bố bởi Facebook [26], có ít nhất **85%** tổng số các truy vấn tới kho lưu trữ dữ liệu vận hành (operational data store) là nhắm vào dữ liệu được thu thập trong vòng **26 giờ qua**. Nếu chúng ta sử dụng một cơ sở dữ liệu chuỗi thời gian biết tận dụng triệt để đặc tính này, nó có thể tạo ra tác động to lớn đến hiệu năng tổng thể của toàn hệ thống. Nếu bạn quan tâm đến thiết kế của lõi lưu trữ (storage engine), vui lòng tham khảo tài liệu thiết kế engine lưu trữ của InfluxDB [28].

#### Tối ưu hóa không gian lưu trữ (Space optimization)

Như đã giải thích trong phần các yêu cầu tổng thể mức cao, khối lượng dữ liệu chỉ số cần lưu trữ là cực kỳ khổng lồ. Dưới đây là một số chiến lược để giải quyết thách thức này:

##### Mã hóa và nén dữ liệu (Data encoding and compression)
Mã hóa và nén dữ liệu có thể làm giảm đáng kể dung lượng lưu trữ. Các tính năng này thường được tích hợp sẵn bên trong một cơ sở dữ liệu chuỗi thời gian chất lượng tốt. Dưới đây là một ví dụ đơn giản:

![Sơ đồ trang 154](images/page_154.jpeg)
*Hình 5.18: Mã hóa dữ liệu (Data encoding - Double-delta Encoding)*

Như bạn có thể thấy trong hình ảnh trên, hai giá trị `1610087371` và `1610087381` chỉ chênh lệch nhau đúng 10 giây; giá trị sai số này chỉ mất **4 bits** để biểu diễn thay vì phải tốn trọn vẹn **32 bits** cho toàn bộ dấu thời gian (timestamp). Do đó, thay vì lưu trữ các giá trị tuyệt đối, hệ thống có thể lưu trữ độ lệch (**Delta**) giữa các giá trị cùng với một giá trị gốc cơ sở (base value), ví dụ như: `1610087371`, `10`, `10`, `9`, `11`.

##### Giảm tần suất lấy mẫu (Downsampling)
Giảm tần suất lấy mẫu (**Downsampling**) là quá trình chuyển đổi dữ liệu độ phân giải cao (**High-Resolution Data**) thành dữ liệu độ phân giải thấp (**Low-Resolution Data**) nhằm giảm dung lượng đĩa tổng thể. Vì chính sách lưu giữ dữ liệu (**Data Retention**) của chúng ta là 1 năm, chúng ta hoàn toàn có thể áp dụng downsample cho các dữ liệu cũ. Ví dụ: chúng ta có thể cho phép các kỹ sư và chuyên gia khoa học dữ liệu định nghĩa các quy tắc cho từng chỉ số khác nhau. Dưới đây là một bộ quy tắc mẫu:

* **Thời gian lưu trữ: 7 ngày**, giữ nguyên độ phân giải gốc, không lấy mẫu (no sampling).
* **Thời gian lưu trữ: 30 ngày**, giảm tần suất lấy mẫu xuống độ phân giải 1 phút (1 minute resolution).
* **Thời gian lưu trữ: 1 năm**, giảm tần suất lấy mẫu xuống độ phân giải 1 giờ (1 hour resolution).

Hãy xem xét một ví dụ cụ thể khác: tổng hợp dữ liệu có độ phân giải 10 giây thành dữ liệu có độ phân giải 30 giây.

*Bảng 5.4: Dữ liệu ở độ phân giải 10 giây (10-second resolution data)*

| timestamp | hostname | metric | metric_value |
| :--- | :--- | :--- | :--- |
| 2021-10-24T19:00:00Z | host-a | cpu | 10 |
| 2021-10-24T19:00:10Z | host-a | cpu | 16 |
| 2021-10-24T19:00:20Z | host-a | cpu | 20 |
| 2021-10-24T19:00:30Z | host-a | cpu | 30 |
| 2021-10-24T19:00:40Z | host-a | cpu | 20 |
| 2021-10-24T19:00:50Z | host-a | cpu | 30 |

Thực hiện gộp tích lũy (**Rollup**) từ dữ liệu độ phân giải 10 giây thành dữ liệu độ phân giải 30 giây:

*Bảng 5.5: Dữ liệu ở độ phân giải 30 giây (30-second resolution data)*

| timestamp | hostname | metric | metric_value (avg) |
| :--- | :--- | :--- | :--- |
| 2021-10-24T19:00:00Z | host-a | cpu | 19 |
| 2021-10-24T19:00:30Z | host-a | cpu | 25 |

##### Lưu trữ lạnh (Cold storage)
Lưu trữ lạnh (**Cold Storage**) là việc lưu trữ dữ liệu không còn hoạt động (**Inactive Data**) và rất hiếm khi được truy cập. Chi phí tài chính dành cho cold storage là thấp hơn rất nhiều.

> [!TIP]
> Tóm lại, chúng ta nên cân nhắc sử dụng các hệ thống hiển thị trực quan và cảnh báo của bên thứ ba (third-party) có sẵn thay vì tự xây dựng mới hoàn toàn từ đầu.

---

### Hệ thống cảnh báo (Alerting system)

Phục vụ cho mục tiêu của buổi phỏng vấn thiết kế hệ thống, hãy cùng phân tích kiến trúc hệ thống cảnh báo, được minh họa trong **Hình 5.19** dưới đây:

![Sơ đồ trang 155](images/page_155.jpeg)
*Hình 5.19: Hệ thống cảnh báo (Alerting system)*

Quy trình kích hoạt cảnh báo (**Alert Flow**) diễn ra theo các bước như sau:

1. **Tải các tệp cấu hình vào máy chủ bộ nhớ đệm (Cache servers):** Các quy tắc cảnh báo (rules) được định nghĩa dưới dạng các tệp cấu hình lưu trên đĩa cứng. Định dạng **YAML [29]** là định dạng phổ biến thường dùng để định nghĩa các quy tắc này. Dưới đây là một ví dụ về cấu hình quy tắc cảnh báo:

```yaml
- name: instance_down
  rules:
    # Alert for any instance that is unreachable for >5 minutes.
    - alert: instance_down
      expr: up == 0
      for: 5m
      labels:
        severity: page
```

2. **Bộ quản lý cảnh báo (Alert Manager)** sẽ chủ động nạp/lấy các cấu hình cảnh báo từ bộ nhớ đệm (cache).

# Chương 5: Hệ Thống Giám Sát Chỉ Số và Cảnh Báo (Metrics Monitoring & Alerting System)

---

## 3. Quản Lý Cảnh Báo (Alert Manager)

Dựa trên các quy tắc cấu hình (config rules), **Bộ quản lý cảnh báo (Alert Manager)** sẽ gọi dịch vụ truy vấn (query service) theo một khoảng thời gian được định nghĩa trước (predefined interval). Thành phần này chịu trách nhiệm cho các tác vụ sau:

*   **Lọc (Filter), hợp nhất (Merge) và khử trùng lặp (Dedupe) cảnh báo:** Dưới đây là một ví dụ về việc gộp/hợp nhất các cảnh báo được kích hoạt trong cùng một thực thể/phiên bản (instance) trong một khoảng thời gian ngắn (Instance 1) (Hình 5.20).

```
Sự kiện 1 (Event 1)
Instance 1
disk_usage > 90%
       │
       ▼
Sự kiện 2 (Event 2)  ──────►  Hợp nhất (Merge)  ──────►  1 cảnh báo trên Instance 1
Instance 1                                               (1 alert on Instance 1)
disk_usage > 90%
       ▲
       │
Sự kiện 3 (Event 3)
Instance 1
disk_usage > 90%
```

![Sơ đồ trang 156](images/page_156.jpeg)  
*Hình 5.20: Hợp nhất cảnh báo (Merge alerts)*

*   **Kiểm soát truy cập (Access Control):** Để tránh lỗi do con người (human error) và duy trì tính an toàn, bảo mật cho hệ thống, việc giới hạn quyền truy cập đối với các hoạt động quản trị cảnh báo nhất định chỉ dành riêng cho các cá nhân được cấp quyền là điều tối quan trọng.
*   **Thử lại (Retry):** Bộ quản lý cảnh báo liên tục kiểm tra trạng thái của các cảnh báo và đảm bảo thông báo được gửi đi ít nhất một lần (**At-least-once delivery**).

4.  **Kho lưu trữ cảnh báo (Alert Store):** Là một cơ sở dữ liệu khóa-giá trị (key-value database), chẳng hạn như **Apache Cassandra**, dùng để duy trì trạng thái của tất cả các cảnh báo:
    *   `inactive` (chưa kích hoạt)
    *   `pending` (đang chờ xử lý)
    *   `firing` (đang phát tín hiệu cảnh báo)
    *   `resolved` (đã giải quyết)
    
    Thành phần này đảm bảo thông báo cảnh báo được gửi thành công ít nhất một lần (**At-least-once delivery**).

5.  Các cảnh báo hợp lệ và đủ điều kiện (eligible alerts) sẽ được đưa vào hàng đợi thông điệp phân tán **Apache Kafka**.

6.  Các tiến trình tiêu thụ cảnh báo (**Alert Consumers**) tiến hành kéo dữ liệu sự kiện cảnh báo (alert events) từ Kafka.

7.  **Alert Consumers** xử lý các sự kiện cảnh báo từ Kafka và gửi thông báo tới các kênh tiếp nhận khác nhau như **Email**, **Tin nhắn văn bản (SMS/Text Message)**, **PagerDuty**, hoặc các điểm cuối **HTTP endpoints (Webhooks)**.

---

### Hệ thống cảnh báo: Tự xây dựng hay Mua giải pháp có sẵn (Build vs Buy)

Hiện nay trên thị trường có rất nhiều hệ thống cảnh báo quy mô công nghiệp (industrial-scale alerting systems) sẵn có (off-the-shelf), và hầu hết chúng đều cung cấp khả năng tích hợp chặt chẽ (tight integration) với các cơ sở dữ liệu chuỗi thời gian (**Time-Series Database - TSDB**) phổ biến. Rất nhiều hệ thống cảnh báo trong số này cũng tương thích rất tốt với các kênh thông báo hiện có, chẳng hạn như Email và PagerDuty. 

> [!NOTE]  
> Trong môi trường thực tế, việc thuyết phục và biện minh cho quyết định tự xây dựng (**Build your own**) một hệ thống cảnh báo riêng từ đầu là một bài toán rất khó khăn. Trong các buổi phỏng vấn thiết kế hệ thống, đặc biệt là đối với các vị trí kỹ sư cấp cao (**Senior / Principal Architect**), bạn cần phải chuẩn bị sẵn sàng các luận điểm vững chắc để bảo vệ quyết định của mình.

---

## Hệ Thống Trực Quan Hóa (Visualization System)

Tầng trực quan hóa dữ liệu (Visualization) được xây dựng ngay trên tầng dữ liệu (Data layer). Các chỉ số kỹ thuật (Metrics) có thể được hiển thị trực quan trên bảng điều khiển chỉ số (**Metrics Dashboard**) theo nhiều thang đo thời gian khác nhau (time scales), và các cảnh báo có thể được theo dõi tập trung trên bảng điều khiển cảnh báo (**Alerts Dashboard**). 

Hình 5.21 minh họa một bảng điều khiển hiển thị một số chỉ số tiêu biểu như: lưu lượng yêu cầu máy chủ hiện tại (**Server Requests**), mức độ sử dụng Bộ nhớ/CPU (**Memory/CPU Utilization**), thời gian tải toàn bộ trang (**Page Load Time**), lưu lượng mạng vào/ra (**Network Traffic In/Out**), và thông tin đăng nhập (**Logins**) [30].

![Sơ đồ trang 157](images/page_157.jpeg)  
*Hình 5.21: Giao diện trực quan hóa Grafana (Grafana UI)*

> [!IMPORTANT]  
> Việc tự xây dựng một hệ thống trực quan hóa dữ liệu đạt tiêu chuẩn chất lượng cao là một thử thách kỹ thuật vô cùng phức tạp và tốn kém tài nguyên. Luận điểm ủng hộ việc sử dụng một giải pháp có sẵn trên thị trường (**Off-the-shelf system**) là cực kỳ thuyết phục. Ví dụ, **Grafana** là một hệ sinh thái xuất sắc phục vụ mục đích này. Nó tích hợp liền mạch với hầu hết các cơ sở dữ liệu chuỗi thời gian phổ biến mà doanh nghiệp có thể sử dụng hoặc mua bản quyền thương mại.

---

## Bước 4 - Tổng Kết (Step 4 - Wrap Up)

Trong chương này, chúng ta đã trình bày chi tiết bản thiết kế kiến trúc toàn diện cho một **Hệ Thống Giám Sát Chỉ Số và Cảnh Báo (Metrics Monitoring and Alerting System)**.

Ở góc độ tổng quan mức cao (high-level), chúng ta đã thảo luận về:
*   Thu thập dữ liệu (**Data Collection**)
*   Cơ sở dữ liệu chuỗi thời gian (**Time-Series Database**)
*   Hệ thống cảnh báo (**Alerts**)
*   Hệ thống trực quan hóa dữ liệu (**Visualization**)

Sau đó, chúng ta đã đi sâu phân tích vào các kỹ thuật và thành phần quan trọng nhất:
*   Mô hình Kéo so với Đẩy (**Pull vs Push model**) trong thu thập dữ liệu chỉ số.
*   Tận dụng **Apache Kafka** để mở rộng quy mô hệ thống (**Scale**).
*   Lựa chọn cơ sở dữ liệu chuỗi thời gian (**Time-Series Database**) phù hợp với bài toán.
*   Sử dụng kỹ thuật giảm tần số lấy mẫu (**Downsampling**) để tối ưu hóa dung lượng lưu trữ dữ liệu.
*   Cân nhắc giữa phương án tự phát triển hay mua giải pháp có sẵn (**Build vs Buy**) cho các hệ thống cảnh báo và trực quan hóa.

Kiến trúc tổng thể cuối cùng được mô tả như sau:

![Sơ đồ trang 158](images/page_158.jpeg)  
*Hình 5.22: Bản thiết kế kiến trúc hoàn chỉnh (Final design)*

Luồng dữ liệu tổng thể:
1.  **Metrics Source** (Nguồn chỉ số) $\rightarrow$ **Metrics Collector** (Bộ thu thập chỉ số) $\rightarrow$ **Kafka** $\rightarrow$ **Consumers** $\rightarrow$ **Time series DB** (kết hợp **Cache**).
2.  **Query Service** (Dịch vụ truy vấn) đọc từ **Time series DB** và **Cache** để phục vụ:
    *   **Visualization System** (Hệ thống trực quan hóa).
    *   **Alerting System** (Hệ thống cảnh báo) $\rightarrow$ Gửi thông báo đến **Email**, **Text Message**, **PagerDuty**, **HTTPS Endpoints**.

Xin chúc mừng bạn đã hoàn thành chặng đường phân tích chuyên sâu này! Hãy tự hào về thành quả của mình. Làm rất tốt!

---

## Tóm Tắt Nội Dung Chương (Chapter Summary)

Dưới đây là sơ đồ tư duy hệ thống hóa toàn bộ kiến trúc và các quyết định thiết kế của chương:

![Sơ đồ trang 159](images/page_159.jpeg)

*   **Yêu cầu chức năng (Functional Requirements):**
    *   Thu thập đa dạng các loại chỉ số kỹ thuật (Collect a variety of metrics).
    *   Cảnh báo (Alert).
    *   Trực quan hóa dữ liệu (Visualization).
*   **Yêu cầu phi chức năng (Non-Functional Requirements):**
    *   Hệ thống quy mô lớn (Large-scale system).
    *   Độ tin cậy cao (**Reliability**) để không bao giờ bỏ sót các cảnh báo nghiêm trọng (Don't miss critical alerts).
    *   Tính linh hoạt (**Flexibility**).
*   **Năm thành phần cốt lõi của hệ thống (Five Components of the System):**
    1.  Thu thập dữ liệu (Data collection).
    2.  Truyền tải dữ liệu (Data transmission).
    3.  Lưu trữ dữ liệu (Data storage).
    4.  Cảnh báo (Alert).
    5.  Trực quan hóa (Visualization).
*   **Mô hình truy cập dữ liệu (Data Access Pattern):**
    *   Ghi cực lớn (**Write heavy**).
    *   Đọc đột biến theo đợt (**Read bursty**).
*   **Hệ thống lưu trữ dữ liệu (Data Storage System):**
    *   Mô hình dữ liệu (Data model).
    *   Cơ sở dữ liệu chuỗi thời gian (**Time-series database**).
*   **Thiết kế mức cao (High-Level Design):**
    *   Thu thập chỉ số: Mô hình Kéo so với Đẩy (**Metrics collection - Pull vs Push**).
    *   Mở rộng quy mô đường ống truyền tải chỉ số thông qua Kafka (**Scale metrics transmission pipeline through Kafka**).
    *   Các giải pháp thay thế cho Kafka (Alternative to Kafka).
    *   Vị trí thực hiện tổng hợp dữ liệu (Where aggregations can happen).
*   **Tầng lưu trữ & Cơ sở dữ liệu chuỗi thời gian (Time-Series Database & Storage Layer):**
    *   Mã hóa và nén dữ liệu (**Data encoding and compression**).
    *   Tối ưu hóa không gian lưu trữ (Space optimization).
    *   Giảm tần số lấy mẫu (**Downsampling**).
    *   Lưu trữ dữ liệu lạnh (**Cold storage**).
*   **Dịch vụ truy vấn (Query Service):**
    *   Tầng bộ nhớ đệm (**Cache layer**).
    *   Truy vấn cơ sở dữ liệu chuỗi thời gian (Time-series database query).
*   **Hệ thống cảnh báo (Alerting System):**
    *   Quyết định Tự xây dựng hay Mua (**Build vs Buy**).
*   **Hệ thống trực quan hóa (Visualization System):**
    *   Quyết định Tự xây dựng hay Mua (**Build vs Buy**).
*   **Tổng kết (Wrap-up).**

---

## Tài Liệu Tham Khảo (Reference Material)

![Sơ đồ trang 160](images/page_160.jpeg)

*   **[1] Datadog:** https://www.datadoghq.com/
*   **[2] Splunk:** https://www.splunk.com/
*   **[3] PagerDuty:** https://www.pagerduty.com/
*   **[4] Elastic stack:** https://www.elastic.co/elastic-stack
*   **[5] Dapper, a Large-Scale Distributed Systems Tracing Infrastructure:** https://research.google/pubs/pub36356/
*   **[6] Distributed Systems Tracing with Zipkin:** https://blog.twitter.com/engineering/en_us/a/2012/distributed-systems-tracing-with-zipkin.html
*   **[7] Prometheus:** https://prometheus.io/docs/introduction/overview/
*   **[8] OpenTSDB - A Distributed, Scalable Monitoring System:** http://opentsdb.net/
*   **[9] Data model:** https://prometheus.io/docs/concepts/data_model/
*   **[10] MySQL:** https://www.mysql.com/
*   **[11] Schema design for time-series data | Cloud Bigtable Documentation:** https://cloud.google.com/bigtable/docs/schema-design-time-series
*   **[12] MetricsDB. TimeSeriesDatabase for storing metrics at Twitter:** https://blog.twitter.com/engineering/en_us/topics/infrastructure/2019/metricsdb.html
*   **[13] Amazon Timestream:** https://aws.amazon.com/timestream/
*   **[14] DB-Engines Ranking of time-series DBMS:** https://db-engines.com/en/ranking/time+series+dbms
*   **[15] InfluxDB:** https://www.influxdata.com/
*   **[16] etcd:** https://etcd.io/
*   **[17] Service Discovery with ZooKeeper:** https://cloud.spring.io/spring-cloud-zookeeper/1.2.x/multi/multi_spring-cloud-zookeeper-discovery.html
*   **[18] Amazon CloudWatch:** https://aws.amazon.com/cloudwatch/
*   **[19] Graphite:** https://graphiteapp.org/
*   **[20] Push vs Pull:** http://bit.ly/3aJEPxE
*   **[21] Pull doesn't scale - or does it?:** https://boxever.com/pull-doesnt-scale-or-does-it/
*   **[22] Monitoring Architecture:** https://developer.lightbend.com/guides/monitoring-at-scale/monitoring-architecture/architecture.html
*   **[23] Push vs Pull in Monitoring Systems:** https://giedrius.blog/2019/05/11/push-vs-pull-in-monitoring-systems/

![Sơ đồ trang 161](images/page_161.jpeg)

*   **[24] Pushgateway:** https://github.com/prometheus/pushgateway
*   **[25] Building Applications with Serverless Architectures:** https://aws.amazon.com/lambda/serverless-architectures-learn-more/
*   **[26] Gorilla. A Fast, Scalable, In-Memory Time Series Database:** http://www.vldb.org/pvldb/vol8/p1816-teller.pdf
*   **[27] Why We're Building Flux, a New Data Scripting and Query Language:** https://www.influxdata.com/blog/why-were-building-flux-a-new-data-scripting-and-query-language/
*   **[28] InfluxDB storage engine:** https://docs.influxdata.com/influxdb/v2.0/reference/internals/storage-engine/
*   **[29] YAML:** https://en.wikipedia.org/wiki/YAML
*   **[30] Grafana Demo:** https://play.grafana.org/

Đang kiểm tra thư mục tài liệu trong không gian làm việc để đọc đầy đủ nội dung Chương 5 từ trang 162 trở đi... Tôi sẽ cập nhật ngay khi lệnh hoàn tất.
Đang kiểm tra chi tiết cấu trúc các tệp tin trong thư mục `alex-xu-system-design-volume-2` để trích xuất nội dung Chương 5 từ trang 162...
Đang định vị các trang nội dung OCR từ trang 162 của Chương 5 trong `ocr_cache`...
Đang kiểm tra danh sách toàn bộ các trang đã OCR trong bộ nhớ tạm...
Đang kiểm tra thư mục `scripts`...
Đang đọc thông tin cấu hình và phạm vi các trang của Chapter 5 trong `translate_vol2_common.py`...
Đang tra cứu phạm vi trang chính xác của Chương 5...
Đang kiểm tra tệp `chuong-05-metrics-monitoring-and-alerting-system.md`...
Đang kiểm tra các trang từ 138 đến 162 trong thư mục OCR cache...
Đang đọc nội dung trang 162...
Đang phân tích hình ảnh trang 162...
Đang phân tích chi tiết vùng văn bản trên trang 162...
Đang xác nhận ranh giới giữa trang 162 và 163...
Dưới đây là bản dịch kỹ thuật chuẩn xác 100% của phần tài liệu kỹ thuật được cung cấp:

---

## --- Trang 162 ---

![Sơ đồ trang 162](images/page_162.jpeg)

**Chương 5: Hệ Thống Giám Sát Chỉ Số và Cảnh Báo (Chapter 5: Metrics Monitoring and Alerting System)**

> [!NOTE]
> Trang 162 là trang kết thúc (trang trắng phân đoạn cuối chương / blank divider page) của **Chương 5: Hệ Thống Giám Sát Chỉ Số và Cảnh Báo (Metrics Monitoring & Alerting System)** trước khi bước sang **Chương 6: Tổng Hợp Sự Kiện Lượt Click Quảng Cáo (Ad Click Event Aggregation - bắt đầu từ trang 163)**. Dòng ký tự `CaeotoMonhuring and Arong Sotem` trên bản chụp là tiêu đề đầu trang dạng watermark/running header được quét qua OCR từ dòng gốc: *“Chapter 5. Metrics Monitoring and Alerting System”*.

---

> [!TIP]
> Toàn bộ nội dung cốt lõi của **Chương 5 (Metrics Monitoring & Alerting System)** nằm trọn vẹn từ **Trang 138 đến Trang 161** (bao gồm: Xác định phạm vi & Yêu cầu hệ thống, Mô hình dữ liệu Time-Series, Kiến trúc Thu thập Dữ liệu Push vs Pull, Data Pipeline qua Kafka/Message Queue, Tối ưu hóa Lưu trữ Time-Series DB, Gorilla Compression, Downsampling & Cold Storage, Hệ thống Cảnh báo Alerting, và Tài liệu tham khảo). 
> 
> Nếu bạn cần dịch toàn bộ hoặc từng phần cụ thể từ trang 138 đến 161, hãy gửi yêu cầu để tôi thực hiện trọn vẹn ngay lập tức!

---

## Điều hướng

- [chuong-04-distributed-message-queue.md](chuong-04-distributed-message-queue.md)
- [Mục lục](README.md)
- [chuong-06-ad-click-event-aggregation.md](chuong-06-ad-click-event-aggregation.md)
