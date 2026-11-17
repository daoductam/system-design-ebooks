# 002 - Bản Chất Của Phỏng Vấn System Design

[← Bài trước](001-gioi-thieu-modern-system-design.md) | [Mục lục](README.md) | [Bài tiếp theo →](003-cac-tang-truu-tuong-abstractions.md)

---


# Phỏng Vấn Thiết Kế Hệ Thống Là Gì? (What Is a System Design Interview?)

Tìm hiểu về các buổi phỏng vấn thiết kế hệ thống (**System Design Interviews - SDIs**) và cách tiếp cận chúng một cách có chiến lược.

Chúng ta sẽ tìm hiểu các nội dung sau:
* Các buổi phỏng vấn SDI khác biệt như thế nào so với các cuộc phỏng vấn khác?
* Chúng ta xử lý một câu hỏi thiết kế hệ thống như thế nào?
* Trình bày thiết kế mức tổng quan (high-level design)
* Những câu hỏi tiềm năng cho mọi buổi SDI
* Sự tiến hóa trong thiết kế của Google
* Các thách thức trong thiết kế (Design challenges)
* Trách nhiệm của một nhà thiết kế hệ thống (System Designer)
* Ai sẽ phải tham gia phỏng vấn thiết kế hệ thống?
* Lý thuyết và thực hành (Theory and practice)

Khóa học thiết kế hệ thống của chúng tôi đều hữu ích như nhau đối với những người đã đi làm và những ai đang chuẩn bị cho các kỳ phỏng vấn. Trong chương này, chúng tôi nhấn mạnh các khía cạnh khác nhau của một buổi phỏng vấn thiết kế hệ thống (SDI) và một số mẹo hữu ích cho những ai đang chuẩn bị cho buổi phỏng vấn sắp tới. Chúng tôi khuyến khích người học nên đọc chương này ngay cả khi bạn không chuẩn bị phỏng vấn, bởi vì một số chủ đề được đề cập trong chương này có thể áp dụng rộng rãi trong thực tế công việc.

---

## Các Buổi Phỏng Vấn SDI Khác Biệt Như Thế Nào So Với Các Cuộc Phỏng Vấn Khác? (How are SDIs different from other interviews?)

Tương tự như bất kỳ cuộc phỏng vấn nào khác, chúng ta cần tiếp cận các buổi phỏng vấn thiết kế hệ thống một cách có chiến lược. SDI rất khác so với phỏng vấn viết mã (Coding Interviews). Hầu như hiếm khi có bất kỳ yêu cầu viết mã (coding) nào trong buổi phỏng vấn này.

### So sánh các cuộc phỏng vấn khác với phỏng vấn thiết kế hệ thống (Other interviews versus a systems design interview)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p002_00.png)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p002_01.png)

* **Các cuộc phỏng vấn khác (Other Interviews):** Thường tập trung vào cấu trúc dữ liệu, giải thuật, và các chi tiết cài đặt mức thấp.
* **Phỏng vấn thiết kế hệ thống (System Design Interview):** Một buổi SDI diễn ra ở mức độ trừu tượng cao hơn rất nhiều (higher level of abstraction). Chúng ta phân tích, xác định các yêu cầu (requirements) và ánh xạ chúng vào các thành phần tính toán (computational components) cũng như các giao thức truyền thông mức cao (high-level communication protocols) để kết nối các hệ thống con (subsystems) này lại với nhau.

Câu trả lời cuối cùng không phải là yếu tố quyết định. Điều quan trọng cốt lõi là **quy trình tư duy** và **hành trình phân tích** mà một ứng viên xuất sắc dẫn dắt người phỏng vấn trải qua.

> [!NOTE]
> So với các bài toán lập trình trong phỏng vấn tuyển dụng, thiết kế hệ thống phản ánh sát thực tế hơn nhiều đối với những nhiệm vụ mà chúng ta sẽ trực tiếp thực hiện trong công việc hàng ngày.

---

## Chúng Ta Xử Lý Một Câu Hỏi Thiết Kế Như Thế Nào? (How do we tackle a design question?)

Các câu hỏi thiết kế hệ thống luôn là những câu hỏi mở (open-ended), và chúng thường được cố tình đưa ra một cách mơ hồ ngay từ đầu. Sự mơ hồ có chủ đích này mô phỏng chính xác thực tế của môi trường kinh doanh hiện đại.

Người phỏng vấn thường hỏi về một bài toán quen thuộc — ví dụ như thiết kế WhatsApp. Tuy nhiên, một ứng dụng WhatsApp thực tế có vô số tính năng phức tạp, và việc đưa toàn bộ các tính năng đó vào yêu cầu cho bản sao WhatsApp clone của chúng ta có thể không phải là một ý tưởng khôn ngoan vì những lý do sau:

