# 003 - Các Tầng Trừu Tượng Trong Hệ Thống (Abstractions)

[← Bài trước](002-phong-van-system-design.md) | [Mục lục](README.md) | [Bài tiếp theo →](004-dac-tinh-phi-chuc-nang.md)

---


# Tại sao các tầng trừu tượng (Abstractions) lại quan trọng?
*(Why Are Abstractions Important?)*

Khám phá tầm quan trọng của tính trừu tượng (abstraction).

**Chúng ta sẽ tìm hiểu các nội dung sau:**
* Trừu tượng hóa (Abstraction) là gì?
* Trừu tượng hóa cơ sở dữ liệu (Database abstraction)
* Trừu tượng hóa trong các hệ thống phân tán (Abstractions in distributed systems)

---

## Trừu tượng hóa (Abstraction) là gì?
*(What is abstraction?)*

**Trừu tượng hóa (Abstraction)** là nghệ thuật che giấu/lược bỏ các chi tiết không cần thiết. Nó cho phép chúng ta tập trung vào bức tranh tổng thể (big picture). Việc nhìn nhận bức tranh tổng thể mang tính sống còn vì nó ẩn đi các độ phức tạp nội tại bên trong, từ đó mang lại cho chúng ta sự hiểu biết rộng hơn về các mục tiêu đã đề ra và duy trì sự tập trung vào các mục tiêu đó. Hình minh họa sau đây là một ví dụ về tính trừu tượng.

![003 - Các Tầng Trừu Tượng Trong Hệ Thống (Abstractions)](images/topic_003_p001_00.png)
*Trừu tượng hóa về một loài chim (Abstraction of a bird)*

Với sự trừu tượng hóa được thể hiện ở trên, chúng ta có thể nói về các loài chim nói chung mà không bị sa lầy vào các chi tiết cụ thể.

> [!NOTE]
> **Ghi chú:** Nếu chúng ta vẽ bức tranh về một con chim cụ thể hoặc các đặc điểm riêng biệt của nó, chúng ta sẽ không đạt được mục tiêu nhận diện mọi loài chim. Khi đó, chúng ta chỉ học được cách nhận diện duy nhất một loại chim cụ thể đó mà thôi.

---

Trong bối cảnh khoa học máy tính, tất cả chúng ta đều sử dụng máy tính cho công việc của mình, nhưng chúng ta không bắt đầu bằng việc chế tạo phần cứng từ con số không (scratch) rồi phát triển một hệ điều hành. Chúng ta sử dụng máy tính cho mục đích hiện tại thay vì đào sâu vào việc xây dựng toàn bộ hệ thống từ đầu.

Các kỹ sư phần mềm (developers) sử dụng rất nhiều thư viện (libraries) để phát triển các hệ thống lớn. Nếu họ phải tự tay xây dựng các thư viện đó, họ sẽ không thể hoàn thành công việc của mình. Các thư viện cung cấp cho chúng ta một giao diện (interface) trực quan, tiện lợi để sử dụng các hàm (functions) và che giấu các chi tiết cài đặt bên trong về cách chúng hoạt động. Một sự trừu tượng hóa tốt cho phép chúng ta tái sử dụng nó trên nhiều dự án khác nhau có cùng nhu cầu tương tự.

---

## Trừu tượng hóa cơ sở dữ liệu
*(Database abstraction)*

**Transactions (Giao dịch)** là một tầng trừu tượng của cơ sở dữ liệu (database abstraction) giúp che giấu đi rất nhiều hệ quả bất lợi khi có nhiều người dùng đồng thời (concurrent users) cùng đọc, ghi, hoặc thay đổi trạng thái dữ liệu (mutating data). Nó cung cấp một giao diện đơn giản gồm lệnh `commit` (trong trường hợp thành công) hoặc `abort` / `rollback` (trong trường hợp thất bại). Dù bằng cách nào, dữ liệu cũng được chuyển dịch một cách an toàn từ một trạng thái nhất quán (consistent state) này sang một trạng thái nhất quán mới. 

Transaction cho phép người dùng cuối (end users) cũng như lập trình viên không bị sa lầy vào các trường hợp biên tinh vi (subtle corner-cases) của việc biến đổi dữ liệu đồng thời, mà thay vào đó tập trung trọn vẹn vào logic nghiệp vụ (business logic) của họ.

---

## Trừu tượng hóa trong các hệ thống phân tán
*(Abstractions in distributed systems)*

Các tầng trừu tượng trong hệ thống phân tán giúp các kỹ sư đơn giản hóa công việc và giải phóng họ khỏi gánh nặng phải trực tiếp xử lý các độ phức tạp tiềm ẩn bên dưới của các hệ thống phân tán (underlying complexity of distributed systems).

Khái niệm trừu tượng hóa hệ thống phân tán ngày càng trở nên phổ biến khi nhiều tập đoàn công nghệ lớn như Amazon AWS, Google Cloud, và Microsoft Azure cung cấp các dịch vụ phân tán (distributed services). Mỗi dịch vụ lại cung cấp các cấp độ cam kết dịch vụ (Service Level Agreements - SLA) khác nhau. Toàn bộ chi tiết kỹ thuật chuyên sâu đằng sau việc hiện thực hóa các dịch vụ phân tán này đều được che giấu hoàn toàn khỏi người dùng, nhờ đó cho phép các kỹ sư tập trung vào tầng ứng dụng thay vì phải đào sâu vào bản chất của các hệ thống phân tán vốn dĩ rất phức tạp.

