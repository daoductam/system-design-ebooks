# Ngày 32: Managing Secrets and Credentials

[← Ngày trước](day-31-cutting-cross-region-latency.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-33-reconstructing-state-with-event-sourcing.md)

---


# NGÀY 32 · THIẾT KẾ HỆ THỐNG (SYSTEM DESIGN)
## Quản lý Secrets và Thông tin xác thực (Managing Secrets and Credentials)

![Minh họa kịch bản quản lý Secrets](images/page_130_00.png)

Startup của bạn vừa bước vào đợt đánh giá kiểm toán **SOC 2** đầu tiên.

Kiểm toán viên đặt câu hỏi: *"Mật khẩu cơ sở dữ liệu (database passwords), khóa API (API keys), và mã thông báo dịch vụ (service tokens) của các bạn đang được lưu trữ ở đâu?"*

Kỹ sư cấp cao (Senior Engineer) của bạn đột nhiên im bặt.

Hóa ra một nửa trong số chúng đang nằm trong các file `.env` đã được commit lên Git từ 18 tháng trước. Ba cái được hardcode trực tiếp vào các biến môi trường của **AWS Lambda** (environment variables). Một cái thậm chí còn nằm trong tin nhắn Slack từ năm 2023.

Hệ thống của bạn hiện có **6 dịch vụ đang chạy trên môi trường production**, **4 môi trường khác nhau**, và **hoàn toàn không có chính sách xoay vòng thông tin xác thực (zero rotation policy)**.

Cấu trúc thiết lập hiện tại như sau:
* **NestJS API** → **Postgres** (mật khẩu nằm trong biến môi trường - env var)
* **NestJS API** → **Stripe** (API key nằm trong biến môi trường - env var)
* **Background workers** → **SQS**, **S3** (AWS credentials nằm trong biến môi trường - env var)
* **3rd-party webhooks** → **HMAC secrets** nằm trong biến môi trường - env var
* **Zero rotation** (Không xoay vòng). **Zero audit trail** (Không có nhật ký theo dõi truy vết). **Zero centralized access control** (Không có kiểm soát truy cập tập trung).

Bạn cần khắc phục toàn bộ vấn đề này. Và bạn **không được phép để hệ thống ngừng hoạt động (zero downtime)**.

---

### CÁC PHƯƠNG ÁN LỰA CHỌN

* **A)** Chuyển toàn bộ sang **AWS Secrets Manager** — gọi qua SDK tại thời điểm chạy (runtime), phân quyền truy cập thông qua **IAM (Identity and Access Management)**, tích hợp sẵn tính năng tự động xoay vòng (**auto-rotation**).
* **B)** Sử dụng **HashiCorp Vault** — hỗ trợ dynamic secrets (bí mật động), chính sách phân quyền chi tiết (**fine-grained policies**), hoạt động trên bất kỳ nền tảng đám mây (**multi-cloud**) hoặc môi trường tại chỗ (**on-premise**).
* **C)** Sử dụng các biến môi trường được inject (tiêm) vào tại thời điểm triển khai (deploy time) thông qua quy trình **CI/CD** — secrets được lưu trữ trong kho bí mật của **GitHub Actions / GitLab CI secrets vault**, không bao giờ ghi xuống đĩa cứng.
* **D)** Mã hóa secrets bằng **AWS KMS (Key Management Service)** và lưu trữ bản mã (**ciphertext**) trong chính cơ sở dữ liệu của bạn — giải mã tại thời điểm chạy (**runtime**), toàn quyền kiểm soát.

---

## NGÀY 32 · ĐÁP ÁN & GIẢI THÍCH CHI TIẾT (ANSWERS & EXPLANATIONS)

![Minh họa kiến trúc Secrets Manager vs các giải pháp khác](images/page_132_00.png)

### Câu trả lời 1

> [!TIP]
> ### ✓ CÂU TRẢ LỜI ĐÚNG: A — AWS Secrets Manager
> 
> Hệ thống của bạn vốn đã thuần AWS (**AWS-native**) với các dịch vụ như Lambda, SQS, S3. **AWS Secrets Manager** cung cấp cho bạn:
> * **Lưu trữ mã hóa tập trung (Centralized encrypted storage)**: Được bảo vệ phía sau bởi **KMS**.
> * **Kiểm soát truy cập dựa trên IAM (IAM-based access control)**: Phân quyền chi tiết trên từng secret cho từng service cụ thể.
> * **Cơ chế tự động xoay vòng tích hợp sẵn (Native auto-rotation)**: Hỗ trợ sẵn cho **Amazon RDS** + viết custom **Lambda rotators** cho tất cả các dịch vụ còn lại.
> * **Mọi lượt truy cập đều được ghi log qua CloudTrail**: Đáp ứng chính xác 100% những gì kiểm toán viên **SOC 2** yêu cầu.
>
> **Chiến lược di chuyển không gây gián đoạn (Zero-downtime migration):** Thay thế việc đọc biến môi trường (env vars) bằng các lệnh gọi SDK `getSecretValue()`, triển khai code mới, sau đó xoay vòng (rotate) các thông tin xác thực cũ sau khi đã xác nhận thông tin xác thực mới hoạt động trơn tru.  
> **Chi phí:** Khoảng ~$0.40/secret/tháng. Đối với 20 secrets, tổng chi phí chỉ khoảng $8/tháng.