1. **Thứ nhất:** Chúng ta có quỹ thời gian rất giới hạn trong buổi phỏng vấn.
2. **Thứ hai:** Chỉ cần làm việc và giải quyết tốt một số chức năng cốt lõi (core functionalities) của hệ thống là đã đủ để chứng minh năng lực giải quyết vấn đề (problem-solving skills) của chúng ta.

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p003_00.png)

Chúng ta có thể chủ động trao đổi với người phỏng vấn rằng có rất nhiều tính năng khác mà một ứng dụng WhatsApp thực tế sở hữu nhưng chúng ta không dự định đưa vào phạm vi thiết kế lần này. Nếu người phỏng vấn có bất kỳ phản đối hay yêu cầu nào khác, chúng ta hoàn toàn có thể điều chỉnh kế hoạch hành động sao cho phù hợp.

Dưới đây là một số thực hành tốt nhất (**Best Practices**) mà chúng ta nên tuân thủ trong suốt buổi phỏng vấn thiết kế hệ thống:

### Các thực hành tốt nhất cho phỏng vấn thiết kế hệ thống (Best practices for system design interview)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p003_01.png)
* **Làm rõ và chốt chắc các yêu cầu (Solidify the requirements):** Ứng viên cần đặt đúng câu hỏi để làm rõ các yêu cầu chức năng (Functional Requirements) và phi chức năng (Non-Functional Requirements).

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p003_02.png)
* **Xác định rõ phạm vi bài toán (Scope the problem):** Ứng viên cũng cần giới hạn phạm vi bài toán một cách chặt chẽ để có thể đưa ra giải pháp toàn diện và khả thi trong khung thời gian giới hạn của buổi phỏng vấn. Các buổi SDI thông thường chỉ kéo dài khoảng **35 đến 40 phút**.

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p003_03.png)
* **Tương tác tích cực với người phỏng vấn (Engage the interviewer):** Giao tiếp với người phỏng vấn là yếu tố sống còn. Hoàn toàn không nên im lặng tự vẽ hay suy nghĩ thiết kế một mình. Thay vào đó, chúng ta phải liên tục tương tác và trao đổi với người phỏng vấn để đảm bảo họ nắm bắt và đồng thuận với luồng tư duy của chúng ta.

---

## Trình Bày Thiết Kế Mức Tổng Quan (Present the high-level design)

Ở mức độ tổng quan (**High-Level Design**), các thành phần có thể bao gồm: frontend, bộ cân bằng tải (**Load Balancers**), bộ nhớ đệm (**Caches**), hệ thống xử lý dữ liệu (**Data Processing**), lưu trữ dữ liệu (**Data Storage**), và các dịch vụ (**Services**). Thiết kế hệ thống sẽ chỉ ra cách các thành phần này khớp nối và phối hợp với nhau.

Một bản vẽ kiến trúc thường biểu diễn các thành phần dưới dạng các khối hộp (boxes). Các mũi tên kết nối giữa các khối này thể hiện luồng giao tiếp ai đang giao tiếp với ai, cũng như cách các khối hoặc thành phần này kết hợp lại với nhau thành một thể thống nhất.

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p003_04.png)

### Một Thiết Kế Mẫu (A sample design)

Các thành phần điển hình trong một sơ đồ kiến trúc bao gồm:
* **Người dùng (Users)**
* **Bộ cân bằng tải (Load Balancer)**
* **Các dịch vụ (Services)**
* **Bộ nhớ đệm (Cache)**
* **Lưu trữ dữ liệu (Data Storage)**

Chúng ta có thể phác thảo một sơ đồ như hình minh họa ở trên cho bài toán được giao và trình bày chi tiết cho người phỏng vấn.

---

## Những Câu Hỏi Tiềm Năng Cho Mọi Buổi SDI (Possible questions for every SDI)

Các buổi SDI thường xuất hiện những câu hỏi xoay quanh việc một thiết kế sẽ tiến hóa như thế nào theo thời gian khi một khía cạnh nào đó của hệ thống tăng lên theo cấp số nhân (order of magnitude) — ví dụ: số lượng người dùng (**Users**), số lượng truy vấn mỗi giây (**Queries Per Second - QPS**), dung lượng dữ liệu, v.v. Trong cộng đồng kỹ thuật hệ thống, có một nguyên lý phổ biến: **khi một khía cạnh của hệ thống tăng lên gấp 10 lần (10x) trở lên, thiết kế hiện tại có thể không còn trụ vững được nữa và bắt buộc phải thay đổi kiến trúc.**

Việc thiết kế và vận hành một hệ thống lớn hơn đòi hỏi sự tính toán cẩn trọng, bởi vì các thiết kế kiến trúc thường không tự động mở rộng tuyến tính (**linearly scale**) theo sự gia tăng nhu cầu tải của hệ thống.

