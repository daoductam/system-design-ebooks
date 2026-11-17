# 032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)

[← Bài trước](031-thiet-ke-twitter.md) | [Mục lục](README.md) | [Bài tiếp theo →](033-thiet-ke-instagram.md)

---


# Thiết Kế Hệ Thống: Hệ Thống Bảng Tin (Newsfeed System)

Tìm hiểu các kiến thức cơ bản về thiết kế hệ thống bảng tin (newsfeed system).

**Nội dung bao gồm:**
* Bảng tin (newsfeed) là gì?
* Chúng ta sẽ thiết kế hệ thống bảng tin như thế nào?

---

## Bảng tin (Newsfeed) là gì?

Bảng tin (newsfeed) của bất kỳ nền tảng mạng xã hội nào (Twitter, Facebook, Instagram) là một danh sách các câu chuyện/bài viết (stories/posts) được tạo ra bởi các thực thể (entities) mà người dùng theo dõi. Bảng tin chứa văn bản (text), hình ảnh (images), video và các hoạt động khác như lượt thích (likes), bình luận (comments), chia sẻ (shares), quảng cáo (advertisements) cùng nhiều nội dung khác. Danh sách này liên tục được cập nhật và hiển thị tới người dùng liên quan trên trang chủ (home page) của họ. Tương tự, một hệ thống bảng tin (newsfeed system) cũng hiển thị bảng tin tới người dùng từ bạn bè (friends), người theo dõi/người được theo dõi (followers/followees), các nhóm (groups) và các trang (pages) khác, bao gồm cả các bài đăng của chính người dùng.

Bảng tin là thành phần thiết yếu đối với người dùng nền tảng mạng xã hội vì nó giúp họ luôn được cập nhật về những bước phát triển mới nhất trong ngành, các vấn đề thời sự và những thông tin liên quan. Nó cũng mang lại cho họ lý do bổ sung để quay trở lại và kết nối thường xuyên với nền tảng. Hàng tỷ người dùng sử dụng các nền tảng như vậy. Thách thức lớn là phải cung cấp một bảng tin cá nhân hóa (personalized newsfeed) theo thời gian thực (real-time) trong khi vẫn đảm bảo hệ thống có khả năng mở rộng (scalable) và tính sẵn sàng cao (highly available).

Chương này sẽ thảo luận về thiết kế cấp cao (high-level design) và thiết kế chi tiết (detailed design) của một hệ thống bảng tin cho một nền tảng mạng xã hội tương tự Facebook, Twitter, Instagram, v.v.

### Bảng tin trên ứng dụng di động (Newsfeeds on a mobile application)

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p002_00.png)

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p002_01.png)

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p002_02.png)

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p002_03.png)

---

## Chúng ta sẽ thiết kế hệ thống bảng tin như thế nào?

Chúng ta chia thiết kế của hệ thống bảng tin thành ba bài học sau:

1. **Yêu cầu (Requirements):** Trong bài học này, chúng ta sẽ xác định các yêu cầu chức năng (functional requirements) và phi chức năng (non-functional requirements). Chúng ta cũng sẽ ước tính yêu cầu tài nguyên (resource requirements) để cung cấp bảng tin cá nhân hóa cho hàng tỷ người dùng mỗi ngày.
2. **Thiết kế (Design):** Chúng ta sẽ thảo luận về thiết kế cấp cao (high-level design) và thiết kế chi tiết (detailed design) của hệ thống bảng tin trong bài học này. Chúng ta cũng sẽ mô tả thiết kế API (API design) và lược đồ cơ sở dữ liệu (database schema) cho thiết kế đề xuất. Hơn nữa, bài học này cũng sẽ giúp chúng ta xếp hạng bảng tin (rank newsfeed) để mang lại trải nghiệm tốt hơn cho người dùng.
3. **Đánh giá (Evaluation):** Trong bài học này, chúng ta sẽ đánh giá thiết kế của hệ thống bảng tin dựa trên các yêu cầu phi chức năng. Chúng ta cũng sẽ làm bài kiểm tra (quiz) để đánh giá mức độ hiểu biết về thiết kế hệ thống bảng tin.

Hãy cùng liệt kê các yêu cầu cho việc thiết kế phiên bản hệ thống bảng tin của chúng ta.

---

## Yêu Cầu Thiết Kế Hệ Thống Bảng Tin (Requirements of a Newsfeed System’s Design)

Làm quen với các yêu cầu và tính toán ước tính để thiết kế một hệ thống bảng tin.

**Nội dung bao gồm:**
* Các yêu cầu (Requirements)
  * Yêu cầu chức năng (Functional requirements)
  * Yêu cầu phi chức năng (Non-functional requirements)
* Ước tính tài nguyên (Resource estimation)
  * Ước tính lưu lượng truy cập (Traffic estimation)
  * Ước tính dung lượng lưu trữ (Storage estimation)
  * Ước tính số lượng máy chủ (Number of servers estimation)
* Các khối xây dựng (Building blocks) sẽ sử dụng

---

## Các yêu cầu (Requirements)

Để giới hạn phạm vi bài toán, chúng ta sẽ tập trung vào các yêu cầu chức năng và phi chức năng sau:

### Yêu cầu chức năng (Functional requirements)

* **Tạo bảng tin (Newsfeed generation):** Hệ thống sẽ tạo bảng tin dựa trên các trang (pages), nhóm (groups) và người theo dõi (followers/entities) mà người dùng theo dõi. Một người dùng có thể có nhiều bạn bè và người theo dõi. Do đó, hệ thống phải có khả năng tạo bảng tin từ tất cả bạn bè và người theo dõi. Thách thức ở đây là lượng nội dung tiềm năng rất khổng lồ. Hệ thống của chúng ta cần quyết định nội dung nào cần chọn cho người dùng và tiếp tục xếp hạng (rank) để quyết định nội dung nào hiển thị trước.
* **Nội dung bảng tin (Newsfeed contents):** Bảng tin có thể chứa văn bản (text), hình ảnh (images) và video.
* **Hiển thị bảng tin (Newsfeed display):** Hệ thống cần đính kèm các bài đăng mới gửi đến (new incoming posts) vào bảng tin cho tất cả người dùng đang hoạt động (active users) dựa trên một cơ chế xếp hạng (ranking mechanism) nào đó. Sau khi được xếp hạng, chúng ta sẽ hiển thị nội dung có thứ hạng cao hơn cho người dùng trước.

### Yêu cầu phi chức năng (Non-functional requirements)

