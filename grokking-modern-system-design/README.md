# 📗 Grokking Modern System Design Interview for Engineers & Managers

> **Nguồn gốc:** Khóa học nổi tiếng của nền tảng **Educative.io**  
> **Ngôn ngữ bản dịch:** Tiếng Việt (Bản dịch nguyên văn 100%, chi tiết từng bài học)  
> **Định dạng:** Markdown chuẩn GitHub  

---

## 🎯 Giới Thiệu Khóa Học

**Grokking Modern System Design** là một trong những chương trình đào tạo thiết kế hệ thống có cấu trúc bài bản và toàn diện nhất hiện nay. Khóa học được thiết kế theo cấu trúc module hoá gồm:
1. **Khái niệm nền tảng & Ước lượng**: Định lượng các đặc tính phi chức năng, độ trễ, băng thông.
2. **19 Khối kiến trúc nền móng (Building Blocks)**: Mổ xẻ sâu vào hoạt động của từng thành phần phân tán như DNS, Load Balancers, Distributed Cache, Messaging Queues, Key-Value Stores, CDN, Blob Store, Sequencer, Distributed Search...
3. **13 Bài toán thiết kế hệ thống thực tế kinh điển**: Thiết kế từ đầu đến cuối các dịch vụ lớn như YouTube, Quora, Google Maps, Yelp, Uber, Twitter, Instagram, TinyURL, Web Crawler, WhatsApp, Google Docs...
4. **Phân tích các sự cố thảm họa trong lịch sử**: Bài học xương máu từ các đợt sập mạng của các ông lớn công nghệ.

---

## 📑 Mục Lục Toàn Bộ 41 Chuyên Đề

### Phần 1: Khái Niệm Nền Tảng & Phương Pháp Luận
- [000 - Mục Lục & Giới Thiệu Khóa Học](000-muc-luc-khoa-hoc.md)
- [001 - Giới Thiệu Thiết Kế Hệ Thống Hiện Đại](001-gioi-thieu-modern-system-design.md)
- [002 - Bản Chất Của Phỏng Vấn System Design](002-phong-van-system-design.md)
- [003 - Các Tầng Trừu Tượng Trong Hệ Thống (Abstractions)](003-cac-tang-truu-tuong-abstractions.md)
- [004 - Các Đặc Tính Phi Chức Năng Của Hệ Thống](004-dac-tinh-phi-chuc-nang.md)
- [005 - Kỹ Năng Ước Tính Đại Khái (Back-of-the-envelope Calculations)](005-uoc-tinh-back-of-the-envelope.md)

### Phần 2: Các Khối Kiến Trúc Nền Tảng (Building Blocks)
- [006 - Giới Thiệu Các Khối Xây Dựng Hệ Thống Hiện Đại](006-gioi-thieu-building-blocks.md)
- [007 - Hệ Thống Phân Giải Tên Miền (Domain Name System - DNS)](007-domain-name-system-dns.md)
- [008 - Bộ Cân Bằng Tải (Load Balancers)](008-can-bang-tai-load-balancers.md)
- [009 - Cơ Sở Dữ Liệu (Databases - SQL vs NoSQL, Replication & Sharding)](009-co-so-du-lieu-databases.md)
- [010 - Kho Lưu Trữ Key-Value (Key-Value Store)](010-luu-tru-key-value-store.md)
- [011 - Mạng Phân Phối Nội Dung (Content Delivery Network - CDN)](011-mang-phan-phoi-noi-dung-cdn.md)
- [012 - Bộ Sinh Số Thứ Tự Toàn Cục (Sequencer / Unique ID Generator)](012-bo-sinh-so-thu-tu-sequencer.md)
- [013 - Hệ Thống Giám Sát Phân Tán (Distributed Monitoring)](013-giam-sat-phan-tan-distributed-monitoring.md)
- [014 - Giám Sát Lỗi Phía Máy Chủ (Server-Side Error Monitoring)](014-giam-sat-loi-server-side.md)
- [015 - Giám Sát Lỗi Phía Máy Khách (Client-Side Error Monitoring)](015-giam-sat-loi-client-side.md)
- [016 - Bộ Nhớ Đệm Phân Tán (Distributed Cache)](016-bo-nho-dem-phan-tan-distributed-cache.md)
- [017 - Hàng Đợi Thông Điệp Phân Tán (Distributed Messaging Queue)](017-hang-doi-thong-diep-messaging-queue.md)
- [018 - Hệ Thống Xuất Bản - Đăng Ký (Pub-Sub Architecture)](018-mo-hinh-pub-sub.md)
- [019 - Bộ Giới Hạn Tần Suất Truy Cập (Rate Limiter)](019-gioi-han-tan-suat-rate-limiter.md)
- [020 - Kho Lưu Trữ Đối Tượng Lớn (Blob Store / Object Storage)](020-kho-luu-tru-blob-store.md)
- [021 - Công Cụ Tìm Kiếm Phân Tán (Distributed Search)](021-tim-kiem-phan-tan-distributed-search.md)
- [022 - Hệ Thống Ghi Log Phân Tán (Distributed Logging)](022-ghi-log-phan-tan-distributed-logging.md)
- [023 - Bộ Điều Phối Tác Vụ Phân Tán (Distributed Task Scheduler)](023-dieu-phoi-tac-vu-task-scheduler.md)
- [024 - Bộ Đếm Phân Mảnh (Sharded Counters)](024-bo-dem-phan-manh-sharded-counters.md)
- [025 - Tổng Kết Các Khối Xây Dựng Hệ Thống](025-tong-ket-building-blocks.md)

