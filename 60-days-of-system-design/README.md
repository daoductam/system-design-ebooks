# 🚀 60 Days of System Design Questions (60 Ngày Luyện Thiết Kế Hệ Thống Thực Chiến)

> **Tài liệu:** Tuyển tập 60 bài toán kiến trúc phân tán thực tế  
> **Định dạng:** Đề bài tình huống thực tế + Lựa chọn phương án + Bẫy phỏng vấn (Traps) + Lời giải phân tích chuyên sâu  
> **Ngôn ngữ bản dịch:** Tiếng Việt (Bản dịch nguyên văn 100%)  

---

## 🎯 Giới Thiệu Bộ Câu Hỏi

Không giống như các tài liệu lý thuyết chung chung, chuỗi **60 Days of System Design** đưa bạn vào các tình huống kỹ thuật "nóng bỏng tay" xảy ra hằng ngày tại các hệ thống quy mô lớn (Production Systems):
- Sự cố truy vấn N+1 làm tê liệt cơ sở dữ liệu.
- Hiện tượng trừ tiền 2 lần (Duplicate charge) trong xử lý thanh toán.
- Sự cố vỡ đệm (Cache Stampede), lệch dữ liệu Read-Your-Writes khi dùng Read Replicas.
- Kiến trúc xử lý nghẽn hàng đợi (Queue Backpressure), Hot Partition Keys.
- Tích hợp AI / LLM / RAG / Vector Database vào hệ thống hiện đại.

Mỗi ngày giải quyết một bài toán với phân tích lý do tại sao phương án chuẩn chiến thắng và vì sao các đáp án bẫy lại dễ dàng đánh lừa các kỹ sư có kinh nghiệm!

---

## 📑 Bảng Phân Bổ 60 Ngày Luyện Tập