* **Khả năng mở rộng (Scalability):** Hệ thống đề xuất phải có khả năng mở rộng cao để hỗ trợ số lượng người dùng ngày càng tăng trên bất kỳ nền tảng nào, chẳng hạn như Twitter, Facebook và Instagram.
* **Khả năng chịu lỗi (Fault tolerance):** Vì hệ thống phải xử lý một lượng lớn dữ liệu; do đó, khả năng chịu lỗi phân vùng (partition tolerance - tính sẵn sàng của hệ thống trong trường hợp xảy ra sự cố mạng giữa các thành phần của hệ thống) là bắt buộc.
* **Tính sẵn sàng (Availability):** Dịch vụ phải có tính sẵn sàng cao (High Availability) để giữ chân người dùng tương tác với nền tảng. Hệ thống có thể đánh đổi tính nhất quán mạnh (strong consistency) để lấy tính sẵn sàng (availability) và khả năng chịu lỗi (fault tolerance), theo định lý PACELC (PACELC theorem).
* **Độ trễ thấp (Low latency):** Hệ thống phải cung cấp bảng tin theo thời gian thực (real-time). Do đó, độ trễ tối đa không được vượt quá 2 giây ($< 2 \text{s}$).

---

## Ước tính tài nguyên (Resource estimation)

Giả sử nền tảng mà hệ thống bảng tin được thiết kế có **1 tỷ người dùng mỗi ngày** (1 billion users/day), trong đó trung bình có **500 triệu người dùng hoạt động hàng ngày (Daily Active Users - DAU)**. Ngoài ra, trung bình mỗi người dùng có **300 bạn bè** và theo dõi **250 trang**. Dựa trên các số liệu thống kê giả định này, hãy xem xét ước tính về lưu lượng truy cập (traffic), dung lượng lưu trữ (storage) và số lượng máy chủ (servers).

### Ước tính lưu lượng truy cập (Traffic estimation)

Giả sử mỗi người dùng hoạt động hàng ngày mở ứng dụng (hoặc trang mạng xã hội) **10 lần một ngày**. Tổng số yêu cầu mỗi ngày sẽ là:

$$500\text{M} \times 10 = 5 \text{ tỷ yêu cầu mỗi ngày (5 billion requests/day)}$$

Chuyển đổi sang số yêu cầu mỗi giây (Requests Per Second - RPS):

$$\frac{5 \times 10^9 \text{ requests}}{86,400 \text{ seconds}} \approx 58\text{K requests/second}$$

> **58K Requests / Second**

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p005_00.png)
*Ước tính lưu lượng truy cập cho hệ thống bảng tin (Traffic estimation for the newsfeed system)*

---

### Ước tính dung lượng lưu trữ (Storage estimation)

Giả sử bảng tin sẽ được tạo ngoại tuyến (generated offline / pre-computed) và được render (kết xuất) khi có yêu cầu. Đồng thời, chúng ta sẽ tính toán trước (precompute) **top 200 bài đăng** cho mỗi người dùng. Hãy tính toán ước tính lưu trữ cho siêu dữ liệu của người dùng (users’ metadata), các bài đăng chứa văn bản (posts containing text) và nội dung đa phương tiện (media content).

#### 1. Ước tính lưu trữ siêu dữ liệu của người dùng (Users’ metadata storage estimation):
Giả sử dung lượng lưu trữ cần thiết cho siêu dữ liệu của một người dùng là $50\text{ KB}$. Đối với $1\text{ tỷ người dùng}$, chúng ta sẽ cần:

$$1\text{B} \times 50\text{KB} = 50\text{TB}$$

| Bảng tính ước tính lưu trữ cho siêu dữ liệu người dùng (Storage Estimation for the Users' Metadata) | Giá trị |
| :--- | :--- |
| **Số lượng người dùng (tính theo tỷ - in billion)** | $1$ |
| **Dung lượng lưu trữ yêu cầu cho siêu dữ liệu một người dùng (tính theo KB)** | $50$ |
| **Tổng dung lượng lưu trữ yêu cầu cho tất cả người dùng (tính theo TB)** | $50$ |

#### 2. Ước tính lưu trữ bài đăng dạng văn bản (Textual post’s storage estimation):
Tất cả các bài đăng đều có thể chứa một số văn bản, chúng ta giả định dung lượng trung bình là $50\text{ KB}$. Ước tính dung lượng lưu trữ cho top 200 bài đăng của $500\text{ triệu người dùng}$ sẽ là:

$$200 \times 500\text{M} \times 50\text{KB} = 5\text{PB}$$

#### 3. Ước tính lưu trữ nội dung đa phương tiện (Media content storage estimate):
Cùng với văn bản, một bài đăng cũng có thể chứa nội dung đa phương tiện. Do đó, chúng ta giả định rằng $\frac{1}{5}$ số bài đăng có video và $\frac{4}{5}$ số bài đăng bao gồm hình ảnh. Kích thước trung bình giả định của hình ảnh là $200\text{ KB}$ và kích thước video là $2\text{ MB}$.

Ước tính dung lượng lưu trữ cho $200$ bài đăng của một người dùng:

$$\left(200 \times 2\text{MB} \times \frac{1}{5}\right) + \left(200 \times 200\text{KB} \times \frac{4}{5}\right) = 80\text{MB} + 32\text{MB} = 112\text{MB}$$

---

# Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)

---

### Tổng Dung Lượng Lưu Trữ Cần Thiết Cho Bài Đăng Của 500 Triệu Người Dùng

Như vậy, chúng ta sẽ cần ít nhất **56 PB** dung lượng lưu trữ đối tượng nhị phân lớn (**Blob Storage**) để lưu trữ nội dung đa phương tiện (**media content**):

$$112\text{ MB} \times 500\text{M} = 56\text{ PB}$$

#### Dung lượng lưu trữ yêu cầu cho 500 triệu người dùng hoạt động mỗi ngày (mỗi người dùng có xấp xỉ 200 bài đăng) bởi hệ thống bảng tin:

| Thành phần dữ liệu | Dung lượng lưu trữ |
| :--- | :--- |
| **Dữ liệu đặc tả của người dùng (Users' metadata)** | 50 TB |
| **Bài đăng dạng văn bản (Textual posts)** | 5 PB |
| **Bài đăng chứa nội dung đa phương tiện (Media content posts)** | 56 PB |

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p007_00.png)

#### Ước tính dung lượng lưu trữ của các bài đăng chứa nội dung văn bản và đa phương tiện (Storage Estimation of Posts Containing Text and Media Content):

| Tham số ước tính | Giá trị |
| :--- | :--- |
| **Số lượng người dùng hoạt động (Number of active users - tính theo triệu)** | 500 |
| **Dung lượng văn bản tối đa cho phép trên mỗi bài đăng (Maximum allowed text storage per post - tính theo KB)** | 50 |
| **Số lượng bài đăng tính toán trước cho mỗi người dùng (Number of precomputed posts per user - Top N)** | 200 |
| **Dung lượng lưu trữ yêu cầu cho các bài đăng văn bản (Storage required for textual posts - tính theo PB)** | 5 |
| **Tổng dung lượng lưu trữ nội dung media yêu cầu cho người dùng hoạt động (Total required media content storage for active users - tính theo PB)** | 56 |

---

### Ước Tính Số Lượng Máy Chủ (Number of Servers Estimation)

Cân nhắc lưu lượng truy cập (**traffic**) và ước tính dung lượng lưu trữ ở trên, hãy cùng ước tính số lượng máy chủ cần thiết để đảm bảo các hoạt động diễn ra trơn tru. 

Nhắc lại rằng một máy chủ thông thường điển hình có thể phục vụ **8.000 yêu cầu mỗi giây (Requests Per Second - RPS)**. Do hệ thống của chúng ta sẽ có khoảng 500 triệu người dùng hoạt động hàng ngày (**Daily Active Users - DAU**), theo phương pháp ước tính trong chương *Các Phép Tính Nhanh Ước Lượng (Back-of-the-Envelope Calculations)*, số lượng máy chủ chúng ta cần là:

$$\text{Số lượng máy chủ} = \frac{\text{DAU}}{\text{RPS của một máy chủ}} = \frac{500\text{M}}{8000} = 62.500\text{ máy chủ}$$

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p008_00.png)