---

### Câu trả lời 2

> [!WARNING]
> ### B — HashiCorp Vault (Cái bẫy của kỹ sư cấp cao - Senior engineer trap)
> 
> **HashiCorp Vault** mạnh mẽ hơn rất nhiều — tính năng **dynamic secrets** (cấp một thông tin xác thực Postgres hoàn toàn mới cho từng request/session và tự hết hạn sau 1 giờ) là một trong những mẫu kiến trúc (pattern) thanh lịch nhất trong hạ tầng production.
> 
> **Tuy nhiên, Vault là hạ tầng mà BẠN phải tự sở hữu và tự vận hành (self-managed infrastructure):**
> * Bạn cần tự duy trì một **Raft cluster** (tối thiểu 3+ nodes), một storage backend lưu trữ, quy trình mở khóa (**unsealing procedures**), kế hoạch khôi phục sau thảm họa (**DR - Disaster Recovery planning**), và một đội ngũ vận hành (**ops team**) chuyên sâu về Vault.
> * Nếu cụm Vault bị sập (down), toàn bộ secrets sẽ không thể truy cập được — kéo theo tất cả các dịch vụ khác đồng loạt tê liệt.
> 
> **Khi nào Vault chiếm ưu thế:** Môi trường đa đám mây (**Multi-cloud**), các yêu cầu bắt buộc chạy tại chỗ (**on-premise**), nhu cầu triển khai **dynamic secrets ở quy mô lớn**, hoặc khi bạn đã có sẵn một đội ngũ chuyên trách hạ tầng (**dedicated infra team**). Nếu bạn đang xây dựng hệ thống **thuần AWS (AWS-native)** với quy mô **dưới 50 kỹ sư** — luôn luôn ưu tiên **Secrets Manager** đầu tiên.

---

### Câu trả lời 3

> [!NOTE]
> ### C — Biến môi trường được inject qua CI/CD (Đúng một phần, sai phạm vi áp dụng - Partially right, wrong scope)
> 
> Kho bí mật của **GitHub Actions / GitLab CI secrets** là nơi chính xác để lưu trữ các secret ở **thời điểm build (build-time)** và **thời điểm deploy (deploy-time)** — ví dụ: thông tin đăng nhập Docker Hub, Terraform tokens, deploy keys.
> 
> **Chúng hoàn toàn không phù hợp cho runtime secrets:**
> * Mật khẩu Database mà ứng dụng cần truy vấn lúc 3 giờ sáng, hay Stripe API key để xử lý live webhook lúc nửa đêm.
> * Những giá trị đó khi bị inject dưới dạng biến môi trường vào các cấu hình của **ECS task definitions** hoặc **Lambda environment**: rất khó để xoay vòng nguyên tử (**atomic rotation**), đồng thời **hoàn toàn không có nhật ký theo dõi (audit trail)** đối với các truy cập ở thời điểm chạy (runtime access).
> 
> **Kết luận:** Phương án **C bổ trợ cho A hoặc B**. Nó không thể thay thế được chúng.

---

### Câu trả lời 4

> [!CAUTION]
> ### D — Tự chế bằng KMS + Database riêng (Hoàn toàn sai - Wrong)
> 
> Đây là hành động **tái phát minh lại Secrets Manager một cách tồi tệ**. Bạn sẽ phải tự gánh vác:
> 1. Quản lý khóa mã hóa (**encryption key management**).
> 2. Tự viết logic xoay vòng thông tin xác thực (**rotation logic**).
> 3. Tự quản lý phân quyền truy cập (**access control**).
> 4. Tự xây dựng hệ thống ghi log kiểm toán (**audit logging**).
> 5. Và duy trì một database mà chính database đó lại... cần thông tin xác thực để kết nối!
> 
> **Vấn đề siêu dữ liệu (The meta-problem):** Lấy secret nào để bảo vệ chính cái kho lưu trữ secret đó? Bạn sẽ rơi vào bài toán **con gà - quả trứng (bootstrapping problem)** mà các dịch vụ quản lý secret được sinh ra để giải quyết triệt để. Đây là giải pháp mà các nhóm kỹ thuật buộc phải tự làm vào năm **2012** trước khi các dịch vụ quản lý chuyên dụng (managed services) ra đời.


---

[← Ngày trước](day-31-cutting-cross-region-latency.md) | [Mục lục](README.md) | [Ngày tiếp theo →](day-33-reconstructing-state-with-event-sourcing.md)