Một câu hỏi phổ biến khác trong SDI có thể là: *Tại sao chúng ta không thiết kế ngay từ đầu một hệ thống có khả năng xử lý khối lượng công việc vượt xa mức cần thiết hoặc dự đoán?*

> [!IMPORTANT]
> **Chi phí tài chính (Dollar Cost):** Chi phí tài chính gắn liền với các dự án phức tạp chính là lý do trọng yếu giải thích tại sao chúng ta không làm như vậy ngay từ đầu (tránh over-engineering gây lãng phí tài nguyên và chi phí vận hành khổng lồ).

---

## Sự Tiến Hóa Trong Thiết Kế Của Google (The design evolution of Google)

Thiết kế của phiên bản sơ khai của Google Search ngày nay nhìn lại có vẻ đơn giản, nhưng vào thời điểm bấy giờ, nó là một kiến trúc vô cùng tinh vi và đột phá. Nó cũng giúp tối ưu và giữ chi phí ở mức thấp, điều kiện tiên quyết để một công ty khởi nghiệp non trẻ như Google có thể tồn tại và phát triển. 

Bài học rút ra là: mọi quyết định mà chúng ta đưa ra với tư cách là một kỹ sư thiết kế hệ thống đều có tác động trực tiếp đến hoạt động kinh doanh và khách hàng của doanh nghiệp. Chúng ta phải đáp ứng hoặc vượt trên cả kỳ vọng của khách hàng thông qua việc tối ưu hóa và sử dụng tài nguyên một cách hiệu quả nhất.

---

## Các Thách Thức Trong Thiết Kế (Design challenges)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p005_00.png)

Mọi thứ chắc chắn sẽ thay đổi và mọi thứ sẽ hỏng hóc theo thời gian vì những lý do sau:
* **Không có một giải pháp hoặc cách tiếp cận duy nhất đúng** cho một bài toán thiết kế hệ thống.
* Phần lớn giải pháp đều được xây dựng dựa trên **các giả định (assumptions)** mà chúng ta đặt ra ban đầu.

---

## Trách Nhiệm Của Người Thiết Kế Hệ Thống (The responsibility of the designer)

Với tư cách là các nhà thiết kế kiến trúc, chúng ta cần phải xây dựng khả năng chịu lỗi (**Fault Tolerance**) ngay từ cấp độ thiết kế (design level). Lý do là hầu hết các hệ thống hiện đại đều sử dụng các linh kiện phần cứng thương mại đại trà (**off-the-shelf components**), và hệ thống có tới hàng triệu thành phần như vậy. Do đó, chắc chắn sẽ luôn có một bộ phận nào đó bị hỏng hóc tại bất kỳ thời điểm nào, và nhiệm vụ của chúng ta là phải che giấu thực tế không mong muốn này khỏi trải nghiệm của khách hàng.

---

## Ai Sẽ Phải Tham Gia Phỏng Vấn Thiết Kế Hệ Thống? (Who gets a system design interview?)

Theo thông lệ truyền thống, các ứng viên từ cấp độ tầm trung đến cao cấp (**Mid-to-Senior level**) có từ 2 năm kinh nghiệm trở lên sẽ phải trải qua ít nhất một vòng phỏng vấn thiết kế hệ thống. Đối với các ứng viên cấp cao hơn (**Senior, Staff, Principal**), việc có 2 đến 3 vòng phỏng vấn SDI là điều hết sức phổ biến.

Gần đây, các tập đoàn công nghệ lớn cũng đã bắt đầu đưa các câu hỏi thiết kế hệ thống vào vòng phỏng vấn của một số ứng viên mới vào nghề (**Junior candidates**). Do đó, không bao giờ là quá sớm để học thiết kế hệ thống nhằm phát triển bản thân và thậm chí bứt tốc sự nghiệp của chúng ta.

---

## Lý Thuyết Và Thực Hành (Theory and practice)

Phần lớn nền tảng lý thuyết của thiết kế hệ thống đều bắt nguồn từ lĩnh vực **Hệ thống phân tán (Distributed Systems)**. Việc ôn tập và củng cố lại các khái niệm này là điều được đặc biệt khuyến nghị.

Educative cung cấp một khóa học xuất sắc về hệ thống phân tán mà chúng ta có thể sử dụng để làm mới kiến thức về các khái niệm nền tảng này.

Hệ thống phân tán cung cấp cho chúng ta các kim chỉ nam về những nguyên tắc phần mềm chín muồi. Chúng bao gồm các thuộc tính sau:

* **Tính bền bỉ (Robustness):** Khả năng duy trì các hoạt động bình thường trong suốt thời kỳ khủng hoảng/sự cố.
* **Khả năng mở rộng (Scalability):** Năng lực mở rộng quy mô xử lý khi tải tăng cao.
* **Tính sẵn sàng (Availability):** Tỉ lệ thời gian hệ thống hoạt động ổn định và sẵn sàng phục vụ.
* **Hiệu năng (Performance):** Năng lực xử lý với độ trễ thấp (**Low Latency**) và thông lượng cao (**High Throughput**).
* **Khả năng mở rộng tính năng (Extensibility):** Dễ dàng nâng cấp, tích hợp thêm các chức năng mới mà không phá vỡ cấu trúc hiện tại.
* **Khả năng phục hồi (Resiliency):** Khả năng tự phục hồi và quay trở lại trạng thái vận hành bình thường trong một khoảng thời gian chấp nhận được sau khi xảy ra gián đoạn hoặc sự cố.

Các thuật ngữ kỹ thuật chuẩn xác này cũng đóng vai trò như một **ngôn ngữ chung (lingua franca)** kết nối giữa người phỏng vấn và ứng viên.

**Ví dụ:** Chúng ta có thể trình bày rằng: *"Chúng ta cần đưa ra sự đánh đổi (trade-off) giữa Tính sẵn sàng (Availability) và Tính nhất quán (Consistency) khi các thành phần mạng gặp sự cố phân vùng mạng (network partitions), bởi vì Định lý CAP (CAP Theorem) chỉ ra rằng chúng ta không thể đảm bảo đồng thời cả hai yếu tố này khi xảy ra phân vùng mạng."* Việc sử dụng ngôn ngữ chung chuẩn mực này giúp việc giao tiếp trở nên rõ ràng, chuẩn xác và chứng minh rằng chúng ta nắm vững cả lý thuyết nền tảng lẫn thực tiễn triển khai.

> [!TIP]
> **Hãy luôn ghi nhớ:** Trách nhiệm của ứng viên là phải chủ động thể hiện toàn bộ kỹ năng và kiến thức chuyên môn của mình cho người phỏng vấn thấy.

---

# Hướng Dẫn Chuẩn Bị Để Thành Công (How to Prepare for Success)

Nắm bắt tổng quan về các hướng dẫn và tài liệu chuẩn bị cho buổi phỏng vấn.

Chúng ta sẽ bao gồm các nội dung sau:
* **Khóa học này (This course)**
* **Các blog kỹ thuật (Technical blogs)**
* **Đặt câu hỏi vì sao một hệ thống hoạt động (Ask why a system works)**
* **Đi đúng hướng (The right direction)**
* **Phỏng vấn thử nghiệm (Mock interviews)**

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p007_00.png)

Sự chuẩn bị kỹ lưỡng và thực chất là yếu tố bắt buộc để gia tăng cơ hội trúng tuyển vào vị trí công việc mà chúng ta ứng tuyển.

Tùy thuộc vào cấp bậc thâm niên (*seniority*) và mức độ thành thạo của từng ứng viên, mỗi người sẽ cần khoảng thời gian chuẩn bị phỏng vấn khác nhau.

Đối với một ứng viên ở mức trung bình, có thể cần từ **3 đến 4 tháng** để chuẩn bị cho một buổi phỏng vấn thiết kế hệ thống (*System Design Interview*).

---

### Khóa học này (This course)

Khóa học này giúp độc giả học mới hoặc trau dồi lại các kỹ năng thiết kế hệ thống của mình. Chúng tôi đã chọn lọc kỹ lưỡng một số bài toán thiết kế kinh điển cùng những bài toán thiết kế mới mẻ nhằm bao quát chiều sâu lẫn chiều rộng đáng kể của mảng thiết kế hệ thống.

Các hoạt động dưới đây có thể giúp đẩy nhanh quá trình chuẩn bị, đồng thời gia tăng sự phong phú và đào sâu hơn nữa kiến thức của ứng viên.

---

### Các blog kỹ thuật (Technical blogs)

Nhiều công ty thường xuyên công bố các chi tiết kỹ thuật chuyên sâu về những thành tựu quan trọng của họ dưới dạng các bài viết blog kỹ thuật (*technical blogs*).

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p008_00.png)

#### Tại sao các công ty lại hào hứng chia sẻ chi tiết kỹ thuật về công việc của họ?

**Lý do đằng sau:**
* Lý do của việc chia sẻ này là nhằm khơi gợi sự hứng thú trong cộng đồng kỹ thuật về việc công ty đang giải quyết những bài toán hóc búa. Họ cũng kỳ vọng sẽ thúc đẩy, thu hút thêm nhiều nhân tài gia nhập công ty.
* Những bài blog công khai như vậy còn giúp quảng bá các sản phẩm của công ty tới nhóm khách hàng doanh nghiệp (B2B - Business-to-Business).
* Thêm vào đó, nguồn tài liệu này giúp công ty đào tạo trước các nhân sự tiềm năng trong tương lai bằng chính thời gian tự học của họ.

