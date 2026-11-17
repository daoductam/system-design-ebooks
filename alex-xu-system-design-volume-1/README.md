# 📘 Alex Xu - System Design Interview: An Insider’s Guide (Tập 1)

> **Tác giả:** Alex Xu  
> **Ngôn ngữ bản dịch:** Tiếng Việt (Bản dịch nguyên văn 100%, đầy đủ hình ảnh, mã nguồn và bảng biểu)  
> **Định dạng:** Markdown chuẩn GitHub  

---

## 🎯 Giới Thiệu Cuốn Sách

Cuốn sách **"System Design Interview: An Insider’s Guide"** của tác giả **Alex Xu** là một trong những tài liệu chuẩn mực và được săn đón nhiều nhất trên thế giới dành cho các kỹ sư phần mềm chuẩn bị bước vào các vòng phỏng vấn thiết kế hệ thống tại các công ty công nghệ hàng đầu (FAANG / Big Tech).

Cuốn sách cung cấp phương pháp luận tư duy hệ thống theo 4 bước rõ ràng, đi từ các nguyên lý cơ bản đến cách tiếp cận từng bài toán thực tế quy mô hàng trăm triệu người dùng.

---

## 📑 Mục Lục Chi Tiết

| Chương | Tên Chương (Tiếng Việt) | Tên Chương Gốc | Nội Dung Trọng Tâm | Liên Kết Đọc |
|:---:|:---|:---|:---|:---:|
| **00** | **Lời Mở Đầu** | *Forward & Introduction* | Tư duy thiết kế hệ thống và cách dùng sách | [📖 Đọc ngay](00-loi-mo-dau.md) |
| **01** | **Quy mô từ 0 đến hàng triệu người dùng** | *Scale From Zero to Millions of Users* | Single server, Database replication, Cache, CDN, Stateless web tier, Multi-DC, Message Queue, Sharding | [📖 Đọc ngay](chuong-01-scale-tu-0-den-trieu-nguoi-dung.md) |
| **02** | **Ước tính quy mô đại khái** | *Back-of-the-envelope Estimation* | Lũy thừa của 2, Độ trễ phần cứng (Latency numbers), Tính toán QPS, Storage, Bandwidth | [📖 Đọc ngay](chuong-02-uoc-luong-dai-khai.md) |
| **03** | **Khung sườn phỏng vấn System Design** | *A Framework for System Design Interviews* | Quy trình 4 bước chuẩn mực: Hiểu yêu cầu, Đề xuất High-level, Deep dive chi tiết, Tổng kết | [📖 Đọc ngay](chuong-03-khung-suon-phong-van-system-design.md) |
| **04** | **Thiết kế Bộ giới hạn tốc độ (Rate Limiter)** | *Design a Rate Limiter* | Token bucket, Leaking bucket, Fixed window, Sliding window log, Sliding window counter, Distributed rate limiting | [📖 Đọc ngay](chuong-04-thiet-ke-rate-limiter.md) |
| **05** | **Thiết kế Băm nhất quán (Consistent Hashing)** | *Design Consistent Hashing* | Vấn đề phân phối lại hash `key % N`, Vòng băm (Hash ring), Server ảo (Virtual nodes) | [📖 Đọc ngay](chuong-05-thiet-ke-consistent-hashing.md) |
| **06** | **Thiết kế Kho lưu trữ Key-Value** | *Design a Key-Value Store* | Định lý CAP, Phân mảnh dữ liệu, Quorum consensus, Xử lý xung đột (Vector clock), Phát hiện lỗi (Gossip protocol) | [📖 Đọc ngay](chuong-06-thiet-ke-key-value-store.md) |
| **07** | **Thiết kế Bộ sinh ID duy nhất phân tán** | *Design a Unique ID Generator in Distributed Systems* | Multi-master, UUID, Ticket Server, Twitter Snowflake 64-bit ID | [📖 Đọc ngay](chuong-07-thiet-ke-unique-id-generator-phan-tan.md) |
| **08** | **Thiết kế Hệ thống rút gọn liên kết (URL Shortener)** | *Design a URL Shortener* | Mã hóa Base62 vs Hashing + Collision, Chuyển hướng HTTP 301 vs 302, Tối ưu cache và database | [📖 Đọc ngay](chuong-08-thiet-ke-url-shortener.md) |
| **09** | **Thiết kế Trình thu thập dữ liệu Web (Web Crawler)** | *Design a Web Crawler* | Thuật ngữ BFS, URL Frontier, Quản lý tính lịch sự (Politeness), Tính mới (Freshness), Xử lý trùng lặp (Dedup) | [📖 Đọc ngay](chuong-09-thiet-ke-web-crawler.md) |
| **10** | **Thiết kế Hệ thống thông báo (Notification System)** | *Design a Notification System* | iOS Push (APNs), Android Push (FCM), SMS, Email, Hàng đợi tin nhắn và chống spam | [📖 Đọc ngay](chuong-10-thiet-ke-he-thong-thong-bao.md) |
| **11** | **Thiết kế Hệ thống Bảng tin (News Feed System)** | *Design a News Feed System* | Feed publishing vs Feed retrieval, Fanout-on-write (Push) vs Fanout-on-read (Pull), Kiến trúc đa tầng cache | [📖 Đọc ngay](chuong-11-thiet-ke-news-feed-system.md) |
| **12** | **Thiết kế Hệ thống Chat trực tuyến** | *Design a Chat System* | HTTP Polling vs Long polling vs WebSocket, Quản lý trạng thái online/offline, Đồng bộ tin nhắn đa thiết bị | [📖 Đọc ngay](chuong-12-thiet-ke-chat-system.md) |
| **13** | **Thiết kế Hệ thống gợi ý tìm kiếm (Search Autocomplete)** | *Design a Search Autocomplete System* | Cấu trúc dữ liệu Cây tiền tố (Trie), Tối ưu bộ nhớ Trie, Pipeline thu thập và phân tích dữ liệu theo thời gian thực | [📖 Đọc ngay](chuong-13-thiet-ke-search-autocomplete.md) |
| **14** | **Thiết kế Nền tảng chia sẻ Video YouTube** | *Design YouTube* | Quy trình Upload video và Stream video, Mã hóa chuyển mã (Transcoding DAG), Tối ưu CDN chi phí thấp | [📖 Đọc ngay](chuong-14-thiet-ke-youtube.md) |
| **15** | **Thiết kế Hệ thống lưu trữ Google Drive** | *Design Google Drive* | Đồng bộ khối phân mảnh (Block-level sync), Thuật toán chống trùng lặp, Theo dõi xung đột và Metadata DB | [📖 Đọc ngay](chuong-15-thiet-ke-google-drive.md) |
| **16** | **Hành trình học tập tiếp diễn & Lời bạt** | *The Learning Continues & Afterword* | Lời khuyên định hướng nghề nghiệp, cách duy trì phản xạ thiết kế hệ thống và cập nhật công nghệ | [📖 Đọc ngay](chuong-16-hanh-trinh-hoc-tap-tiep-dien.md) |

---

[← Quay lại Trang Chủ](../README.md)