Các ứng dụng ngày nay không thể duy trì tính phản hồi nhanh/hoạt động ổn định (responsive/functional) nếu chúng chỉ dựa trên một node đơn lẻ (single node) do số lượng người dùng đang tăng trưởng theo cấp số nhân. Các tầng trừu tượng trong hệ thống phân tán giúp các kỹ sư chuyển đổi sang kiến trúc phân tán một cách nhanh chóng nhằm mở rộng quy mô (scale) ứng dụng của họ.

> [!NOTE]
> **Ghi chú:** Chúng ta sẽ thấy việc ứng dụng các tầng trừu tượng trong giao tiếp mạng (communications), tính nhất quán của dữ liệu (data consistency), và xử lý lỗi hệ thống (failures) xuyên suốt chương này. Mục đích là để truyền tải các tư tưởng cốt lõi, chứ không nhất thiết phải đi vào toàn bộ các chi tiết vi mô, phức tạp của từng khái niệm.

---

# Các tầng trừu tượng trong mạng: Gọi thủ tục từ xa (RPC - Remote Procedure Calls)
*(Network Abstractions: Remote Procedure Calls)*

Tìm hiểu sâu về khái niệm gọi thủ tục từ xa (RPC) và cách chúng hỗ trợ các nhà phát triển phần mềm.

**Chúng ta sẽ tìm hiểu các nội dung sau:**
* RPC là gì? (What is an RPC?)
* RPC hoạt động như thế nào? (How does RPC work?)
* Tóm tắt (Summary)

**Gọi thủ tục từ xa (Remote Procedure Calls - RPC)** cung cấp một tầng trừu tượng mô phỏng một lời gọi hàm cục bộ (local procedure call) cho các nhà phát triển bằng cách che giấu toàn bộ sự phức tạp của việc đóng gói (packing/marshaling) và truyền tải các tham số hàm qua môi trường mạng tới máy chủ từ xa (remote server), nhận kết quả trả về, cũng như quản lý các cơ chế thử lại mạng (network retries).

---

## RPC là gì?
*(What is an RPC?)*

RPC là một giao thức truyền thông liên tiến trình (Inter-Process Communication - IPC) được sử dụng rộng rãi trong các hệ thống phân tán. Trong mô hình tham chiếu mạng OSI (OSI model), RPC trải dài trên cả tầng giao vận (Transport layer) và tầng ứng dụng (Application layer).

Cơ chế RPC được áp dụng khi một chương trình máy tính kích hoạt thực thi một thủ tục (procedure) hoặc chương trình con (subroutine) bên trong một không gian địa chỉ riêng biệt (separate address space) trên một máy tính khác.

> [!NOTE]
> **Ghi chú:** Thủ tục hoặc chương trình con được viết mã y hệt như một lời gọi hàm cục bộ/thông thường (regular/local procedure call) mà lập trình viên không cần phải viết mã tường minh cho các chi tiết tương tác mạng từ xa.

---

## RPC hoạt động như thế nào?
*(How does RPC work?)*

Khi chúng ta thực hiện một lời gọi thủ tục từ xa:
1. Môi trường của bên gọi (calling environment) sẽ tạm dừng (pause/block).
2. Các tham số của thủ tục được truyền tải qua mạng tới môi trường nơi thủ tục đó sẽ được thực thi.
3. Khi việc thực thi thủ tục hoàn tất, kết quả được trả ngược về môi trường gọi, nơi quá trình thực thi tiếp tục chạy tiếp tục như một lời gọi hàm thông thường.

Để hiểu rõ cơ chế hoạt động, chúng ta hãy xem xét ví dụ về một chương trình Client - Server. Có **5 thành phần chính** tham gia vào hệ thống RPC:

* **Client** (Máy khách / Tiến trình gọi)
* **Client stub** (Cuống mã phía Client - đóng vai trò proxy đại diện cục bộ)
* **Server** (Máy chủ / Tiến trình thực thi)
* **Server stub** (Cuống mã phía Server - đóng vai trò bộ phân giải và điều phối cục bộ)
* **RPC runtime** (Môi trường thực thi RPC / Tầng hạ tầng RPC)

Client, Client stub và một thực thể (instance) của RPC runtime chạy trên máy Client. Server, Server stub và một thực thể của RPC runtime chạy trên máy Server.

---

### Quy trình các bước thực thi trong RPC:

1. **Client** khởi tạo tiến trình **Client stub** bằng cách truyền vào các tham số như một lời gọi hàm thông thường. Client stub được lưu trữ trong không gian địa chỉ của Client.
2. **Client stub** chuyển đổi các tham số sang một định dạng chuẩn hóa (serialization/marshaling) và đóng gói chúng thành một thông điệp (message). Sau khi đóng gói tham số, Client stub yêu cầu tầng **RPC runtime** cục bộ chuyển giao thông điệp này tới Server.
3. **RPC runtime** tại phía Client chuyển phát thông điệp tới Server thông qua kết nối mạng. Sau khi gửi thông điệp tới Server, nó chuyển sang trạng thái chờ nhận kết quả phản hồi từ Server.
4. **RPC runtime** tại phía Server tiếp nhận thông điệp qua mạng và chuyển tiếp nó cho **Server stub**.

