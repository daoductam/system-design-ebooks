# 009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)

[← Bài trước](008-can-bang-tai-load-balancers.md) | [Mục lục](README.md) | [Bài tiếp theo →](010-luu-tru-key-value-store.md)

---


# Giới thiệu về Cơ sở dữ liệu (Introduction to Databases)

Hiểu rõ cơ sở dữ liệu là gì và các ca sử dụng (use cases) của nó trong thiết kế hệ thống (system design).

---

### Nội dung bao gồm:
- **Đặt vấn đề (Problem statement)**
- **Các hạn chế của lưu trữ bằng tệp tin (Limitations of file storage)**
- **Giải pháp (Solution)**
- **Ưu điểm (Advantages)**
- **Chúng ta sẽ tìm hiểu về cơ sở dữ liệu như thế nào? (How will we explain databases?)**

---

## Đặt vấn đề (Problem statement)

Hãy bắt đầu với một câu hỏi đơn giản: **Liệu chúng ta có thể xây dựng một ứng dụng phần mềm mà không cần sử dụng cơ sở dữ liệu (database) hay không?** 

Giả sử chúng ta có một ứng dụng tương tự như WhatsApp. Mọi người sử dụng ứng dụng của chúng ta để giao tiếp với bạn bè của họ. Giờ đây, chúng ta có thể lưu trữ thông tin (danh sách tên người dùng và các tin nhắn tương ứng của họ) vĩnh viễn ở đâu, bằng cách nào và truy xuất lại dữ liệu đó ra sao?

Chúng ta có thể sử dụng một tệp tin (file) đơn giản để lưu trữ tất cả các bản ghi (records) trên từng dòng riêng biệt và truy xuất chúng từ chính tệp tin đó. Tuy nhiên, việc sử dụng tệp tin để lưu trữ gặp phải một số hạn chế nhất định.

---

## Các hạn chế của lưu trữ bằng tệp tin (Limitations of file storage)

- Chúng ta không thể cung cấp khả năng quản lý đồng thời (**concurrent management**) cho các người dùng riêng biệt đang truy cập vào các tệp lưu trữ từ các vị trí địa lý khác nhau.
- Chúng ta không thể cấp các quyền truy cập khác nhau (**different access rights**) cho các người dùng khác nhau.
- Hệ thống sẽ mở rộng quy mô (**scale**) và đảm bảo tính sẵn sàng (**availability**) như thế nào khi thêm vào hàng nghìn mục dữ liệu mới?
- Làm thế nào để chúng ta tìm kiếm nội dung cho các người dùng khác nhau trong một khoảng thời gian ngắn?

---

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p002_00.png)

### Các hạn chế cốt lõi của lưu trữ tệp tin:
- Truy cập đồng thời vào dữ liệu bởi nhiều người dùng (**Concurrent access to data by multiple users**)
- Các quyền truy cập khác nhau cho các người dùng khác nhau (**Different access rights to different users**)
- Tốc độ bị ảnh hưởng bởi hàng triệu người dùng (**Speed affected by millions of users**)

---

## Giải pháp (Solution)

Các hạn chế nêu trên có thể được giải quyết bằng cách sử dụng **cơ sở dữ liệu (databases)**.

> **Cơ sở dữ liệu (database)** là một tập hợp dữ liệu có tổ chức, có thể được quản lý và truy cập một cách dễ dàng. Cơ sở dữ liệu được tạo ra nhằm giúp việc lưu trữ (**store**), truy xuất (**retrieve**), sửa đổi (**modify**) và xóa bỏ (**delete**) dữ liệu trở nên dễ dàng hơn trong mối liên kết với các quy trình xử lý dữ liệu khác nhau.

Một số ứng dụng thực tế sử dụng hệ thống quản trị cơ sở dữ liệu bao gồm hệ thống ngân hàng (**banking systems**), cửa hàng mua sắm trực tuyến (**online shopping stores**), v.v. Các tổ chức khác nhau sở hữu quy mô cơ sở dữ liệu khác nhau tùy theo nhu cầu của họ.

> [!NOTE]
> Theo một nguồn tài liệu, **World Data Center for Climate (WDCC)** là cơ sở dữ liệu lớn nhất thế giới. Nó chứa khoảng 220 terabytes dữ liệu web và 6 petabytes dữ liệu bổ sung.

Có hai loại cơ sở dữ liệu cơ bản:
1. **SQL** (cơ sở dữ liệu quan hệ - relational databases)
2. **NoSQL** (cơ sở dữ liệu phi quan hệ - non-relational databases)

Chúng khác nhau về trường hợp sử dụng mục tiêu (**intended use case**), loại thông tin mà chúng lưu trữ và phương pháp lưu trữ (**storage method**) mà chúng áp dụng.

---

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p002_01.png)

*Cơ sở dữ liệu quan hệ có cấu trúc được định nghĩa chặt chẽ như các thuộc tính (các cột của bảng). Các cơ sở dữ liệu NoSQL như cơ sở dữ liệu dạng tài liệu (document databases) thường có cấu trúc dữ liệu do tầng ứng dụng tự định nghĩa (application-defined structure of data).*

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p002_02.png)
*Ví dụ về cơ sở dữ liệu SQL (Users table)*

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p002_03.png)
*Ví dụ về cơ sở dữ liệu NoSQL (Product Document)*

Cơ sở dữ liệu quan hệ (**relational databases**), tương tự như danh bạ điện thoại ghi lại số liên lạc và địa chỉ, được tổ chức ngăn nắp và có lược đồ định sẵn (**predetermined schemas**). Cơ sở dữ liệu phi quan hệ (**non-relational databases**), tương tự như thư mục tệp tin lưu trữ mọi thứ từ thông tin cố định của một người cho đến sở thích mua sắm của họ, thì phi cấu trúc (**unstructured**), phân tán và mang đặc trưng lược đồ động (**dynamic schema**). Chúng ta sẽ thảo luận chi tiết về sự khác biệt cũng như các phân loại của chúng trong bài học tiếp theo.

---

## Ưu điểm (Advantages)

Một cơ sở dữ liệu đạt chuẩn là thành phần thiết yếu cho mọi doanh nghiệp hoặc tổ chức. Điều này là do cơ sở dữ liệu lưu trữ toàn bộ thông tin quan trọng về tổ chức, chẳng hạn như hồ sơ nhân sự, các giao dịch (**transactions**), thông tin tiền lương, v.v. Dưới đây là một số lý do tại sao cơ sở dữ liệu lại đóng vai trò quan trọng:

- **Quản lý lượng dữ liệu lớn (Managing large data):** Một khối lượng dữ liệu khổng lồ có thể được xử lý dễ dàng bằng cơ sở dữ liệu, điều mà các công cụ khác không thể thực hiện được.
- **Truy xuất dữ liệu chính xác / Tính nhất quán của dữ liệu (Retrieving accurate data / data consistency):** Nhờ vào các ràng buộc (**constraints**) khác nhau trong cơ sở dữ liệu, chúng ta có thể truy xuất dữ liệu chính xác bất cứ khi nào mong muốn.
- **Dễ dàng cập nhật (Easy updation):** Việc cập nhật dữ liệu trong cơ sở dữ liệu là khá dễ dàng thông qua ngôn ngữ thao tác dữ liệu (**Data Manipulation Language - DML**).
- **Bảo mật (Security):** Cơ sở dữ liệu đảm bảo tính an toàn của dữ liệu. Cơ sở dữ liệu chỉ cho phép những người dùng được ủy quyền (**authorized users**) truy cập vào dữ liệu.
- **Tính toàn vẹn dữ liệu (Data integrity):** Cơ sở dữ liệu đảm bảo tính toàn vẹn dữ liệu bằng cách áp dụng các ràng buộc khác nhau đối với dữ liệu.
- **Tính sẵn sàng (Availability):** Cơ sở dữ liệu có thể được sao chép (thông qua kỹ thuật sao chép dữ liệu - **data replication**) trên các máy chủ khác nhau, và các bản sao này có thể được cập nhật đồng thời. Các bản sao này (**replicas**) đảm bảo tính sẵn sàng (**availability**).
- **Khả năng mở rộng (Scalability):** Cơ sở dữ liệu được phân chia (thông qua kỹ thuật phân vùng dữ liệu - **data partitioning**) nhằm quản lý tải trên một nút đơn lẻ (**single node**). Kỹ thuật này giúp gia tăng khả năng mở rộng (**scalability**).

---

## Chúng ta sẽ tìm hiểu về cơ sở dữ liệu như thế nào? (How will we explain databases?)

Chúng tôi chia chương về cơ sở dữ liệu thành bốn bài học:
1. **Các loại cơ sở dữ liệu (Types of Databases):** Chúng ta sẽ thảo luận về các loại cơ sở dữ liệu khác nhau, cùng với ưu và nhược điểm của chúng.
2. **Sao chép dữ liệu (Data Replication):** Chúng ta sẽ thảo luận sao chép dữ liệu là gì và các mô hình sao chép khác nhau cùng với ưu và nhược điểm của chúng.
3. **Phân vùng dữ liệu (Data Partitioning):** Chúng ta sẽ thảo luận phân vùng dữ liệu là gì và các mô hình phân vùng khác nhau cùng với ưu và nhược điểm của chúng.
4. **Phân tích chi phí - lợi ích (Cost-benefit analysis):** Chúng ta sẽ thảo luận về phương pháp phân mảnh cơ sở dữ liệu (**database sharding**) nào là tối ưu nhất cho từng loại cơ sở dữ liệu khác nhau.

Hãy bắt đầu bằng việc tìm hiểu các loại cơ sở dữ liệu khác nhau và các trường hợp sử dụng ưu tiên (**preferred use cases**) của chúng.

---

# Các loại Cơ sở dữ liệu (Types of Databases)

Hiểu rõ các loại cơ sở dữ liệu khác nhau và các ca sử dụng (use cases) của chúng trong thiết kế hệ thống.

---

### Nội dung bao gồm:
- **Cơ sở dữ liệu quan hệ (Relational databases)**
- **Tại sao lại dùng cơ sở dữ liệu quan hệ? (Why relational databases?)**
  - Tính linh hoạt (Flexibility)
  - Giảm thiểu dư thừa (Reduced redundancy)
  - Xử lý đồng thời (Concurrency)
  - Khả năng tích hợp (Integration)
  - Sao lưu và phục hồi sau thảm họa (Backup and disaster recovery)
- **Nhược điểm (Drawback)**
  - Sự bất tương thích về trở kháng (Impedance mismatch)
- **Tại sao lại dùng cơ sở dữ liệu phi quan hệ (NoSQL)? (Why non-relational (NoSQL) databases?)**
- **Các loại cơ sở dữ liệu NoSQL (Types of NoSQL databases)**
  - Cơ sở dữ liệu khóa - giá trị (Key-value database)
  - Cơ sở dữ liệu dạng tài liệu (Document database)
  - Cơ sở dữ liệu đồ thị (Graph database)
  - Cơ sở dữ liệu dạng cột (Columnar database)
- **Nhược điểm của cơ sở dữ liệu NoSQL (Drawbacks of NoSQL databases)**
  - Thiếu chuẩn hóa (Lack of standardization)
  - Tính nhất quán (Consistency)
- **Lựa chọn cơ sở dữ liệu phù hợp (Choose the right database)**
- **Câu hỏi kiểm tra nhanh (Quiz)**

Như chúng ta đã thảo luận trước đó, cơ sở dữ liệu được chia làm hai loại: **quan hệ (relational)** và **phi quan hệ (non-relational)**. Hãy cùng phân tích chi tiết các loại này.

---

## Cơ sở dữ liệu quan hệ (Relational databases)

Cơ sở dữ liệu quan hệ tuân thủ các lược đồ (**schemas**) cụ thể trước khi thực hiện lưu trữ dữ liệu. Dữ liệu được lưu trữ trong cơ sở dữ liệu quan hệ đã có cấu trúc định sẵn từ trước. Nhìn chung, mô hình này tổ chức dữ liệu thành một hoặc nhiều quan hệ (còn được gọi là bảng - **tables**), với một khóa định danh duy nhất (**unique key**) cho mỗi bộ dữ liệu (bộ - **tuple** / thực thể bản ghi - **instance**). Mỗi thực thể dữ liệu (**entity**) bao gồm các phiên bản (**instances**) và các thuộc tính (**attributes**), trong đó các thực thể bản ghi được lưu trữ dưới dạng các hàng (**rows**), còn các thuộc tính của mỗi bản ghi được lưu trữ dưới dạng các cột (**columns**). Vì mỗi bộ dữ liệu có một khóa duy nhất, một bộ dữ liệu trong bảng này có thể liên kết với một bộ dữ liệu trong các bảng khác bằng cách lưu trữ các khóa chính (**primary keys**) sang các bảng khác, thường được gọi là khóa ngoại (**foreign keys**).

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p002_04.png)

Ngôn ngữ truy vấn có cấu trúc (**Structured Query Language - SQL**) được sử dụng để thao tác với cơ sở dữ liệu. Điều này bao gồm việc chèn (**insertion**), xóa (**deletion**) và truy xuất (**retrieval**) dữ liệu.

Có nhiều lý do dẫn đến sự phổ biến và vị thế thống trị của cơ sở dữ liệu quan hệ, bao gồm: tính đơn giản, độ mạnh mẽ vững chắc (**robustness**), tính linh hoạt, hiệu năng, khả năng mở rộng (**scalability**) và khả năng tương thích cao trong việc quản lý dữ liệu thông thường chung.

---

### Các thuộc tính ACID (ACID Properties)

Cơ sở dữ liệu quan hệ cung cấp các thuộc tính: **Nguyên tử (Atomicity)**, **Nhất quán (Consistency)**, **Cô lập (Isolation)** và **Bền vững (Durability)** — gọi tắt là **ACID** — nhằm duy trì tính toàn vẹn của cơ sở dữ liệu.

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p002_05.png)

ACID là một tầng trừu tượng (**abstraction**) mạnh mẽ giúp đơn giản hóa các tương tác phức tạp với dữ liệu và che giấu đi rất nhiều hiện tượng bất thường (**anomalies**) như:
- Đọc dữ liệu rác / bẩn (**dirty reads**)
- Ghi dữ liệu rác / bẩn (**dirty writes**)
- Sai lệch đọc (**read skew**)
- Mất cập nhật (**lost updates**)
- Sai lệch ghi (**write skew**)
- Đọc bóng ma (**phantom reads**)

Tất cả được gói gọn phía sau một thao tác hủy giao dịch đơn giản (**transaction abort**).

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p002_06.png)

> [!NOTE]
> Tuy nhiên, theo thiết kế, ACID giống như một "chiếc búa tạ" đủ đa năng cho mọi vấn đề. Nếu một ứng dụng cụ thể nào đó chỉ cần xử lý một vài hiện tượng bất thường nhất định, sẽ có cơ hội để sử dụng một giải pháp tùy biến (**custom solution**) nhằm đạt được hiệu năng cao hơn, mặc dù việc này sẽ làm tăng thêm độ phức tạp.

---

### Phân tích chi tiết về ACID:

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p002_07.png)

- **Tính nguyên tử (Atomicity):** Một giao dịch (**transaction**) được coi là một đơn vị nguyên tử duy nhất. Do đó, hoặc là toàn bộ các câu lệnh bên trong giao dịch sẽ được thực thi thành công, hoặc là không có câu lệnh nào được thực thi cả. Nếu một câu lệnh bị lỗi trong quá trình thực hiện giao dịch, toàn bộ giao dịch đó phải bị hủy bỏ (**aborted**) và khôi phục trạng thái cũ (**rolled back**).
- **Tính nhất quán (Consistency):** Tại bất kỳ thời điểm nào, cơ sở dữ liệu phải luôn ở trạng thái nhất quán, và nó phải duy trì ở trạng thái nhất quán sau mỗi giao dịch. Ví dụ: nếu nhiều người dùng muốn xem cùng một bản ghi từ cơ sở dữ liệu, hệ thống phải trả về kết quả tương tự nhau trong mỗi lần truy vấn.

---

### --- Trang 7 ---

* **Isolation (Tính cô lập):** Trong trường hợp có nhiều giao dịch (**concurrent transactions**) thực thi đồng thời, chúng không được phép gây ảnh hưởng lẫn nhau. Trạng thái cuối cùng của cơ sở dữ liệu phải tương đương như khi các giao dịch được thực thi một cách tuần tự (**sequentially**).
* **Durability (Tính bền vững):** Hệ thống phải đảm bảo rằng các giao dịch đã hoàn tất thành công sẽ tồn tại vĩnh viễn trong cơ sở dữ liệu, ngay cả khi xảy ra sự cố sập hệ thống (**system failure events**).