#### Số lượng máy chủ yêu cầu cho hệ thống bảng tin: **62.500 máy chủ**

#### Bảng ước tính máy chủ (Servers Estimation):

| Tham số | Giá trị |
| :--- | :--- |
| **Số lượng người dùng hoạt động (tính theo triệu)** | 500 |
| **RPS của một máy chủ** | 8.000 |
| **Số lượng máy chủ yêu cầu** | 62.500 |

---

### Các Thành Phần Khối Dựng Cơ Bản Sẽ Sử Dụng (Building Blocks We Will Use)

Kiến trúc thiết kế của hệ thống bảng tin (**newsfeed system**) sử dụng các thành phần khối dựng cơ bản (**building blocks**) sau:

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p008_01.png)  
*Các khối dựng cơ bản để thiết kế một hệ thống bảng tin*

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p008_02.png)  
**Cơ sở dữ liệu (Database)**

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p008_03.png)  
**Mạng phân phối nội dung (CDN - Content Delivery Network)**

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p008_04.png)  
**Lưu trữ nhị phân lớn (Blob storage)**

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p008_05.png)  
**Bộ cân bằng tải (Load balancer)**

* **Cơ sở dữ liệu (Database(s))**: Cần thiết để lưu trữ các bài đăng từ nhiều thực thể khác nhau và bảng tin cá nhân hóa đã được khởi tạo. Nó cũng được sử dụng để lưu trữ dữ liệu đặc tả của người dùng (**users' metadata**) và mối quan hệ của họ với các thực thể khác, chẳng hạn như bạn bè và người theo dõi (**friends and followers**).
* **Bộ nhớ đệm (Cache)**: Là một khối dựng quan trọng để lưu giữ dữ liệu được truy cập thường xuyên, cho dù đó là các bài đăng và bảng tin hay dữ liệu đặc tả của người dùng.
* **Lưu trữ nhị phân lớn (Blob storage)**: Rất cần thiết để lưu trữ các nội dung đa phương tiện (**media content**), ví dụ như hình ảnh và video.
* **CDN (Content Delivery Network)**: Phân phối nội dung một cách hiệu quả tới người dùng cuối (**end-users**), giúp giảm độ trễ (**Latency**) và giảm tải gánh nặng cho các máy chủ phía sau (**back-end servers**).
* **Bộ cân bằng tải (Load balancers)**: Cần thiết để phân phối hàng triệu yêu cầu truy xuất bảng tin gửi đến từ các máy khách (**clients**) vào cụm máy chủ sẵn sàng phục vụ (**available server pool**).

> [!NOTE]
> Trong phần tiếp theo, chúng ta sẽ tập trung vào thiết kế mức tổng thể (**High-Level Design**) và thiết kế chi tiết (**Detailed Design**) của hệ thống bảng tin.

---

## Thiết Kế Hệ Thống Bảng Tin (Design of a Newsfeed System)

Tìm hiểu cách thiết kế một hệ thống bảng tin.

### Nội dung bao gồm:
* Thiết kế mức tổng thể của hệ thống bảng tin (**High-level design of a newsfeed system**)
* Thiết kế API (**API design**)
  * Khởi tạo bảng tin của người dùng (`generateNewsfeed`)
  * Lấy bảng tin của người dùng (`getNewsfeed`)
* Lược đồ lưu trữ (**Storage schema**)
* Thiết kế chi tiết (**Detailed design**)
  * Dịch vụ khởi tạo bảng tin (**The newsfeed generation service**)
  * Dịch vụ xuất bản bảng tin (**The newsfeed publishing service**)
  * Dịch vụ xếp hạng bảng tin (**The newsfeed ranking service**)
  * Xếp hạng bài đăng và xây dựng bảng tin (**Posts ranking and newsfeed construction**)
* Tích hợp toàn bộ hệ thống (**Putting everything together**)

Hãy cùng thảo luận về thiết kế mức tổng quan và chi tiết của một hệ thống bảng tin dựa trên các yêu cầu đã được đề cập trong phần trước.

---

### Thiết Kế Mức Tổng Thể Của Hệ Thống Bảng Tin (High-Level Design of a Newsfeed System)

Về cơ bản, hệ thống bảng tin chịu trách nhiệm cho hai tác vụ chính sau:

1. **Khởi tạo bảng tin (Feed generation)**: Bảng tin được tạo ra bằng cách tổng hợp các bài đăng (hoặc các mục bảng tin - **feed items**) từ bạn bè và người theo dõi dựa trên một cơ chế xếp hạng (**ranking mechanism**) nhất định.
2. **Xuất bản bảng tin (Feed publishing)**: Khi một bảng tin/bài đăng được xuất bản, dữ liệu liên quan sẽ được ghi vào bộ nhớ đệm (**cache**) và cơ sở dữ liệu (**database**). Dữ liệu này có thể là văn bản hoặc bất kỳ nội dung đa phương tiện nào. Một bài đăng chứa dữ liệu từ bạn bè và người theo dõi sẽ được đẩy/phân phối vào bảng tin của người dùng.

Hãy cùng chuyển sang thiết kế mức tổng thể của hệ thống bảng tin. Hệ thống bao gồm hai phần thiết yếu nói trên, được thể hiện trong sơ đồ dưới đây:

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p011_00.png)  
*Thiết kế mức tổng thể của hệ thống Bảng Tin (High-level design of the Newsfeed system)*

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p011_01.png)  
*(1) Tầng kết nối người dùng và cân bằng tải (Clients & Load Balancer)*

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p011_02.png)  
*(2) Tầng Web Servers làm nhiệm vụ trung gian, xác thực và điều hướng*

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p011_03.png)  
*(3) Dịch vụ thông báo (Notification service) tiếp nhận bài đăng mới*

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p011_04.png)  
*(4) Dịch vụ khởi tạo bảng tin (Newsfeed generation service) và xuất bản (Publishing service)*

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p011_05.png)  
*(5) Cụm dịch vụ bài đăng (Post service), Lưu trữ Blob, Cache và Database*