> [!NOTE]
> **Ghi chú:** **RPC runtime** chịu trách nhiệm truyền tải các thông điệp giữa Client và Server qua môi trường mạng. Trách nhiệm của RPC runtime cũng bao gồm việc tự động truyền lại gói tin khi có lỗi (retransmission), gửi thông báo xác nhận nhận tin (acknowledgment - ACK), và mã hóa dữ liệu (encryption).

5. **Server stub** giải nén (unpacks/unmarshals) thông điệp, trích xuất các tham số ra khỏi gói tin, và gọi hàm/thủ tục mong muốn trên Server bằng một lời gọi hàm cục bộ (local procedure call) để thực hiện tác vụ được yêu cầu.

---

### Sơ đồ luồng hoạt động của RPC (The workflow of an RPC):

```
+---------------------------------------------------------------------------------------------------+
| CLIENT MACHINE                                                    SERVER MACHINE                  |
|                                                                                                   |
|  [ Client ]                                                        [ Server ]                     |
|      |                                                                 ^                          |
|    1 | Call                                                          5 | Call                     |
|      v                                                                 |                          |
|  [ Client stub ] (Pack / Unpack)                                   [ Server stub ] (Unpack / Pack)|
|      |                                                                 ^                          |
|    2 | Send                                                          4 | Receive                  |
|      v                                                                 |                          |
|  [ RPC runtime ]                                                   [ RPC runtime ]                |
|      |                                                                 ^                          |
|    3 | ---- Call packet (qua mạng) ----------------------------------> |                          |
|      |                                                                                            |
|      | <--- Result packet (qua mạng) --------------------------------- |                          |
|      v                                                                 |                          |
|  [ RPC runtime ]                                                   [ RPC runtime ]                |
|      |                                                                 ^                          |
|    9 | Receive                                                       7 | Send                     |
|      v                                                                 |                          |
|  [ Client stub ]                                                   [ Server stub ]                |
|      |                                                                 ^                          |
|   10 | Return                                                        6 | Return                   |
|      v                                                                 |                          |
|  [ Client ]                                                        [ Server ]                     |
+---------------------------------------------------------------------------------------------------+
```

*Các bước tuần tự từ 1 đến 10:*
* **(1)** Client gọi Client stub (`Call`).
* **(2)** Client stub đóng gói (`Pack`) và yêu cầu RPC runtime gửi đi (`Send`).
* **(3)** Client RPC runtime gửi gói tin cuộc gọi (`Call packet`) qua mạng sang Server và chuyển sang trạng thái chờ (`Wait`).
* **(4)** Server RPC runtime nhận gói tin (`Receive`) và chuyển tiếp cho Server stub.
* **(5)** Server stub giải nén gói tin (`Unpack`) và gọi hàm thực thi (`Execute`) trên Server code.
* **(6)** Sau khi hàm trên Server hoàn tất với các tham số đầu vào, kết quả được trả về (`Return`) cho Server stub.
* **(7)** Server stub đóng gói kết quả (`Pack`) thành một thông điệp và gửi nó (`Send`) tới tầng RPC runtime của Server tại tầng giao vận (Transport layer).
* **(8)** RPC runtime của Server truyền gói tin kết quả (`Result packet`) trở lại cho RPC runtime của Client qua mạng.
* **(9)** RPC runtime phía Client nhận gói tin (`Receive`), giao cho Client stub giải nén (`Unpack`).
* **(10)** Client stub trả kết quả (`Return`) về cho mã nguồn Client tiếp tục thực thi.

---

### --- Trang 7 ---

[Quay lại (Back)]  
**Tại Sao Các Tầng Trừu Tượng Lại Quan Trọng? (Why Are Abstractions Important?)**  
[Đánh dấu đã hoàn thành (Mark As Completed)]  
[Tiếp theo (Next)]  
**Phổ Mô Hình Nhất Quán (Spectrum of Consistency Models)**  

... runtime thông qua mạng (network).  
9. **RPC runtime** phía client đang chờ kết quả sẽ tiếp nhận kết quả và chuyển tới **client stub**.  
10. **Client stub** giải nén (unpack/deserialize) kết quả, và tại thời điểm này tiến trình thực thi sẽ trả về cho phía gọi (caller).  

> [!NOTE]
> Các dịch vụ phía back-end (Back-end services) sử dụng **RPC (Remote Procedure Call)** làm cơ chế giao tiếp ưu tiên hàng đầu nhờ vào hiệu năng cao (**High Performance**) và tầng trừu tượng đơn giản: gọi mã nguồn từ xa (remote code) như gọi các hàm cục bộ (local functions).

#### Tóm tắt (Summary)
Phương thức **RPC** tương tự như việc gọi một thủ tục cục bộ (local procedure), ngoại trừ việc thủ tục được gọi thường được thực thi trong một tiến trình khác và trên một máy tính khác.

RPC cho phép các kỹ sư phát triển xây dựng các ứng dụng trên nền tảng của các hệ thống phân tán (**Distributed Systems**). Các nhà phát triển có thể sử dụng phương thức RPC mà không cần phải nắm rõ chi tiết về giao tiếp mạng (**Network Communication**). Nhờ đó, họ có thể tập trung vào các khía cạnh thiết kế hệ thống thay vì các chi tiết đặc thù ở tầng máy móc và tầng truyền thông mạng.

---

### --- Trang 8 ---