Nhiều hệ quản trị cơ sở dữ liệu (**DBMS - Database Management Systems**) khác nhau được sử dụng để định nghĩa lược đồ cơ sở dữ liệu quan hệ (**relational database schema**) cùng với các thao tác khác, chẳng hạn như lưu trữ, truy xuất và thực thi các câu truy vấn **SQL** trên dữ liệu. Một số hệ quản trị cơ sở dữ liệu (**DBMS**) phổ biến bao gồm:
* **MySQL**
* **Oracle Database**
* **Microsoft SQL Server**
* **IBM DB2**
* **PostgreSQL**
* **SQLite**

#### Tại sao nên dùng cơ sở dữ liệu quan hệ (Why relational databases)?

Cơ sở dữ liệu quan hệ là lựa chọn mặc định của các chuyên gia phần mềm đối với việc lưu trữ dữ liệu có cấu trúc (**structured data storage**). Loại cơ sở dữ liệu này sở hữu rất nhiều ưu điểm vượt trội. Một trong những sức mạnh lớn nhất của cơ sở dữ liệu quan hệ là tính trừu tượng hóa của các giao dịch **ACID** (**ACID transactions**) và các ngữ nghĩa lập trình liên quan. Điều này mang lại sự thuận tiện rất lớn cho lập trình viên ứng dụng cuối khi sử dụng cơ sở dữ liệu quan hệ. Hãy cùng điểm lại một số tính năng quan trọng của cơ sở dữ liệu quan hệ:

##### Tính linh hoạt (Flexibility)
Trong ngữ cảnh của **SQL**, ngôn ngữ định nghĩa dữ liệu (**DDL - Data Definition Language**) mang lại cho chúng ta sự linh hoạt để chỉnh sửa cơ sở dữ liệu, bao gồm các bảng (**tables**), các cột (**columns**), đổi tên bảng và các thay đổi khác. **DDL** thậm chí còn cho phép chúng ta thay đổi lược đồ (**modify schema**) ngay trong khi các truy vấn khác đang diễn ra và máy chủ cơ sở dữ liệu vẫn đang hoạt động liên tục.

##### Giảm thiểu sự dư thừa (Reduced redundancy)
Một trong những ưu điểm lớn nhất của cơ sở dữ liệu quan hệ là loại bỏ sự dư thừa dữ liệu (**data redundancy**). Thông tin liên quan đến một thực thể (**entity**) cụ thể sẽ xuất hiện trong một bảng, trong khi dữ liệu liên quan đến thực thể cụ thể đó lại xuất hiện ở các bảng khác được liên kết 

---

### --- Trang 8 ---

thông qua các khóa ngoại (**foreign keys**). Quy trình này được gọi là chuẩn hóa (**normalization**) và có thêm lợi ích bổ sung là loại bỏ các phụ thuộc không nhất quán (**inconsistent dependency**).

##### Tính đồng thời (Concurrency)
Tính đồng thời (**Concurrency**) là một yếu tố quan trọng khi thiết kế cơ sở dữ liệu cấp doanh nghiệp (**enterprise database**). Trong trường hợp như vậy, dữ liệu được đọc và ghi bởi rất nhiều người dùng cùng một lúc. Chúng ta cần phải điều phối các tương tác này để tránh sự không nhất quán trong dữ liệu — ví dụ, tình trạng đặt phòng khách sạn bị trùng lặp (**double booking**). Tính đồng thời trong cơ sở dữ liệu quan hệ được xử lý thông qua cơ chế truy cập dữ liệu theo giao dịch (**transactional access**). Như đã giải thích trước đó, một giao dịch được coi là một thao tác nguyên tử (**atomic operation**), do đó nó cũng đóng vai trò trong việc xử lý lỗi nhằm hoàn tác (**rollback**) hoặc xác nhận ghi nhận (**commit**) giao dịch khi thực thi thành công.

##### Tích hợp (Integration)
Quá trình tổng hợp dữ liệu từ nhiều nguồn khác nhau là một nghiệp vụ phổ biến trong các ứng dụng doanh nghiệp. Một cách thông dụng để thực hiện việc tổng hợp này là tích hợp một cơ sở dữ liệu dùng chung (**shared database**), nơi nhiều ứng dụng cùng lưu trữ dữ liệu của chúng. Bằng cách này, tất cả các ứng dụng có thể dễ dàng truy cập dữ liệu của nhau, trong khi các biện pháp kiểm soát tương tranh (**concurrency control measures**) sẽ đảm trách việc điều phối quyền truy cập của nhiều ứng dụng.

##### Sao lưu và khắc phục thảm họa (Backup and disaster recovery)
Cơ sở dữ liệu quan hệ đảm bảo trạng thái của dữ liệu luôn nhất quán (**consistent**) tại bất kỳ thời điểm nào. Các thao tác xuất (**export**) và nhập (**import**) giúp việc sao lưu (**backup**) và khôi phục (**restoration**) trở nên dễ dàng hơn. Hầu hết các cơ sở dữ liệu quan hệ dựa trên nền tảng đám mây (**cloud-based relational databases**) đều thực hiện việc nhân bản phản chiếu liên tục (**continuous mirroring**) để tránh mất mát dữ liệu và giúp quá trình phục hồi diễn ra nhanh chóng, thuận tiện hơn.

#### Nhược điểm (Drawback)

##### Sự bất đối xứng trở kháng (Impedance mismatch)
Bất đối xứng trở kháng (**Impedance mismatch**) là sự khác biệt giữa mô hình quan hệ (**relational model**) và các cấu trúc dữ liệu trên bộ nhớ trong (**in-memory data structures**). Mô hình quan hệ tổ chức dữ liệu thành một cấu trúc dạng bảng với các quan hệ (**relations**) và các bộ giá trị/bản ghi (**tuples**). Thao tác **SQL** trên dữ liệu có cấu trúc này tạo ra các quan hệ tương thích với đại số quan hệ (**relational algebra**). Tuy nhiên, nó tồn tại một số hạn chế. Cụ thể, các giá trị trong một bảng chỉ nhận các giá trị vô hướng đơn giản (**scalar values**) chứ không thể là một cấu trúc phức tạp (**structure**) hay một danh sách (**list**). Trường hợp này hoàn toàn khác biệt so với khi xử lý trong bộ nhớ (**in-memory**), nơi mà một cấu trúc dữ liệu phức tạp hoàn toàn có thể được

---

### --- Trang 9 ---

lưu trữ. Để làm cho các cấu trúc phức tạp tương thích được với các quan hệ, chúng ta sẽ cần một phép chuyển đổi dữ liệu dưới góc độ của đại số quan hệ. Do đó, sự bất đối xứng trở kháng đòi hỏi phải có sự biên dịch/chuyển đổi qua lại giữa hai cách biểu diễn, như được minh họa trong hình bên dưới:

> [!NOTE]
> **Một giá trị tổng hợp đơn lẻ trong tầng hiển thị (View) được cấu thành từ nhiều hàng và bảng trong cơ sở dữ liệu quan hệ:**
>
> * **Các bảng trong CSDL quan hệ:**
>   * **Orders (Đơn hàng):** ID: 501
>   * **Customers (Khách hàng):** John
>   * **Order lines (Các dòng đơn hàng):**
>     * Mã 0321293555 | Số lượng: 2 | Đơn giá: $52 | Tổng: $74
>     * Mã 0451601912 | Số lượng: 1 | Đơn giá: $40 | Tổng: $40
>     * Mã 0451495032 | Số lượng: 1 | Đơn giá: $67 | Tổng: $67
>   * **Credit cards (Thẻ tín dụng):**
>     * Thẻ: Amex | Số thẻ (CC Number): 22255 | Ngày hết hạn (expiry): 04/2027
>
> * **Cấu trúc In-Memory tương ứng (View biểu diễn đối tượng):**
>   * `Customer: John`
>   * `line items:` (Danh sách các mục hàng)
>   * `payment details:`
>     * `Card: Amex`
>     * `CC Number: 22255`
>     * `expiry: 04/2027`

#### Tại sao nên dùng cơ sở dữ liệu phi quan hệ - NoSQL (Why non-relational (NoSQL) databases)?

Một cơ sở dữ liệu **NoSQL** được thiết kế nhằm hỗ trợ đa dạng các mô hình dữ liệu (**data models**) khác nhau để truy cập và quản lý dữ liệu. Có nhiều loại cơ sở dữ liệu **NoSQL** khác nhau mà chúng ta sẽ giải thích chi tiết trong phần tiếp theo. Các cơ sở dữ liệu này được sử dụng trong những ứng dụng đòi hỏi khối lượng lớn dữ liệu bán cấu trúc (**semi-structured**) và phi cấu trúc (**unstructured**), độ trễ thấp (**low latency**), cùng các mô hình dữ liệu linh hoạt. Điều này có thể đạt được bằng cách nới lỏng một số ràng buộc khắt khe về tính nhất quán dữ liệu (**data consistency**) vốn có của các cơ sở dữ liệu khác. Dưới đây là một số đặc tính nổi bật của cơ sở dữ liệu **NoSQL**:

* **Thiết kế đơn giản (Simple design):** Không giống như cơ sở dữ liệu quan hệ, **NoSQL** không đòi hỏi phải giải quyết bài toán bất đối xứng trở kháng (**impedance mismatch**) — ví dụ, lưu trữ toàn bộ dữ liệu của nhân viên trong một tài liệu (**document**) duy nhất thay vì phải chia ra nhiều bảng đòi hỏi các phép nối

---

### --- Trang 10 ---

  giao (**JOIN operations**). Chiến lược này giúp việc lập trình trở nên đơn giản và dễ dàng hơn, viết ít mã nguồn hơn, gỡ lỗi (**debug**) và bảo trì thuận tiện hơn.
* **Mở rộng theo chiều ngang (Horizontal scaling):** Về căn bản, **NoSQL** được ưu tiên lựa chọn nhờ khả năng vận hành cơ sở dữ liệu trên một cụm máy chủ lớn (**large cluster**). Điều này giải quyết triệt để bài toán khi số lượng người dùng đồng thời (**concurrent users**) tăng đột biến. **NoSQL** giúp việc mở rộng quy mô theo chiều ngang (**scale out**) trở nên dễ dàng hơn, bởi vì dữ liệu liên quan đến một nhân viên cụ thể được lưu trữ tập trung trong một tài liệu thay vì phân mảnh trên nhiều bảng nằm rải rác giữa các nút (**nodes**). Cơ sở dữ liệu **NoSQL** thường phân tán dữ liệu trên nhiều nút và tự động cân bằng dữ liệu cũng như các truy vấn giữa các nút. Trong trường hợp xảy ra lỗi nút (**node failure**), nút đó có thể được thay thế một cách trong suốt (**transparently replaced**) mà không gây gián đoạn ứng dụng.
* **Tính sẵn sàng cao (Availability):** Để nâng cao tính sẵn sàng của dữ liệu, việc thay thế nút có thể được thực hiện mà không cần thời gian ngừng hoạt động của ứng dụng (**zero downtime**). Hầu hết các biến thể của cơ sở dữ liệu phi quan hệ đều hỗ trợ nhân bản dữ liệu (**data replication**) để đảm bảo tính sẵn sàng cao (**High Availability**) và khả năng khắc phục thảm họa (**Disaster Recovery**).
* **Hỗ trợ dữ liệu phi cấu trúc và bán cấu trúc (Support for unstructured and semi-structured data):** Nhiều cơ sở dữ liệu **NoSQL** có khả năng làm việc với dữ liệu không có lược đồ cố định (**schemaless**) tại thời điểm cấu hình cơ sở dữ liệu hoặc ghi dữ liệu. Ví dụ, cơ sở dữ liệu tài liệu (**document databases**) là phi cấu trúc; chúng cho phép các tài liệu (**JSON, XML, BSON**, v.v.) có các trường dữ liệu khác nhau. Ví dụ, một tài liệu **JSON** có thể có ít trường hơn tài liệu khác.
* **Chi phí (Cost):** Chi phí bản quyền cho nhiều hệ quản trị cơ sở dữ liệu quan hệ (**RDBMS**) là khá đắt đỏ, trong khi nhiều cơ sở dữ liệu **NoSQL** là mã nguồn mở và được cung cấp miễn phí. Tương tự, một số **RDBMS** phụ thuộc vào các hệ thống phần cứng và lưu trữ độc quyền, tốn kém, trong khi các cơ sở dữ liệu **NoSQL** thường tận dụng các cụm máy chủ thương mại giá rẻ (**commodity servers**).

Cơ sở dữ liệu **NoSQL** được phân chia thành nhiều danh mục dựa trên bản chất của các thao tác và tính năng, bao gồm: kho lưu trữ tài liệu (**document store**), cơ sở dữ liệu dạng cột (**columnar database**), kho lưu trữ khóa - giá trị (**key-value store**), và cơ sở dữ liệu đồ thị (**graph database**). Chúng ta sẽ thảo luận chi tiết từng loại cùng với các trường hợp sử dụng (**use cases**) của chúng dưới góc nhìn thiết kế hệ thống trong các phần tiếp theo.

#### Các loại cơ sở dữ liệu NoSQL (Types of NoSQL databases)

Các loại cơ sở dữ liệu **NoSQL** khác nhau được mô tả dưới đây:
* **Phi quan hệ (Non-Relational)**

---

### --- Trang 11 ---

> [!IMPORTANT]
> **Phân loại các cơ sở dữ liệu NoSQL (The types of NoSQL databases):**
>
> ```
>                     Non-Relational (Phi quan hệ)
>       ┌───────────────┬──────────────────────┬──────────────────────┐
>       │               │                      │                      │
> Key-value store   Document          Column-oriented /         Graph
> (Kho khóa -      (Tài liệu)             columnar             (Đồ thị)
>   giá trị)                           (Hướng cột)
>       │               │                      │                      │
>   DynamoDB         MongoDB               Cassandra                Neo4j
> ```

##### Cơ sở dữ liệu khóa - giá trị (Key-value database)

Cơ sở dữ liệu khóa - giá trị sử dụng các phương thức khóa - giá trị tương tự như bảng băm (**hash tables**) để lưu trữ dữ liệu dưới dạng các cặp khóa - giá trị (**key-value pairs**). Chúng ta có thể thấy điều này được mô tả trong hình vẽ ở các đoạn văn dưới đây. Ở đây, khóa đóng vai trò là khóa duy nhất hoặc khóa chính (**primary key**), còn giá trị có thể là bất kỳ thứ gì, từ các giá trị vô hướng đơn giản (**scalar values**) cho đến các đối tượng phức tạp (**complex objects**). Các cơ sở dữ liệu này cho phép dễ dàng phân vùng dữ liệu (**partitioning**) và mở rộng theo chiều ngang (**horizontal scaling**). Một số cơ sở dữ liệu khóa - giá trị phổ biến bao gồm **Amazon DynamoDB**, **Redis** và **Memcached DB**.

**Trường hợp sử dụng (Use case):** Cơ sở dữ liệu khóa - giá trị hoạt động cực kỳ hiệu quả đối với các ứng dụng định hướng phiên (**session-oriented applications**). Các ứng dụng định hướng phiên, chẳng hạn như ứng dụng web, lưu trữ dữ liệu của người dùng trong bộ nhớ chính (**main memory**) hoặc trong cơ sở dữ liệu suốt thời gian phiên làm việc diễn ra. Dữ liệu này có thể bao gồm thông tin hồ sơ người dùng, các gợi ý cá nhân hóa, chương trình khuyến mãi mục tiêu, mã giảm giá và nhiều thông tin khác. Một mã định danh duy nhất (một khóa - **key**) được gán cho phiên của mỗi người dùng để thuận tiện cho việc truy cập và lưu trữ. Do đó, một lựa chọn tối ưu hơn để lưu trữ loại dữ liệu này chính là cơ sở dữ liệu khóa - giá trị.

Hình dưới đây minh họa một ví dụ về cơ sở dữ liệu khóa - giá trị. Mã định danh sản phẩm (**Product ID**) và Loại sản phẩm (**Type**) được kết hợp lại để đóng vai trò là khóa chính (**primary key**). Cặp thuộc tính này được coi là khóa đại diện cho cơ sở dữ liệu khóa - giá trị này. Hơn nữa, lược đồ (**schema**) để lưu trữ các thuộc tính của mặt hàng được định nghĩa dựa trên bản chất của mặt hàng và số lượng các thuộc tính mà nó sở hữu.