#### Thảo luận về các thành phần chính được thể hiện trong thiết kế mức tổng quan:

1. **Người dùng (User(s))**: Người dùng có thể tạo một bài đăng kèm nội dung hoặc gửi yêu cầu lấy bảng tin của họ.
2. **Bộ cân bằng tải (Load balancer)**: Điều hướng lưu lượng truy cập (**traffic**) đến một trong các máy chủ web (**web servers**).
3. **Máy chủ Web (Web servers)**: Đóng gói các dịch vụ phía sau (**back-end services**) và đóng vai trò như một lớp trung gian giữa người dùng và các dịch vụ khác nhau. Ngoài việc thực thi xác thực (**authentication**) và giới hạn tốc độ truy cập (**rate-limiting**), các máy chủ web chịu trách nhiệm chuyển tiếp lưu lượng truy cập tới các dịch vụ back-end khác.
4. **Dịch vụ thông báo (Notification service)**: Thông báo cho dịch vụ tạo bảng tin (**newsfeed generation service**) bất cứ khi nào có bài đăng mới từ bạn bè hoặc người theo dõi, đồng thời gửi thông báo đẩy (**push notification**).
5. **Dịch vụ khởi tạo bảng tin (Newsfeed generation service)**: Dịch vụ này tạo các bảng tin từ bài đăng của những người theo dõi/bạn bè của một người dùng và lưu trữ chúng trong bộ nhớ đệm bảng tin (**newsfeed cache**).
6. **Dịch vụ xuất bản bảng tin (Newsfeed publishing service)**: Chịu trách nhiệm xuất bản bảng tin lên dòng thời gian (**timeline**) của người dùng từ bộ nhớ đệm bảng tin. Dịch vụ này cũng đính kèm ảnh thu nhỏ (**thumbnail**) của nội dung đa phương tiện từ kho lưu trữ nhị phân (**blob storage**) cùng liên kết dẫn đến nội dung đó vào bảng tin dành cho người dùng.
7. **Dịch vụ bài đăng (Post-service)**: Bất cứ khi nào người dùng yêu cầu tạo bài đăng, `post-service` sẽ được gọi; bài đăng vừa tạo sẽ được lưu vào cơ sở dữ liệu bài đăng (**post database**) và bộ nhớ đệm tương ứng (**post cache**). Nội dung đa phương tiện trong bài đăng được lưu trữ tại kho lưu trữ nhị phân (**blob storage**).

---

### Thiết Kế API (API Design)

API là phương thức chính để các máy khách (**clients**) giao tiếp với hệ thống máy chủ (**servers**). Thông thường, các API bảng tin chạy trên nền tảng HTTP, cho phép client thực hiện các hành động bao gồm: đăng trạng thái, truy xuất bảng tin, kết bạn, v.v. 

Mục tiêu chính của chúng ta là **khởi tạo** và **lấy** bảng tin của người dùng; do đó, các API sau đây là thiết yếu:

#### 1. Khởi tạo bảng tin của người dùng (Generate user’s newsfeed)

API sau đây được sử dụng để tạo bảng tin cho một người dùng:

```http
generateNewsfeed(user_id)
```

API này tiếp nhận ID của người dùng (`user_id`), sau đó xác định danh sách bạn bè và những người theo dõi của họ. API này sinh ra các bảng tin bao gồm nhiều bài đăng tổng hợp. 

> [!TIP]
> Do các thành phần nội bộ của hệ thống sử dụng API này, nó hoàn toàn có thể được gọi ở chế độ ngoại tuyến (**offline mode**) để **tính toán trước (pre-generate)** bảng tin cho người dùng. Các bảng tin được tạo trước này sẽ được lưu trữ trên hệ thống lưu trữ bền vững (**persistent storage**) và bộ nhớ đệm liên kết (**associated cache**).

**Tham số sử dụng trong lệnh gọi API này:**

| Tham số (Parameter) | Mô tả (Description) |
| :--- | :--- |
| `user_id` | Định danh duy nhất của người dùng cần được tạo bảng tin. |

---

#### 2. Lấy bảng tin của người dùng (Get user’s newsfeed)

API sau đây được sử dụng để lấy danh sách bảng tin của người dùng:

```http
getNewsfeed(user_id, count)
```

---

### API Lấy Bảng Tin (`getNewsfeed`)

Lời gọi API `getNewsfeed(.)` trả về một đối tượng JSON bao gồm danh sách các bài đăng (posts).

Các tham số sau được sử dụng cho API này:

| Tham số (Parameter) | Mô tả (Description) |
| :--- | :--- |
| `user_id` | Định danh duy nhất của người dùng mà hệ thống sẽ lấy dữ liệu bảng tin (newsfeed). |
| `count` | Số lượng mục tin (feed items / bài đăng) sẽ được truy xuất trong mỗi yêu cầu. |

---

### Lược Đồ Lưu Trữ (Storage Schema)

Các quan hệ cơ sở dữ liệu (database relations) cho hệ thống bảng tin (newsfeed system) như sau:

*   **`User` (Người dùng):** Quan hệ này chứa dữ liệu về một người dùng. Một người dùng cũng có thể là người theo dõi (follower) hoặc bạn bè (friend) của những người dùng khác.
*   **`Entity` (Thực thể):** Quan hệ này lưu trữ dữ liệu liên quan đến bất kỳ thực thể nào, chẳng hạn như các trang (pages), nhóm (groups), v.v.
*   **`Feed_item` (Mục tin):** Dữ liệu về các bài đăng do người dùng tạo được lưu trữ trong quan hệ này.
*   **`Media` (Đa phương tiện):** Thông tin về nội dung đa phương tiện được lưu trữ trong quan hệ này.

#### Lược Đồ Cơ Sở Dữ Liệu Cho Hệ Thống Bảng Tin (Database Schema)

