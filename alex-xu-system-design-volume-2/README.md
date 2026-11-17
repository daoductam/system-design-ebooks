# Alex Xu - System Design Interview: An Insider's Guide (Volume 2)

Bản dịch tiếng Việt chuẩn kỹ thuật (100% nguyên văn đầy đủ) của tác phẩm kinh điển **System Design Interview – An Insider's Guide: Volume 2** của tác giả **Alex Xu** & **Sahn Lam**.

Toàn bộ 13 chương chuyên sâu cùng Lời mở đầu, Mục lục và Phụ lục chỉ mục được chuyển ngữ chi tiết, giữ nguyên độ sâu kỹ thuật kiến trúc hệ thống phân tán cấp độ thực tế (Production Scale) cùng toàn bộ sơ đồ kiến trúc độ phân giải cao.

---

## 📚 Mục Lục Toàn Tập (Table of Contents)

| STT | Tên Chương | Chủ Đề Kỹ Thuật Chính | Liên Kết |
| :---: | :--- | :--- | :---: |
| 📖 | **Lời Mở Đầu & Mục Lục** | Giới thiệu, Lời cảm ơn & Định hướng phỏng vấn | [00-loi-mo-dau.md](00-loi-mo-dau.md) |
| 01 | **Chương 1: Dịch Vụ Định Vị Lân Cận** *(Proximity Service)* | LBS, Geohash, Quadtree, Google S2, Spatial Indexing | [chuong-01-proximity-service.md](chuong-01-proximity-service.md) |
| 02 | **Chương 2: Tìm Bạn Bè Gần Đây** *(Nearby Friends)* | WebSocket, Redis Pub/Sub, Location Cache, P2P Routing | [chuong-02-nearby-friends.md](chuong-02-nearby-friends.md) |
| 03 | **Chương 3: Google Maps** | Navigation, Geocoding, Map Tile Service, Shortest Path (Dijkstra/A*) | [chuong-03-google-maps.md](chuong-03-google-maps.md) |
| 04 | **Chương 4: Hàng Đợi Tin Nhắn Phân Tán** *(Distributed Message Queue)* | Kafka Architecture, Partitioning, Replication, Consumer Groups, Zero-copy | [chuong-04-distributed-message-queue.md](chuong-04-distributed-message-queue.md) |
| 05 | **Chương 5: Giám Sát Chỉ Số & Cảnh Báo** *(Metrics Monitoring & Alerting)* | Time-series DB, Pull vs Push, OpenTSDB/Prometheus, Aggregation | [chuong-05-metrics-monitoring-and-alerting-system.md](chuong-05-metrics-monitoring-and-alerting-system.md) |
| 06 | **Chương 6: Tổng Hợp Sự Kiện Click Quảng Cáo** *(Ad Click Aggregation)* | Stream Processing, MapReduce, Flink/Spark Streaming, Exactly-once | [chuong-06-ad-click-event-aggregation.md](chuong-06-ad-click-event-aggregation.md) |
| 07 | **Chương 7: Hệ Thống Đặt Phòng Khách Sạn** *(Hotel Reservation System)* | Concurrency Control, Pessimistic/Optimistic Locking, Idempotency, 2PC/Saga | [chuong-07-hotel-reservation-system.md](chuong-07-hotel-reservation-system.md) |
| 08 | **Chương 8: Dịch Vụ Email Phân Tán** *(Distributed Email Service)* | SMTP, POP3/IMAP, Storage Replication, Search Indexing, Spam Filter | [chuong-08-distributed-email-service.md](chuong-08-distributed-email-service.md) |
| 09 | **Chương 9: Lưu Trữ Đối Tượng Chuẩn S3** *(S3-like Object Storage)* | Block vs File vs Object, Erasure Coding, Multipart Upload, Metadata Store | [chuong-09-s3-like-object-storage.md](chuong-09-s3-like-object-storage.md) |
| 10 | **Chương 10: Bảng Xếp Hạng Game Thời Gian Thực** *(Gaming Leaderboard)* | Redis Sorted Sets, Point Updates, Sharding, Segment Trees | [chuong-10-real-time-gaming-leaderboard.md](chuong-10-real-time-gaming-leaderboard.md) |
| 11 | **Chương 11: Hệ Thống Thanh Toán** *(Payment System)* | Payment Gateway, Double-entry Bookkeeping, Reconciliation, Exactly-once | [chuong-11-payment-system.md](chuong-11-payment-system.md) |
| 12 | **Chương 12: Ví Điện Tử** *(Digital Wallet)* | In-memory Balance, Raft Consensus, Distributed Transactions, CQRS | [chuong-12-digital-wallet.md](chuong-12-digital-wallet.md) |
| 13 | **Chương 13: Sàn Giao Dịch Chứng Khoán** *(Stock Exchange)* | Order Book, Matching Engine, Low Latency Network (LMAX), Sequencer | [chuong-13-stock-exchange.md](chuong-13-stock-exchange.md) |
| 📝 | **Lời Kết & Chỉ Mục** | Tổng kết hành trình, Phương pháp phỏng vấn & Index | [14-loi-ket-va-index.md](14-loi-ket-va-index.md) |

---

## 🎯 Điểm Nổi Bật Của Tài Liệu
1. **Dịch nguyên văn 100%:** Giữ trọn vẹn mọi dòng giải thích, công thức tính toán tải (Back-of-the-envelope estimation), chi tiết API và database schema.
2. **Thuật ngữ chuẩn công nghiệp:** Giữ nguyên thuật ngữ tiếng Anh gốc trong ngoặc đơn song ngữ để tiện tra cứu và phỏng vấn tại các công ty công nghệ đa quốc gia.
3. **Sơ đồ trực quan:** Tích hợp trực tiếp các sơ đồ kiến trúc độ phân giải cao theo đúng ngữ cảnh của từng phần trong chương.
4. **Định dạng trực quan:** Sử dụng callout box GitHub (`[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`), bảng biểu đối chiếu và khối mã nguồn rõ ràng.