## Phổ Các Mô Hình Nhất Quán (Spectrum of Consistency Models)

Tìm hiểu về các mô hình nhất quán (**Consistency Models**) và xác định xem mô hình nào phù hợp với các yêu cầu của ứng dụng chúng ta.

**Chúng ta sẽ bao quát các nội dung sau:**
* Tính nhất quán là gì? (What is consistency?)
* Tính nhất quán cuối cùng (Eventual consistency)
* Tính nhất quán nhân quả (Causal consistency)
* Tính nhất quán tuần tự (Sequential consistency)
* Tính nhất quán nghiêm ngặt hay tuyến tính hóa (Strict consistency aka linearizability)
* Tóm tắt (Summary)

### Tính nhất quán là gì? (What is consistency?)
Trong các hệ thống phân tán (**Distributed Systems**), tính nhất quán (**Consistency**) có thể mang nhiều tầng ý nghĩa:
* Một là: Mỗi nút bản sao (**Replica Node**) đều có cùng một góc nhìn dữ liệu (same view of data) tại một thời điểm nhất định.
* Hai là: Mỗi yêu cầu đọc (**Read Request**) đều nhận được giá trị của lần ghi gần nhất (**Recent Write**).

Đây không phải là những định nghĩa duy nhất về tính nhất quán, bởi vì có rất nhiều biến thể/hình thái nhất quán khác nhau. Thông thường, các mô hình nhất quán cung cấp cho chúng ta các tầng trừu tượng (**Abstractions**) để lập luận và đánh giá về tính đúng đắn (**Correctness**) của một hệ thống phân tán khi thực hiện đồng thời các thao tác đọc dữ liệu (**Reads**), ghi dữ liệu (**Writes**), và đột biến dữ liệu (**Mutations**).

Nếu chúng ta phải thiết kế hoặc xây dựng một ứng dụng cần đến hệ thống lưu trữ của bên thứ ba như S3 hoặc Cassandra, chúng ta có thể xem xét các bảo đảm về tính nhất quán (**Consistency Guarantees**) được cung cấp bởi S3 để quyết định xem có nên sử dụng nó hay không. Hãy cùng khám phá các loại tính nhất quán khác nhau.

**Hai đầu cực của phổ nhất quán (Spectrum of Consistency) là:**
* Nhất quán mạnh nhất (**Strongest consistency**)
* Nhất quán yếu nhất (**Weakest consistency**)

---

### --- Trang 9 ---

Có các mô hình nhất quán nằm giữa hai đầu cực này, một số trong đó được thể hiện qua minh họa sau:

*Đây là phổ của các mô hình nhất quán. Các bảo đảm nhất quán (Consistency guarantees) sẽ trở nên mạnh dần khi chúng ta di chuyển sang bên phải.*

| Yếu nhất (Weakest) $\longrightarrow$ Mạnh nhất (Strongest) |
| :--- |
| **Mô hình nhất quán yếu nhất (Weakest consistency model):** Nhất quán cuối cùng (**Eventual consistency**) |
| $\downarrow$ |
| Nhất quán nhân quả (**Causal consistency**) |
| $\downarrow$ |
| Nhất quán tuần tự (**Sequential consistency**) |
| $\downarrow$ |
| **Mô hình nhất quán mạnh nhất (Strongest consistency model):** Nhất quán nghiêm ngặt / Tuyến tính hóa (**Strict consistency / Linearizability**) |

> [!IMPORTANT]
> **Sự khác biệt giữa Tính nhất quán trong ACID và Tính nhất quán trong Định lý CAP:**
> * **Quy tắc cơ sở dữ liệu là trọng tâm của Tính nhất quán trong ACID (ACID Consistency):** Nếu một lược đồ cơ sở dữ liệu (**Schema**) chỉ định rằng một giá trị phải là duy nhất (**Unique**), một hệ thống nhất quán sẽ đảm bảo giá trị đó là duy nhất xuyên suốt mọi thao tác. Nếu một khóa ngoại (**Foreign Key**) chỉ định rằng việc xóa một hàng cũng sẽ xóa các hàng liên quan, một hệ thống nhất quán đảm bảo rằng trạng thái không thể chứa các hàng liên quan một khi hàng gốc đã bị hủy bỏ.
> * **Tính nhất quán trong CAP (CAP Consistency):** Đảm bảo rằng trong một hệ thống phân tán, mọi bản sao (**Replica**) của cùng một giá trị logic đều có cùng một giá trị chính xác tại mọi thời điểm. Cần lưu ý rằng đây là một **bảo đảm ở mức logic (Logical Guarantee)** thay vì ở mức vật lý (Physical Guarantee). Do giới hạn vận tốc ánh sáng, việc sao chép các con số/dữ liệu xuyên suốt một cụm (**Cluster**) có thể mất một khoảng thời gian nhất định (**Replication Lag**). Bằng cách ngăn chặn các client truy cập vào các giá trị khác nhau ở các nút riêng biệt, cụm hệ thống vẫn có thể cung cấp một bức tranh toàn cảnh nhất quán về mặt logic.

### Tính nhất quán cuối cùng (Eventual consistency)
**Nhất quán cuối cùng (Eventual consistency)** là mô hình nhất quán yếu nhất. Các ứng dụng không có yêu cầu khắt khe về thứ tự thực thi (**Ordering Requirements**) và không bắt buộc các thao tác đọc phải trả về giá trị của lần ghi mới nhất sẽ lựa chọn mô hình này. Nhất quán cuối cùng đảm bảo rằng tất cả các bản sao (**Replicas**) cuối cùng sẽ trả về cùng một giá trị cho yêu cầu đọc, nhưng giá trị được trả về