```sql
User
User_ID:            varchar(32) (PK)
Name:               varchar(32)
Email:              varchar(32)
CreationDate:       datetime
Mobile:             varchar(32)
LastLogin:          datetime

Entity (Page or Group)
Entity_ID:          varchar (PK)
Name:               varchar(32)
Description:        varchar(512)
CreationDate:       datetime
Creator:            User_ID (FK)

Feed_Item
Feed_Item_ID:       varchar (PK)
Creator:            User_ID (FK)
Content:            varchar(512)
Entity_ID:          Entity_ID (FK)
CreationDate:       datetime
Likes_count:        int
Media_ID:           int

Media
Media_ID:           int (PK)
Description:        varchar(256)
Path:               varchar(256)
Views_count:        int
CreationDate:       datetime
```

Chúng ta sử dụng một cơ sở dữ liệu đồ thị (Graph Database) để lưu trữ các mối quan hệ giữa người dùng, bạn bè và người theo dõi (followers). Để đạt được mục đích này, chúng ta tuân theo mô hình đồ thị thuộc tính (property graph model). Chúng ta có thể hình dung một cơ sở dữ liệu đồ thị bao gồm hai bảng quan hệ (relational tables):

1. Dành cho các đỉnh (vertices) đại diện cho người dùng.
2. Dành cho các cạnh (edges) biểu thị các mối quan hệ giữa họ.

Do đó, chúng ta tuân theo một lược đồ quan hệ (relational schema) cho kho lưu trữ đồ thị (graph store), như được hiển thị trong hình bên dưới. Lược đồ này sử dụng kiểu dữ liệu PostgreSQL JSON để lưu trữ các thuộc tính của từng đỉnh (người dùng) hoặc cạnh (mối quan hệ).

Một biểu diễn thay thế của `User` có thể được hiển thị trong cơ sở dữ liệu đồ thị bên dưới. Trong đó `Users_ID` vẫn giữ nguyên và các thuộc tính được lưu trữ dưới định dạng tệp JSON.

#### Lược Đồ Của Cơ Sở Dữ Liệu Đồ Thị Lưu Trữ Các Mối Quan Hệ Giữa Những Người Dùng

```sql
User
Users_ID:           int (PK)
properties:         JSON

Relationship
Relation_ID:        int (PK)
Relation_from:      int REFERENCES User (User_ID)
Relation_towards:   int REFERENCES User (Users_ID)
Label:              varchar(32)
properties:         JSON
```

Hình minh họa dưới đây mô tả cách đồ thị có thể được biểu diễn bằng cách sử dụng lược đồ quan hệ:

* `782` (User's ID)
* `399` (User's ID)
* `Relation_ID`: 111
* `Label`: Following

Đối với đồ thị đơn giản ở trên, với các `Users_ID` là `782` và `399`, bảng `Relationship` sẽ có các bản ghi (entries) sau:

* `User_ID`: 782
* `User_ID`: 399

#### Đồ Thị Giữa Hai Người Dùng Gồm Hai Đỉnh Và Một Cạnh

| Relation_ID | Relation_from | Relation_towards | Label | Properties |
| :--- | :--- | :--- | :--- | :--- |
| **111** | 782 | 399 | Following | Một số mô tả dưới dạng kiểu dữ liệu JSON (*Some description as a JSON data type*) |

*(Bảng Relationship)*

---

### Thiết Kế Chi Tiết (Detailed Design)

Hãy cùng khám phá chi tiết thiết kế của hệ thống bảng tin (newsfeed system).

Như đã thảo luận trước đó, có hai phần chính trong hệ thống bảng tin: **Newsfeed Publishing** (Xuất bản bảng tin) và **Newsfeed Generation** (Tạo bảng tin). Do đó, chúng ta sẽ thảo luận về cả hai phần, bắt đầu với dịch vụ tạo bảng tin (Newsfeed Generation Service).

#### Dịch Vụ Tạo Bảng Tin (The Newsfeed Generation Service)

Bảng tin (Newsfeed) được tạo bằng cách tổng hợp (aggregated) các bài đăng (hoặc các mục tin - feed items) từ bạn bè, người theo dõi (followers) của người dùng và các thực thể khác (các trang và các nhóm).

Trong thiết kế được đề xuất của chúng tôi, dịch vụ tạo bảng tin chịu trách nhiệm tạo bảng tin. Khi một yêu cầu lấy bảng tin từ một người dùng (giả sử là Alice) được nhận tại các máy chủ web (Web Servers), máy chủ web sẽ thực hiện một trong hai cách:

* Gọi dịch vụ tạo bảng tin để tạo tin (generate feeds), bởi vì một số người dùng không thường xuyên truy cập nền tảng, do đó bảng tin của họ chỉ được tạo theo yêu cầu (on-demand / on their request).
* Lấy bảng tin đã được tạo sẵn (pre-generated newsfeed) cho những người dùng hoạt động tích cực (active users), những người truy cập nền tảng thường xuyên.

Các bước sau đây được thực hiện theo trình tự để tạo bảng tin cho Alice:

1. **Bước 1:** Dịch vụ tạo bảng tin truy xuất ID của tất cả người dùng và thực thể mà Alice theo dõi từ cơ sở dữ liệu đồ thị (Graph Database).
2. **Bước 2:** Khi các ID được truy xuất từ cơ sở dữ liệu đồ thị, bước tiếp theo là lấy thông tin bạn bè của họ (những người theo dõi và thực thể) từ bộ nhớ đệm người dùng (User Cache), bộ nhớ đệm này được cập nhật thường xuyên bất cứ khi nào cơ sở dữ liệu người dùng (User Database) được cập nhật/sửa đổi.
3. **Bước 3:** Ở bước này, dịch vụ sẽ truy xuất các bài đăng mới nhất, phổ biến nhất và có liên quan nhất cho các ID đó từ bộ nhớ đệm bài đăng (Post Cache). Đây là những bài đăng mà chúng ta có thể hiển thị trên bảng tin của Alice.
4. **Bước 4:** Dịch vụ xếp hạng (Ranking Service) xếp hạng các bài đăng dựa trên mức độ liên quan của chúng đối với Alice. Điều này đại diện cho bảng tin hiện tại của Alice.
5. **Bước 5:** Bảng tin được lưu trữ trong bộ nhớ đệm bảng tin (Newsfeed Cache), từ đó $N$ bài đăng hàng đầu ($top\ N\ posts$) được xuất bản lên dòng thời gian (timeline) của Alice. *(Quy trình xuất bản được thảo luận chi tiết trong phần tiếp theo).*
6. **Bước 6:** Cuối cùng, bất cứ khi nào Alice cuộn đến cuối dòng thời gian của mình, $N$ bài đăng tiếp theo sẽ được tìm nạp về màn hình của cô ấy từ bộ nhớ đệm bảng tin.

Quy trình được minh họa trong hình ảnh sau:

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p016_00.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p016_01.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p016_02.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p016_03.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p016_04.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p016_05.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p016_06.png)

**Cách thức hoạt động của dịch vụ tạo bảng tin (Working of the newsfeed generation service):**
* Clients (Khách hàng)
* Load Balancer (Bộ cân bằng tải)
* Web Servers (Máy chủ Web)
* Newsfeed Generation Service (Dịch vụ tạo bảng tin)
* User Cache (Bộ nhớ đệm người dùng)
* Graph Database (Cơ sở dữ liệu đồ thị)
* User Database (Cơ sở dữ liệu người dùng)
* Post Cache (Bộ nhớ đệm bài đăng)
* Post Database (Cơ sở dữ liệu bài đăng)
* Newsfeed Cache Servers holding constructed feeds and ranked feeds (Các máy chủ bộ nhớ đệm bảng tin lưu trữ các bảng tin đã được cấu thành và xếp hạng)
* Ranking Service (Dịch vụ xếp hạng)
* CDN (Mạng phân phối nội dung)
* Các bước luồng xử lý: 1, 2, 3, 4, 5

> [!NOTE]
> **Điểm Cần Suy Ngẫm (Point to Ponder)**
> 
> **Câu hỏi:** Việc tạo và lưu trữ bảng tin cho từng người dùng trong bộ nhớ đệm (Cache) đòi hỏi một lượng bộ nhớ khổng lồ (bước 5 trong phần trên). Có cách nào để giảm mức tiêu thụ bộ nhớ này không?
> 
> **Ẩn câu trả lời (Hide Answer):** Một cách hiệu quả về mặt bộ nhớ (memory-efficient) là chỉ lưu trữ ánh xạ giữa người dùng và các bài đăng tương ứng của họ trong một bảng tại bộ nhớ đệm, tức là `<Post_ID, User_ID>`. Trong giai đoạn xuất bản bảng tin (feed publishing phase), hệ thống sẽ truy xuất các bài đăng từ cơ sở dữ liệu bài đăng (Post Database) và tạo bảng tin cho người dùng theo dõi một người dùng khác có `User_ID`.

---

#### Dịch Vụ Xuất Bản Bảng Tin (The Newsfeed Publishing Service)

Tại giai đoạn này, các bảng tin đã được tạo cho người dùng từ bạn bè, người theo dõi và các thực thể tương ứng của họ và được lưu trữ dưới dạng `<Post_ID, User_ID>` trong bộ nhớ đệm bảng tin (Newsfeed Cache).

Bây giờ, câu hỏi đặt ra là các bảng tin được tạo cho Alice sẽ được xuất bản lên dòng thời gian (timeline) của cô ấy như thế nào?

Dịch vụ xuất bản bảng tin (Newsfeed Publishing Service) lấy một danh sách các ID bài đăng từ bộ nhớ đệm bảng tin. Dữ liệu được lấy từ bộ nhớ đệm bảng tin là một bộ (tuple) gồm ID bài đăng và ID người dùng, tức là `<Post_ID, User_ID>`. Sau đó, dữ liệu hoàn chỉnh về các bài đăng và người dùng được truy xuất từ bộ nhớ đệm người dùng (Users Cache) và bộ nhớ đệm bài đăng (Posts Cache) để tạo thành một bảng tin hoàn chỉnh (entirely constructed newsfeed).

Trong bước cuối cùng, bảng tin đã được xây dựng hoàn chỉnh sẽ được gửi đến máy khách (Alice) bằng cách sử dụng một trong các phương pháp lan tỏa (fan-out approaches). Bảng tin phổ biến và nội dung đa phương tiện cũng được lưu trữ trong CDN để truy xuất nhanh chóng (fast retrieval).

> [!NOTE]
> **Vấn đề gì sẽ xảy ra khi tạo bảng tin theo yêu cầu của người dùng (còn gọi là live updates)?**

**Dịch vụ xuất bản bảng tin đang hoạt động (The newsfeed publishing service in action):**

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p018_00.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p018_01.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p018_02.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p018_03.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p018_04.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p018_05.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p018_06.png)

