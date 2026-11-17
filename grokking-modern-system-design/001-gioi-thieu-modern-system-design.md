# 001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại

[← Bài trước](000-muc-luc-khoa-hoc.md) | [Mục lục](README.md) | [Bài tiếp theo →](002-phong-van-system-design.md)

---


# Giới Thiệu Thiết Kế Hệ Thống Hiện Đại (Introduction to Modern System Design)

Cung cấp cái nhìn tổng quan về các chủ đề chúng ta sẽ cùng tìm hiểu trong khóa học này.

---

### Nội dung bao gồm các chủ đề sau:
* **Thiết kế hệ thống là gì? (What is system design?)**
* **Thiết kế hệ thống hiện đại sử dụng các khối xây dựng nền tảng (Modern system design using building blocks)**
* **Về khóa học này (About this course)**
* **Ai nên tham gia khóa học này? (Who should take this course?)**
* **Điều kiện tiên quyết của khóa học (Prerequisites for this course)**

---

## 1. Thiết kế hệ thống là gì? (What is system design?)

**Thiết kế hệ thống (System design)** là quá trình định nghĩa các thành phần (components) và sự tích hợp giữa chúng, các giao diện lập trình ứng dụng (APIs), cũng như các mô hình dữ liệu (data models) nhằm xây dựng các hệ thống quy mô lớn (large-scale systems) đáp ứng trọn vẹn một tập hợp các **yêu cầu chức năng (functional requirements)** và **yêu cầu phi chức năng (non-functional requirements)** đã đề ra.

Thiết kế hệ thống vận dụng các khái niệm cốt lõi của **mạng máy tính (computer networking)**, **tính toán song song (parallel computing)** và **các hệ thống phân tán (distributed systems)** để kiến tạo nên những hệ thống có khả năng mở rộng tốt (scale well) và đạt hiệu năng cao (performant). Về bản chất tự nhiên, các hệ thống phân tán có khả năng mở rộng rất tốt. Tuy nhiên, chúng cũng vốn mang tính phức tạp nội tại rất cao (inherently complex). Kỷ luật và phương pháp luận của thiết kế hệ thống chính là công cụ giúp chúng ta chế ngự sự phức tạp này và hoàn thành công việc một cách hiệu quả.

```
+-------------------------------------------------------+
|                    System design                      |
|                  (Thiết kế hệ thống)                  |
+---------------------------+---------------------------+
                            |
         +------------------+------------------+
         |                                     |
+--------v---------+                 +---------v--------+
|    Computer      |                 |   Distributed    |
|   networking     |                 |     systems      |
|  (Mạng máy tính) |                 | (Hệ thống phân   |
+--------+---------+                 |      tán)        |
         |                           +---------+--------+
         |                                     |
         +------------------+------------------+
                            |
                  +---------v---------+
                  | Parallel computing|
                  |(Tính toán song    |
                  |       song)       |
                  +-------------------+
```

Thiết kế hệ thống hướng tới mục tiêu xây dựng các hệ thống có tính **đáng tin cậy (reliable)**, **hiệu quả (effective)** và **dễ bảo trì (maintainable)**, cùng với nhiều đặc tính quan trọng khác:

* **Hệ thống đáng tin cậy (Reliable systems):** Xử lý và khắc phục hiệu quả các sự cố (faults), hỏng hóc (failures) và lỗi phát sinh (errors).
* **Hệ thống hiệu quả (Effective systems):** Đáp ứng đầy đủ mọi nhu cầu của người dùng và các yêu cầu nghiệp vụ (business requirements).
* **Hệ thống dễ bảo trì (Maintainable systems):** Linh hoạt và dễ dàng mở rộng quy mô tăng lên hoặc thu hẹp lại (scale up or down). Khả năng bổ sung tính năng mới cũng thuộc phạm vi của tính dễ bảo trì.

---

## 2. Thiết kế hệ thống hiện đại sử dụng các khối xây dựng nền tảng (Modern system design using building blocks)

Chúng tôi đã tách biệt các thành phần thiết kế thường dùng—chẳng hạn như **bộ cân bằng tải (Load Balancers)**—thành các **khối xây dựng cơ bản (basic building blocks)** phục vụ cho việc thiết kế hệ thống ở mức kiến trúc cấp cao (high-level system design). Cách tiếp cận này giải quyết hai mục đích cốt lõi:

1. **Thứ nhất:** Cho phép chúng ta mổ xẻ, thảo luận chi tiết từng khối xây dựng và giải quyết các bài toán thiết kế thu nhỏ (mini-design problems) đầy thú vị của riêng chúng.
2. **Thứ hai:** Khi bước vào giải quyết một bài toán thiết kế cụ thể, chúng ta có thể tập trung hoàn toàn vào các khía cạnh đặc thù của bài toán đó, chỉ rõ khối xây dựng nào sẽ được sử dụng và cách phối hợp chúng ra sao. Điều này giúp loại bỏ triệt để việc lặp lại các cuộc thảo luận về những thành phần thiết kế phổ biến.

Chúng tôi đã xác định **16 khối xây dựng nền tảng (sixteen building blocks)** đóng vai trò quyết định trong việc thiết kế các hệ thống hiện đại.

> [!NOTE]
> **Các hệ thống hiện đại được thiết kế dựa trên các khối xây dựng nền tảng (Modern systems are designed using fundamental building blocks):**
> 
> *Khối xây dựng nền tảng (Building Blocks) $\rightarrow$ Thiết kế hệ thống hiện đại (Modern System Design)*

---

## 3. Về khóa học này (About this course)

Khóa học này tập trung vào việc thiết kế các hệ thống có khả năng **mở rộng quy mô (scalability)** khi lượng người dùng tăng vọt, duy trì **tính sẵn sàng cao (High Availability)** ngay cả khi đối mặt với nhiều loại lỗi/hỏng hóc khác nhau (**Fault Tolerance**), và đáp ứng các mục tiêu chức năng với **hiệu năng (performance)** xuất sắc. 

Trong thực tế, xây dựng hệ thống là một **quá trình lặp liên tục (iterative process)**: chúng ta bắt đầu với một bản thiết kế tương đối tốt, đo lường và đánh giá hiệu năng thực tế của nó, sau đó tối ưu hóa và cải tiến thiết kế ở chu kỳ lặp kế tiếp.

Trọng tâm của khóa học là đưa người học đắm chìm vào những nỗ lực thiết kế hệ thống được tuyển chọn kỹ lưỡng, trang bị đầy đủ năng lực để tự tin giải quyết bất kỳ bài toán thiết kế mới lạ nào—dù là trong một buổi phỏng vấn thiết kế hệ thống (system design interview) hay một dự án thực tế tại doanh nghiệp. Khóa học hướng tới việc **truyền tải bản chất của các khái niệm** thay vì đưa ra các bản thiết kế mẫu rập khuôn (boilerplate designs). 

Dưới đây là những khoảng trống kiến thức quan trọng mà khóa học này hướng tới khỏa lấp:

---

### Một góc nhìn mới mẻ về thiết kế hệ thống (A fresh look at system design)
Nhiều khóa học thiết kế hệ thống thường đưa ra một "công thức đóng khung" để giải quyết một bài toán cụ thể. Điều này có vẻ hấp dẫn trong các tình huống chịu áp lực cao như phỏng vấn, nhưng nó lại cổ xúy việc ghi nhớ máy móc một giải pháp có sẵn thay vì thực sự thấu hiểu tường tận gốc rễ vấn đề để đưa ra phương án xử lý thích hợp. 

Nếu thiết kế hệ thống chỉ đơn thuần là việc áp dụng công thức, có lẽ chúng ta đã không cần đến con người để làm công việc này. Thiết kế hệ thống vừa là một môn **khoa học**, vừa là một **nghệ thuật**; và việc tiếp cận một bài toán thiết kế từ **các nguyên lý nền tảng đầu tiên (first principles)** sẽ mang lại một tư duy hoàn toàn mới mẻ, đột phá.

![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p002_00.png)
![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p002_01.png)
![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p002_02.png)
![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p002_03.png)
![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p002_04.png)
![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p002_05.png)
![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p002_06.png)

---

### Đi sâu và mở rộng toàn diện (Going deep and broad)
Chúng ta sẽ giải quyết một số bài toán truyền thống quen thuộc, nhưng đi kèm với các cuộc thảo luận chuyên sâu đa chiều. Chúng tôi cung cấp những lý giải xác đáng, rõ ràng về lý do tại sao một thành phần lại được lựa chọn bất chấp các yếu tố phải đánh đổi (**tradeoffs**). 

> [!TIP]
> **Ví dụ điển hình:** Chúng tôi giải thích cặn kẽ tại sao lại sử dụng một cơ sở dữ liệu cụ thể (database), một hệ thống lưu bộ nhớ đệm (caching system), hay một kỹ thuật cân bằng tải (load balancing technique) xác định trong từng bản thiết kế.

