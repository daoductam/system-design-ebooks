# Cơ chế xác thực một lần Single Sign-On (SSO)

[← Mục lục](README.md)

---

# SSO (Single Sign-On) là gì?

Một người bạn gần đây đã phải trải qua trải nghiệm đầy phiền toái khi bị đăng xuất khỏi hàng loạt trang web mà họ sử dụng hàng ngày. Trải nghiệm này chắc hẳn quen thuộc với hàng triệu người dùng web, và việc khắc phục nó là một quá trình vô cùng tẻ nhạt. Nó có thể bao gồm việc cố gắng nhớ lại nhiều mật khẩu đã quên từ lâu, hoặc gõ tên những con thú cưng thời thơ ấu để trả lời các câu hỏi bảo mật. SSO giải quyết sự bất tiện này và giúp cuộc sống trực tuyến trở nên thuận tiện hơn. Nhưng cơ chế hoạt động của nó như thế nào?

Về cơ bản, **Single Sign-On (SSO)** là một cơ chế xác thực (*authentication scheme*). Nó cho phép người dùng đăng nhập vào nhiều hệ thống khác nhau chỉ bằng một định danh duy nhất (**single ID**).

Sơ đồ dưới đây minh họa cách thức hoạt động của SSO:

![Quy trình hoạt động của SSO](images/page_012_00.jpeg)

---

### Quy trình hoạt động chi tiết (Step-by-step Flow):

* **Bước 1:** Người dùng truy cập vào **Gmail** (hoặc bất kỳ dịch vụ email nào). Gmail phát hiện người dùng chưa đăng nhập, do đó chuyển hướng (*redirect*) họ đến máy chủ xác thực SSO (**SSO authentication server**). Máy chủ này cũng nhận thấy người dùng chưa đăng nhập. Kết quả là người dùng tiếp tục được chuyển hướng đến trang đăng nhập SSO, nơi họ nhập thông tin đăng nhập (*login credentials*) của mình.
* **Bước 2 - 3:** Máy chủ xác thực SSO tiến hành xác thực thông tin đăng nhập, tạo một phiên làm việc tổng thể (**global session**) cho người dùng và khởi tạo một mã xác thực (**token**).
* **Bước 4 - 7:** Gmail xác thực token này với máy chủ xác thực SSO. Máy chủ xác thực ghi nhận hệ thống Gmail và trả về kết quả hợp lệ (**"valid"**). Sau đó, Gmail trả về tài nguyên được bảo vệ (*protected resource*) cho người dùng.
* **Bước 8:** Từ Gmail, người dùng điều hướng sang một trang web khác thuộc sở hữu của Google, ví dụ như **YouTube**.
* **Bước 9 - 10:** YouTube phát hiện người dùng chưa đăng nhập tại trang của mình và gửi yêu cầu xác thực. Máy chủ xác thực SSO nhận diện người dùng đã đăng nhập từ trước (thông qua global session) và trả về token.
* **Bước 11 - 14:** YouTube xác thực token với máy chủ xác thực SSO. Máy chủ xác thực ghi nhận hệ thống YouTube và phản hồi hợp lệ (**"valid"**). YouTube cấp quyền truy cập tài nguyên được bảo vệ cho người dùng.

Quá trình hoàn tất và người dùng khôi phục lại quyền truy cập vào tài khoản của mình trên toàn bộ hệ sinh thái.

---

### Góc thảo luận (Over to you):

* **Câu hỏi 1:** Bạn đã từng triển khai hệ thống SSO trong các dự án thực tế của mình chưa? Phần thách thức/khó khăn nhất bạn từng gặp phải là gì?
* **Câu hỏi 2:** Đâu là phương thức đăng nhập (*sign-in method*) ưa thích của bạn và lý do vì sao?

---
*Tham khảo thêm các đầu sách bán chạy về Thiết kế hệ thống (System Design):*  
* Bản in (*Paperback*): **Amazon** | Bản điện tử (*Digital*): **ByteByteGo**.

---

[← Mục lục](README.md)