---

### --- Trang 10 ---

không có nghĩa bắt buộc phải là giá trị mới nhất ngay lập tức. Tuy nhiên, giá trị cuối cùng rồi cũng sẽ đạt đến trạng thái mới nhất của nó.

![003 - Các Tầng Trừu Tượng Trong Hệ Thống (Abstractions)](images/topic_003_p010_00.png)

* **1 of 6:**
  * Trạng thái ban đầu: $x = 2$
  * Hệ thống phân tán nhất quán cuối cùng (**Eventual consistent distributed system**).
  * Ban đầu, giá trị của $x$ là $2$.
* **2 of 6:**
  * Tại thời điểm $T1$: Alice gửi một yêu cầu ghi: `T1: write(x) = 10` để cập nhật giá trị của $x$ thành $10$.
  * Hệ thống phân tán nhất quán cuối cùng tiếp nhận yêu cầu.
* **3 of 6:**
  * $x = 2 \rightarrow 10$
  * `T1: write(x) = 10` từ Alice.
  * Hệ thống lưu trữ giá trị đã được cập nhật của $x$.

---

### --- Trang 11 ---

![003 - Các Tầng Trừu Tượng Trong Hệ Thống (Abstractions)](images/topic_003_p011_00.png)

* **4 of 6:**
  * Tại thời điểm $T2$, Alice và Bob cùng gửi yêu cầu đọc giá trị của $x$: `T2: read(x)`.
  * Hệ thống phân tán nhất quán cuối cùng xử lý các yêu cầu đọc.
* **5 of 6:**
  * Alice và Bob đọc từ một nút bản sao khác (**Different Replica**), nơi mà các giá trị vẫn chưa được cập nhật tới, do đó họ nhận về giá trị cũ (**Stale value**):
    * `Alice: T2: read(x) -> 2`
    * `Bob: T2: read(x) -> 2`
  * Hệ thống trả về cùng một giá trị cho cả hai yêu cầu đọc, nhưng giá trị này đã cũ.
* **6 of 6:**
  * Tại thời điểm $T3$, hệ thống đạt đến trạng thái ổn định (**Stable state**) và trả về giá trị mới nhất cho cả hai yêu cầu đọc:
    * `Alice: T3: read(x) -> 10`
    * `Bob: T3: read(x) -> 10`

---

### --- Trang 12 ---

Nhất quán cuối cùng (**Eventual consistency**) đảm bảo tính sẵn sàng cao (**High Availability**).

#### Ví dụ (Example)
Hệ thống phân giải tên miền (**DNS - Domain Name System**) là một hệ thống có tính sẵn sàng cao (**Highly Available System**), cho phép tra cứu tên cho hàng trăm triệu thiết bị trên toàn bộ Internet. Nó sử dụng mô hình **nhất quán cuối cùng (Eventual Consistency)** và không nhất thiết phải phản ánh các giá trị mới nhất ngay lập tức.

> [!NOTE]
> **Cassandra** là một cơ sở dữ liệu NoSQL có tính sẵn sàng cao (**Highly Available NoSQL Database**), cung cấp mô hình **nhất quán cuối cùng (Eventual Consistency)**.

---

### Tính nhất quán nhân quả (Causal consistency)
**Nhất quán nhân quả (Causal consistency)** hoạt động bằng cách phân loại các thao tác thành các thao tác phụ thuộc (**Dependent Operations**) và các thao tác độc lập (**Independent Operations**). Các thao tác phụ thuộc còn được gọi là các **thao tác có quan hệ nhân quả (Causally-related Operations)**. Mô hình nhất quán nhân quả duy trì và bảo toàn trật tự thực thi của các thao tác có quan hệ nhân quả này.

Trong minh họa sau đây, tiến trình $P1$ thực hiện ghi giá trị $a$ tại vị trí $x$ (`write(x)a`). Để tiến trình $P2$ có thể ghi giá trị $b$ tại vị trí $y$ (`write(y)b`), trước tiên nó cần phải tính toán giá trị của $b$. Vì $b = x + 5$, nên thao tác đọc trên $x$ (`read(x)a`) phải được thực hiện trước khi ghi $b$ vào vị trí $y$. Đó là lý do tại sao `read(x)a` và `write(y)b` là các thao tác có quan hệ nhân quả với nhau (**Causally related**).

```text
Trục thời gian (Time) ----------------------------------------------------->

Tiến trình P1:  write(x)a
                 [ x = a ]
                     \
                      \ (Quan hệ nhân quả)
                       v
Tiến trình P2:          read(x)a  -------->  write(y)b
                        [ b = x + 5 ]        [ y = b ]

----------------------------------------------------------------------------
Các thao tác có quan hệ nhân quả (Causally related operations)
```

---

## --- Trang 13 ---

### Tính nhất quán nhân quả (Causal Consistency)

Mô hình này không đảm bảo thứ tự (ordering) cho các thao tác (operations) không có quan hệ nhân quả với nhau. Những thao tác này có thể được nhìn thấy theo các thứ tự khác nhau.