### Phần 3: Thiết Kế Các Hệ Thống Thực Tế Kinh Điển (Real-World System Designs)
- [026 - Thiết Kế YouTube (Video Streaming Platform)](026-thiet-ke-youtube.md)
- [027 - Thiết Kế Quora (Hỏi Đáp Quy Mô Lớn)](027-thiet-ke-quora.md)
- [028 - Thiết Kế Google Maps (Bản Đồ & Dẫn Đường Toàn Cầu)](028-thiet-ke-google-maps.md)
- [029 - Thiết Kế Dịch Vụ Tìm Kiếm Địa Điểm Lân Cận (Proximity Service - Yelp)](029-thiet-ke-dich-vu-lan-can-yelp.md)
- [030 - Thiết Kế Uber (Dịch Vụ Gọi Xe Trực Tuyến Theo Thời Gian Thực)](030-thiet-ke-uber.md)
- [031 - Thiết Kế Twitter (Mạng Xã Hội Microblogging)](031-thiet-ke-twitter.md)
- [032 - Thiết Kế Hệ Thống Bảng Tin (Newsfeed System)](032-thiet-ke-newsfeed-system.md)
- [033 - Thiết Kế Instagram (Nền Tảng Chia Sẻ Ảnh & Video)](033-thiet-ke-instagram.md)
- [034 - Thiết Kế Dịch Vụ Rút Gọn Đường Dẫn (TinyURL)](034-thiet-ke-dich-vu-rut-gon-tinyurl.md)
- [035 - Thiết Kế Bộ Thu Thập Dữ Liệu Web (Web Crawler)](035-thiet-ke-web-crawler.md)
- [036 - Thiết Kế WhatsApp (Ứng Dụng Nhắn Tin Trực Tuyến Đa Nền Tảng)](036-thiet-ke-whatsapp.md)
- [037 - Thiết Kế Tính Năng Gợi Ý Tìm Kiếm (Typeahead Suggestion)](037-thiet-ke-typeahead-suggestion.md)
- [038 - Thiết Kế Trình Soạn Thảo Văn Bản Cộng Tác (Google Docs)](038-thiet-ke-google-docs.md)

### Phần 4: Đúc Kết & Bài Học Thực Nghiệm
- [039 - Những Thất Bại Kinh Điển Trong Thiết Kế Hệ Thống (Spectacular Failures)](039-that-bai-kinh-dien.md)
- [040 - Lời Kết & Lời Khuyên Cho Kỹ Sư Hệ Thống](040-loi-ket.md)

---

[← Quay lại Trang Chủ](../README.md)