---

### --- Trang 12 ---

> [!NOTE]
> **Dữ liệu được lưu trữ dưới dạng cặp khóa - giá trị trong DynamoDB, trong đó khóa là sự kết hợp của hai thuộc tính (Product ID và Type):**
>
> * **Bảng: Products (Sản phẩm)**
> * **Primary key (Khóa chính) = Partition key (Khóa phân vùng) + Sort key (Khóa sắp xếp):**
>   * Khóa phân vùng (**Partition key**): `Product ID` (ví dụ: `1`, `2`, `2`, `3`)
>   * Khóa sắp xếp (**Sort key**): `Type` (ví dụ: `Book ID`, `Album ID`, `Album ID: Track ID`, `Movie ID`)
> * **Attributes (Các thuộc tính) — Lược đồ được định nghĩa riêng cho từng mục (Schema is defined per item):**
>   * Mặt hàng 1 (Sách): `As You Like It` | Tác giả: `Shakespeare` | Năm: `1623`
>   * Mặt hàng 2 (Album): `6 Partitas` | Tác giả: `Bach`
>   * Mặt hàng 2 (Track nhạc): `Partita No. 1`
>   * Mặt hàng 3 (Phim): `The Kid` | Định dạng: `Movie` | Tên phim: `The Lion King`

##### Cơ sở dữ liệu tài liệu (Document database)

Cơ sở dữ liệu tài liệu được thiết kế để lưu trữ và truy xuất các tài liệu dưới các định dạng như **XML**, **JSON**, **BSON**, v.v. Các tài liệu này được cấu thành từ một cấu trúc dữ liệu cây phân cấp (**hierarchical tree data structure**) có thể bao gồm các ánh xạ (**maps**), các tập hợp (**collections**) và các giá trị vô hướng (**scalar values**). Các tài liệu trong loại cơ sở dữ liệu này có thể có cấu trúc và dữ liệu biến đổi linh hoạt khác nhau. **MongoDB** và **Google Cloud Firestore** là các ví dụ tiêu biểu về cơ sở dữ liệu tài liệu.

**Trường hợp sử dụng (Use case):** Cơ sở dữ liệu tài liệu rất phù hợp cho dữ liệu danh mục phi cấu trúc (**unstructured catalog data**), chẳng hạn như các tệp **JSON** hoặc các dữ liệu phân cấp có cấu trúc phức tạp khác. Ví dụ, trong các ứng dụng thương mại điện tử (**e-commerce applications**), một sản phẩm có thể có tới hàng ngàn thuộc tính, điều này là bất khả thi để lưu trữ hiệu quả trong một cơ sở dữ liệu quan hệ do ảnh hưởng tiêu cực đến hiệu năng đọc (**reading performance**). Đây chính là lúc cơ sở dữ liệu tài liệu phát huy vai trò, khi nó có thể lưu trữ hiệu quả từng thuộc tính trong một tệp tài liệu duy nhất giúp quản lý dễ dàng và tăng tốc độ đọc dữ liệu. Ngoài ra, đây cũng là một lựa chọn tuyệt vời cho các ứng dụng quản lý nội dung (**content management applications**), chẳng hạn như các nền tảng blog và nền tảng chia sẻ video. Một thực thể được ứng dụng yêu cầu sẽ được lưu trữ dưới dạng một tài liệu đơn lẻ trong các ứng dụng như vậy.

---

### --- Trang 13 ---

Ví dụ sau đây minh họa dữ liệu được lưu trữ trong một tài liệu **JSON** (**JSON document**). Dữ liệu này là thông tin về một cá nhân. Nhiều thuộc tính khác nhau được lưu trữ trong tệp, bao gồm `id`, `name`, `email`, v.v.

**Một tệp JSON chứa dữ liệu của một doanh nhân:**

```json
1  {
2    "id": 1001,
3    "name": "Brown",
4    "title": "Mr.",
5    "email": "brown@anyEmail.com",
6    "cell": "123-465-9999",
7    "likes": [
8       "designing",
9       "cycling",
10      "skiing"
11   ],
12   "businesses": [
13      {
14        "name": "ABC co.",
15        "partner": "Vike",
16        "status": "Bankrupt",
17        "date_founded": {
18           "$date": "2021-12-10"
19        }
20      }
21   ]
22 }
```

#### Cơ sở dữ liệu đồ thị (Graph Database)

Cơ sở dữ liệu đồ thị (**Graph databases**) sử dụng cấu trúc dữ liệu đồ thị (**graph data structure**) để lưu trữ dữ liệu, trong đó các đỉnh (**nodes**) đại diện cho các thực thể (**entities**), và các cạnh (**edges**) biểu diễn mối quan hệ giữa các thực thể. Việc tổ chức các node dựa trên các mối quan hệ dẫn đến các mẫu hình (**patterns**) thú vị giữa các node. Loại cơ sở dữ liệu này cho phép chúng ta lưu trữ dữ liệu một lần và sau đó diễn giải nó theo nhiều cách khác nhau dựa trên các mối quan hệ. Các cơ sở dữ liệu đồ thị phổ biến bao gồm **Neo4J**, **OrientDB**, và **InfiniteGraph**. Dữ liệu đồ thị được giữ trong các tệp lưu trữ (**store files**) để lưu trữ bền vững (**persistent storage**). Mỗi tệp chứa dữ liệu cho một phần cụ thể của đồ thị, chẳng hạn như các node, liên kết (**links**), thuộc tính (**properties**), v.v.

Trong hình bên dưới, một số dữ liệu được lưu trữ bằng cấu trúc dữ liệu đồ thị trong các node được kết nối với nhau qua các edge đại diện cho các mối quan hệ giữa các node. Mỗi node có một số thuộc tính, như `Name`, `ID`, và `Age`. Node có `ID: 2` có `Name` là *James* và `Age` là *29* tuổi.

---

### --- Trang 14 ---

**Một đồ thị bao gồm các node và các liên kết (links). Đồ thị này ghi lại các thực thể và mối quan hệ của chúng với nhau:**

* **Node (Đỉnh / Thực thể):**
  * `ID: 1` | `Name: Robert` | `Age: 25`
  * `ID: 2` | `Name: James` | `Age: 29`
  * `ID: 3` | `Type: Group` | `Name: Cricket`

* **Edge / Link (Cạnh / Mối quan hệ):**
  * `ID: 230` | `Label: Knows` | `Since: 2010/11/03`
  * `ID: 231` | `Label: Knows` | `Since: 2010/11/03`
  * `ID: 232` | `Label: Is_Member` | `Since: 2015/10/07`
  * `ID: 233` | `Label: Member`
  * `ID: 234` | `Label: Member`
  * `ID: 235` | `Label: Is_Member` | `Since: 2018/05/04`

> [!NOTE]
> **Use case (Trường hợp sử dụng):** Cơ sở dữ liệu đồ thị có thể được sử dụng trong các ứng dụng mạng xã hội (**social applications**) và cung cấp các sự kiện, số liệu thú vị giữa các loại người dùng khác nhau cũng như các hoạt động của họ. Trọng tâm của cơ sở dữ liệu đồ thị là lưu trữ dữ liệu và mở đường để thúc đẩy việc phân tích và đưa ra quyết định dựa trên các mối quan hệ giữa các thực thể. Bản chất của cơ sở dữ liệu đồ thị giúp chúng phù hợp với nhiều ứng dụng khác nhau, chẳng hạn như tuân thủ quy định và quyền riêng tư của dữ liệu (**data regulation and privacy**), nghiên cứu học máy (**machine learning research**), các ứng dụng dựa trên dịch vụ tài chính (**financial services-based applications**), và nhiều lĩnh vực khác.

#### Cơ sở dữ liệu dạng cột (Columnar Database)

Cơ sở dữ liệu dạng cột (**Columnar databases**) lưu trữ dữ liệu theo các cột (**columns**) thay vì theo các hàng (**rows**). Chúng cho phép truy cập vào tất cả các mục trong cột của cơ sở dữ liệu một cách nhanh chóng và hiệu quả. Các cơ sở dữ liệu dạng cột phổ biến bao gồm **Cassandra**, **HBase**, **Hypertable**, và **Amazon Redshift**.

> [!NOTE]
> **Use case (Trường hợp sử dụng):** Cơ sở dữ liệu dạng cột mang lại hiệu quả cao cho một số lượng lớn các truy vấn tổng hợp (**aggregation queries**) và phân tích dữ liệu (**data analytics queries**). Nó làm giảm đáng kể các yêu cầu về I/O đĩa (**disk I/O**) và lượng dữ liệu cần thiết phải nạp từ đĩa. Ví dụ: trong các ứng dụng liên quan đến các tổ chức tài chính, có nhu cầu tính tổng các giao dịch tài chính trong một khoảng thời gian. Cơ sở dữ liệu dạng cột giúp thao tác này nhanh hơn chỉ bằng cách đọc cột chứa số tiền, bỏ qua các thuộc tính khác của khách hàng.

---

### --- Trang 15 ---

Hình sau minh họa một ví dụ về cơ sở dữ liệu dạng cột, nơi dữ liệu được lưu trữ theo định dạng hướng cột (**column-oriented format**). Điều này khác với các cơ sở dữ liệu quan hệ (**relational databases**), vốn lưu trữ dữ liệu theo hướng dòng (**row-oriented fashion**):

#### Cơ sở dữ liệu hướng cột và hướng dòng (Column-oriented and row-oriented database)

**Bảng dữ liệu mẫu:**

| Emp-no | Dept-Id | Hire_date | Emp-ln | Emp-fn |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1 | 01-01-2001 | Smith | Herry |
| 2 | 1 | 01-02-2003 | Jones | John |
| 3 | 1 | 07-01-2002 | Young | Sue |
| 4 | 2 | 12-04-2001 | Henry | Bill |
| 5 | 3 | 01-01-1999 | Stemle | Laura |
| 6 | 3 | 01-01-2000 | Jung | Robert |

* **Cơ sở dữ liệu hướng dòng (Row-oriented database):**
  * Dòng 1: `1, 1, 01-01-2001, Smith, Herry`
  * Dòng 2: `2, 1, 01-02-2003, Jones, John`
  * Dòng 3: `3, 1, 07-01-2002, Young, Sue`
  * ...

* **Cơ sở dữ liệu hướng cột (Column-oriented database):**
  * Cột `Emp-no`: `1, 2, 3, 4, 5, 6`
  * Cột `Dept-Id`: `1, 1, 1, 2, 3, 3`
  * Cột `Hire_date`: `01-01-2001, 01-02-2003, 07-01-2002, 12-04-2001, 01-01-1999, 01-01-2000`
  * Cột `Emp-ln`: `Smith, Jones, Young, Henry, Stemle, Jung`
  * Cột `Emp-fn`: `Herry, John, Sue, Bill, Laura, Robert`

#### Nhược điểm của cơ sở dữ liệu NoSQL (Drawbacks of NoSQL databases)

##### Thiếu tính tiêu chuẩn hóa (Lack of standardization)
**NoSQL** không tuân theo bất kỳ tiêu chuẩn cụ thể nào, giống như cách các cơ sở dữ liệu quan hệ tuân theo đại số quan hệ (**relational algebra**). Việc chuyển đổi ứng dụng (**porting applications**) từ một loại cơ sở dữ liệu NoSQL này sang một loại khác có thể là một thách thức lớn.

##### Tính nhất quán (Consistency)
Các cơ sở dữ liệu NoSQL cung cấp các sản phẩm khác nhau dựa trên các đánh đổi cụ thể (**trade-offs**) giữa **tính nhất quán** (**Consistency**) và **tính sẵn sàng** (**Availability**) khi các lỗi (**failures**) có thể xảy ra. Chúng ta sẽ không có được tính toàn vẹn dữ liệu mạnh mẽ (**strong data integrity**), chẳng hạn như tính toàn vẹn khóa chính (**primary integrity**) và tính toàn vẹn tham chiếu (**referential integrity**) như trong cơ sở dữ liệu quan hệ. Dữ liệu có thể không đạt được tính nhất quán mạnh (**strongly consistent**) mà sẽ hội tụ chậm rãi bằng cách sử dụng một mô hình yếu hơn như **nhất quán cuối cùng** (**Eventual Consistency**).

---

### --- Trang 16 ---

#### Chọn đúng cơ sở dữ liệu (Choose the right database)

Nhiều yếu tố ảnh hưởng đến việc lựa chọn cơ sở dữ liệu được sử dụng trong một ứng dụng. Bảng so sánh giữa cơ sở dữ liệu quan hệ (**relational databases**) và cơ sở dữ liệu phi quan hệ (**non-relational databases**) được trình bày dưới đây để giúp chúng ta đưa ra lựa chọn:

**Cơ sở dữ liệu quan hệ và phi quan hệ (Relational and Non-relational Databases):**

| Cơ sở dữ liệu quan hệ (Relational Database) | Cơ sở dữ liệu phi quan hệ (Non-relational Database) |
| :--- | :--- |
| Nếu dữ liệu cần lưu trữ là **dữ liệu có cấu trúc** (**structured**) | Nếu dữ liệu cần lưu trữ là **dữ liệu phi cấu trúc** (**unstructured**) |
| Nếu các **thuộc tính ACID** (**ACID properties**) là bắt buộc | Nếu có nhu cầu **tuần tự hóa và giải tuần tự hóa dữ liệu** (**serialize and deserialize data**) |
| Nếu kích thước của dữ liệu **tương đối nhỏ** và có thể nằm vừa trên một node (**fit on a node**) | Nếu kích thước của dữ liệu cần lưu trữ là **lớn** (**large**) |

> [!NOTE]
> **Ghi chú (Note):** Khi cơ sở dữ liệu NoSQL mới ra đời, chúng khác biệt hoàn toàn về cách lập trình và sử dụng so với các cơ sở dữ liệu truyền thống. Tuy nhiên, nhờ vào các nghiên cứu sâu rộng trong giới học thuật và công nghiệp trong nhiều năm qua, ranh giới khác biệt đối với lập trình viên giữa NoSQL và các kho lưu trữ truyền thống đang dần mờ nhạt. Chúng ta có thể sử dụng cùng các cú pháp SQL để giao tiếp với một kho lưu trữ NoSQL và đạt được mức hiệu năng (**performance**) cùng tính nhất quán (**consistency**) tương đương với một kho lưu trữ truyền thống. **Google Cloud Spanner** là một ví dụ điển hình cho loại cơ sở dữ liệu này: hỗ trợ sao chép dữ liệu đa vùng địa lý (**geo-replicated**) với khả năng tự động phân mảnh theo chiều ngang (**automatic horizontal sharding**) và chụp ảnh nhanh toàn cục của dữ liệu ở tốc độ cao (**high-speed global snapshots of data**).

#### Câu hỏi ôn tập (Quiz)
Kiểm tra kiến thức của bạn về các loại cơ sở dữ liệu khác nhau thông qua một bài trắc nghiệm.

---

### --- Trang 17 ---

**Back** (Quay lại)  
**Introduction to Databases** (Giới thiệu về Cơ sở dữ liệu)  
**Mark As Completed** (Đánh dấu đã hoàn thành)  
**Next** (Tiếp theo)  
**Data Replication** (Sao chép dữ liệu)

**Câu hỏi:**
> **Which database should we use when we have unstructured data and there’s a need for high performance?**  
> *(Chúng ta nên sử dụng cơ sở dữ liệu nào khi có dữ liệu phi cấu trúc và có nhu cầu về hiệu năng cao?)*

* **Reset Quiz** (Làm lại bài trắc nghiệm)
* **Question 1 of 6** (Câu hỏi 1 / 6)
* **0 attempted** (0 câu đã trả lời)
* **Submit Answer** (Nộp câu trả lời)
* **1**

---

### --- Trang 18 ---

# Sao chép dữ liệu (Data Replication)

Hiểu rõ các mô hình mà thông qua đó dữ liệu được sao chép qua nhiều node khác nhau.