Nhìn chung, **tính nhất quán nhân quả (Causal consistency)** yếu hơn, nhưng lại mạnh hơn mô hình **tính nhất quán cuối cùng (Eventual consistency)**. Nó được sử dụng để ngăn chặn các hành vi phi trực giác (non-intuitive behaviors).

#### Ví dụ (Example)
Mô hình nhất quán nhân quả được sử dụng trong một hệ thống bình luận (commenting system). Ví dụ, đối với các phản hồi cho một bình luận trên một bài đăng Facebook, chúng ta muốn hiển thị các bình luận phản hồi sau bình luận mà nó trả lời. Điều này là do tồn tại mối quan hệ nhân quả (cause-and-effect relationship) giữa một bình luận và các câu trả lời của nó.

> [!NOTE]  
> **Lưu ý:** Có rất nhiều mô hình nhất quán (consistency models) khác ngoài bốn mô hình được thảo luận trong bài học này, và vẫn còn dư địa cho các mô hình nhất quán mới. Các nhà nghiên cứu đã phát triển thêm các mô hình nhất quán mới. Ví dụ, Wyatt Lloyd và các cộng sự đã đề xuất mô hình **Causal+ Consistency** để tăng tốc độ cho một số loại giao dịch (transactions) cụ thể.

---

### Tính nhất quán tuần tự (Sequential Consistency)

**Tính nhất quán tuần tự (Sequential consistency)** mạnh hơn mô hình tính nhất quán nhân quả (Causal consistency). Nó bảo toàn thứ tự được chỉ định bởi chương trình của từng client. Tuy nhiên, tính nhất quán tuần tự không đảm bảo rằng các thao tác ghi (writes) sẽ hiển thị tức thì (instantaneously) hoặc theo cùng thứ tự mà chúng diễn ra dựa theo một đồng hồ toàn cục (global clock).

#### Ví dụ (Example)
Trong các ứng dụng mạng xã hội (social networking applications), chúng ta thường không bận tâm về thứ tự xuất hiện bài đăng của một số người bạn với nhau. Tuy nhiên, chúng ta vẫn kỳ vọng các bài đăng của một người bạn duy nhất phải xuất hiện theo đúng thứ tự mà chúng được tạo ra. Tương tự như vậy, chúng ta kỳ vọng các bình luận của bạn bè trong một bài đăng được hiển thị theo đúng thứ tự mà chúng được gửi lên (submitted). Mô hình tính nhất quán tuần tự đáp ứng được tất cả các đặc tính này.

---

## --- Trang 14 ---

### Tính nhất quán nghiêm ngặt hay Tuyến tính hóa (Strict Consistency aka Linearizability)

**Tính nhất quán nghiêm ngặt (Strict consistency)** hay **Tuyến tính hóa (Linearizability)** là mô hình nhất quán mạnh nhất. Mô hình này đảm bảo rằng một yêu cầu đọc (read request) từ bất kỳ bản sao nào (replicas) đều sẽ nhận được giá trị ghi mới nhất (latest write value). Một khi client nhận được thông báo xác nhận (acknowledgment - ACK) rằng thao tác ghi đã được thực hiện, các client khác có thể đọc được giá trị đó ngay lập tức.

Rất khó để đạt được tính tuyến tính hóa (Linearizability) trong một hệ thống phân tán (distributed system). Một số nguyên nhân dẫn đến những thách thức này là độ trễ mạng biến thiên (variable network delays) và các sự cố lỗi (failures). Chuỗi slide minh họa sau đây mô tả cách mà độ trễ mạng biến thiên khiến cho các bên khác nhau có thể nhìn thấy các giá trị khác nhau.

---

#### Diễn tiến từng bước minh họa (Slides 1 đến 9)

#### Bước 1 / 9
```
[ Node A ]           [ Node B ]
  x = 2                x = 2
(Alice)
          [ Node C ]
            x = 2
  (Bob)               (John)
```
* **Mô tả:** Có ba người dùng trong một hệ thống bao gồm ba nút / bản sao (nodes / replicas), và mỗi nút ban đầu đều có giá trị $x = 2$.  
*(1 of 9)*

---

## --- Trang 15 ---

#### Bước 2 / 9
```
[ Node A ]           [ Node B ]
  x = 2                x = 2
(Alice)
  |
  +-- T1: write(x): 10
          [ Node C ]
            x = 2
  (Bob)               (John)
```
* **Mô tả:** Alice yêu cầu một thao tác ghi (write operation) để thay đổi giá trị của $x$ thành $10$.  
*(2 of 9)*

---

#### Bước 3 / 9
```
[ Node A ]           [ Node B ]
  x = 10               x = 2
(Alice)
  |  ^
  |  |-- ack
  +-- T1: write(x): 10
          [ Node C ]
            x = 2
  (Bob)               (John)
```
* **Mô tả:** Nút A (Node A) thực hiện thao tác ghi lên $x$ và trả về một thông báo xác nhận (acknowledgment - ack) cho Alice.  
*(3 of 9)*

---

## --- Trang 16 ---

#### Bước 4 / 9
```
[ Node A ]           [ Node B ]
  x = 10  -----------> x = 2
(Alice)     forward
  |  ^         write
  |  |-- ack     |
  +-- T1: write(x): 10
          [ Node C ]
            x = 2
  (Bob)               (John)
```
* **Mô tả:** Nút A chuyển tiếp thao tác ghi (forwards the write operation) đến các nút khác trong hệ thống.  
*(4 of 9)*