> [!NOTE]
> Luôn có một ranh giới mong manh giữa những gì một công ty cần giữ bí mật vì lợi thế cạnh tranh (*competitive edge*) và những gì có thể công khai ra ngoài cộng đồng.

Chúng ta có thể nghiên cứu các blog này để nắm bắt góc nhìn sâu sắc về những thách thức hoặc bài toán mà công ty đã gặp phải, cũng như những thay đổi mà họ đã thực hiện trong kiến trúc thiết kế để ứng phó với các thách thức đó.

> [!NOTE]
> Việc liên tục cập nhật các cải tiến kỹ thuật này là điều rất quan trọng đối với các kỹ sư chuyên nghiệp, và nó lại càng đặc biệt tối quan trọng đối với một ứng viên đi phỏng vấn.

Một số blog kỹ thuật quan trọng bao gồm:
* **Engineering at Meta**
* **Meta Research**
* **AWS Architecture Blog**
* **Amazon Science Blog**
* **Netflix TechBlog**
* **Google Research**
* **Engineering at Quora**
* **Uber Engineering Blog**
* **Databricks Blog**
* **Pinterest Engineering**
* **BlackRock Engineering**
* **Lyft Engineering**
* **Salesforce Engineering**

> [!NOTE]
> Chúng ta luôn phải đón nhận các tài liệu chưa qua bình duyệt học thuật (*non-peer-reviewed material*) với sự cẩn trọng nhất định (*take with a grain of salt*). Hãy tư duy về những gì các blog trình bày một cách có phản biện và bằng sự nhạy bén kỹ thuật (*technical acumen*) để đánh giá xem điều họ nói có hợp lý hay không. Nếu điều đó chưa hợp lý, đây sẽ là một cơ hội tuyệt vời để thảo luận vấn đề cùng đồng nghiệp và bạn bè.

---

### Đặt câu hỏi vì sao một hệ thống hoạt động (Ask why a system works)

Bằng cách tự đặt ra cho bản thân những câu hỏi đúng đắn, ứng viên có thể suy nghĩ thấu suốt qua những tình huống phức tạp, mập mờ và thiếu dữ kiện (*ambiguous situations*).

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p010_00.png)

* **Tìm hiểu cách các ứng dụng phổ biến hoạt động ở mức kiến trúc cấp cao (*high level*)**: Ví dụ như Instagram, Twitter, v.v.
* **Bắt đầu thấu hiểu và đặt câu hỏi tại sao một thành phần cụ thể lại được sử dụng thay vì một thành phần khác**: Ví dụ: Firebase so với SQL Database.
* **Xây dựng các dự án cá nhân nghiêm túc (*serious side projects*)**: Bắt đầu với một sản phẩm đơn giản, sau đó cải tiến và tối ưu hóa dần dần.
* **Xây dựng một hệ thống từ con số không (*from scratch*)**: Làm quen với toàn bộ quy trình cũng như các chi tiết kỹ thuật trong quá trình kiến thiết hệ thống.
* **Tự xây dựng lại bản sao (*clone*) của một ứng dụng phổ biến mà không cần xem hướng dẫn (*tutorials*)**.

---

### Đi đúng hướng (The right direction)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p010_01.png)

Thiết kế hệ thống (*System Design*) làm việc với các thành phần ở mức kiến trúc cấp cao (*higher level*), và chúng ta cần tránh sa đà vào các chi tiết triển khai cụ thể vụn vặt (*avoid going into the trenches*).

**Chúng ta nên tập trung ít hơn vào cơ chế hoạt động chi tiết (*mechanics*) và tập trung nhiều hơn vào các đánh đổi (*trade-offs*).**

Ví dụ, việc thảo luận xem có nên dùng thư viện Room thay vì dùng SQLite thuần (*raw SQLite*) hay không sẽ không mang lại nhiều giá trị, bởi Room thực chất chỉ là một lớp bọc ngoài (*wrapper*) của SQLite. Một cuộc thảo luận tốt hơn nhiều sẽ là về việc sử dụng cơ sở dữ liệu quan hệ truyền thống như **MySQL** hay sử dụng kho lưu trữ **NoSQL** như **MongoDB**. Hướng thảo luận thứ hai này sẽ giúp chúng ta phân tích và xác định rõ ràng sự đánh đổi (*trade-offs*) giữa hai giải pháp.

Chúng ta nên bắt đầu từ các khía cạnh cấp cao (*high-level stuff*), bởi vì các chi tiết kỹ thuật cấp thấp (*low-level details*) sẽ tự động xuất hiện khi phân tích sâu hơn.