**Chúng ta sẽ đề cập đến các nội dung sau:**
* **Replication** (Sao chép dữ liệu)
* **Synchronous versus asynchronous replication** (Sao chép đồng bộ so với không đồng bộ)
* **Data replication models** (Các mô hình sao chép dữ liệu)
  * **Single leader/primary-secondary replication** (Sao chép đơn Leader / Primary-Secondary)
  * **Primary-secondary replication methods** (Các phương pháp sao chép Primary-Secondary)
    * **Statement-based replication** (Sao chép dựa trên câu lệnh)
    * **Write-ahead log (WAL) shipping** (Vận chuyển nhật ký ghi trước - WAL shipping)
    * **Logical (row-based) log replication** (Sao chép nhật ký logic / dựa trên dòng)
  * **Multi-leader replication** (Sao chép đa Leader)
    * **Conflict** (Xung đột)
    * **Handle conflicts** (Xử lý xung đột)
      * **Conflict avoidance** (Tránh xung đột)
      * **Last-write-wins** (Ghi đè lần cuối thắng - LWW)
      * **Custom logic** (Logic tùy biến)
    * **Multi-leader replication topologies** (Các topo sao chép đa Leader)
  * **Peer-to-peer/leaderless replication** (Sao chép ngang hàng / Không có Leader)
    * **Quorums** (Túc số / Quorum)

Dữ liệu là một tài sản quý giá đối với một tổ chức vì nó thúc đẩy toàn bộ hoạt động kinh doanh. Dữ liệu cung cấp những hiểu biết kinh doanh quan trọng (**critical business insights**) về những gì là trọng yếu và những gì cần phải thay đổi. Các tổ chức cũng cần phải lưu trữ an toàn và phục vụ dữ liệu khách hàng theo yêu cầu (**on demand**). Khả năng truy cập kịp thời vào dữ liệu cần thiết dưới các điều kiện biến đổi (lượng đọc và ghi tăng vọt, lỗi ổ đĩa và lỗi node, sự cố mất mạng và mất nguồn điện, v.v.) là yêu cầu bắt buộc để vận hành thành công một doanh nghiệp trực tuyến.

Chúng ta cần các đặc tính sau từ kho lưu trữ dữ liệu (**data store**) của mình:

---

# Thiết Kế Hệ Thống Phân Tán: Nhân Bản Dữ Liệu (Data Replication)

* **Khả năng sẵn sàng khi có lỗi (Availability under faults):** Khả năng hệ thống vẫn duy trì hoạt động khi xảy ra lỗi một số ổ đĩa, nút mạng (nodes), gián đoạn mạng (network outages) và mất nguồn điện.
* **Khả năng mở rộng (Scalability):** Mở rộng linh hoạt khi lượng tác vụ đọc (reads), ghi (writes) và các thao tác khác gia tăng.
* **Hiệu năng (Performance):** Đạt độ trễ thấp (low latency) và thông lượng cao (high throughput) phục vụ cho phía máy khách (clients).

Việc đạt được tất cả các đặc tính nêu trên trên một nút đơn lẻ (single node) là một thách thức rất lớn, thậm chí là bất khả thi.

---

## 1. Nhân Bản Dữ Liệu (Replication)

**Nhân bản (Replication)** đề cập đến việc duy trì nhiều bản sao của dữ liệu tại nhiều nút mạng khác nhau (ưu tiên phân tán theo vị trí địa lý - geographically distributed) nhằm đạt được tính sẵn sàng cao (**High Availability**), khả năng mở rộng (**Scalability**) và hiệu năng (**Performance**). 

Trong bài học này, chúng ta giả định rằng một nút đơn lẻ là đủ dung lượng để lưu trữ toàn bộ dữ liệu của hệ thống. Chúng ta sẽ không sử dụng giả định này khi thảo luận về việc phân mảnh dữ liệu (**partitioning/sharding**) trên nhiều nút mạng. Trên thực tế, các khái niệm về **Replication** (nhân bản) và **Partitioning** (phân vùng/phân mảnh) thường đi liền với nhau.

Tuy nhiên, song hành cùng nhiều lợi ích như tính sẵn sàng (**Availability**), cơ chế nhân bản cũng mang lại nhiều sự phức tạp. Nhân bản tương đối đơn giản nếu dữ liệu được nhân bản không đòi hỏi phải thay đổi thường xuyên. Vấn đề cốt lõi trong nhân bản phát sinh khi chúng ta phải duy trì các thay đổi trên dữ liệu nhân bản theo thời gian.

Các vấn đề phức tạp bổ sung có thể phát sinh do cơ chế nhân bản bao gồm:
* Làm thế nào để giữ cho nhiều bản sao dữ liệu luôn nhất quán (**consistent**) với nhau?
* Làm thế nào để xử lý các nút bản sao (**replica nodes**) bị sự cố/hỏng hóc?
* Chúng ta nên thực hiện nhân bản đồng bộ (**synchronously**) hay bất đồng bộ (**asynchronously**)?
* Làm thế nào để giải quyết độ trễ nhân bản (**replication lag**) trong trường hợp nhân bản bất đồng bộ?
* Chúng ta xử lý các thao tác ghi đồng thời (**concurrent writes**) như thế nào?
* Mô hình nhất quán (**consistency model**) nào cần được cung cấp/công bố cho các lập trình viên ứng dụng cuối?

Chúng ta sẽ lần lượt khám phá câu trả lời cho những câu hỏi này trong bài học hôm nay.

---

### Mô Hình Nhân Bản Hoạt Động (Replication in action)

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p020_00.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p020_01.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p020_02.png)

* **Cơ sở dữ liệu gốc (Original database)**
* **Bản sao 1 (Replica 1)**
* **Bản sao 2 (Replica 2)**
* **Bản sao 3 (Replica 3)**
* **Người dùng (User)**
* **Máy chủ (Server)**

Trước khi đi sâu giải thích các loại hình nhân bản khác nhau, chúng ta hãy cùng tìm hiểu về hai phương pháp tiếp cận: nhân bản đồng bộ (**synchronous replication**) và nhân bản bất đồng bộ (**asynchronous replication**).

---

## 2. Nhân Bản Đồng Bộ vs Bất Đồng Bộ (Synchronous versus Asynchronous Replication)

Có hai phương thức để truyền bá/phổ biến (**disseminate**) các thay đổi đến các nút bản sao (**replica nodes**):
1. **Nhân bản đồng bộ (Synchronous replication)**
2. **Nhân bản bất đồng bộ (Asynchronous replication)**

* Trong **nhân bản đồng bộ (synchronous replication)**: Nút chính (**primary node**) phải chờ các thông điệp xác nhận (**acknowledgments - ACK**) từ các nút thứ cấp (**secondary nodes**) về việc đã cập nhật dữ liệu xong. Sau khi nhận đủ phản hồi xác nhận từ tất cả các nút thứ cấp, nút chính mới phản hồi kết quả thành công về cho phía client.
* Ngược lại, trong **nhân bản bất đồng bộ (asynchronous replication)**: Nút chính không cần chờ thông điệp xác nhận từ các nút thứ cấp mà sẽ phản hồi thành công ngay cho client ngay sau khi tự cập nhật dữ liệu trên chính nó xong.

> [!TIP]
> **Ưu điểm của nhân bản đồng bộ:** Tất cả các nút thứ cấp (**secondary nodes**) luôn hoàn toàn đồng nhất và cập nhật mới nhất với nút chính (**primary node**).

> [!WARNING]
> **Nhược điểm của nhân bản đồng bộ:** Nếu một trong các nút thứ cấp không phản hồi xác nhận do sự cố sập nút hoặc lỗi mạng (**network fault**), nút chính sẽ không thể phản hồi xác nhận cho client cho đến khi nhận được xác nhận thành công từ nút bị sự cố. Điều này gây ra độ trễ rất cao (**high latency**) trong thời gian phản hồi từ nút chính về cho client.

Mặt khác:
* **Ưu điểm của nhân bản bất đồng bộ:** Nút chính có thể tiếp tục tiến trình xử lý công việc của mình ngay cả khi tất cả các nút thứ cấp đều gặp sự cố ngừng hoạt động (**down**).
* **Nhược điểm của nhân bản bất đồng bộ:** Nếu nút chính gặp sự cố hư hỏng hoàn toàn, các thao tác ghi (**writes**) chưa kịp sao chép sang các nút thứ cấp sẽ bị mất vĩnh viễn (**data loss**).

Đoạn phân tích trên đã giải thích rõ sự đánh đổi (**trade-off**) cốt lõi giữa **Tính nhất quán của dữ liệu (Data Consistency)** và **Tính sẵn sàng (Availability)** khi các thành phần khác nhau của hệ thống gặp sự cố hỏng hóc.

---

### Sơ Đồ Quy Trình: Nhân Bản Đồng Bộ vs Bất Đồng Bộ

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p022_00.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p022_01.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p022_02.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p022_03.png)

```
[Khách hàng / Client]
       │
       ▼ Ghi X (Write X)
[Nút Chính / Primary] ──► Tự ghi cục bộ (Writes locally)
       ├──► Ghi X (Write X) ──────────► [Nút Thứ Cấp I / Secondary I]
       ├──► Ghi X (Write X) ──────────► [Nút Thứ Cấp II / Secondary II]
       │                                       │
       │◄── Ghi hoàn tất (Write complete) ─────┘
       │◄── Ghi hoàn tất (Write complete) ─────┘
       ▼
Ghi hoàn tất (Write complete) -> Trả về Client
(Cơ chế Đồng bộ / Synchronous)

─────────────────────────────────────────────────────────────

[Khách hàng / Client]
       │
       ▼ Ghi Y (Write Y)
[Nút Chính / Primary] ──► Tự ghi cục bộ (Writes locally)
       │
       ├──► Ghi hoàn tất (Write complete) -> Trả về Client ngay lập tức
       │    (Cơ chế Bất đồng bộ / Asynchronous)
       │
       ├──► Ghi Y (Write Y) ──────────► [Nút Thứ Cấp I / Secondary I] (Ghi hoàn tất / Write complete)
       └──► Ghi Y (Write Y) ──────────► [Nút Thứ Cấp II / Secondary II] (Ghi hoàn tất / Write complete)
```

---

## 3. Các Mô Hình Nhân Bản Dữ Liệu (Data Replication Models)

Bây giờ, chúng ta cùng thảo luận về các cơ chế nhân bản dữ liệu khác nhau. Trong phần này, chúng ta sẽ phân tích các mô hình sau kèm theo điểm mạnh và điểm yếu của từng mô hình:
1. **Nhân bản đơn máy chủ điều phối / Chính - Phụ (Single leader or primary-secondary replication)**
2. **Nhân bản đa máy chủ điều phối (Multi-leader replication)**
3. **Nhân bản ngang hàng / Không máy chủ điều phối (Peer-to-peer or leaderless replication)**

---

### Mô Hình Đơn Máy Chủ Điều Phối / Chính - Phụ (Single Leader / Primary-Secondary Replication)

Trong mô hình **Primary-Secondary replication**, dữ liệu được nhân bản trên nhiều nút khác nhau:
* **Một nút** được chỉ định đóng vai trò là **Primary (nút chính / leader)**. Nút này chịu trách nhiệm xử lý toàn bộ các thao tác ghi (**writes**) đối với dữ liệu được lưu trữ trên cụm (**cluster**). Nút chính cũng đồng thời gửi tất cả các thao tác ghi này đến các nút thứ cấp (**secondary nodes / followers**) và giữ cho chúng luôn ở trạng thái đồng bộ (**in sync**).
* Thao tác đọc (**reads**) có thể được thực hiện từ nút chính hoặc từ bất kỳ nút thứ cấp nào.
* Các thay đổi dữ liệu sẽ được truyền bá (**propagate**) từ nút chính đến các nút thứ cấp.
* Tất cả các cập nhật/ghi mới đều bắt buộc phải thực hiện vào nút chính.

```
       [Tất cả cập nhật ghi vào nút Primary]
                        │
                        ▼
               ┌─────────────────┐
               │  Nút Chính      │◄── (Có thể đọc từ Primary)
               │  (Primary)      │
               └────────┬────────┘
                        │ Các thay đổi được truyền bá (Changes propagate)
             ┌──────────┴──────────┐
             ▼                     ▼
     ┌───────────────┐     ┌───────────────┐
     │  Nút Thứ Cấp  │     │  Nút Thứ Cấp  │
     │  (Secondary)  │     │  (Secondary)  │
     └───────────────┘     └───────────────┘
     (Có thể thực hiện đọc từ các nút Secondary)
```

#### Đánh giá kiến trúc:
* **Trường hợp sử dụng phù hợp:** Cơ chế **Primary-Secondary** rất phù hợp khi tải công việc của chúng ta thiên về đọc nhiều (**read-heavy workload**). Để mở rộng quy mô tốt hơn khi lượng client đọc gia tăng, chúng ta có thể bổ sung thêm nhiều nút cấp dưới (**followers**) và phân phối đều tải đọc (**distribute the read load**) trên các nút follower sẵn có.
* **Hạn chế:** Việc nhân bản dữ liệu tới quá nhiều nút follower có thể biến nút Primary thành điểm nghẽn cổ chai (**bottleneck**). Ngoài ra, mô hình Primary-Secondary hoàn toàn **không phù hợp** nếu tải công việc của hệ thống thiên về ghi nhiều (**write-heavy workload**).
* **Khả năng chịu lỗi đọc (Read resilient):** Một ưu điểm khác của mô hình Primary-Secondary là có khả năng phục hồi khi đọc. Các nút thứ cấp vẫn có thể tiếp tục tiếp nhận và xử lý các yêu cầu đọc trong trường hợp nút chính bị sự cố hỏng hóc. Do đó, đây là một cách tiếp cận cực kỳ hữu ích cho các ứng dụng có cường độ đọc cao (**read-intensive applications**).
* **Vấn đề bất nhất quán (Inconsistency):** Việc nhân bản thông qua phương pháp này sẽ tiềm ẩn tính bất nhất quán nếu chúng ta sử dụng nhân bản bất đồng bộ (**asynchronous replication**). Các client khi đọc dữ liệu từ các bản sao khác nhau có thể nhìn thấy dữ liệu không nhất quán trong trường hợp nút chính bị lỗi mà chưa kịp truyền tải các dữ liệu cập nhật sang các nút thứ cấp. Vì vậy, nếu nút chính bị sập hoàn toàn, bất kỳ bản cập nhật nào bị bỏ lỡ chưa kịp chuyển sang các nút thứ cấp đều có thể bị mất vĩnh viễn.

---

> [!NOTE]
> ### Điểm Cần Suy Ngẫm (Point to Ponder)
> **Câu hỏi:** Điều gì sẽ xảy ra khi nút chính (Primary node) bị lỗi sập?
> 
> **Giải đáp:**
> Trong trường hợp nút chính bị lỗi, một nút thứ cấp có thể được chỉ định/thăng cấp làm nút chính mới, giúp đẩy nhanh quá trình khôi phục của hệ thống so với việc chờ khôi phục nút chính ban đầu. Có hai phương pháp tiếp cận để chọn nút chính mới:
> 1. **Phương pháp thủ công (Manual approach):** Người quản trị hệ thống (**operator**) sẽ trực tiếp đưa ra quyết định nút nào sẽ trở thành nút chính và phát thông báo cấu hình này tới tất cả các nút thứ cấp còn lại.
> 2. **Phương pháp tự động (Automatic approach):** Khi các nút thứ cấp phát hiện nút chính đã bị lỗi/mất liên lạc, chúng sẽ tự động bầu chọn nút chính mới thông qua một quy trình bỏ phiếu được gọi là bầu cử trưởng nhóm (**leader election**).

---

### Các Phương Pháp Nhân Bản Trong Mô Hình Primary-Secondary

Có nhiều phương pháp nhân bản khác nhau được áp dụng trong kiến trúc **Primary-Secondary**:
1. Nhân bản dựa trên câu lệnh (**Statement-based replication**)
2. Chuyển giao nhật ký ghi trước (**Write-ahead log (WAL) shipping**)
3. Nhân bản nhật ký logic theo hàng (**Logical (row-based) log replication**)

Hãy cùng thảo luận chi tiết từng phương pháp:

#### 1. Nhân bản dựa trên câu lệnh (Statement-based replication)
Trong phương pháp tiếp cận nhân bản dựa trên câu lệnh, nút chính (**primary node**) sẽ lưu lại toàn bộ các câu lệnh mà nó đã thực thi (như `INSERT`, `DELETE`, `UPDATE`, v.v.) và gửi trực tiếp các câu lệnh này sang các nút thứ cấp (**secondary nodes**) để thực thi lại. Loại hình nhân bản này từng được áp dụng phổ biến trong MySQL trước phiên bản 5.1.