* Clients (Khách hàng)
* Load Balancer (Bộ cân bằng tải)
* Web Servers (Máy chủ Web)
* Newsfeed Publishing Service (Dịch vụ xuất bản bảng tin)
* User Cache (Bộ nhớ đệm người dùng)
* Newsfeed Cache (Bộ nhớ đệm bảng tin)
* User Database (Cơ sở dữ liệu người dùng)
* Blob Storage (Kho lưu trữ đối tượng nhị phân lớn)
* Post Database (Cơ sở dữ liệu bài đăng)
* Post Cache (Bộ nhớ đệm bài đăng)
* CDN (Mạng phân phối nội dung)

> [!NOTE]
> **Điểm Cần Suy Ngẫm (Point to Ponder)**
> 
> **Câu hỏi:** Bảng tin của bạn bè và người theo dõi được cập nhật như thế nào khi một người dùng tạo một bài đăng mới?

---

# Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)

---

## 1. Dịch Vụ Xếp Hạng Bảng Tin (The Newsfeed Ranking Service)

*Ẩn câu trả lời (Hide Answer)*

Khi một người dùng, chẳng hạn như Bob, tạo một bài đăng mới, nó sẽ được lưu trữ trong cơ sở dữ liệu bài đăng (Post Database) và bộ nhớ đệm bài đăng (Post Cache). Ở bước tiếp theo, dịch vụ tạo bảng tin (Newsfeed Generation Service) sẽ tạo ra một bảng tin cho bạn bè và những người theo dõi (followers) của Bob, đồng thời bộ nhớ đệm bảng tin (Newsfeed Cache) sẽ được cập nhật. Bảng tin đã cập nhật sẽ được phân phối tới những người dùng tương ứng trong sự kiện làm mới trang/màn hình (page/screen refresh event) tiếp theo.

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p019_00.png)

Thông thường, chúng ta thấy các bài đăng quan trọng và phù hợp nhất (relevant and important posts) xuất hiện ở trên cùng của bảng tin bất cứ khi nào đăng nhập vào tài khoản mạng xã hội của mình. Việc xếp hạng này liên quan đến nhiều thuật toán xếp hạng và gợi ý nâng cao (advanced ranking and recommendation algorithms).

Trong thiết kế của chúng ta, **dịch vụ xếp hạng bảng tin (Newsfeed Ranking Service)** bao gồm các thuật toán này hoạt động dựa trên nhiều đặc trưng/thuộc tính (features) khác nhau, chẳng hạn như: lịch sử hoạt động trong quá khứ của người dùng, lượt thích (likes), lượt không thích (dislikes), bình luận (comments), số lượt nhấp chuột (clicks) và nhiều yếu tố khác. Các thuật toán này cũng thực hiện các chức năng sau:

* **Lựa chọn các bài đăng "ứng viên" (candidate posts)** để hiển thị trong một bảng tin.
* **Loại bỏ các bài đăng chứa thông tin sai lệch (misinformation) hoặc giật gân câu khách (clickbait)** khỏi danh sách các bài đăng ứng viên.
* **Tạo danh sách bạn bè** mà người dùng thường xuyên tương tác.
* **Chọn các chủ đề** mà người dùng đã dành nhiều thời gian tương tác hơn.

Hệ thống xếp hạng xem xét tất cả các điểm trên để dự đoán các bài đăng phù hợp và quan trọng nhất đối với một người dùng.

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p019_01.png)

*Máy chủ bộ nhớ đệm lưu trữ các bảng tin đã được xây dựng và các bảng tin đã được xếp hạng (Cache servers holding constructed feeds and ranked feeds) | Dịch vụ xếp hạng (Ranking service) | CDN*

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p019_02.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p019_03.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p019_04.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p019_05.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p019_06.png)

---

## 2. Xếp Hạng Bài Đăng Và Xây Dựng Bảng Tin (Posts Ranking and Newsfeed Construction)

Các bảng tin đã xếp hạng (ranked newsfeeds) được lưu trữ trong các máy chủ bộ nhớ đệm (cache servers).

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p020_00.png)

*Bộ cân bằng tải (Load Balancer) | Máy khách (Clients) | Máy chủ Web (Web Servers) | Dịch vụ xuất bản bảng tin (Newsfeed Publishing Service) | Bộ nhớ đệm người dùng (User Cache) | Cơ sở dữ liệu người dùng (User Database) | Lưu trữ Blob (Blob Storage) | Cơ sở dữ liệu bài đăng (Post Database) | Bộ nhớ đệm bài đăng (Post Cache)*

Cơ sở dữ liệu bài đăng (Post Database) chứa các bài đăng được xuất bản bởi các người dùng khác nhau. Giả sử có 10 bài đăng trong cơ sở dữ liệu được xuất bản bởi 5 người dùng khác nhau. Mục tiêu của chúng ta là chỉ xếp hạng 4 bài đăng trong số 10 bài đăng đó cho một người dùng (ví dụ: Bob) - người đang theo dõi 5 người dùng khác nhau này. Chúng ta thực hiện các bước sau để xếp hạng từng bài đăng và tạo bảng tin cho Bob:

1. **Trích xuất đặc trưng (Feature Extraction):** Nhiều đặc trưng khác nhau như lượt thích (likes), bình luận (comments), chia sẻ (shares), danh mục (category), thời lượng (duration), v.v. được trích xuất từ mỗi bài đăng.
2. **Tính toán độ liên quan (Relevance Calculation):** Dựa trên lịch sử trước đây của Bob được lưu trong cơ sở dữ liệu người dùng (User Database), độ liên quan được tính toán cho từng bài đăng thông qua các thuật toán xếp hạng và máy học (machine learning) khác nhau.
3. **Gán điểm liên quan (Relevance Score Assignment):** Một điểm liên quan được gán, chẳng hạn từ 1 đến 5, trong đó 1 biểu thị bài đăng ít liên quan nhất và 5 đại diện cho bài đăng có độ liên quan cao nhất.
4. **Lựa chọn Top-K (Top Selection):** 4 bài đăng hàng đầu được chọn ra từ 10 bài đăng dựa trên các điểm số đã được gán.
5. **Hợp nhất và hiển thị (Aggregation & Presentation):** 4 bài đăng hàng đầu được kết hợp và trình bày trên dòng thời gian (timeline) của Bob theo thứ tự giảm dần của điểm số được gán.

Hình sau minh họa 4 bài đăng hàng đầu được hiển thị trên dòng thời gian của Bob:

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p020_01.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p020_02.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p020_03.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p020_04.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p020_05.png)

*Một bảng tin gồm 4 bài đăng hàng đầu dựa trên các điểm số liên quan:*
* Điểm liên quan = 5 (Relevance score = 5)
* Điểm liên quan = 4 (Relevance score = 4)
* Điểm liên quan = 3 (Relevance score = 3)
* Điểm liên quan = 2 (Relevance score = 2)

Xếp hạng bảng tin bằng các thuật toán máy học và xếp hạng khác nhau là một tác vụ tiêu tốn nhiều tài nguyên tính toán (computationally intensive task). Trong thiết kế của chúng ta, dịch vụ xếp hạng (Ranking Service) thực hiện việc xếp hạng bài đăng và xây dựng các bảng tin. Dịch vụ này bao gồm các hệ thống xử lý dữ liệu lớn (big-data processing systems) có thể sử dụng phần cứng chuyên dụng như bộ xử lý đồ họa (GPUs - Graphics Processing Units) và bộ xử lý tensor (TPUs - Tensor Processing Units).

> [!NOTE]
> **Theo Facebook:**
> *"Đối với mỗi người trên Facebook, chúng tôi cần đánh giá hàng nghìn đặc trưng (features) để xác định điều gì người đó có thể thấy phù hợp nhất nhằm dự đoán những gì mỗi người trong số họ muốn xem trên bảng tin của mình."*
>
> Điều này hàm ý rằng chúng ta cần năng lực tính toán khổng lồ (enormous computational power) và các thuật toán học máy phức tạp (sophisticated learning algorithms) để kết hợp tất cả các đặc trưng nhằm tạo ra một bảng tin chất lượng tốt trong một khoảng thời gian ngắn hợp lý.

![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p021_00.png)
![032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](images/topic_032_p021_01.png)

---

## 3. Tổng Hợp Toàn Bộ Kiến Trúc Hệ Thống (Putting Everything Together)

*Quay lại (Back) | Yêu cầu của Hệ thống Bảng tin... (Requirements of a Newsfeed Syste…) | Đánh dấu hoàn thành (Mark As Completed) | Tiếp theo (Next) | Đánh giá Hệ thống Bảng tin... (Evaluation of a Newsfeed System’s …)*

Sơ đồ sau đây tổng hợp toàn bộ các dịch vụ liên quan đến thiết kế chi tiết của hệ thống bảng tin:

### Thiết kế chi tiết của hệ thống bảng tin (The detailed design of newsfeed system)