---

#### Bước 5 / 9
```
[ Node A ]           [ Node B ]
  x = 10               x = 10
(Alice)
  |  ^
  |  |-- ack
  +-- T1: write(x): 10
          [ Node C ]
            x = 2
  (Bob)               (John)
```
* **Mô tả:** Nút B (Node B) nhận được thao tác ghi và thay đổi giá trị của $x$ thành $10$.  
*(5 of 9)*

---

## --- Trang 17 ---

#### Bước 6 / 9
```
[ Node A ]           [ Node B ]
  x = 10               x = 10
(Alice)                  ^
  |  ^                   |
  |  |-- ack             +-- T2: read(x)
  +-- T1: write(x): 10
          [ Node C ]
            x = 2
  (Bob)               (John)
```
* **Mô tả:** John yêu cầu một thao tác đọc (read operation), thao tác này được thực hiện trên Nút B (Node B).  
*(6 of 9)*

---

#### Bước 7 / 9
```
[ Node A ]           [ Node B ]
  x = 10               x = 10
(Alice)                  |  ^
  |  ^                   v  |
  |  |-- ack             10 +-- T2: read(x)
  +-- T1: write(x): 10
          [ Node C ]
            x = 2
  (Bob)               (John)
```
* **Mô tả:** Nút B đã có giá trị mới nhất của $x$ và trả giá trị đó về cho John (giá trị 10).  
*(7 of 9)*

---

## --- Trang 18 ---

#### Bước 8 / 9
```
[ Node A ]           [ Node B ]
  x = 10               x = 10
(Alice)                  |  ^
  |  ^                   v  |
  |  |-- ack             10 +-- T2: read(x)
  +-- T1: write(x): 10
          [ Node C ]
            x = 2
             ^
             |-- T3: read(x)
  (Bob)               (John)
```
* **Mô tả:** Sau John, Bob yêu cầu một thao tác đọc trên $x$, thao tác này được thực hiện trên Nút C (Node C).  
*(8 of 9)*

---

#### Bước 9 / 9
```
[ Node A ]           [ Node B ]
  x = 10               x = 10
(Alice)                  |  ^
  |  ^                   v  |
  |  |-- ack             10 +-- T2: read(x)
  +-- T1: write(x): 10
          [ Node C ]
            x = 2
            |  ^
            v  |-- T3: read(x)
            2
  (Bob)               (John)
```
* **Mô tả:** Nút C vẫn chưa nhận được thao tác ghi (write operation), do đó nó trả về giá trị cũ của $x = 2$ cho Bob.  
*(9 of 9)*

---

> [!IMPORTANT]  
> Thông thường, **sao chép đồng bộ (Synchronous Replication)** là một trong những thành tố cần thiết để đạt được tính nhất quán mạnh (Strong Consistency), mặc dù bản thân nó chưa đủ. Chúng ta có thể cần đến các thuật toán đồng thuận (Consensus Algorithms) như **Paxos** và **Raft** để đạt được tính nhất quán mạnh.

---

# --- Trang 19 ---

Quay lại (Back)  
Trừu tượng hóa mạng: Lời gọi thủ tục từ xa… (Network Abstractions: Remote Proc…)  
Đánh dấu đã hoàn thành (Mark As Completed)  
Tiếp theo (Next)  
Phổ các mô hình lỗi (The Spectrum of Failure Models)

Tính tuần tự hóa (Linearizability) ảnh hưởng trực tiếp đến tính sẵn sàng (**Availability**) của hệ thống, đó là lý do tại sao nó không phải lúc nào cũng được áp dụng. Các ứng dụng có yêu cầu tính nhất quán mạnh (**Strong Consistency**) thường sử dụng các kỹ thuật như nhân bản dựa trên túc số (**Quorum-based Replication**) để tăng tính sẵn sàng cho hệ thống.

### Ví dụ (Example)
Việc cập nhật mật khẩu của một tài khoản đòi hỏi tính nhất quán nghiêm ngặt (**Strict Consistency**). Ví dụ: nếu phát hiện hoạt động đáng ngờ trên tài khoản ngân hàng của mình, chúng ta sẽ lập tức đổi mật khẩu để không người dùng trái phép nào có thể truy cập vào tài khoản được nữa. Nếu vẫn có khả năng truy cập tài khoản bằng mật khẩu cũ do thiếu tính nhất quán nghiêm ngặt, thì việc đổi mật khẩu sẽ trở thành một chiến lược bảo mật vô dụng.

> [!NOTE]
> **Ghi chú:** Cơ sở dữ liệu Spanner của Google tuyên bố đạt chuẩn tuyến tính hóa (**Linearizable**) đối với nhiều hoạt động của mình.

### Tóm tắt (Summary)
Các dịch vụ tuyến tính hóa (**Linearizable Services**) dường như thực thi các giao dịch/thao tác theo thứ tự tuần tự trong thời gian thực. Chúng giúp việc xây dựng các ứng dụng phù hợp bên trên trở nên dễ dàng hơn bằng cách giới hạn số lượng giá trị mà dịch vụ có thể trả về cho các tiến trình ứng dụng.