Cách tiếp cận này thoạt nhìn có vẻ tối ưu nhưng tồn tại nhiều nhược điểm lớn:
* Bất kỳ hàm bất định nào (**nondeterministic function** - ví dụ như hàm lấy thời gian `NOW()`, `RAND()`) đều có thể dẫn đến kết quả ghi khác nhau hoàn toàn giữa nút chính (**leader**) và nút phụ (**follower**).
* Nếu một câu lệnh ghi phụ thuộc vào một thao tác ghi trước đó, và cả hai câu lệnh này đến nút follower theo sai thứ tự, kết quả dữ liệu đầu ra trên nút follower sẽ trở nên không xác định (**uncertain**).

#### 2. Chuyển giao nhật ký ghi trước (Write-ahead log (WAL) shipping)
Trong phương pháp chuyển giao nhật ký ghi trước (**WAL shipping**), trước khi thực thi truy vấn, nút chính sẽ ghi lại thao tác đó vào một tệp nhật ký chuyên biệt gọi là tệp nhật ký ghi trước (**write-ahead log file**). Sau đó, nó sử dụng các chuỗi nhật ký này để sao chép dữ liệu sang các nút thứ cấp. Cơ chế này được áp dụng rộng rãi trong PostgreSQL và Oracle.

> [!WARNING]
> **Hạn chế của WAL shipping:** Tệp WAL chỉ định nghĩa dữ liệu ở mức độ rất thấp (mức độ khối đĩa / byte-level). Nó liên kết chặt chẽ (**tightly coupled**) với cấu trúc bên trong của công cụ cơ sở dữ liệu (**database engine**). Điều này làm cho việc nâng cấp phiên bản phần mềm trên nút leader và các nút follower trở nên vô cùng phức tạp và khó khăn (không thể chạy khác phiên bản engine).

#### 3. Nhân bản nhật ký logic theo hàng (Logical (row-based) log replication)
Trong phương pháp nhân bản nhật ký logic (dựa trên hàng dữ liệu), tất cả các nút thứ cấp sẽ nhân bản các thay đổi dữ liệu thực tế. Ví dụ, nếu một hàng được chèn mới hoặc bị xóa trong một bảng, các nút thứ cấp sẽ nhân bản chính xác sự thay đổi đối với hàng đó trong bảng cụ thể. Nhật ký nhị phân (**binary log**) sẽ ghi lại các biến đổi đối với các bảng cơ sở dữ liệu trên nút chính ở cấp độ bản ghi (**record level**).

Để tạo một bản sao của nút chính, nút thứ cấp chỉ việc đọc luồng dữ liệu này và cập nhật lại các bản ghi tương ứng của nó. Nhân bản theo hàng (**Row-based replication**) không gặp phải các khó khăn như WAL bởi vì nó không đòi hỏi thông tin chi tiết về cách bố trí lưu trữ dữ liệu vật lý bên trong công cụ cơ sở dữ liệu (**database engine**).

---

## 4. Nhân Bản Đa Máy Chủ Điều Phối (Multi-Leader Replication)

Như đã thảo luận ở phần trên, mô hình nhân bản đơn máy chủ điều phối (**single leader replication**) khi kết hợp với nhân bản bất đồng bộ (**asynchronous replication**) tồn tại một nhược điểm lớn: Hệ thống chỉ có duy nhất một nút chính (**primary node**) và toàn bộ các thao tác ghi (**writes**) đều bắt buộc phải đi qua nút này, gây giới hạn nghiêm trọng về mặt hiệu năng (**limits the performance**). Trong trường hợp nút chính gặp sự cố hỏng hóc,... *(tài liệu còn tiếp tục)*

---

# Kiến Trúc Nhân Bản Dữ Liệu Phân Tán (Distributed Data Replication Architecture)

...các nút thứ cấp (secondary nodes) có thể sẽ không có dữ liệu được cập nhật mới nhất từ cơ sở dữ liệu.

## 1. Mô Hình Nhân Bản Đa Nút Chính (Multi-Leader Replication)

**Nhân bản Đa Nút Chính (Multi-leader replication)** là một giải pháp thay thế cho kiến trúc nhân bản đơn nút chính (single leader replication). Trong mô hình này, có nhiều nút chính (**primary nodes**) cùng xử lý các yêu cầu ghi (writes) và sau đó truyền (replicate) các thay đổi này đến tất cả các nút chính và nút thứ cấp khác. Kiểu nhân bản này thường được sử dụng trong các cơ sở dữ liệu kết hợp với các công cụ bên ngoài, chẳng hạn như **Tungsten Replicator** cho MySQL.

Mô hình nhân bản này cực kỳ hữu ích trong các ứng dụng cho phép người dùng tiếp tục làm việc ngay cả khi ngoại tuyến (**offline**) — ví dụ: ứng dụng lịch làm việc (calendar application), nơi chúng ta có thể lên lịch các cuộc họp ngay cả khi không có kết nối Internet. Ngay khi chúng ta trực tuyến (**online**) trở lại, ứng dụng sẽ đồng bộ và nhân bản các thay đổi từ cơ sở dữ liệu cục bộ (điện thoại di động hoặc máy tính xách tay của chúng ta đóng vai trò như một **primary node**) sang các nút khác trong hệ thống.

---

### Mô Hình Nhân Bản Dữ Liệu Đa Nút Chính (Tô-pô All-to-All)

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p025_00.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p025_01.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p025_02.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p025_03.png)

* **Tất cả các cập nhật được thực hiện tới nút chính (Primary):** All updates are made to the primary node
* **Đọc có thể được thực hiện từ nút chính hoặc nút thứ cấp:** Read can be done from primary or secondary node
* **Các thay đổi lan truyền tới các nút chính khác:** Changes propagate to other primary nodes
* **Các thay đổi lan truyền tới nút thứ cấp:** Changes propagate to secondary nodes

---

### Xung Đột Dữ Liệu (Conflict)

Nhân bản đa nút chính đem lại hiệu năng (**Performance**) và khả năng mở rộng (**Scalability**) tốt hơn so với nhân bản đơn nút chính, nhưng nó cũng mang một nhược điểm chí mạng. Vì tất cả các nút chính đều đồng thời tiếp nhận và xử lý các yêu cầu ghi, chúng có thể cùng sửa đổi cùng một bản ghi dữ liệu, từ đó tạo ra **xung đột (conflict)** giữa các nút. 

> [!WARNING]
> **Ví dụ về xung đột:** Giả sử cùng một dữ liệu được chỉnh sửa bởi hai client cùng một lúc. Trong trường hợp đó, các thao tác ghi sẽ thực hiện thành công cục bộ trên nút chính tương ứng của mỗi client; tuy nhiên, khi các bản ghi này được truyền bất đồng bộ (**asynchronously**) sang các nút chính khác, xung đột dữ liệu sẽ xảy ra.

---

### Xử Lý Xung Đột (Handle Conflicts)

Xung đột có thể dẫn đến việc các nút khác nhau lưu trữ dữ liệu khác nhau (bất nhất quán dữ liệu). Tình trạng này cần phải được xử lý một cách hiệu quả mà không làm mất mát bất kỳ dữ liệu nào. Hãy cùng thảo luận một số phương pháp tiếp cận để xử lý xung đột:

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p026_00.png)

#### Tránh Xung Đột (Conflict Avoidance)
Một chiến lược đơn giản để giải quyết xung đột là ngăn chặn không cho chúng xảy ra ngay từ đầu. Xung đột có thể tránh được nếu ứng dụng đảm bảo và xác minh được rằng tất cả các thao tác ghi cho một bản ghi cụ thể luôn đi qua cùng một **leader**.

Tuy nhiên, xung đột vẫn có thể phát sinh nếu một người dùng di chuyển đến một vị trí địa lý khác và hiện tại kết nối gần hơn với một trung tâm dữ liệu (**data center**) khác. Khi điều đó xảy ra, hệ thống buộc phải định tuyến lại lưu lượng mạng (**reroute traffic**). Trong các kịch bản như vậy, phương pháp tránh xung đột sẽ thất bại và dẫn đến các thao tác ghi đồng thời (**concurrent writes**).

#### Ghi Đè Lần Cuối Thắng (Last-Write-Wins - LWW)
Mỗi nút sử dụng đồng hồ cục bộ (**local clock**) của chính mình để gán một nhãn thời gian (**timestamp**) cho từng thao tác cập nhật. Khi xuất hiện xung đột, bản cập nhật có timestamp mới nhất sẽ được chọn giữ lại.

> [!IMPORTANT]
> Phương pháp tiếp cận này cũng có thể tạo ra nhiều khó khăn phức tạp, bởi vì việc đồng bộ hóa đồng hồ giữa các nút (**clock synchronization**) là một bài toán vô cùng nan giải trong các hệ thống phân tán (**distributed systems**). Hiện tượng lệch xung nhịp đồng hồ (**clock skew**) có thể trực tiếp dẫn đến việc mất mát dữ liệu ngoài ý muốn.

#### Logic Tự Định Nghĩa (Custom Logic)
Với phương pháp tiếp cận này, chúng ta có thể tự viết mã xử lý nghiệp vụ riêng để giải quyết xung đột tùy theo nhu cầu cụ thể của ứng dụng. Logic tự định nghĩa này có thể được thực thi trên cả tiến trình đọc (**reads**) lẫn tiến trình ghi (**writes**). Khi hệ thống phát hiện xung đột, nó sẽ gọi trình xử lý xung đột tùy biến (**custom conflict handler**) của chúng ta.

---

### Các Mô Hình Tô-Pô Nhân Bản Đa Nút Chính (Multi-Leader Replication Topologies)

Có rất nhiều kiến trúc tô-pô được áp dụng để triển khai nhân bản đa nút chính, chẳng hạn như **tô-pô vòng tròn (circular topology)**, **tô-pô hình sao (star topology)**, và **tô-pô tất cả-với-tất cả (all-to-all topology)**:
* Phổ biến nhất là **tô-pô all-to-all**.
* Trong tô-pô hình sao và tô-pô vòng tròn, tồn tại một nhược điểm tương tự: nếu một nút gặp sự cố (**fail**), nó có thể làm ảnh hưởng và gián đoạn toàn bộ hệ thống. Đó là lý do tại sao **all-to-all** là mô hình tô-pô được ứng dụng rộng rãi nhất.

---

## 2. Mô Hình Nhân Bản Ngang Hàng / Không Nút Chính (Peer-to-Peer / Leaderless Replication)

Trong mô hình nhân bản chính - phụ (**primary-secondary replication**), nút chính vừa là điểm nghẽn cổ chai (**bottleneck**), vừa là điểm hỏng đơn lẻ (**Single Point of Failure - SPOF**). Hơn nữa, nó chỉ giúp đạt được khả năng mở rộng đọc (**read scalability**) nhưng thất bại trong việc cung cấp khả năng mở rộng ghi (**write scalability**). 

Mô hình nhân bản ngang hàng (**peer-to-peer / leaderless replication**) giải quyết triệt để các vấn đề này bằng cách loại bỏ hoàn toàn nút chính duy nhất. Tất cả các nút đều có vai trò và trọng số ngang nhau, đồng thời đều có khả năng tiếp nhận cả yêu cầu đọc lẫn ghi (**reads and writes requests**). Amazon đã phổ biến hóa kiến trúc này qua hệ thống lưu trữ dữ liệu **DynamoDB** của họ.

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p028_00.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p028_01.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p028_02.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p028_03.png)

* **Các nút giao tiếp các thao tác ghi với nhau:** Nodes communicate their writes to each other
* **Tất cả các nút đọc và ghi toàn bộ dữ liệu:** All nodes read and write all data

Tương tự như nhân bản primary-secondary, kiểu nhân bản này cũng có thể phát sinh tính bất nhất quán (**inconsistency**). Nguyên nhân là do khi nhiều nút cùng chấp thuận các yêu cầu ghi, nó có thể dẫn đến các thao tác ghi đồng thời (**concurrent writes**). Một giải pháp hữu ích được áp dụng để giải quyết sự bất nhất quán giữa ghi - ghi (**write-write inconsistency**) được gọi là **Quorums**.

---

### Cơ Chế Biểu Quyết Đa Số (Quorums)

Giả sử chúng ta có 3 nút. Nếu có ít nhất 2 trong 3 nút đảm bảo trả về kết quả cập nhật thành công, điều đó có nghĩa là chỉ có tối đa 1 nút gặp sự cố. Điều này cũng đồng nghĩa với việc nếu chúng ta đọc dữ liệu từ 2 nút, chắc chắn ít nhất một trong số chúng sẽ chứa phiên bản cập nhật mới nhất, và hệ thống của chúng ta có thể tiếp tục hoạt động bình thường.

> [!NOTE]
> **Định luật Quorum:**
> Nếu chúng ta có $n$ nút:
> * Mỗi thao tác ghi phải được cập nhật thành công trên ít nhất $w$ nút để được xem là một lần ghi thành công.
> * Chúng ta phải đọc dữ liệu từ ít nhất $r$ nút.
>
> Chúng ta sẽ luôn nhận được giá trị cập nhật mới nhất từ thao tác đọc miễn là:
> $$w + r > n$$
> Bởi vì điều này đảm bảo ít nhất một trong các nút được đọc nằm trong tập hợp các nút đã được ghi giá trị cập nhật mới nhất.

Các thao tác đọc và ghi biểu quyết (**quorum reads and writes**) luôn tuân thủ nghiêm ngặt các giá trị $r$ và $w$ này. Các tham số $n$, $w$, và $r$ đều có thể cấu hình linh hoạt trong các cơ sở dữ liệu tuân theo kiến trúc kiểu Dynamo (**Dynamo-style databases**).

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p029_00.png)
![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p029_01.png)

* **Số lượng bản sao (Replicas):** $n = 3$ (Replica 1, Replica 2, Replica 3)
* **Số lượng ghi thành công (Successful writes):** $w = 2$ (Writer nhận Success từ Replica 1 và Replica 2; Failed từ Replica 3)
* **Số lượng đọc thành công (Successful reads):** $r = 2$ (Reader nhận dữ liệu từ Replica 2 và Replica 3)
* **Kết quả:** Reader nhận được giá trị cập nhật mới nhất từ **Replica 2**.

Để biết thêm thông tin chi tiết về chủ đề Quorum, hãy tham khảo các liên kết sau:
* *What is Quorum?*
* *What is Quorum in distributed systems?*

---

## Điều Hướng & Câu Hỏi Ôn Tập (Quiz)

* **Quay lại (Back):** Các Loại Cơ Sở Dữ Liệu (Types of Databases)
* **Đánh dấu hoàn thành (Mark As Completed)**
* **Tiếp theo (Next):** Phân Vùng Dữ Liệu (Data Partitioning)

### **Câu Hỏi (Q):**
> **Cơ chế nhân bản nào là phù hợp nhất (thông lượng cao - high throughput, độ trễ thấp tới client - low latency to client, chi phí/độ phức tạp triển khai thấp - low implementation overhead) khi khối lượng công việc (workload) của hệ thống thiên về đọc dữ liệu (read-heavy)?**

* [ ] **Đặt lại câu hỏi (Reset Quiz)**
* [ ] **Gửi câu trả lời (Submit Answer)**

---

# Phân Vùng Dữ Liệu (Data Partitioning)

Tìm hiểu về các mô hình phân vùng dữ liệu (**Data Partitioning Models**) cùng với ưu điểm và nhược điểm của chúng.

### Chúng ta sẽ tìm hiểu các nội dung sau:
- Tại sao chúng ta lại phân vùng dữ liệu? (**Why do we partition data?**)
- Phân mảnh dữ liệu (**Sharding**)
- Phân mảnh theo chiều dọc (**Vertical sharding**)
- Phân mảnh theo chiều ngang (**Horizontal sharding**)
- Phân mảnh dựa trên dải khóa (**Key-range based sharding**)
  - Ưu điểm (**Advantages**)
  - Nhược điểm (**Disadvantages**)
- Phân mảnh dựa trên băm (**Hash-based sharding**)
  - Ưu điểm (**Advantages**)
  - Nhược điểm (**Disadvantages**)
- Băm nhất quán (**Consistent hashing**)
  - Ưu điểm của băm nhất quán (**Advantages of consistent hashing**)
  - Nhược điểm của băm nhất quán (**Disadvantages of consistent hashing**)