---

### Phỏng vấn thử nghiệm (Mock interviews)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p011_00.png)

Phỏng vấn thử nghiệm (*Mock interviews*) là một cách tuyệt vời để chuẩn bị cho các buổi phỏng vấn thiết kế hệ thống.

Hình thức này bao gồm việc ghép cặp với một người bạn và để họ đặt câu hỏi phỏng vấn. Trong trường hợp không thể nhờ bạn bè, một chiến lược khác là tự ghi âm/ghi hình bản thân và đóng cả hai vai: người phỏng vấn (*interviewer*) lẫn người được phỏng vấn (*interviewee*). Với phương pháp này, chúng ta có thể tự đánh giá, phê bình chính mình hoặc gửi bản ghi cho một người bạn có chuyên môn để nhận phản hồi (*feedback*).

> [!NOTE]
> Vì không có buổi phỏng vấn thử nào có thể mô phỏng hoàn toàn 100% một buổi phỏng vấn thực tế, bạn nên tham gia các buổi phỏng vấn thật tại các công ty. Một khi đã trải qua một hoặc hai buổi phỏng vấn thực tế, chúng ta sẽ có khả năng đánh giá chuẩn xác hơn điều gì mình đã làm tốt và điều gì chưa đạt yêu cầu.

---

# Cách Thể Hiện Tốt Trong Buổi Phỏng Vấn (How to Perform Well)

Nắm bắt các mẹo hữu ích về cách thể hiện trong một buổi phỏng vấn thiết kế hệ thống.

Chúng ta sẽ bao gồm các nội dung sau:
* **Những việc cần làm trong buổi phỏng vấn (What to do during the interview)**
* **Lên chiến lược, sau đó chia để trị (Strategize, then divide and conquer)**
* **Đặt câu hỏi làm rõ và tinh chỉnh yêu cầu (Ask refining questions)**
* **Xử lý dữ liệu (Handle data)**
* **Thảo luận về các thành phần hệ thống (Discuss the components)**
* **Thảo luận về các đánh đổi (Discuss trade-offs)**
* **Những điều không nên làm trong buổi phỏng vấn (What not to do in an interview)**

---

### Những việc cần làm trong buổi phỏng vấn (What to do during the interview)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p012_00.png)

Chúng tôi đặc biệt nhấn mạnh rằng ứng viên cần nỗ lực để tránh thể hiện sự thiếu tính nguyên bản (*unoriginal*). Người phỏng vấn rất có thể đã đặt câu hỏi tương tự cho rất nhiều ứng viên trước đó. Việc tái hiện lại một bản thiết kế rập khuôn, tầm thường (*run-of-the-mill design*) có thể sẽ không gây được ấn tượng với người phỏng vấn.

Đồng thời, buổi phỏng vấn có thể là một tình huống gây nhiều căng thẳng (*stressful situation*). Việc chuẩn bị sẵn một kế hoạch rõ ràng để công phá bài toán (*plan to attack the problem*) là một chiến lược rất tốt. Tùy thuộc vào mỗi ứng viên, có thể có nhiều chiến lược khác nhau để tiếp cận một bài toán thiết kế. Chúng tôi đề xuất kỹ thuật dưới đây:

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p012_01.png)

### Lên chiến lược, sau đó chia để trị (Strategize, then divide and conquer)

Chúng tôi khuyến nghị đưa các hoạt động sau vào tiến trình của buổi phỏng vấn:

---

# Các hoạt động cần đưa vào buổi phỏng vấn (Activities to include in the interview)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p013_00.png)

1. **Đặt các câu hỏi tinh chỉnh (Ask refining questions)**
2. **Xử lý dữ liệu (Handle the data)**
3. **Thảo luận về các thành phần (Discuss the components)**
4. **Thảo luận về sự đánh đổi (Discuss trade-offs)**

---

## 1. Đặt các câu hỏi tinh chỉnh (Ask refining questions)

Chúng ta cần thấu hiểu bài toán thiết kế và các yêu cầu kỹ thuật của nó. Để làm được điều này, chúng ta có thể đóng vai trò như một **Product Manager (Quản lý sản phẩm)** và ưu tiên các tính năng chính bằng cách đặt ra các câu hỏi tinh chỉnh cho người phỏng vấn. 

Mục tiêu cốt lõi là cùng đồng hành với người phỏng vấn trên hành trình làm rõ lý do tại sao thiết kế của chúng ta lại tối ưu. Những buổi phỏng vấn này được thiết kế để đánh giá xem liệu chúng ta có khả năng suy luận một cách logic để chuyển hóa các yêu cầu mơ hồ, chưa rõ ràng thành một hệ thống cụ thể hay không.