| Ngày | Chủ Đề Tình Huống Kỹ Thuật | Trọng Tâm Kiến Trúc | Liên Kết Đọc |
|:---:|:---|:---|:---:|
| **Day 01** | Tách rời Ứng dụng Di động khỏi Backend | API Gateway vs BFF Pattern | [📖 Day 01](day-01-decoupling-mobile-backend.md) |
| **Day 02** | Xử lý triệt để bài toán N+1 Query | JOIN, Eager Loading vs Dataloader | [📖 Day 02](day-02-killing-n-plus-1-query.md) |
| **Day 03** | Giới hạn lưu lượng không bị bùng nổ biên (Boundary Bursts) | Token Bucket vs Sliding Window Log | [📖 Day 03](day-03-rate-limiting-without-boundary-bursts.md) |
| **Day 04** | Chống trừ tiền trùng lặp trong thanh toán | Idempotency Keys & Database Locks | [📖 Day 04](day-04-preventing-duplicate-payment-charges.md) |
| **Day 05** | Chiến lược phân mảnh cơ sở dữ liệu (Database Sharding) | Range vs Hash vs Directory-based | [📖 Day 05](day-05-choosing-a-database-sharding-strategy.md) |
| **Day 06** | Khóa phân tán an toàn cho tác vụ định kỳ (Distributed Lock) | Redis Redlock vs Database Lease | [📖 Day 06](day-06-safe-distributed-locks-for-cron-jobs.md) |
| **Day 07** | Đảm bảo thứ tự sự kiện trong Message Queue | Partition Key, Kafka vs SQS FIFO | [📖 Day 07](day-07-event-ordering-in-a-message-queue.md) |
| **Day 08** | Đồng bộ hóa dữ liệu giữa Cache và Database | Cache-Aside, Write-Through vs CDC | [📖 Day 08](day-08-keeping-cache-and-database-in-sync.md) |
| **Day 09** | Tách biệt mô hình Đọc và Ghi (CQRS Pattern) | Read/Write DB, Event Sourcing | [📖 Day 09](day-09-splitting-read-and-write-data-models.md) |
| **Day 10** | Giao dịch phân tán giữa các Microservices | Saga Pattern (Orchestration vs Choreography) | [📖 Day 10](day-10-distributed-transactions-across-services.md) |
| **Day 11** | Xử lý cơ chế thử lại của Webhook mang tính lũy nghiệm | Idempotent Consumer & Deduplication | [📖 Day 11](day-11-handling-webhook-retries-idempotently.md) |
| **Day 12** | Đánh chỉ mục (Indexing) cho bảng ghi chép cường độ cao | B-Tree vs LSM-Tree, BRIN Index | [📖 Day 12](day-12-indexing-a-high-ingest-table.md) |
| **Day 13** | Quản lý Connection Pool dùng chung | PgBouncer, HikariCP, Connection Exhaustion | [📖 Day 13](day-13-managing-a-shared-connection-pool.md) |
| **Day 14** | Triển khai an toàn các thay đổi rủi ro cao | Canary Deployment, Feature Flags | [📖 Day 14](day-14-safely-rolling-out-a-risky-change.md) |
| **Day 15** | Kiểm tra siêu tốc "Người dùng đã xem nội dung này chưa?" | Cấu trúc dữ liệu Bloom Filter | [📖 Day 15](day-15-fast-has-user-seen-this-checks.md) |
| **Day 16** | Khắc phục vấn đề Hot Partition Key | Salting Key, Two-Tier Aggregation | [📖 Day 16](day-16-taming-a-hot-partition-key.md) |
| **Day 17** | Kiểm soát áp lực ngược (Backpressure) trên Consumer | Rate throttling, Reactive Streams | [📖 Day 17](day-17-backpressure-on-overwhelmed-consumer.md) |
| **Day 18** | Vượt qua thảm họa sập bộ nhớ đệm (Cache Stampede) | Mutex Lock, Early Expiration | [📖 Day 18](day-18-surviving-a-cache-stampede.md) |
| **Day 19** | Đảm bảo tính nhất quán Read-Your-Writes với Read Replicas | Replication Lag, Session Pinning | [📖 Day 19](day-19-read-your-writes-with-read-replicas.md) |
| **Day 20** | Cách ly lỗi từ hệ thống phụ thuộc phía hạ lưu | Circuit Breaker Pattern & Fallback | [📖 Day 20](day-20-containing-a-failing-downstream-dependency.md) |
| **Day 21** | Lựa chọn giao thức truyền tải thời gian thực | WebSocket vs Server-Sent Events vs gRPC | [📖 Day 21](day-21-choosing-a-real-time-streaming-transport.md) |
| **Day 22** | Truyền thông điệp tin cậy giữa các dịch vụ | Transactional Outbox Pattern | [📖 Day 22](day-22-reliable-messaging-across-services.md) |
| **Day 23** | Lan truyền bảng tin (Feed Fanout) cho tài khoản người nổi tiếng | Hybrid Push-Pull Fanout Model | [📖 Day 23](day-23-feed-fanout-for-celebrity-accounts.md) |
| **Day 24** | Phân trang tập dữ liệu lớn siêu hiệu quả | Keyset / Cursor Pagination vs OFFSET | [📖 Day 24](day-24-paginating-large-result-sets-efficiently.md) |
| **Day 25** | Xử lý nghẽn hàng đợi khi đột biến lưu lượng (Traffic Spike) | Auto-scaling consumers, DLQ | [📖 Day 25](day-25-queue-backpressure-under-traffic-spike.md) |
| **Day 26** | Nhất quán dữ liệu Cache trên luồng Ghi | Cache Invalidation, Read-Through | [📖 Day 26](day-26-write-path-cache-consistency.md) |
| **Day 27** | Cập nhật câu trả lời của LLM theo thời gian thực | Kiến trúc RAG Pipeline | [📖 Day 27](day-27-keeping-an-llm-answers-up-to-date.md) |
| **Day 28** | Lựa chọn Vector Database cho tìm kiếm ngữ nghĩa | Pinecone, Milvus, pgvector, Qdrant | [📖 Day 28](day-28-choosing-a-vector-store-for-semantic-search.md) |
| **Day 29** | Điều phối quy trình đa tác tử (Multi-Agent Workflow) | Agent Choreography & State Graph | [📖 Day 29](day-29-coordinating-a-multi-agent-workflow.md) |
| **Day 30** | Lựa chọn hệ thống lưu trữ tệp (File Storage Backend) | Block Storage vs Object Storage (S3) | [📖 Day 30](day-30-choosing-a-file-storage-backend.md) |
| **Day 31 - 60** | Xem tiếp các tình huống chuyên sâu khác... | Multi-Tenant SaaS, Zero-Downtime Migration, v.v. | [👉 Xem danh sách đầy đủ](README.md) |

---

[← Quay lại Trang Chủ](../README.md)