- Tái cân bằng các phân vùng (**Rebalance the partitions**)
  - Tránh dùng phép chia lấy dư băm `hash mod n` (**Avoid hash mod n**)
  - Số lượng phân vùng cố định (**Fixed number of partitions**)
  - Phân vùng động (**Dynamic partitioning**)
  - Phân vùng theo tỷ lệ với các nút (**Partition proportionally to nodes**)
- Phân vùng và chỉ mục phụ (**Partitioning and secondary indexes**)
  - Phân vùng chỉ mục phụ theo tài liệu (**Partition secondary indexes by document**)
  - Phân vùng chỉ mục phụ theo thuật ngữ (**Partition secondary indexes by the term**)
- Định tuyến yêu cầu (**Request routing**)
- ZooKeeper
- Kết luận (**Conclusion**)

---

## Tại sao chúng ta lại phân vùng dữ liệu? (Why do we partition data?)

Dữ liệu là tài sản của bất kỳ tổ chức nào. Lượng dữ liệu ngày càng gia tăng cùng với lưu lượng truy cập đọc/ghi (**read/write traffic**) đồng thời vào dữ liệu đã tạo ra áp lực lớn về khả năng mở rộng (**scalability**) lên các cơ sở dữ liệu truyền thống. Hệ quả là, độ trễ (**latency**) và thông lượng (**throughput**) đều bị ảnh hưởng tiêu cực. Các cơ sở dữ liệu truyền thống vẫn rất hấp dẫn nhờ vào các đặc tính ưu việt của chúng như truy vấn theo dải (**range queries**), các chỉ mục phụ (**secondary indices**), và các giao dịch giao dịch tuân thủ tính chất ACID (**ACID properties**).

Đến một thời điểm nhất định, một cơ sở dữ liệu chạy trên một nút đơn lẻ (**single node-based database**) sẽ không còn đủ sức để gánh vác khối lượng tải đó nữa. Chúng ta có thể cần phải phân tán dữ liệu trên nhiều nút (**nodes**) nhưng vẫn phải bảo đảm cung cấp được tất cả các đặc tính tuyệt vời của cơ sở dữ liệu quan hệ (**relational databases**). Trên thực tế, việc cung cấp các đặc tính giống như cơ sở dữ liệu đơn nút trên một cơ sở dữ liệu phân tán (**distributed database**) đã được chứng minh là một thách thức vô cùng lớn.

Một giải pháp là chuyển dữ liệu sang một hệ thống dạng NoSQL. Tuy nhiên, khối lượng mã nguồn lịch sử kế thừa (**historical codebase**) cùng với sự gắn kết chặt chẽ của nó với các cơ sở dữ liệu truyền thống khiến cho việc chuyển đổi này trở thành một bài toán vô cùng tốn kém để giải quyết.

Các tổ chức có thể mở rộng quy mô cơ sở dữ liệu truyền thống bằng cách sử dụng giải pháp của bên thứ ba (**third-party solution**). Nhưng thông thường, việc tích hợp giải pháp của bên thứ ba luôn đi kèm với những sự phức tạp riêng. Quan trọng hơn, có rất nhiều cơ hội để tối ưu hóa cho bài toán cụ thể đang gặp phải nhằm đạt được hiệu năng vượt trội hơn nhiều so với một giải pháp đa dụng chung chung (**general-purpose solution**).

Phân vùng dữ liệu (**Data partitioning**) (hay còn gọi là phân mảnh - **sharding**) cho phép chúng ta sử dụng nhiều nút, trong đó mỗi nút quản lý một phần của toàn bộ dữ liệu. Để xử lý tốc độ truy vấn (**query rates**) và dung lượng dữ liệu ngày càng gia tăng, chúng ta phải nỗ lực đạt được các phân vùng cân bằng và tải đọc/ghi cân bằng (**balanced read/write load**).

Chúng ta sẽ thảo luận về các phương pháp phân vùng dữ liệu khác nhau, các thách thức liên quan và giải pháp cho chúng trong bài học này.

---

## Phân mảnh dữ liệu (Sharding)

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p033_00.png)
*Một cơ sở dữ liệu với hai phân vùng (Partition 0 và Partition 1) để phân phối dữ liệu và khối lượng tải đọc/ghi liên quan từ Người dùng (User) thông qua Máy chủ Cơ sở dữ liệu (Database Server).*

Để chia sẻ tải giữa nhiều nút, chúng ta cần phân vùng dữ liệu bằng một cơ chế được gọi là phân vùng (**partitioning**) hoặc phân mảnh (**sharding**). Trong cách tiếp cận này, chúng ta chia nhỏ một tập dữ liệu lớn thành các khối dữ liệu nhỏ hơn và lưu trữ tại các nút khác nhau trên mạng của chúng ta.

Việc phân vùng bắt buộc phải cân bằng để mỗi phân vùng nhận được lượng dữ liệu xấp xỉ bằng nhau. Nếu việc phân vùng bị mất cân bằng, phần lớn các truy vấn sẽ dồn vào một vài phân vùng nhất định. Những phân vùng bị quá tải này sẽ tạo ra điểm nghẽn cổ chai của hệ thống (**system bottleneck**). Hiệu quả của việc phân vùng sẽ bị tổn hại nghiêm trọng vì một phần lớn các truy vấn truy xuất dữ liệu sẽ bị gửi đến các nút đang chứa các phân vùng bị tắc nghẽn nghiêm trọng. Những phân vùng như vậy được gọi là các điểm nóng (**hotspots**). Nhìn chung, chúng ta sử dụng hai cách sau để phân mảnh dữ liệu:

1. **Phân mảnh theo chiều dọc (Vertical sharding)**
2. **Phân mảnh theo chiều ngang (Horizontal sharding)**

---

### Phân mảnh theo chiều dọc (Vertical sharding)

Chúng ta có thể đặt các bảng khác nhau vào các thực thể cơ sở dữ liệu (**database instances**) khác nhau, vốn có thể đang chạy trên các máy chủ vật lý khác nhau. Chúng ta cũng có thể chia nhỏ một bảng thành nhiều bảng sao cho một số cột nằm ở bảng này trong khi các cột còn lại nằm ở bảng khác. Chúng ta cần phải cẩn trọng nếu có các phép kết nối (**joins**) giữa nhiều bảng. Tốt nhất là chúng ta nên giữ các bảng này cùng nhau trên một mảnh (**shard**).

Thông thường, phân mảnh theo chiều dọc được sử dụng để tăng tốc độ truy xuất dữ liệu từ một bảng chứa các cột có văn bản rất dài (**wide text**) hoặc một đối tượng nhị phân lớn (**blob - binary large object**). Trong trường hợp này, cột chứa văn bản lớn hoặc blob sẽ được tách sang một bảng khác.

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p033_01.png)

Như được minh họa ở hình trên, bảng `Employee` ban đầu được chia thành hai bảng: một bảng `Employee` tinh giản và một bảng `EmployeePicture`. Bảng `EmployeePicture` chỉ có hai cột là `EmployeeID` và `Picture`, được tách ra từ bảng gốc. Hơn nữa, khóa chính (**primary key**) `EmployeeID` của bảng `Employee` được thêm vào cả hai bảng đã phân vùng. Điều này giúp cho việc đọc và ghi dữ liệu trở nên dễ dàng hơn, và việc tái cấu trúc (**reconstruction**) lại bảng gốc được thực hiện một cách hiệu quả.

Phân mảnh theo chiều dọc có những điểm phức tạp riêng và phù hợp hơn với việc phân vùng thủ công (**manual partitioning**), nơi mà các bên liên quan (**stakeholders**) phải cân nhắc kỹ lưỡng để quyết định cách phân chia dữ liệu. Ngược lại, phân mảnh theo chiều ngang lại rất thích hợp để tự động hóa ngay cả trong các điều kiện động (**dynamic conditions**).

> [!NOTE]
> Việc tạo các mảnh (**shards**) bằng cách di chuyển các bảng cụ thể của một cơ sở dữ liệu sang các vị trí khác nhau cũng là một dạng của phân mảnh theo chiều dọc. Thông thường, những bảng này được gom vào cùng một shard vì chúng hay xuất hiện cùng nhau trong các truy vấn, chẳng hạn như trong các phép kết nối (**joins**). Chúng ta sẽ thấy một ví dụ về trường hợp sử dụng như vậy ở phần sau của khóa học.

---

### Phân mảnh theo chiều ngang (Horizontal sharding)

Đôi khi, một số bảng trong cơ sở dữ liệu trở nên quá lớn và làm ảnh hưởng tiêu cực đến độ trễ đọc/ghi (**read/write latency**). Phân mảnh hoặc phân vùng theo chiều ngang được sử dụng để chia một bảng thành nhiều bảng bằng cách chia nhỏ dữ liệu theo từng dòng (**row-wise**). Mỗi phân vùng của bảng gốc được phân phối trên các máy chủ cơ sở dữ liệu được gọi là một mảnh (**shard**). Thông thường, có hai chiến lược sẵn có:

1. **Phân mảnh dựa trên dải khóa (Key-range based sharding)**
2. **Phân mảnh dựa trên băm (Hash-based sharding)**

---

### Phân mảnh dựa trên dải khóa (Key-range based sharding)

Trong phân mảnh dựa trên dải khóa, mỗi phân vùng được chỉ định một dải khóa liên tục (**continuous range of keys**).

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p033_02.png)

Trong hình trên, việc phân vùng theo chiều ngang trên bảng `Invoice` được thực hiện bằng cách sử dụng phân mảnh dựa trên dải khóa với `Customer_Id` đóng vai trò là khóa phân vùng (**partition key**). Hai bảng có màu sắc khác nhau đại diện cho hai phân vùng (Database shard 1 và Database shard 2).

Đôi khi, một cơ sở dữ liệu bao gồm nhiều bảng bị ràng buộc với nhau bởi các mối quan hệ khóa ngoại (**foreign key relationships**). Trong trường hợp như vậy, việc phân vùng theo chiều ngang được thực hiện bằng cách sử dụng **cùng một khóa phân vùng** trên tất cả các bảng trong một quan hệ. Các bảng (hoặc bảng con) thuộc về cùng một khóa phân vùng sẽ được phân phối đến cùng một mảnh cơ sở dữ liệu (**database shard**). 

Hình ảnh minh họa cho thấy nhiều bảng có cùng một khóa phân vùng được đặt chung trong một mảnh cơ sở dữ liệu duy nhất:

| Bảng / Khóa | Database shard 1 (Shard_Id: 1, 2) | Database shard 2 (Shard_Id: 3, 4) |
| :--- | :--- | :--- |
| **Bảng Invoice** *(Customer_Id, Creation_date, Invoice_Id)* | • Customer_Id: 1, 01-01-2015, Invoice_Id: 5101<br>• Customer_Id: 2, 10-01-2017, Invoice_Id: 5201<br>• Customer_Id: 2, 05-11-2018, Invoice_Id: 5301 | • Customer_Id: 3, 30-01-2017, Invoice_Id: 5102<br>• Customer_Id: 3, 10-12-2017, Invoice_Id: 5202<br>• Customer_Id: 4, 07-11-2017, Invoice_Id: 5302 |
| **Bảng Customer** *(Customer_Id, Name)* | • 1: Company A<br>• 2: Company B | • 3: Company C<br>• 4: Company D |
| **Bảng Invoice_item** *(Customer_Id, Invoice_item_Id, Invoice_Id)* | • 1, 11101, 5101<br>• 1, 11201, 5101<br>• 2, 11301, 5201<br>• 2, 11401, 5201 | • 3, 11102, 5102<br>• 3, 11202, 5102<br>• 3, 11302, 5202<br>• 4, 11402, 5302 |

Các kỹ thuật thiết kế cơ bản được sử dụng trong phân mảnh đa bảng (**multi-table sharding**) bao gồm:

- **Khóa phân vùng trong bảng ánh xạ Customer:** Bảng này nằm trên mỗi shard và lưu trữ các khóa phân vùng được sử dụng trong shard đó. Ứng dụng tạo ra một logic ánh xạ giữa các khóa phân vùng và các shard cơ sở dữ liệu bằng cách đọc bảng này từ tất cả các shard để giúp việc ánh xạ đạt hiệu quả cao. Đôi khi, ứng dụng sử dụng các thuật toán nâng cao để xác định vị trí của một khóa phân vùng thuộc về một shard cụ thể.
- **Cột khóa phân vùng (`Customer_Id`) được sao chép sang tất cả các bảng khác như một điểm cô lập dữ liệu (data isolation point):** Phương pháp này có sự đánh đổi giữa việc tăng dung lượng lưu trữ và việc định vị các shard mong muốn một cách hiệu quả. Ngoài ra, nó còn rất hữu ích cho việc phân phối dữ liệu và khối lượng công việc (**workload distribution**) đến các shard cơ sở dữ liệu khác nhau.
- **Logic định tuyến dữ liệu (Data routing logic):** Tầng ứng dụng (**application tier**) sử dụng khóa phân vùng để ánh xạ các truy vấn cụ thể đến đúng shard cơ sở dữ liệu tương ứng.
- **Tính duy nhất của khóa chính (Primary keys uniqueness):** Các khóa chính phải là duy nhất trên toàn bộ các shard cơ sở dữ liệu để tránh xung đột khóa (**key collision**) trong quá trình di chuyển dữ liệu giữa các shard và khi hợp nhất dữ liệu trong môi trường xử lý phân tích trực tuyến (**OLAP - Online Analytical Processing**).
- **Cột `Creation_date` đóng vai trò là điểm nhất quán dữ liệu (data consistency point):** Với giả định rằng đồng hồ của tất cả các nút đều được đồng bộ hóa, cột này được sử dụng làm tiêu chí để hợp nhất dữ liệu từ tất cả các shard cơ sở dữ liệu vào môi trường phân tích chung.

---

# Kiến Trúc Phân Vùng Dữ Liệu (Database Sharding & Partitioning)

...cái nhìn toàn cục (global view) khi thực sự cần thiết.

### Ưu điểm (Advantages)
Sử dụng phương pháp phân mảnh dựa trên dải khóa (key-range-based sharding), cơ chế truy vấn theo dải (range query) rất dễ triển khai. Chúng ta biết chính xác nơi nào (node nào, shard nào) cần tìm kiếm một dải khóa cụ thể.

Các truy vấn dải (range queries) có thể được thực thi bằng cách sử dụng các khóa phân vùng (partitioning keys), và các khóa này có thể được lưu trữ trong các phân vùng theo thứ tự đã sắp xếp. Cách thức sắp xếp chính xác diễn ra như thế nào theo thời gian khi có dữ liệu mới nạp vào sẽ phụ thuộc vào từng triển khai cụ thể (implementation-specific).

### Nhược điểm (Disadvantages)
* Các truy vấn theo dải (range queries) không thể thực hiện được nếu dùng các khóa khác ngoài khóa phân vùng (partitioning key).
* Nếu các khóa không được lựa chọn hợp lý, một số node có thể phải lưu trữ nhiều dữ liệu hơn do lưu lượng truy cập (traffic) phân bổ không đồng đều (uneven distribution).

---

## Phân mảnh dựa trên hàm băm (Hash-based sharding)

Phân mảnh dựa trên hàm băm (Hash-based sharding) sử dụng một hàm dạng băm (hash-like function) trên một thuộc tính, và nó tạo ra các giá trị khác nhau dựa trên thuộc tính được dùng để thực hiện phân vùng. Khái niệm cốt lõi là áp dụng một hàm băm lên khóa để nhận về một giá trị băm (hash value), sau đó lấy phần dư (`mod`) cho tổng số phân vùng. Một khi đã tìm được hàm băm phù hợp cho các khóa, chúng ta có thể cấp cho mỗi phân vùng một dải giá trị băm (thay vì một dải khóa). Bất kỳ khóa nào có giá trị băm rơi vào bên trong dải đó sẽ được lưu giữ tại phân vùng tương ứng.

Trong hình minh họa dưới đây, chúng ta sử dụng một hàm băm có dạng:

$$\text{Value} \pmod n$$

Trong đó $n$ là số lượng node, ở đây là bốn ($n = 4$). Chúng ta phân bổ các khóa vào các node bằng cách kiểm tra giá trị mod của từng khóa:
* Các khóa có giá trị mod bằng $2$ được phân bổ vào **Node 2**.
* Các khóa có giá trị mod bằng $1$ được phân bổ vào **Node 1**.
* Các khóa có giá trị mod bằng $3$ được phân bổ vào **Node 3**.
* Do không có khóa nào có giá trị mod bằng $0$, **Node 0** bị để trống.