Chúng ta phải luôn đảm bảo rằng mình đang giải quyết đúng bài toán. Thông thường, việc chia các yêu cầu thành hai nhóm chính sẽ mang lại hiệu quả rõ rệt:

* **Các yêu cầu mà máy khách (Clients) cần trực tiếp:** Ví dụ: khả năng gửi tin nhắn theo thời gian thực (near real-time) tới bạn bè.
* **Các yêu cầu cần thiết một cách gián tiếp:** Ví dụ: hiệu năng của dịch vụ nhắn tin (messaging service performance) không được suy giảm khi tải người dùng (user load) tăng cao.

> [!NOTE]
> Giới chuyên môn gọi hai nhóm này lần lượt là **Yêu cầu chức năng (Functional Requirements)** và **Yêu cầu phi chức năng (Non-functional Requirements)**.

---

## 2. Xử lý dữ liệu (Handle data)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p014_00.png)

Chúng ta cần xác định và hiểu rõ bản chất của dữ liệu cùng các đặc tính kỹ thuật của nó nhằm tìm kiếm các hệ thống lưu trữ dữ liệu (**Data Storage Systems**) và các thành phần xử lý dữ liệu (**Data Processing Components**) phù hợp cho thiết kế hệ thống.

Dưới đây là một số câu hỏi quan trọng cần tự đặt ra khi tìm kiếm các hệ thống và thành phần phù hợp:

* **Kích thước dữ liệu (Data Size) ở thời điểm hiện tại là bao nhiêu?**
* **Tốc độ tăng trưởng dữ liệu dự kiến theo thời gian (Growth Rate) là bao nhiêu?**
* **Dữ liệu sẽ được tiêu thụ (Data Consumption) bởi các hệ thống con khác hoặc người dùng cuối như thế nào?**
* **Dữ liệu thuộc dạng thiên về đọc (Read-heavy) hay thiên về ghi (Write-heavy)?**
* **Chúng ta cần tính nhất quán nghiêm ngặt (Strict Consistency) của dữ liệu, hay tính nhất quán cuối cùng (Eventual Consistency) là đủ đáp ứng?**
* **Mục tiêu về độ bền vững của dữ liệu (Durability Target) là gì?**
* **Chúng ta cần tuân thủ những yêu cầu nào về quyền riêng tư (Privacy) và quy định pháp lý (Regulatory Requirements) đối với việc lưu trữ hoặc truyền tải dữ liệu người dùng?**

---

## 3. Thảo luận về các thành phần (Discuss the components)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p014_01.png)

### Các thành phần (Components)
Ở một góc độ nhất định, công việc của chúng ta có thể được hiểu là việc xác định xem chúng ta sẽ sử dụng những thành phần nào, chúng sẽ được đặt ở đâu, và cách thức chúng tương tác với nhau ra sao.

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p014_02.png)

Một ví dụ điển hình là việc lựa chọn loại cơ sở dữ liệu — liệu một cơ sở dữ liệu truyền thống mang tính quy chuẩn (Conventional Database / RDBMS) có đáp ứng được không, hay chúng ta nên sử dụng một cơ sở dữ liệu phi quan hệ (NoSQL Database)?

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p014_03.png)

> [!IMPORTANT]
> **Câu hỏi tình huống:**  
> Có thể xảy ra những trường hợp chúng ta có những luận điểm rất thuyết phục để sử dụng cơ sở dữ liệu NoSQL, nhưng người phỏng vấn lại kiên quyết yêu cầu chúng ta phải sử dụng một cơ sở dữ liệu truyền thống (Traditional Database). Chúng ta nên làm gì trong trường hợp này?

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p014_04.png)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p014_05.png)

### Giải pháp (Hide the solution)
Với tư cách là các kỹ sư thiết kế (Designers), chúng ta sẽ phải đối mặt với một nhiệm vụ khó khăn hơn, bởi vì chúng ta sẽ cần phải sử dụng cơ sở dữ liệu truyền thống và phải thực hiện thêm các giải pháp bổ trợ để khắc phục những hạn chế hoặc thách thức kỹ thuật mà nó mang lại.

Trong trường hợp này, về bản chất chúng ta sẽ phải phát minh ra một thành phần kiến trúc mới.

Những tình huống tương tác thực tế như vậy trong các buổi phỏng vấn chính là cơ hội tuyệt vời để chúng ta thể hiện năng lực và tư duy thiết kế hệ thống của mình.

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p015_00.png)

> [!NOTE]
> Chúng ta thường trừu tượng hóa các chi tiết nội tại của các thành phần thành các khối hình hộp (Boxes) và sử dụng các mũi tên (Arrows) để biểu diễn luồng tương tác giữa chúng. Việc định nghĩa các giao diện lập trình hướng người dùng (**User-facing APIs**) ở mức khái quát cao (High-level) có thể hỗ trợ rất tốt trong việc hiểu sâu hơn về dữ liệu hệ thống cũng như các yêu cầu tương tác.

