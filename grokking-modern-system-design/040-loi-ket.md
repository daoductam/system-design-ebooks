# 040 - Lời Kết & Lời Khuyên Cho Kỹ Sư Hệ Thống

[← Bài trước](039-that-bai-kinh-dien.md) | [Mục lục](README.md) | [Bài tiếp theo →](README.md)

---


# 040 - Lời Kết & Tổng Kết Khóa Học Thiết Kế Hệ Thống (Conclusions)

![040 - Lời Kết & Lời Khuyên Cho Kỹ Sư Hệ Thống](images/topic_040_p001_00.png)

## Lời Kết (Conclusions)

Hãy cùng tổng kết lại những gì chúng ta đã học trong khóa học này.

Trước khi kết luận, chúng tôi xin chúc mừng bạn đã hoàn thành một khóa học đầy thách thức như vậy!

Trong suốt khóa học này, chúng ta đã tiếp cận hoạt động thiết kế hệ thống (**System Design**) dưới lăng kính của các khối kiến trúc cơ bản (**Basic Building Blocks**) — đó là các hệ thống con cốt lõi (**fundamental subsystems**) được kết hợp lại để tạo nên một hệ thống lớn hơn. Phương pháp tiếp cận này cho phép chúng ta tập trung chuyên sâu vào các kịch bản nghiệp vụ cụ thể (**specific business use cases**) thay vì phải lặp lại các khái niệm tuần hoàn.

Chúng tôi đã cẩn trọng lựa chọn các bài toán thiết kế từ nhiều lĩnh vực nghiệp vụ khác nhau, và đã nỗ lực làm rõ các khía cạnh độc bản hoặc các thách thức kỹ thuật đặc thù trong từng bài toán thiết kế hệ thống đó.

---

## Các Khía Cạnh Độc Bản Của Từng Bài Toán Thiết Kế (Unique Aspects of Each Design Problem)

| Bài Toán Thiết Kế (Design Problem) | Khía Cạnh Độc Bản Của Thiết Kế (Unique Aspect of Design) |
| :--- | :--- |
| **YouTube** | Xây dựng các kho lưu trữ dữ liệu tùy biến (**custom data stores**) như **Vitess** và **BigTable** nhằm đáp ứng nhu cầu mở rộng quy mô (**Scalability**). |
| **Quora** | Phân mảnh dọc (**Vertical Sharding**) cơ sở dữ liệu MySQL nhằm đáp ứng yêu cầu về khả năng mở rộng quy mô (**Scalability**). |
| **Google Maps** | Sử dụng kỹ thuật phân đoạn bản đồ (**segmentation of a map**) nhằm đáp ứng nhu cầu mở rộng quy mô (**Scalability**) và đạt được tính sẵn sàng cao (**High Availability**). |
| **Yelp** | Sử dụng cấu trúc dữ liệu cây tứ phân (**Quadtrees**) để truy xuất tốc độ cao đối với dữ liệu không gian (**spatial data**). |
| **Uber** | Dịch vụ thanh toán (**payment service**) cải tiến nhằm đảm bảo phát hiện gian lận (**fraud detection**), và ghép nối tài xế với khách hàng thông qua bản đồ (**matching drivers using maps**). |
| **Twitter** | Sử dụng các bộ cân bằng tải phía client (**client-side load balancers**) cho nhiều dịch vụ với hàng nghìn kết nối nhằm giảm thiểu độ trễ (**Latency**). |
| **Newsfeed** | Hệ thống gợi ý (**recommendation system**) nhằm đảm bảo xếp hạng (**ranking**) và đưa ra các đề xuất bài viết (**feed suggestions**). |
| **Instagram** | Một ví dụ hoàn hảo về cách các khối kiến trúc nền tảng (**building blocks**) khác nhau kết hợp lại để xây dựng nên một hệ thống vừa có khả năng mở rộng quy mô (**scalable**) vừa đạt hiệu năng cao (**performant system**). |
| **TinyURL** | Mã hóa định danh (**Encoding IDs**) theo hệ thống cơ số 58 (**Base-58 system**) để tạo các URL rút gọn duy nhất. |
| **Web Crawler** | Phát hiện, nhận diện và xử lý các bẫy thu thập dữ liệu web (**Web crawler traps**). |
| **WhatsApp** | Quản lý tin nhắn cho người dùng đang ngoại tuyến (**offline users**). |
| **Typeahead** | Ứng dụng cấu trúc dữ liệu cây tiền tố (**Trie**) hiệu năng cao để cung cấp các gợi ý tìm kiếm theo thời gian thực. |
| **Google Docs** | Quản lý tương tranh (**Concurrency management**) cho các thao tác ghi đồng thời (**simultaneous writes**), sử dụng các kỹ thuật như Biến đổi thao tác (**Operational Transformation - OT**) và Kiểu dữ liệu sao chép không xung đột (**Conflict-free Replicated Data Type - CRDT**). |

> [!NOTE]
> Tại thời điểm này, chúng ta đã hoàn thiện bộ công cụ thiết kế hệ thống (**system design toolbox**) của mình, và giờ đây chúng ta có thể tự tin lựa chọn đúng công cụ cho từng bài toán thực tế phía trước.

> [!TIP]
> Chúng tôi hy vọng rằng khóa học này đã giúp bạn tích lũy đầy đủ kiến thức để phân tích, thiết kế các bài toán mới cũng như kiến trúc các giải pháp hoàn chỉnh dựa trên các khối thành phần cốt lõi (**building blocks**). Hãy áp dụng ngay những kiến thức thiết kế hệ thống này vào thực tế để kiến tạo nên những hệ thống phân tán xuất sắc!

---

## Hoàn Thành Khóa Học (Course Completion)

- **[Quay lại (Back)]**
- **AWS Wide Spread Outage** (Sự Cố Gián Đoạn Diện Rộng Của AWS)
- **[Đánh dấu đã hoàn thành (Mark As Completed)]**

Cuối cùng, chúng tôi xin gửi lời cảm ơn chân thành tới bạn vì đã dành thời gian và nỗ lực để hoàn thành toàn bộ khóa học này! 

Chúng tôi hy vọng đây là một trải nghiệm học tập tuyệt vời đối với bạn. Xin vui lòng gửi email hoặc để lại bình luận trên diễn đàn cộng đồng của chúng tôi đối với bất kỳ ý kiến đóng góp hay đề xuất nào mà bạn có.

**— Đội ngũ Educative (Team Educative)**


---

[← Bài trước](039-that-bai-kinh-dien.md) | [Mục lục](README.md) | [Bài tiếp theo →](README.md)