Đồng thời, khóa học cũng giải quyết các bài toán thiết kế hoàn toàn mới mẻ, chạm tới không chỉ **khả năng mở rộng (Scalability)** mà còn là **tính sẵn sàng (High Availability)**, **tính dễ bảo trì (Maintainability)**, **tính nhất quán (Consistency)**, và **khả năng chịu lỗi (Fault Tolerance)**. Tổng thể, các bài toán truyền thống kết hợp cùng các bài toán hiện đại sẽ bao quát toàn bộ mọi khía cạnh của công việc thiết kế hệ thống ngày nay. Kỳ vọng của chúng tôi là khóa học này sẽ chuẩn bị nền tảng vững chắc nhất để học viên giải quyết hiệu quả bất kỳ thách thức thiết kế mới nào gặp phải.

Các hệ thống thực tế vô cùng phức tạp, và thông thường, chúng ta cần đưa ra các giả định hợp lý để giới hạn phạm vi bài toán (scope a problem) một cách chính xác. Chúng tôi đào sâu chi tiết từng bài toán để người học nắm bắt trọn vẹn bản chất của các hệ thống ngoài đời thực.

![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p003_00.png)

---

### Quy trình lặp liên tục (Iterative process)
Trong thực tế, các hệ thống luôn được hoàn thiện qua từng chu kỳ lặp. Chúng ta thường khởi đầu bằng một kiến trúc đơn giản, nhưng khi các điểm nghẽn cổ chai (**bottlenecks**) nảy sinh ở một hoặc nhiều thành phần, một bản thiết kế mới cải tiến trở nên tất yếu. 

Trong một số bài toán thiết kế, chúng ta sẽ dựng lên một bản thiết kế ban đầu, xác định rõ các điểm nghẽn, và tiến hành nâng cấp nó. Khi phải làm việc dưới áp lực hạn hẹp về mặt thời gian, bạn có thể không có đủ điều kiện để lặp đi lặp lại nhiều lần. Tuy nhiên, chúng tôi vẫn khuyến nghị quy trình chuẩn gồm **hai vòng lặp**:
1. **Vòng lặp đầu tiên:** Nỗ lực tối đa để đưa ra một bản thiết kế khả thi (chiếm khoảng 80% quỹ thời gian của bạn).
2. **Vòng lặp thứ hai:** Dành cho việc tinh chỉnh, khắc phục điểm nghẽn và cải tiến.

Một lựa chọn khác là linh hoạt điều chỉnh thiết kế ngay khi chúng ta phát hiện ra những góc nhìn thấu đáo mới (new insights). Chắc chắn rằng, khi càng dành nhiều thời gian nghiên cứu sâu một bài toán, chúng ta sẽ càng khám phá ra những chi tiết kỹ thuật mới giá trị.

![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p004_00.png)
![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p004_01.png)

---

### Học tập tương tác chủ động (Interactive learning)
Chúng tôi mang đến rất nhiều cơ hội thực hành để bạn tích lũy kinh nghiệm thiết kế hệ thống thực chiến:
* Một số bài toán sẽ hướng dẫn người học từng bước một qua lộ trình chi tiết để kiến tạo nên hệ thống hoàn chỉnh.
* Chúng tôi cũng cung cấp các ví dụ thực tế nơi người học phải tự tay thiết kế toàn bộ hệ thống từ đầu đến cuối (**end-to-end**) mà không có bất kỳ bước gợi ý sẵn nào.
* Các khái niệm quan trọng sẽ được củng cố và khắc sâu thông qua hệ thống câu hỏi tình huống và các bài kiểm tra trắc nghiệm (quizzes).

![001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](images/topic_001_p005_00.png)

---

## 4. Ai nên tham gia khóa học này? (Who should take this course?)

Thiết kế hệ thống dành cho bất kỳ kỹ sư phần mềm nào khao khát thăng tiến vượt bậc trong sự nghiệp của mình:

### 1. Chuẩn bị phỏng vấn (Interview preparation)
Thời gian gần đây, thiết kế hệ thống đã trở thành một phần trọng yếu không thể thiếu trong các vòng phỏng vấn tuyển dụng kỹ sư phần mềm. Khóa học này hỗ trợ đắc lực cho các kỹ sư chuẩn bị tốt nhất cho phỏng vấn. Chúng tôi có một cẩm nang hướng dẫn chi tiết và bài bản về quy trình chuẩn bị phỏng vấn thiết kế hệ thống tại **Chương 2** của khóa học dành cho các học viên quan tâm.

