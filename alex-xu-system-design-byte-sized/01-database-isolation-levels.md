# Cấp độ cô lập trong Cơ sở dữ liệu (Database Isolation Levels)

[← Mục lục](README.md)

---

# Các mức cô lập cơ sở dữ liệu (Database Isolation Levels) là gì? Chúng được dùng để làm gì?

**Tính cô lập của cơ sở dữ liệu (Database isolation)** cho phép một giao dịch (transaction) thực thi như thể không có bất kỳ giao dịch nào khác đang chạy đồng thời (concurrently).

Sơ đồ bên dưới minh họa 4 mức độ cô lập (isolation levels).

![Các mức độ cô lập trong cơ sở dữ liệu](images/page_005_00.jpeg)

* 🔹 **Serializable**: Đây là mức độ cô lập cao nhất. Các giao dịch đồng thời được đảm bảo sẽ thực thi theo trình tự tuần tự (in sequence).
* 🔹 **Repeatable Read**: Dữ liệu được đọc trong suốt quá trình giao dịch vẫn giữ nguyên như tại thời điểm giao dịch bắt đầu.
* 🔹 **Read Committed**: Dữ liệu sửa đổi chỉ có thể được đọc sau khi giao dịch đã được xác nhận (committed).
* 🔹 **Read Uncommitted**: Dữ liệu sửa đổi có thể được đọc bởi các giao dịch khác trước khi một giao dịch được xác nhận (committed).

---

### Cơ chế hoạt động của MVCC và Khóa (Locks)

Tính cô lập được đảm bảo thông qua **MVCC (Multi-Version Consistency Control - Kiểm soát đồng thời đa phiên bản)** và **các khóa (locks)**.

Sơ đồ dưới đây lấy **Repeatable Read** làm ví dụ để minh họa cách MVCC hoạt động:

* Có hai cột ẩn (hidden columns) cho mỗi hàng: `transaction_id` và `roll_pointer`.
* Khi giao dịch A (transaction A) bắt đầu, một **Read View** mới với `transaction_id = 201` được tạo ra. Ngay sau đó, giao dịch B (transaction B) bắt đầu, và một **Read View** mới với `transaction_id = 202` được tạo ra.
* Lúc này giao dịch A sửa đổi số dư (`balance`) thành 200, một dòng mới của nhật ký (log) được tạo ra, và con trỏ `roll_pointer` trỏ về dòng dữ liệu cũ.
* Trước khi giao dịch A xác nhận (commits), giao dịch B đọc dữ liệu số dư (`balance`). Giao dịch B phát hiện thấy `transaction_id = 201` chưa được commit, nên nó đọc bản ghi đã commit kế tiếp (`transaction_id = 200`).
* Thậm chí ngay cả khi giao dịch A đã commit, giao dịch B vẫn đọc dữ liệu dựa trên **Read View** đã được tạo tại thời điểm giao dịch B bắt đầu. Do đó, giao dịch B luôn luôn đọc dữ liệu với `balance = 100`.

---

**Đến lượt bạn**: Bạn đã từng thấy các mức cô lập (isolation levels) bị sử dụng sai cách bao giờ chưa? Điều đó có gây ra sự cố gián đoạn nghiêm trọng (serious outages) nào không?

—  
Tham khảo các cuốn sách thiết kế hệ thống bán chạy nhất của chúng tôi:  
* Bản bìa mềm (Paperback): **Amazon**  
* Bản kỹ thuật số (Digital): **ByteByteGo**

---

[← Mục lục](README.md)