Các thành phần giao diện người dùng (**Front-end components**), bộ cân bằng tải (**Load Balancers**), bộ nhớ đệm (**Caches**), cơ sở dữ liệu (**Databases**), tường lửa (**Firewalls**), và mạng phân phối nội dung (**CDNs - Content Delivery Networks**) chỉ là một vài ví dụ tiêu biểu trong số các thành phần của hệ thống.

---

## 4. Thảo luận về sự đánh đổi (Discuss trade-offs)

Hãy luôn ghi nhớ rằng: **Không có câu trả lời duy nhất đúng cho một bài toán thiết kế.** Nếu chúng ta giao cùng một đề bài cho hai nhóm kỹ sư khác nhau, họ hoàn toàn có thể đưa ra hai thiết kế hoàn toàn khác nhau.

Dưới đây là một số lý do giải thích tại sao lại có sự đa dạng như vậy trong các giải pháp thiết kế:
* **Các thành phần khác nhau luôn có những ưu và nhược điểm (Pros & Cons) khác nhau.** Chúng ta cần cân nhắc kỹ lưỡng xem giải pháp nào là phù hợp nhất với ngữ cảnh của mình.
* **Những sự lựa chọn khác nhau đi kèm với chi phí khác nhau về cả phương diện tài chính lẫn độ phức tạp kỹ thuật (Technical Complexity).** Chúng ta cần tối ưu hóa và sử dụng tài nguyên một cách hiệu quả nhất.
* **Mỗi thiết kế đều tồn tại những điểm yếu nhất định.** Với tư cách là người thiết kế hệ thống, chúng ta phải nhận thức rõ toàn bộ các điểm yếu đó, đồng thời cần chuẩn bị sẵn một kế hoạch tiếp theo (Follow-up plan) để xử lý chúng.

Chúng ta nên chủ động chỉ ra các điểm yếu trong thiết kế của mình cho người phỏng vấn và giải thích lý do tại sao chúng ta chưa giải quyết chúng ở thời điểm hiện tại. 

*Một ví dụ cụ thể:* Thiết kế hiện tại của chúng ta có thể chưa xử lý được mức tải gấp mười lần (10x Load), nhưng chúng ta không dự tính hệ thống sẽ chạm đến ngưỡng tải đó trong tương lai gần. Thay vào đó, chúng ta xây dựng một hệ thống giám sát (**Monitoring System**) để theo dõi sát sao sự tăng trưởng của tải theo thời gian, bảo đảm rằng một thiết kế mới có thể được triển khai kịp thời khi cần. Đây là một ví dụ điển hình cho việc chúng ta **chủ ý giữ lại một điểm yếu kỹ thuật để tối ưu hóa và tiết kiệm chi phí hệ thống**.

Trong một hệ thống phân tán quy mô lớn, luôn có những thành phần gặp sự cố tại bất kỳ thời điểm nào (**Something is always failing in a big system**). Chúng ta bắt buộc phải tích hợp khả năng chịu lỗi (**Fault Tolerance**) và bảo mật (**Security**) vào ngay trong kiến trúc thiết kế của mình.

---

## Những điều không nên làm trong buổi phỏng vấn (What not to do in an interview)

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p016_00.png)

Dưới đây là một số điều chúng ta nên tuyệt đối tránh trong một buổi phỏng vấn thiết kế hệ thống:

* **Không viết mã nguồn (Code) trong phỏng vấn System Design.**
* **Không bắt tay vào xây dựng hệ thống mà không có kế hoạch rõ ràng.**
* **Không làm việc trong im lặng.**
* **Không đưa ra các con số mà không có căn cứ hoặc lý do cụ thể.** Chúng ta phải luôn định hình ngữ cảnh và cơ sở tính toán cho các con số đó.
* **Nếu chúng ta không biết một vấn đề nào đó, đừng che đậy và đừng giả vờ như mình đã biết.**

![002 - Bản Chất Của Phỏng Vấn System Design](images/topic_002_p016_01.png)

> [!NOTE]
> Nếu người phỏng vấn yêu cầu chúng ta thiết kế một hệ thống mà chúng ta chưa từng nghe nói đến bao giờ, hãy thành thật chia sẻ điều đó với họ. Người phỏng vấn hoặc sẽ giải thích bản chất hệ thống đó cho chúng ta, hoặc họ có thể chủ động chuyển sang một câu hỏi khác.


---

[← Bài trước](001-gioi-thieu-modern-system-design.md) | [Mục lục](README.md) | [Bài tiếp theo →](003-cac-tang-truu-tuong-abstractions.md)