### 2. Kỹ sư phát triển phần mềm (Software developers)
Thiết kế hệ thống trước hết hướng đến các **Back-end Developers** đang phấn đấu trở thành **Principal Engineers** hoặc **Solution Architects**. Lý do là vì các kỹ sư này là những người trực tiếp tiếp nhận và xử lý dữ liệu thực tế của người dùng. Một khi dữ liệu được tầng giao diện (Frontend) gửi về các hệ thống Back-end, việc xử lý dữ liệu một cách hiệu quả, an toàn và tối ưu chính là yếu tố quyết định sự thành bại của toàn bộ ứng dụng. 

Song song đó, các lập trình viên **Full-stack** hoặc **Front-end** cũng rất cần học thiết kế hệ thống để nâng cao tầm nhìn và chất lượng công việc của mình. Đồng thời, các kỹ sư đảm bảo độ tin cậy hệ thống (**SREs - Site Reliability Engineers**) làm việc theo ca trực on-call trong môi trường Production luôn phải đối mặt với muôn vàn sự cố phức tạp mỗi ngày; kiến thức thiết kế hệ thống sẽ giúp các SRE nhanh chóng và chuẩn xác tìm ra nguyên nhân gốc rễ (**root causes**) của những sự cố phức tạp đó.

### 3. Giám đốc sản phẩm / Quản lý dự án (Product/Project managers)
Thách thức to lớn trong quản lý sản phẩm và dự án là làm sao xây dựng được những hệ thống có khả năng mở rộng tốt (**scale well**) và duy trì hiệu năng cao (**perform effectively**) bền bỉ theo thời gian. Những nhà quản lý am hiểu sâu về thiết kế hệ thống có thể dẫn dắt, định hướng kiến trúc cho các hệ thống quy mô lớn đạt hiệu năng vượt trội. Do đó, việc thấu hiểu các khái niệm thiết kế hệ thống là điều tối quan trọng để các Product/Project Manager dẫn dắt quá trình thiết kế và phát triển các ứng dụng thành công.

### 4. Người đam mê học hỏi thiết kế hệ thống (System design learners)
Thiết kế hệ thống là một lĩnh vực cực kỳ thú vị và bất kỳ ai trong ngành công nghệ đều có thể nhận được giá trị to lớn từ nó. Khóa học này giúp học viên hiểu rõ cách thức các tập đoàn công nghệ khổng lồ hàng đầu thế giới thiết kế, xây dựng các ứng dụng thành công từ con số không và liên tục tối ưu chúng qua thời gian. Nhiều học viên khác cũng có thể hiện thực hóa và phát triển ý tưởng khởi nghiệp của riêng mình thành một ứng dụng quy mô lớn nhờ những kiến thức thu nhận từ khóa học này.

---

## 5. Điều kiện tiên quyết của khóa học (Prerequisites for this course)

Chúng tôi mặc định rằng bạn đã nắm vững các **khái niệm cơ bản về hệ thống phân tán (distributed systems)**. Thiết kế hệ thống kế thừa rất nhiều khái niệm tinh hoa từ các hệ thống phân tán. Chúng tôi có một khóa học xuất sắc dành cho những học viên muốn ôn tập và củng cố lại các nền tảng về hệ thống phân tán. 

Bên cạnh hệ thống phân tán, việc trang bị trước một số kiến thức cơ bản về **mạng máy tính (computer networking)** và **hệ điều hành (operating systems)** cũng sẽ hỗ trợ bạn rất nhiều trước khi bước vào khóa học này.

---

# Cấu trúc Khóa học Thiết kế Hệ thống Hiện đại (Course Structure for Modern System Design)

Nắm bắt tổng quan về cấu trúc và những ưu điểm vượt trội của khóa học thiết kế hệ thống (system design) này.

**Chúng ta sẽ bao quát các nội dung sau:**
* **Cấu trúc của khóa học (Structure of the course)**
* **Những điểm mạnh của khóa học (Strengths of the course)**

---

## Cấu trúc của khóa học (Structure of the course)

Khóa học này bao gồm **40 chương**. Các chương này được phân đoạn thành **4 phần** riêng biệt dưới đây:

1. **Phần Giới thiệu (Introduction):** Phần mở đầu bao gồm 5 chương. 
   * Chương đầu tiên giới thiệu về khóa học và các đặc trưng cốt lõi của nó.
   * Chương thứ hai hướng dẫn chi tiết cách chuẩn bị cho một buổi phỏng vấn thiết kế hệ thống (**System Design Interview**).
   * Chương thứ ba thảo luận về các tầng trừu tượng hóa (**abstractions**) khác nhau trong kỹ thuật phần mềm.
   * Tiếp theo, chúng ta phân tích các đặc tính phi chức năng (**non-functional characteristics / non-functional requirements**) thiết yếu mà mọi hệ thống quy mô lớn (**large-scale systems**) bắt buộc phải sở hữu (như **High Availability**, **Scalability**, **Fault Tolerance**, **Latency**, **Throughput**,...).
   * Chúng ta khép lại phần này với các phép tính ước lượng nhanh (**back-of-the-envelope calculations**), kỹ năng cho phép dự toán tài nguyên phần cứng, dung lượng lưu trữ và băng thông trong quá trình giải quyết các bài toán thiết kế.

2. **Các khối kiến trúc nền tảng (Building blocks):** Phần “Building Blocks” bắt đầu bằng một bài học nhập môn giới thiệu **16 khối kiến trúc phân tán cốt lõi**. Mỗi building block sẽ được mổ xẻ, phân tích chi tiết trong một chương độc lập. Chúng ta kết thúc phần này bằng một chương "Tổng kết" (**Conclusion**), đóng vai trò làm cầu nối dẫn nhập sang phần tiếp theo.

3. **Các bài toán thiết kế thực tế (Design problems):** Đây là phần trọng tâm ("the meat") của khóa học, được tinh tuyển kỹ lưỡng từ **13 bài toán thiết kế hệ thống kinh điển và thực tế**.

4. **Phần kết luận (Epilogue):** Phần “Epilogue” tổng kết toàn bộ khóa học, bao gồm 2 chương:
   * Chương thứ nhất phân tích các sự cố sập hệ thống chấn động (**spectacular failures**), minh họa cách mà trong môi trường thực tế (*production*), ngay cả một sơ suất nhỏ cũng có thể đánh sập hoàn toàn một ứng dụng quy mô khổng lồ và thành công rực rỡ. Những sự cố này đôi khi là khó tránh khỏi, nhưng chúng ta sẽ nhấn mạnh các giải pháp giảm thiểu rủi ro (**mitigation measures**) tương ứng.
   * Khóa học sẽ khép lại với chương đúc kết và nhận định tổng quan (**concluding remarks**).

> [!NOTE]
> Mặc dù chúng tôi đã nỗ lực tối đa để giữ cho từng chương có tính độc lập cao nhất có thể, độc giả vẫn sẽ thấy hữu ích nhất khi tiếp cận và đọc chúng theo đúng trình tự được sắp xếp sẵn.

---

## Danh mục cấu trúc khóa học (Course Outline Map)

Dưới đây là sơ đồ liệt kê chi tiết các module và chương học:

### 1. Phần Giới thiệu (Introduction)
* Giới thiệu khóa học (**Introduction**)
* Phỏng vấn Thiết kế Hệ thống là gì? (**System Design Interview**)
* Các tầng trừu tượng hóa trong hệ thống (**Abstractions**)
* Các đặc tính phi chức năng của hệ thống (**Non-functional system characteristics**)
* Các phép tính ước lượng nhanh (**Back-of-the-envelope calculations**)

### 2. Các khối kiến trúc nền tảng (Building Blocks)
* Khái niệm mở đầu về Building Blocks
* Hệ thống phân giải tên miền (**DNS - Domain Name System**)
* Bộ cân bằng tải (**Load Balancers**)
* Cơ sở dữ liệu (**Databases**)
* Kho lưu trữ Khóa - Giá trị (**Key-value store**)
* Mạng phân phối nội dung (**CDN - Content Delivery Network**)
* Bộ sinh định danh tuần tự (**Sequencer / Unique ID Generator**)
* Giám sát phía Client (**Monitoring client-side**)
* Máy chủ giám sát (**Monitoring server**)
* Hệ thống giám sát phân tán (**Distributed monitoring**)
* Bộ nhớ đệm phân tán (**Distributed cache**)
* Hệ thống hàng đợi thông điệp phân tán (**Distributed messaging**)
* Hệ thống Xuất bản - Đăng ký (**Pub-sub system**)
* Bộ điều phối giới hạn tốc độ (**Rate limiter**)
* Kho lưu trữ đối tượng nhị phân lớn (**Blob store / Binary Large Object Store**)
* Công cụ tìm kiếm phân tán (**Distributed search**)
* Hệ thống thu thập và xử lý nhật ký phân tán (**Distributed logging**)
* Bộ lập lịch tác vụ phân tán (**Distributed task scheduler**)
* Bộ đếm phân mảnh (**Sharded counters**)
* Tổng kết các khối kiến trúc (**Concluding building blocks**)