* **Bộ cân bằng tải (Load Balancer)**
* **Máy khách (Clients)**
* **Máy chủ Web (Web Servers)**
* **Dịch vụ bảng tin (Newsfeed Service)**
* **Dịch vụ thông báo (Notification Service)**
* **Dịch vụ xuất bản bảng tin (Newsfeed Publishing Service)**
* **Dịch vụ bài đăng (Post Service)**
* **Lưu trữ Blob (Blob Storage)**
* **Bộ nhớ đệm người dùng (User Cache)**
* **Bộ nhớ đệm bài đăng (Post Cache)**
* **Cơ sở dữ liệu đồ thị (Graph Database)**
* **Cơ sở dữ liệu người dùng (User Database)**
* **Cơ sở dữ liệu bài đăng (Post Database)**
* **Các máy chủ bộ nhớ đệm bảng tin chứa các bảng tin đã được xây dựng và bảng tin đã xếp hạng (Newsfeed Cache Servers holding constructed feeds and ranked feeds)**
* **Dịch vụ xếp hạng (Ranking Service)**
* **Mạng phân phối nội dung (CDN - Content Delivery Network)**
* **Cơ sở dữ liệu bảng tin (Newsfeed Database)**

Trong bài học này, chúng ta đã thảo luận về thiết kế tổng thể của hệ thống bảng tin, lược đồ cơ sở dữ liệu (Database Schema) và hệ thống xếp hạng bảng tin (Newsfeed Ranking System). Trong bài học tiếp theo, chúng ta sẽ đánh giá các yêu cầu của hệ thống.

---

## 4. Đánh Giá Thiết Kế Hệ Thống Bảng Tin (Evaluation of a Newsfeed System's Design)

Đánh giá thiết kế bảng tin đối với các yêu cầu phi chức năng (Non-Functional Requirements) của nó.

Chúng ta sẽ bao gồm các nội dung sau:
* Đáp ứng các yêu cầu (Fulfill requirements)
* Câu đố về thiết kế hệ thống bảng tin (Quiz on the newsfeed system’s design)
* Tóm tắt (Summary)

### Đáp Ứng Các Yêu Cầu (Fulfill Requirements)

Các yêu cầu phi chức năng cho thiết kế hệ thống bảng tin được đề xuất bao gồm: **Khả năng mở rộng (Scalability)**, **Khả năng chịu lỗi (Fault Tolerance)**, **Tính sẵn sàng cao (Availability)** và **Độ trễ thấp (Low Latency)**. Hãy cùng thảo luận cách hệ thống được đề xuất đáp ứng các yêu cầu này:

1. **Khả năng mở rộng (Scalability):** Hệ thống được đề xuất có khả năng mở rộng để xử lý số lượng người dùng ngày càng tăng. Các tài nguyên cần thiết, bao gồm bộ cân bằng tải (Load Balancers), máy chủ web (Web Servers) và các máy chủ liên quan khác, được thêm vào hoặc gỡ bỏ theo nhu cầu (on-demand).
2. **Khả năng chịu lỗi (Fault Tolerance):** Việc sao chép dữ liệu (Replication) bao gồm siêu dữ liệu của người dùng (user metadata), bài đăng và bảng tin giúp hệ thống có khả năng chịu lỗi. Hơn nữa, các tài nguyên dự phòng (redundant resources) luôn sẵn sàng để xử lý sự cố hỏng hóc của một máy chủ hoặc thành phần của nó.
3. **Tính sẵn sàng (Availability):** Hệ thống đạt mức độ sẵn sàng cao (High Availability) bằng cách cung cấp các máy chủ dự phòng và sao chép dữ liệu trên chúng. Khi người dùng bị ngắt kết nối do lỗi ở máy chủ, phiên làm việc sẽ được tái lập thông qua bộ cân bằng tải tới một máy chủ khác. Hơn nữa, dữ liệu (siêu dữ liệu người dùng, bài đăng và bảng tin) được lưu trữ trên các cụm cơ sở dữ liệu khác nhau và có tính dự phòng (redundant database clusters), mang lại tính sẵn sàng cao và độ bền vững dữ liệu (durability).
4. **Độ trễ thấp (Low Latency):** Chúng ta có thể giảm thiểu độ trễ của hệ thống ở nhiều cấp độ khác nhau bằng cách:
   * **Các máy chủ phân tán theo vị trí địa lý (Geographically distributed servers)** và bộ nhớ đệm (cache) liên kết với chúng. Bằng cách này, chúng ta đưa dịch vụ đến gần hơn với người dùng.
   * **Sử dụng CDN (Content Delivery Networks)** cho các bảng tin và nội dung đa phương tiện (media content) được truy cập thường xuyên.

---

## 5. Câu Đố Về Thiết Kế Hệ Thống Bảng Tin (Quiz on the Newsfeed System's Design)

Kiểm tra mức độ hiểu biết của bạn về các khái niệm liên quan đến thiết kế hệ thống bảng tin với một bài kiểm tra ngắn.

> **Câu hỏi:** Thành phần nào chịu trách nhiệm lưu trữ các mối quan hệ giữa người dùng, bạn bè và những người theo dõi của họ? *(Which component is responsible for storing relationships between users, their friends, and followers?)*
>
> *Đặt lại câu đố (Reset Quiz) | Câu hỏi 1 trên 4 (Question 1 of 4) | 0 lần thử (0 attempted) | Gửi câu trả lời (Submit Answer)*

---

## 6. Tóm Tắt (Summary)

Trong chương này, chúng ta đã học cách thiết kế một hệ thống bảng tin ở quy mô lớn (at scale). Thiết kế của chúng ta đã xếp hạng khối lượng dữ liệu khổng lồ của người dùng để hiển thị nội dung được tuyển chọn cẩn thận nhằm mang lại trải nghiệm người dùng tốt hơn và tăng mức độ tương tác (engagement). Thiết kế bảng tin của chúng ta đủ tổng quát để có thể áp dụng ở nhiều hệ thống thực tế như bảng tin Twitter (Twitter feeds), bài đăng Facebook (Facebook posts), hệ thống gợi ý của YouTube và Instagram (YouTube and Instagram recommendations), các ứng dụng tin tức (News applications), v.v.

---

### Trang 25

[Quay lại (Back)]

## Thiết Kế Hệ Thống Bảng Tin (Design of a Newsfeed System)

[Đánh dấu Đã hoàn thành (Mark As Completed)]

[Tiếp theo (Next)]

## Thiết Kế Hệ Thống: Instagram (System Design: Instagram)

---

> [!NOTE]
> Đoạn văn bản nguồn trên là các nút điều hướng chuyển trang (Navigation Controls) và tiêu đề liên kết giữa hai chủ đề kiến trúc hệ thống phân tán: **Thiết Kế Hệ Thống Bảng Tin (Design of a Newsfeed System)** và **Thiết Kế Hệ Thống: Instagram (System Design: Instagram)**. Toàn bộ nội dung và cấu trúc nguyên bản đã được chuyển ngữ đầy đủ và chính xác 100%.


---

[← Bài trước](031-thiet-ke-twitter.md) | [Mục lục](README.md) | [Bài tiếp theo →](033-thiet-ke-instagram.md)