---

### Minh họa: Hash-based sharding

| Khóa (Key) | Giá trị (Value) | Hàm băm $f = \text{Value} \pmod 4$ | Node được gán |
| :--- | :--- | :--- | :--- |
| 1 | 226666502 | 2 | Node 2 |
| 2 | 150355825 | 1 | Node 1 |
| 3 | 266622091 | 3 | Node 3 |
| 4 | 133825114 | 2 | Node 2 |
| 5 | 209053885 | 1 | Node 1 |
| 6 | 159421699 | 3 | Node 3 |

*Node 0: Trống (không có khóa nào có mod = 0)*

#### Ưu điểm (Advantages)
* Các khóa được phân bổ đồng đều (uniformly distributed) trên toàn bộ các node.

#### Nhược điểm (Disadvantages)
* Chúng ta không thể thực hiện các truy vấn theo dải (range queries) với kỹ thuật này. Các khóa sẽ bị phân tán rải rác trên tất cả các phân vùng.

> [!NOTE]
> **Có bao nhiêu Shard trên mỗi cơ sở dữ liệu? (How many shards per database?)**
> 
> Dựa trên thực nghiệm, chúng ta có thể xác định một node có thể phục vụ bao nhiêu tải với hiệu năng chấp nhận được. Điều này giúp tìm ra dung lượng dữ liệu tối đa mà chúng ta muốn lưu trữ trên bất kỳ một node đơn lẻ nào.
> 
> Ví dụ: nếu xác định có thể đặt tối đa 50 GB dữ liệu trên một node, chúng ta có phép tính sau:
> * Kích thước cơ sở dữ liệu (Database size) = $10\text{ TB}$
> * Kích thước của một shard đơn lẻ (Size of a single shard) = $50\text{ GB}$
> * Số lượng shard mà cơ sở dữ liệu cần được phân bổ = $10\text{ TB} / 50\text{ GB} = 200\text{ shards}$

---

## Băm nhất quán (Consistent Hashing)

Băm nhất quán (Consistent Hashing) gán cho mỗi máy chủ (server) hoặc phần tử (item) trong bảng băm phân tán (Distributed Hash Table) một vị trí trên một vòng tròn trừu tượng, gọi là vòng băm (ring), bất kể số lượng máy chủ hiện có trong bảng là bao nhiêu. Cơ chế này cho phép các máy chủ và các đối tượng mở rộng quy mô (scale) mà không làm ảnh hưởng tiêu cực đến hiệu năng tổng thể của toàn hệ thống.

### Ưu điểm của Consistent Hashing (Advantages of consistent hashing)
* Dễ dàng mở rộng theo chiều ngang (scale horizontally).
* Tăng thông lượng (Throughput) và cải thiện độ trễ (Latency) của ứng dụng.

### Nhược điểm của Consistent Hashing (Disadvantages of consistent hashing)
* Việc gán ngẫu nhiên các node trên vòng băm (ring) có thể gây ra hiện tượng phân bổ không đồng đều (non-uniform distribution).

---

## Tái cân bằng các phân vùng (Rebalance the partitions)

Tải truy vấn (query load) có thể bị mất cân bằng giữa các node do nhiều nguyên nhân, bao gồm các nguyên nhân sau:
* Sự phân bổ dữ liệu không đồng đều (unequal distribution).
* Có quá nhiều tải tập trung vào một phân vùng đơn lẻ (single partition).
* Lưu lượng truy vấn gia tăng đột biến, và chúng ta cần bổ sung thêm nhiều node hơn để đáp ứng kịp thời.

Chúng ta có thể áp dụng các chiến lược sau để tái cân bằng phân vùng (rebalance partitions):

---

### Tránh sử dụng hàm băm mod n (Avoid hash mod n)

Thông thường, chúng ta tránh sử dụng giá trị băm của một khóa dạng $\text{hash} \pmod n$ để phân vùng (trước đó chúng ta sử dụng cơ chế này chỉ nhằm mục đích giải thích khái niệm băm theo cách đơn giản nhất). 

Vấn đề khi thêm hoặc bớt các node trong trường hợp dùng $\text{hash} \pmod n$ là số phân vùng của mọi node đều bị thay đổi, dẫn đến một khối lượng dữ liệu khổng lồ phải di chuyển. 

* **Ví dụ:** Giả sử ta có $\text{hash(key)} = 1235$.
  * Nếu ban đầu ta có 5 node, khóa sẽ bắt đầu nằm ở Node 1 (vì $1235 \pmod 5 = 0$).
  * Khi thêm một node mới ($n = 6$), khóa sẽ buộc phải chuyển sang Node 6 (vì $1235 \pmod 6 = 5$), và cứ tiếp tục như vậy.
  
Việc di chuyển các khóa từ node này sang node khác trên diện rộng như vậy khiến chi phí tái cân bằng (rebalancing) trở nên vô cùng tốn kém.

---

### Số lượng phân vùng cố định (Fixed number of partitions)

Trong cách tiếp cận này, số lượng phân vùng cần tạo được cố định ngay tại thời điểm chúng ta thiết lập cơ sở dữ liệu. Chúng ta tạo ra số lượng phân vùng lớn hơn rất nhiều so với số lượng node thực tế, sau đó gán các phân vùng này cho các node. Khi một node mới được thêm vào hệ thống, nó có thể tiếp nhận lại một vài phân vùng từ các node hiện có cho đến khi toàn bộ phân vùng được chia đều.

Phương pháp này có một mặt hạn chế: Kích thước của mỗi phân vùng sẽ tăng dần theo tổng dung lượng dữ liệu trong cụm (cluster), vì tất cả các phân vùng đều chứa một phần nhỏ của tổng dữ liệu.
* Nếu kích thước phân vùng quá nhỏ, nó sẽ gây ra quá nhiều chi phí quản lý vận hành (overhead) do ta phải duy trì một số lượng lớn các phân vùng nhỏ.
* Nếu kích thước phân vùng quá lớn, việc tái cân bằng các node và phục hồi sau sự cố lỗi node (node failures) sẽ trở nên rất đắt đỏ.

Do đó, việc lựa chọn đúng số lượng phân vùng là điều tối quan trọng. Phương pháp số lượng phân vùng cố định này được sử dụng trong **Elasticsearch**, **Riak**, và nhiều hệ thống khác.

---

### Phân vùng động (Dynamic partitioning)

Trong cách tiếp cận này, khi kích thước của một phân vùng chạm đến ngưỡng giới hạn (threshold), nó sẽ tự động được chia đôi thành hai phân vùng bằng nhau. Một trong hai phân vùng vừa tách sẽ được gán cho một node, và phân vùng còn lại được gán cho một node khác. Bằng cách này, tải được phân chia đồng đều. Số lượng phân vùng tự thích ứng linh hoạt với tổng lượng dữ liệu—đây chính là ưu điểm lớn của phân vùng động.

Tuy nhiên, cách tiếp cận này tồn tại một nhược điểm lớn: Rất khó để thực hiện tái cân bằng động (dynamic rebalancing) trong khi hệ thống vẫn đang tiếp nhận và phục vụ các thao tác đọc và ghi (reads/writes). Tái cân bằng động trong quá trình đọc/ghi là một thách thức cực lớn vì nó liên quan đến việc di chuyển dữ liệu giữa các node, gây ra độ trễ (latency) và các xung đột tiềm ẩn (potential conflicts). Việc đảm bảo tính nhất quán của dữ liệu (Data Consistency) khi dữ liệu vừa bị di chuyển vừa bị truy cập đồng thời, cộng với việc duy trì tính sẵn sàng (Availability) — có thể phải tạm dừng thao tác đọc/ghi trong lúc tái cân bằng — sẽ tạo ra những sự phức tạp nghiêm trọng làm ảnh hưởng đến hiệu năng và độ tin cậy của toàn hệ thống. Cách tiếp cận này được áp dụng trong **HBase** và **MongoDB**.

---

### Phân vùng tỷ lệ thuận với số node (Partition proportionally to nodes)

Trong phương pháp này, số lượng phân vùng tỷ lệ thuận với số lượng node, nghĩa là mỗi node sở hữu một số lượng phân vùng cố định. Ở các cách tiếp cận trước, số lượng phân vùng phụ thuộc vào kích thước của tập dữ liệu; nhưng ở đây thì không phải như vậy. 

* Khi số lượng node giữ nguyên không đổi, kích thước của mỗi phân vùng sẽ tăng dần theo dung lượng của tập dữ liệu.
* Ngược lại, khi số lượng node tăng lên, kích thước của các phân vùng sẽ thu nhỏ lại. 

Khi một node mới gia nhập vào mạng lưới, nó sẽ chia tách ngẫu nhiên một số lượng phân vùng hiện có, sau đó tiếp quản một nửa phần được tách và giữ nguyên nửa còn lại. Điều này có thể dẫn đến hiện tượng phân chia không đồng đều (unfair split). Cách tiếp cận này được sử dụng bởi **Cassandra** và **Ketama**.

---

> [!NOTE]
> ### Điểm Cần Suy Ngẫm (Point to Ponder)
> **Câu hỏi:** Ai là người thực hiện việc tái cân bằng (rebalancing)? Cơ chế này diễn ra tự động (automatic) hay thủ công (manual)?
> 
> **Lời giải đáp:**
> Có hai phương thức để thực hiện tái cân bằng: **Tự động (automatic)** và **Thủ công (manual)**.
> * Trong tái cân bằng tự động, không có sự can thiệp của quản trị viên. Hệ thống tự động xác định khi nào cần thực hiện phân vùng và khi nào cần di chuyển dữ liệu từ node này sang node khác.
> * Trong tái cân bằng thủ công, quản trị viên (administrator) sẽ trực tiếp xác định thời điểm và phương thức thực hiện phân vùng. 
> 
> Các tổ chức sẽ tiến hành tái cân bằng tùy theo nhu cầu riêng của họ. Một số sử dụng cơ chế tự động, và một số sử dụng cơ chế thủ công.

---

## Phân vùng và chỉ mục phụ (Partitioning and secondary indexes)

Chúng ta đã thảo luận về các cơ chế phân vùng theo mô hình dữ liệu khóa-giá trị (key-value data model), trong đó các bản ghi được truy xuất thông qua khóa chính (primary keys). Nhưng điều gì sẽ xảy ra nếu chúng ta bắt buộc phải truy cập các bản ghi thông qua các chỉ mục phụ (secondary indexes)? 

Chỉ mục phụ (secondary indexes) là các bản ghi không được định danh trực tiếp bằng khóa chính, mà chỉ là một phương thức để tìm kiếm một giá trị cụ thể nào đó. Ví dụ: trong hình minh họa phân vùng ngang ở trên chứa bảng khách hàng (`customer table`), ta cần tìm kiếm tất cả các khách hàng có cùng năm tạo tài khoản.

Chúng ta có thể thực hiện phân vùng với các chỉ mục phụ theo các phương thức sau:

---

### 1. Phân vùng chỉ mục phụ theo tài liệu (Partition secondary indexes by document)

Mỗi phân vùng hoàn toàn độc lập trong cách tiếp cận lập chỉ mục này. Mỗi phân vùng sở hữu các chỉ mục phụ của riêng nó và chỉ bao quát các tài liệu (documents) nằm bên trong chính phân vùng đó. Nó hoàn toàn không quan tâm đến dữ liệu đang được lưu giữ ở các phân vùng khác. 

Nếu chúng ta muốn ghi bất kỳ dữ liệu nào vào cơ sở dữ liệu, chúng ta chỉ cần xử lý duy nhất phân vùng chứa mã định danh tài liệu (Document ID) mà chúng ta đang ghi. Cơ chế này còn được gọi là **chỉ mục cục bộ (local index)**.

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p042_00.png)

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p042_01.png)

Trong hình minh họa, có ba phân vùng, mỗi phân vùng đều có định danh và dữ liệu riêng biệt. Nếu chúng ta muốn lấy toàn bộ các `customer ID` có tên là `John`, chúng ta bắt buộc phải gửi yêu cầu truy vấn đến **toàn bộ các phân vùng**.

> [!WARNING]
> Tuy nhiên, kiểu truy vấn này trên các chỉ mục phụ có thể rất đắt đỏ (expensive). Do bị giới hạn bởi độ trễ (latency) của một phân vùng có hiệu năng kém nhất (poor-performing partition), độ trễ tổng thể của truy vấn đọc (read query latencies) có thể bị kéo tăng lên đáng kể.

---

### 2. Phân vùng chỉ mục phụ theo thuật ngữ (Partition secondary indexes by the term)
Thay vì tạo một chỉ mục phụ cho từng phân vùng (chỉ mục cục bộ - local index), chúng ta có thể...

---

### Trang 43

tạo một chỉ mục toàn cục (global index) cho các thuật ngữ thứ cấp (secondary terms) bao trùm dữ liệu từ tất cả các phân vùng (partitions).

Trong hình minh họa bên dưới, chúng ta tạo các chỉ mục trên tên (thuật ngữ/term mà chúng ta dùng để phân vùng) và lưu trữ tất cả các chỉ mục cho tên trên các nút (nodes) riêng biệt. Để lấy `cust_id` của tất cả khách hàng có tên là "John", chúng ta phải xác định chỉ mục thuật ngữ (term index) của mình nằm ở đâu. Chỉ mục 0 (`Index 0`) chứa tất cả các khách hàng có tên bắt đầu từ "A" đến "M". Chỉ mục 1 (`Index 1`) bao gồm tất cả các khách hàng có tên bắt đầu từ "N" đến "Z". Vì John nằm trong `Index 0`, chúng ta sẽ truy xuất danh sách `cust_id` có tên John từ `Index 0`.

Phân vùng chỉ mục phụ theo thuật ngữ (Partitioning secondary indexes by term) mang lại hiệu quả đọc cao hơn (read-efficient) so với phân vùng chỉ mục phụ theo tài liệu (partitioning secondary indexes by document). Điều này là do nó chỉ truy cập vào phân vùng chứa thuật ngữ đó. Tuy nhiên, một thao tác ghi (write) đơn lẻ trong phương pháp này lại tác động đến nhiều phân vùng, khiến phương pháp này tiêu tốn nhiều tài nguyên ghi (write-intensive) và trở nên phức tạp.

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p043_00.png)

#### Phân vùng chỉ mục phụ theo thuật ngữ (Partitioning secondary indexes by term)
- **Partition 0**
- **Partition 1**
- **Partition 2**

*Get cust_id where cust_name = "John"*

- **Index 0**: Chứa các tên bắt đầu từ A–M (*Contains names starting from A-M*)
- **Index 1**: Chứa các tên bắt đầu từ N–Z (*Contains names starting from N-Z*)

*Get cust_id where cust_name = "John"*  
*Get cust_id where cust_name = "John"*  

![009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](images/topic_009_p043_01.png)

---

### Định tuyến yêu cầu (Request routing)

Chúng ta đã học cách phân vùng dữ liệu của mình. Tuy nhiên, một câu hỏi được đặt ra ở đây:
Làm thế nào để một client biết được cần kết nối tới nút (node) nào khi thực hiện một yêu cầu? Việc phân bổ các phân vùng cho các nút sẽ thay đổi sau quá trình tái cân bằng (rebalancing). Nếu chúng ta muốn đọc một khóa cụ thể (specific key), làm thế nào để chúng ta biết được địa chỉ IP nào cần kết nối để đọc?

---

### Trang 44

Vấn đề này còn được gọi là **phát hiện dịch vụ (service discovery)**. Dưới đây là một vài phương pháp tiếp cận cho vấn đề này:

1. **Cho phép các client gửi yêu cầu tới bất kỳ nút nào trong mạng lưới (network).** Nếu nút đó không chứa dữ liệu được yêu cầu, nó sẽ chuyển tiếp (forward) yêu cầu đó đến nút có chứa dữ liệu liên quan.
2. **Phương pháp thứ hai bao gồm một tầng định tuyến (routing tier).** Tất cả các yêu cầu trước tiên đều được chuyển tiếp đến tầng định tuyến, và tầng này sẽ xác định nút nào cần kết nối để thực hiện yêu cầu.
3. **Các client đã có sẵn thông tin liên quan đến việc phân vùng và phân vùng nào được kết nối với nút nào.** Do đó, chúng có thể trực tiếp liên hệ với nút chứa dữ liệu mà chúng cần.