Các dịch vụ tuyến tính hóa có hiệu năng kém hơn so với các dịch vụ có tính nhất quán yếu hơn (**Weaker Consistency**) để đánh đổi lấy các đảm bảo mạnh mẽ của chúng. Hãy nghĩ về một thao tác đọc (**Read**) trong một kho lưu trữ khóa-giá trị (**Key-Value Store**) trả về giá trị được ghi bởi một thao tác ghi đồng thời (**Concurrent Write**). Thao tác đọc này sẽ không áp đặt bất kỳ giới hạn nào lên các thao tác đọc trong tương lai nếu kho khóa-giá trị có tính nhất quán yếu.

Các lập trình viên ứng dụng phải thỏa hiệp giữa hiệu năng (**Performance**) và tính sẵn sàng (**Availability**) nếu họ sử dụng các dịch vụ có mô hình nhất quán mạnh (**Strong Consistency Models**). Các mô hình có thể phá vỡ các bất biến (**Invariants**) của các ứng dụng được xây dựng bên trên chúng để đổi lấy hiệu năng cao hơn.

---

# --- Trang 20 ---

## Phổ các mô hình lỗi (The Spectrum of Failure Models)
Tìm hiểu về các lỗi trong hệ thống phân tán (**Distributed Systems**) và mức độ phức tạp khi xử lý chúng.

**Chúng ta sẽ tìm hiểu các nội dung sau:**
- Dừng do lỗi (Fail-stop)
- Sập (Crash)
- Lỗi bỏ sót (Omission failures)
- Lỗi thời gian (Temporal failures)
- Lỗi Byzantine (Byzantine failures)

Lỗi là điều hiển nhiên trong thế giới của các hệ thống phân tán và có thể xuất hiện theo nhiều cách khác nhau. Chúng có thể đến rồi đi, hoặc tồn tại dai dẳng trong một thời gian dài.

Các mô hình lỗi (**Failure Models**) cung cấp cho chúng ta một khuôn khổ để suy luận về tác động của các lỗi và những phương thức khả thi để xử lý chúng.

Dưới đây là một minh họa trình bày phổ của các mô hình lỗi khác nhau:

> Đây là một phổ của các mô hình lỗi. Mức độ khó khăn khi xử lý một lỗi tăng dần khi chúng ta dịch chuyển sang phía bên phải.

```
Dễ xử lý                                                          Khó xử lý
(Easy to deal with)                                    (Difficult to deal with)
<----------------------------------------------------------------------------->
Fail-stop  ------>  Crash  ------>  Omission  ------>  Temporal  ------>  Byzantine
```

- **Fail-stop** (Dừng do lỗi)
- **Crash** (Sập)
- **Omission** (Bỏ sót)
- **Temporal** (Thời gian)
- **Byzantine** (Lỗi Byzantine)

### Dừng do lỗi (Fail-stop)

---

# --- Trang 21 ---

Quay lại (Back)  
Phổ các mô hình nhất quán (Spectrum of Consistency Models)  
Đánh dấu đã hoàn thành (Mark As Completed)  
Tiếp theo (Next)  
Tính sẵn sàng (Availability)

Trong loại lỗi này, một nút (**Node**) trong hệ thống phân tán sẽ ngừng hoạt động vĩnh viễn. Tuy nhiên, các nút khác vẫn có thể phát hiện được nút đó thông qua việc giao tiếp với nó.  
Từ góc nhìn của người xây dựng hệ thống phân tán, các lỗi dừng do lỗi (**Fail-stop failures**) là đơn giản và tiện lợi nhất để xử lý.

### Sập (Crash)
Trong loại lỗi này, một nút trong hệ thống phân tán sẽ ngừng hoạt động một cách âm thầm trong im lặng, và các nút khác không thể phát hiện ra rằng nút đó đã ngừng hoạt động.

### Lỗi bỏ sót (Omission failures)
Trong các lỗi bỏ sót, nút gặp lỗi khi gửi hoặc nhận các thông điệp (**Messages**). Có hai loại lỗi bỏ sót:
- Nếu nút không thể phản hồi lại yêu cầu gửi đến, lỗi này được gọi là **lỗi bỏ sót gửi (Send Omission Failure)**.
- Nếu nút không nhận được yêu cầu và do đó không thể xác nhận (Acknowledge - ACK) nó, lỗi này được gọi là **lỗi bỏ sót nhận (Receive Omission Failure)**.

### Lỗi thời gian (Temporal failures)
Trong các lỗi thời gian, nút vẫn tạo ra kết quả chính xác, nhưng lại quá trễ để có thể sử dụng được. Lỗi này có thể xuất phát từ thuật toán kém tối ưu, chiến lược thiết kế tồi, hoặc do mất đồng bộ hóa giữa các xung đồng hồ của bộ vi xử lý (**Processor Clocks**).

### Lỗi Byzantine (Byzantine failures)
Trong các lỗi Byzantine, nút biểu hiện các hành vi ngẫu nhiên bất thường như truyền các thông điệp tùy tiện vào những thời điểm tùy tiện, tạo ra các kết quả sai lệch, hoặc đột ngột dừng lại giữa chừng. Điều này chủ yếu xảy ra do một cuộc tấn công bởi một thực thể độc hại (**Malicious Entity**) hoặc do lỗi phần mềm (**Software Bug**). Lỗi Byzantine là loại lỗi thách thức và khó xử lý nhất trong hệ thống phân tán.

---

# --- Trang 22 ---


---

[← Bài trước](002-phong-van-system-design.md) | [Mục lục](README.md) | [Bài tiếp theo →](004-dac-tinh-phi-chuc-nang.md)