### 3. Các bài toán thiết kế thực tế (Design Problems)
* Thiết kế YouTube (**Design YouTube**)
* Thiết kế Quora (**Design Quora**)
* Thiết kế Google Maps / Google Drive (**Design Google**)
* Thiết kế Yelp (**Design Yelp**)
* Thiết kế Uber (**Design Uber**)
* Thiết kế Twitter (**Design Twitter**)
* Thiết kế Newsfeed mạng xã hội (**Design Newsfeed**)
* Thiết kế Instagram (**Design Instagram**)
* Thiết kế TinyURL (**Design TinyURL**)
* Thiết kế Web Crawler (**Design Web crawler**)
* Thiết kế WhatsApp (**Design WhatsApp**)
* Thiết kế Hệ thống tìm kiếm gợi ý tự động Typeahead (**Design Typeahead**)
* Thiết kế Công cụ tìm kiếm Google (**Design Google Search**)

### 4. Phần kết luận (Epilogue)
* Những sự cố sập hệ thống chấn động trong thực tế (**Spectacular failures**)
* Lời kết và nhận định tổng quan (**Concluding remarks**)

---

## Những điểm mạnh của khóa học (Strengths of the course)

Bên cạnh việc lấp đầy những khoảng trống cốt lõi thường thấy ở các khóa học hiện hành khác, chúng tôi tin tưởng rằng khóa học này sở hữu những thế mạnh vượt trội. Bảng dưới đây tóm tắt các điểm mạnh cùng những lợi thế cạnh tranh của khóa học so với phần còn lại:

| Điểm mạnh (Strengths) | Lợi thế cạnh tranh (Advantage) |
| :--- | :--- |
| **Các khối kiến trúc nền tảng (Building blocks)** | Đây là cách tiếp cận hiện đại đối với thiết kế hệ thống, nơi mà các hệ thống phức tạp được kiến trúc bằng cách ghép nối từ các khối thành phần nhỏ hơn. |
| **Xem Building blocks như các bài toán thiết kế độc lập (Building blocks as design problems)** | Chúng tôi coi mỗi khối kiến trúc nền tảng là một bài toán thiết kế độc lập, hoàn chỉnh và tự thân (*standalone design problem*). |
| **Cải tiến thiết kế từng bước (Incremental improvement to design)** | Giải pháp thiết kế theo từng lớp (**layer-by-layer design**) giải quyết triệt để các điểm nghẽn cổ chai (**bottlenecks**) phát sinh, mang lại giải pháp đơn giản và có tính nâng cấp dần cho các hệ thống phức tạp. |
| **Đánh giá và kiểm chứng thiết kế (Evaluating the design)** | Tính minh bạch và trách nhiệm giải trình của giải pháp thiết kế được đưa ra, chứng minh rõ ràng tính hiệu quả và độ tin cậy của bản thiết kế. |
| **Giải quyết bài toán truyền thống bằng thiết kế cập nhật (Solving the traditional problems with updated designs)** | Khóa học liên tục cập nhật các xu hướng và tiêu chuẩn kỹ thuật thiết kế mới nhất của ngành công nghiệp. |
| **Bổ sung các bài toán thiết kế mới (New design problems added)** | Khóa học mang đến những bản cập nhật hiện đại hóa cho các vấn đề thiết kế hệ thống đã có tuổi đời hàng thập kỷ. |
| **Bộ sưu tập bài toán thiết kế được tinh tuyển (Careful collection of design problems)** | Mỗi bài toán đều mang những khía cạnh độc bản xét trên phương diện bản chất vấn đề và kỹ thuật thiết kế. |
| **Được đóng góp bởi các chuyên gia từ FAANG (Contributions by experts from FAANG)** | Cơ hội học hỏi tư duy kỹ thuật đỉnh cao từ những kỹ sư giỏi nhất trong ngành. |

> [!IMPORTANT]
> **Hãy cùng bắt đầu hành trình chinh phục Thiết kế Hệ thống (System Design) của chúng ta ngay bây giờ!**


---

[← Bài trước](000-muc-luc-khoa-hoc.md) | [Mục lục](README.md) | [Bài tiếp theo →](002-phong-van-system-design.md)
