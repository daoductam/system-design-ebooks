# Lưu trữ mật khẩu an toàn trong Cơ sở dữ liệu (Password Hashing & Salting)

[← Mục lục](README.md)

---

# Làm thế nào để lưu trữ mật khẩu an toàn trong cơ sở dữ liệu? (How to store passwords safely in the database?)

Hãy cùng tìm hiểu chi tiết.

---

### Những điều TUYỆT ĐỐI KHÔNG NÊN LÀM (Things NOT to do)

* 🔹 **Lưu trữ mật khẩu dưới dạng văn bản thuần (plain text):** Đây không phải là một ý hay vì bất kỳ ai có quyền truy cập nội bộ (*internal access*) đều có thể nhìn thấy chúng.
* 🔹 **Lưu trực tiếp mã băm mật khẩu (password hash):** Cách này là **chưa đủ**, vì hệ thống rất dễ bị tấn công bởi các cuộc tấn công tính toán trước (*precomputation attacks*), chẳng hạn như tấn công bằng bảng cầu vồng (*rainbow tables*).
* 🔹 **Để giảm thiểu các cuộc tấn công tính toán trước:** Chúng ta thêm muối (*salt*) vào mật khẩu.

---

### Muối (Salt) là gì? (What is salt?)

Theo hướng dẫn từ **OWASP**: 

> *"Muối (salt) là một chuỗi ký tự ngẫu nhiên, duy nhất được thêm vào mỗi mật khẩu như một phần của quá trình băm (hashing process)."*

---

### Sơ đồ quy trình lưu trữ và xác thực mật khẩu

![Quy trình lưu trữ và xác thực mật khẩu an toàn](images/page_015_00.jpeg)

---

### Cách lưu trữ mật khẩu và muối? (How to store a password and salt?)

1. 1️⃣ **Muối (salt) không nhằm mục đích giữ bí mật** và nó hoàn toàn có thể được lưu trữ dưới dạng văn bản thuần (*plain text*) trong cơ sở dữ liệu. Nó được sử dụng để đảm bảo rằng kết quả băm (*hash result*) là duy nhất đối với mỗi mật khẩu.
2. 2️⃣ **Mật khẩu có thể được lưu trữ trong cơ sở dữ liệu theo định dạng sau:**
   $$\text{hash}(\text{password} + \text{salt})$$

---

### Quy trình xác thực mật khẩu như thế nào? (How to validate a password?)

Để xác thực một mật khẩu (*validate a password*), hệ thống có thể thực hiện thông qua quy trình sau:

| Bước | Hành động | Chi tiết kỹ thuật |
| :---: | :--- | :--- |
| **1️⃣** | **Nhập mật khẩu** | Phía máy khách (*client*) nhập mật khẩu. |
| **2️⃣** | **Truy xuất muối** | Hệ thống lấy giá trị muối (*salt*) tương ứng từ cơ sở dữ liệu (*database*). |
| **3️⃣** | **Băm giá trị mới (H1)** | Hệ thống ghép muối (*salt*) vào mật khẩu và tiến hành băm. Gọi giá trị băm này là **H1**. |
| **4️⃣** | **So sánh (H1 vs H2)** | Hệ thống so sánh **H1** và **H2**, trong đó **H2** là giá trị băm đã được lưu trữ trong cơ sở dữ liệu. Nếu chúng khớp nhau, mật khẩu là hợp lệ. |

---

**Dành cho bạn suy ngẫm:** Chúng ta có thể sử dụng thêm những cơ chế nào khác để đảm bảo an toàn cho mật khẩu? *(Gợi ý kiến trúc: Sử dụng các hàm băm chậm chống brute-force phần cứng như **Bcrypt**, **Argon2**, **PBKDF2**, hoặc bổ sung **Pepper** lưu tại KMS/HSM)*.

—  
*Tham khảo các cuốn sách thiết kế hệ thống bán chạy nhất của chúng tôi:*  
*Sách bìa mềm: Amazon \| Bản điện tử: ByteByteGo.*

---

[← Mục lục](README.md)