Trong tất cả các phương pháp này, thách thức cốt lõi là làm thế nào để các thành phần này nắm bắt được các cập nhật trong việc phân vùng của các nút.

#### ZooKeeper
Để theo dõi các thay đổi trong cụm (cluster), nhiều hệ thống dữ liệu phân tán cần một máy chủ quản lý riêng biệt như **ZooKeeper**. ZooKeeper theo dõi tất cả các ánh xạ (mappings) trong mạng lưới, và mỗi nút đều kết nối tới ZooKeeper để lấy thông tin. Bất cứ khi nào có thay đổi trong việc phân vùng, hoặc khi một nút được thêm vào hay gỡ bỏ, ZooKeeper sẽ được cập nhật và thông báo cho tầng định tuyến (routing tier) về sự thay đổi đó. HBase, Kafka và SolrCloud đều sử dụng ZooKeeper.

#### Kết luận (Conclusion)
Đối với tất cả các hệ thống phân tán hiện nay, phân vùng (partitioning) đã trở thành giao thức tiêu chuẩn. Bởi vì các hệ thống ngày càng chứa lượng dữ liệu khổng lồ, việc phân vùng dữ liệu là điều hoàn toàn hợp lý vì nó giúp tăng tốc cả tác vụ đọc lẫn ghi. Nó giúp gia tăng **tính sẵn sàng (High Availability)**, **khả năng mở rộng (Scalability)**, và **hiệu năng (Performance)** của hệ thống.

---

### Trang 45

*Back*  
**Nhân bản dữ liệu (Data Replication)**  
*Mark As Completed*  
*Next*  
**Các đánh đổi trong Cơ sở dữ liệu (Trade-offs in Databases)**  

---

### Trang 46

# Các đánh đổi trong Cơ sở dữ liệu (Trade-offs in Databases)

Tìm hiểu khi nào nên sử dụng phân mảnh ngang (horizontal sharding) thay vì phân mảnh dọc (vertical sharding) và ngược lại.

### Chúng ta sẽ tìm hiểu các nội dung sau:
- Phương pháp phân mảnh cơ sở dữ liệu nào là tốt nhất?
- Ưu điểm và nhược điểm của cơ sở dữ liệu tập trung (centralized database)
  - Ưu điểm
  - Nhược điểm
- Ưu điểm và nhược điểm của cơ sở dữ liệu phân tán (distributed database)
  - Ưu điểm
  - Nhược điểm
- Tối ưu hóa truy vấn và tốc độ xử lý trong cơ sở dữ liệu phân tán
  - Giả định các tham số
  - Các phương pháp tiếp cận khả thi
- Kết luận

---

### Phương pháp phân mảnh cơ sở dữ liệu nào là tốt nhất? (Which is the best database sharding approach?)

Cả phân mảnh ngang (horizontal sharding) và phân mảnh dọc (vertical sharding) đều liên quan đến việc bổ sung tài nguyên vào hạ tầng tính toán của chúng ta. Các bên liên quan về mặt nghiệp vụ (business stakeholders) phải quyết định phương pháp nào là phù hợp cho tổ chức. Chúng ta phải mở rộng tài nguyên của mình một cách tương ứng để tổ chức và hoạt động kinh doanh phát triển, ngăn ngừa thời gian chết (downtime), và giảm **độ trễ (Latency)**.

Chúng ta có thể mở rộng các tài nguyên này thông qua sự kết hợp của việc điều chỉnh CPU, yêu cầu bộ nhớ vật lý (physical memory), điều chỉnh ổ đĩa cứng (hard disk), và **băng thông mạng (network bandwidth)**.

Các phần tiếp theo sẽ giải thích các ưu và nhược điểm của việc không phân mảnh (no sharding) so với có phân mảnh (sharding).

---

### Ưu điểm và nhược điểm của cơ sở dữ liệu tập trung (Advantages and disadvantages of a centralized database)

---

### Trang 47

#### Ưu điểm (Advantages)
- Việc bảo trì dữ liệu, chẳng hạn như cập nhật và sao lưu (backups) của một cơ sở dữ liệu tập trung, là rất dễ dàng.
- Cơ sở dữ liệu tập trung cung cấp **tính nhất quán mạnh mẽ hơn (stronger consistency)** và các giao dịch **ACID** tốt hơn so với cơ sở dữ liệu phân tán.
- Cơ sở dữ liệu tập trung cung cấp mô hình lập trình đơn giản hơn nhiều cho các lập trình viên ứng dụng cuối so với cơ sở dữ liệu phân tán.
- Doanh nghiệp sẽ hiệu quả hơn khi chỉ có một lượng dữ liệu nhỏ cần lưu trữ, vốn có thể nằm trọn vẹn trên một nút duy nhất (single node).

#### Nhược điểm (Disadvantages)
- Cơ sở dữ liệu tập trung có thể bị chậm lại, gây ra **độ trễ cao (high latency)** cho người dùng cuối, khi số lượng truy vấn mỗi giây (queries per second - QPS) truy cập vào cơ sở dữ liệu tập trung tiệm cận đến giới hạn của một nút đơn lẻ.
- Cơ sở dữ liệu tập trung có **điểm lỗi đơn lẻ (Single Point of Failure - SPOF)**. Do đó, xác suất hệ thống không thể truy cập được (unavailability) là cao hơn rất nhiều.

---

### Ưu điểm và nhược điểm của cơ sở dữ liệu phân tán (Advantages and disadvantages of a distributed database)

#### Ưu điểm (Advantages)
- Việc truy cập dữ liệu trong cơ sở dữ liệu phân tán rất nhanh và dễ dàng vì dữ liệu được truy xuất từ phân mảnh cơ sở dữ liệu (database shard) gần nhất hoặc phân mảnh thường xuyên được sử dụng.
- Dữ liệu với các mức độ minh bạch phân tán khác nhau (distribution transparency) có thể được lưu trữ ở các vị trí tách biệt.
- Các giao dịch tải cao bao gồm nhiều truy vấn có thể được chia thành nhiều truy vấn con (subqueries) đã được tối ưu hóa, có thể được xử lý theo cách thức **song song (parallel fashion)**.

#### Nhược điểm (Disadvantages)
- Đôi khi, dữ liệu cần được lấy từ nhiều địa điểm (multiple sites), dẫn đến việc tiêu tốn nhiều thời gian hơn dự kiến.
- Các quan hệ (relations/tables) được phân vùng theo chiều dọc hoặc chiều ngang giữa các nút khác nhau. Do đó, các thao tác như phép nối (**joins**) cần phải tái tạo lại các quan hệ hoàn chỉnh bằng cách tìm nạp dữ liệu một cách cẩn thận. Những thao tác này có thể trở nên

---

### Trang 48

tốn kém (expensive) và phức tạp hơn rất nhiều.
- Rất khó để duy trì **tính nhất quán của dữ liệu (data consistency)** giữa các địa điểm (sites) trong cơ sở dữ liệu phân tán, và điều này đòi hỏi các biện pháp bổ sung phức tạp.
- Các hoạt động cập nhật và sao lưu trong cơ sở dữ liệu phân tán cần nhiều thời gian để đồng bộ hóa dữ liệu (synchronize data).

---

### Tối ưu hóa truy vấn và tốc độ xử lý trong cơ sở dữ liệu phân tán (Query optimization and processing speed in a distributed database)

Một giao dịch trong cơ sở dữ liệu phân tán phụ thuộc vào loại truy vấn, số lượng địa điểm/phân mảnh (sites/shards) liên quan, tốc độ giao tiếp mạng, và các yếu tố khác như phần cứng bên dưới cùng loại cơ sở dữ liệu được sử dụng. Tuy nhiên, như một ví dụ cụ thể, hãy giả sử một truy vấn truy cập vào ba bảng: `Store`, `Product`, và `Sales`, nằm trên các địa điểm (sites) khác nhau.

Số lượng thuộc tính (attributes) trong mỗi bảng được đưa ra trong hình sau:

#### Lược đồ cơ sở dữ liệu gồm ba bảng: Store, Product, và Sales (Database schema consisting of three tables: Store, Product, and Sales)

##### Bảng Store (Store)
| Store_key | City | Region |
| :--- | :--- | :--- |
| 1 | New York | East |
| 2 | San Francisco | West |
| 3 | Atlanta | East |
| 5 | Chicago | Central |
| 4 | Los Angeles | West |

##### Bảng Product (Product)
| Product_key | Description | Brand |
| :--- | :--- | :--- |
| 1 | Toy Story | Wolf |
| 2 | The Hobbit | Warner Bros. |
| 4 | The Juror | MKF Studio |
| 5 | Jurassic Park | Universal Picture |
| 3 | The Batman | Warner Bros. |

##### Bảng Sales (Sales)
| Store_key | Product_key | Sales | Cost | Profit |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1 | 4.76 | 1.5 | 3.26 |
| 2 | 2 | 14.24 | 7.2 | 7.04 |
| 3 | 4 | 7.79 | 1.76 | 7.03 |
| 5 | 5 | 3.6 | 2.45 | 1.15 |
| 4 | 3 | 4.4 | 3.23 | 1.17 |

- Bảng `Store`: Lưu trữ tại địa điểm A (**Stored at site A**)
- Bảng `Product`: Lưu trữ tại địa điểm B (**Stored at site B**)
- Bảng `Sales`: Lưu trữ tại địa điểm A (**Stored at site A**)

Hãy giả sử sự phân bổ của cả hai bảng trên các địa điểm khác nhau như sau:

---

# Tối Ưu Hóa Truy Vấn Trong Cơ Sở Dữ Liệu Phân Tán (Distributed Query Optimization)

---

### Phân Bố Dữ Liệu Ban Đầu Tại Các Site

Bảng **Store** có $10.000$ bộ dữ liệu (tuples / bản ghi) được lưu trữ tại **site A**.  
Bảng **Product** có $100.000$ bộ dữ liệu được lưu trữ tại **site B**.  
Bảng **Sales** có $1.000.000$ (một triệu) bộ dữ liệu được lưu trữ tại **site A**.  

Hiện tại, giả sử chúng ta cần xử lý câu truy vấn (query) sau:

```sql
SELECT Store_key 
FROM (Store JOIN Sales JOIN Product)
WHERE Region = 'East' AND Brand = 'Wolf';
```

Truy vấn trên thực hiện các phép nối (**JOIN operations**) trên các bảng **Store**, **Sales** và **Product**, sau đó trích xuất các giá trị `Store_key` từ bảng kết quả sinh ra sau các phép nối.

Tiếp theo, giả định mỗi bộ dữ liệu (tuple) được lưu trữ có độ dài là **$200$ bits** (tương đương với **$25$ Bytes**).

Hơn nữa, số lượng bản ghi ước tính (**estimated cardinalities**) của một số kết quả trung gian như sau:
* Số lượng sản phẩm thuộc thương hiệu **Wolf** là **$10$**.
* Số lượng cửa hàng thuộc khu vực miền Đông (**East region stores**) là **$3.000$** (vì có tổng cộng $10.000$ dòng trong bảng `Store`, và $3.000$ dòng có khu vực là `East`).

---

### Giả Định Về Mạng Truyền Thông (Communication Assumptions)

* **Tốc độ truyền dữ liệu (Data rate)**: $50\text{ Mbits/giây (50M bits per second)}$
* **Độ trễ truy cập (Access delay)**: $0{,}1\text{ giây (0.1 second)}$

#### Giả định các tham số (Parameters assumption)
Trước khi xử lý truy vấn bằng các cách tiếp cận khác nhau, hãy định nghĩa một số tham số:
* $a$: Tổng độ trễ truy cập (**Total access delay**)
* $b$: Tốc độ truyền dữ liệu (**Data rate**)
* $v$: Tổng khối lượng dữ liệu truyền tải (**Total data volume**)

Bây giờ, hãy tính tổng thời gian truyền thông (**total communication time**), ký hiệu là $T$, theo công thức sau:

$$T = a + \frac{v}{b}$$

---

### Các Cách Tiếp Cận Khả Thi (Possible Approaches)

Hãy thử các cách tiếp cận khả thi sau để thực thi truy vấn:

#### Cách 1: Di chuyển bảng Product sang site A và xử lý truy vấn tại A
*(Move the Product table to site A and process the query at A)*

$$T = 0{,}1 + \frac{100.000 \times 200}{50.000.000} = 0{,}5\text{ giây}$$

> [!NOTE]
> Ở đây, $0{,}1$ là độ trễ truy cập (**access delay**) của bảng tại site A, và $100.000$ là số lượng bộ dữ liệu trong bảng `Product`. Kích thước của mỗi bộ dữ liệu tính theo bit là $200$, và $50.000.000$ là tốc độ truyền dữ liệu (**data rate**). Các con số $200$ và $50.000.000$ này hoàn toàn giống nhau cho tất cả các phép tính tiếp theo dưới đây.

---

#### Cách 2: Di chuyển bảng Store và Sales sang site B và xử lý truy vấn tại B
*(Move Store and Sales to site B and process the query at B)*

$$T = 0{,}2 + \frac{(10.000 + 1.000.000) \times 200}{50.000.000} = 4{,}24\text{ giây}$$

> [!NOTE]
> Ở đây, $0{,}2$ là độ trễ truy cập (**access delay**) của hai bảng `Store` và `Sales` (mỗi bảng $0{,}1$ giây). Các con số $10.000$ và $1.000.000$ lần lượt là số lượng bộ dữ liệu trong bảng `Store` và bảng `Sales`.

---

#### Cách 3: Lọc điều kiện Brand tại site B thành 'Wolf' (gọi là phép chọn - selection) và di chuyển kết quả sang site A
*(Restrict Brand at site B to Wolf (called selection) and move the result to site A)*

$$T = 0{,}1 + \frac{10 \times 200}{50.000.000} \approx 0{,}1\text{ giây}$$

> [!NOTE]
> Ở đây, $0{,}1$ là độ trễ truy cập (**access delay**) của bảng `Product`. Số lượng bản ghi mang thương hiệu **Wolf** là $10$, do đó số lượng bộ dữ liệu truyền đi chỉ là $10$.

---

### So Sánh Và Đánh Giá

Khi so sánh cả ba cách tiếp cận:
* Cách tiếp cận thứ ba mang lại cho chúng ta **độ trễ thấp nhất (least latency: $\approx 0{,}1$ giây)**.
* Chúng ta đã không tính toán phương án lọc tại site A vì số lượng dòng sẽ lớn hơn rất nhiều, và do đó khối lượng dữ liệu (**data volume**) sẽ lớn hơn so với trường hợp thứ ba (lọc tại site B trước rồi mới nạp/truy xuất dữ liệu về).

> [!IMPORTANT]
> Ví dụ thực tế này chứng minh rằng việc **tối ưu hóa truy vấn cẩn trọng (careful query optimization)** đóng vai trò tối quan trọng trong cơ sở dữ liệu phân tán (**Distributed Database**).

---

### Kết Luận (Conclusion)

Việc phân phối dữ liệu (**Data distribution** bao gồm phân mảnh dọc - **Vertical Sharding** và phân mảnh ngang - **Horizontal Sharding**) qua nhiều node nhằm mục đích cải thiện các đặc tính sau, với điều kiện tiên quyết là các truy vấn phải được tối ưu hóa:

* **Độ tin cậy / Khả năng chịu lỗi (Reliability / Fault-Tolerance)**
* **Hiệu năng (Performance)**
* **Cân bằng dung lượng lưu trữ và chi phí tài chính (Balanced storage capacity and dollar costs)**

Cả hai mô hình cơ sở dữ liệu tập trung (**Centralized Databases**) và cơ sở dữ liệu phân tán (**Distributed Databases**) đều có những ưu điểm và nhược điểm riêng. Chúng ta nên lựa chọn giải pháp phù hợp tùy theo các yêu cầu cụ thể của ứng dụng.

---

> **Điều hướng tài liệu:**  
> [⬅️ Quay lại: Phân vùng dữ liệu (Data Partitioning)] | [Đánh dấu hoàn thành (Mark As Completed)] | [Tiếp theo: Thiết kế hệ thống: Kho lưu trữ Key-Value (System Design: The Key-value Store) ➡️]


---

[← Bài trước](008-can-bang-tai-load-balancers.md) | [Mục lục](README.md) | [Bài tiếp theo →](010-luu-tru-key-value-store.md)
