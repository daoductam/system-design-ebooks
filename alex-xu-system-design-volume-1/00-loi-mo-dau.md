# Lời Mở Đầu (Forward & Introduction)

[Mục lục](README.md) | [Chương 01: Quy mô từ 0 đến hàng triệu người dùng →](chuong-01-scale-tu-0-den-trieu-nguoi-dung.md)

---

## System Design Interview: An Insider’s Guide

Bản quyền đã được bảo hộ. Cuốn sách này hoặc bất kỳ phần nào trong đó không được sao chép hoặc sử dụng dưới bất kỳ hình thức nào nếu không có sự cho phép bằng văn bản của nhà xuất bản, ngoại trừ việc sử dụng các đoạn trích ngắn trong một bài đánh giá sách.

### Về tác giả:
**Alex Xu** là một kỹ sư phần mềm giàu kinh nghiệm và là một doanh nhân khởi nghiệp. Trước đây, anh từng làm việc tại Twitter, Apple, Zynga và Oracle. Anh tốt nghiệp bằng Thạc sĩ Khoa học (M.S.) tại Đại học Carnegie Mellon. Anh có niềm đam mê mãnh liệt đối với việc thiết kế và triển khai các hệ thống phức tạp.

- **Email liên hệ:** systemdesigninsider@gmail.com
- **Biên tập viên:** Paul Solomon

---

## LỜI TỰA (FORWARD)

Chúng tôi rất vui mừng vì bạn đã quyết định đồng hành cùng chúng tôi trên con đường học tập và chinh phục các buổi phỏng vấn thiết kế hệ thống (*system design interviews*).

Các câu hỏi phỏng vấn thiết kế hệ thống luôn là thử thách khó khăn nhất trong toàn bộ các vòng phỏng vấn kỹ thuật. Đề bài thường yêu cầu ứng viên phải tự tay thiết kế kiến trúc cho một hệ thống phần mềm hoàn chỉnh, chẳng hạn như hệ thống Bảng tin (News Feed), Tìm kiếm Google (Google Search), Hệ thống Chat trực tuyến (Chat System), v.v. Những câu hỏi dạng này rất dễ gây nản lòng và hoang mang vì không có bất kỳ khuôn mẫu cố định nào để sao chép. Phạm vi của câu hỏi thường rất rộng và mơ hồ. Toàn bộ tiến trình phỏng vấn diễn ra theo hướng mở (*open-ended*) và không hề có một đáp án chuẩn mực duy nhất hay một lời giải tuyệt đối đúng.

Các công ty công nghệ lớn áp dụng rộng rãi vòng phỏng vấn thiết kế hệ thống bởi kỹ năng giao tiếp và năng lực giải quyết vấn đề được kiểm tra tại đây rất tương đồng với công việc hằng ngày của một kỹ sư phần mềm thực thụ. Ứng viên sẽ được đánh giá dựa trên:
- Cách phân tích một bài toán mơ hồ thành các yêu cầu cụ thể.
- Cách giải quyết bài toán từng bước một cách có hệ thống.
- Khả năng giải thích ý tưởng kỹ thuật, thảo luận cùng người khác, cũng như năng lực đánh giá và tối ưu hóa hệ thống.

*(Lưu ý về văn phong: Trong nguyên tác tiếng Anh, tác giả sử dụng đại từ giống cái "she" xuyên suốt cuốn sách để câu văn mượt mà và tôn trọng sự bình đẳng, không hề có ý hạ thấp hay phân biệt đối xử với các nam kỹ sư).*

---

### Bản chất của các câu hỏi thiết kế hệ thống

Các câu hỏi thiết kế hệ thống luôn là những đề bài mở. Giống hệt như trong thực tế, cùng một bài toán luôn có vô vàn biến thể và các cách tiếp cận khác nhau. Kết quả mong đợi cuối cùng là đưa ra được một kiến trúc khả thi nhằm đạt được các mục tiêu thiết kế đã đề ra. Quá trình thảo luận có thể rẽ sang nhiều hướng khác nhau tùy thuộc vào người phỏng vấn (*interviewer*):
- Một số người phỏng vấn sẽ muốn xem xét kiến trúc tổng thể cấp cao (*high-level architecture*) để bao quát mọi khía cạnh.
- Một số khác lại chọn tập trung đào sâu (*deep dive*) vào một hoặc vài khu vực trọng yếu nhất định.

Thông thường, việc hiểu rõ các **yêu cầu hệ thống**, **rào cản/ràng buộc (constraints)** và **các điểm nghẽn cổ chai (bottlenecks)** là yếu tố quyết định để định hình hướng đi chung cho cả người phỏng vấn và ứng viên.

---

### Mục tiêu của cuốn sách này

Mục tiêu tối thượng của cuốn sách này là cung cấp cho bạn một **chiến lược đáng tin cậy và có hệ thống** để tiếp cận bất kỳ câu hỏi thiết kế hệ thống nào. Việc trang bị đúng chiến lược và nền tảng kiến thức vững vàng là chìa khóa sống còn dẫn đến thành công trong một buổi phỏng vấn.

1. **Trang bị nền tảng kiến thức vững chắc:** Cung cấp hiểu biết chuyên sâu về cách xây dựng một hệ thống có khả năng mở rộng quy mô cao (*scalable system*). Càng tích lũy nhiều kiến thức từ cuốn sách, bạn càng được trang bị vũ khí sắc bén để giải quyết các bài toán hóc búa.
2. **Cung cấp khung sườn từng bước (Step-by-step framework):** Cuốn sách hướng dẫn chi tiết cách tiếp cận một bài toán phỏng vấn từ A đến Z. Thông qua rất nhiều ví dụ thực tế được minh họa sinh động, bạn sẽ nắm được quy trình chuẩn xác để áp dụng.

Với việc kiên trì luyện tập đều đặn, bạn hoàn toàn có thể tự tin bước vào và chinh phục xuất sắc bất kỳ buổi phỏng vấn thiết kế hệ thống nào!

---

[Mục lục](README.md) | [Chương 01: Quy mô từ 0 đến hàng triệu người dùng →](chuong-01-scale-tu-0-den-trieu-nguoi-dung.md)
