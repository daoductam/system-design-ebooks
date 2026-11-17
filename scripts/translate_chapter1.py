import fitz
import subprocess
import os

doc = fitz.open('design.interview.alex/System Design Interview VOL 1 BUY.pdf')

sections = [
    ("Phần 1: Thiết lập máy chủ đơn lẻ & Cơ sở dữ liệu", 4, 8),
    ("Phần 2: Mở rộng dọc vs ngang & Bộ cân bằng tải & Nhân bản CSDL", 8, 14),
    ("Phần 3: Bộ nhớ đệm (Cache) & Mạng phân phối nội dung (CDN)", 14, 19),
    ("Phần 4: Tầng Web phi trạng thái (Stateless Web Tier) & Đa trung tâm dữ liệu", 19, 24),
    ("Phần 5: Message Queue, Giám sát, Logging & Phân mảnh CSDL (Sharding)", 24, 32),
]

def translate_chunk(title, text):
    prompt = f"""Bạn là kỹ sư trưởng hệ thống phần mềm phân tán (Principal Distributed Systems Architect). Hãy dịch TOÀN BỘ tài liệu kỹ thuật sau sang tiếng Việt chuẩn kỹ thuật, văn phong rõ ràng, chuyên nghiệp theo định dạng Markdown chuẩn GitHub.

Yêu cầu nghiêm ngặt:
1. DỊCH ĐẦY ĐỦ NGUYÊN VĂN 100%, TUYỆT ĐỐI KHÔNG TÓM TẮT, KHÔNG CẮT BỚT BẤT KỲ CÂU, DÒNG HAY CHI TIẾT KỸ THUẬT NÀO.
2. Giữ nguyên các thuật ngữ kỹ thuật trong ngoặc hoặc dùng song ngữ: Load Balancer, Web Server, Database Replication, Master/Slave, Cache-aside, CDN, TTL, Stateless, Sharding, Resharding, Celebrity problem, v.v.
3. Khi nhắc đến hình ảnh minh họa trong văn bản, hãy chèn đúng cú pháp Markdown hình ảnh:
   - Figure 1-1: ![Figure 1-1](images/page_006_00.jpeg)
   - Figure 1-2: ![Figure 1-2](images/page_006_01.jpeg)
   - Figure 1-3: ![Figure 1-3](images/page_008_00.jpeg)
   - Figure 1-4: ![Figure 1-4](images/page_010_00.jpeg)
   - Figure 1-5: ![Figure 1-5](images/page_012_00.jpeg)
   - Figure 1-6: ![Figure 1-6](images/page_015_00.jpeg)
   - Figure 1-7: ![Figure 1-7](images/page_015_01.jpeg)
   - Figure 1-9: ![Figure 1-9](images/page_017_00.jpeg)
   - Figure 1-10: ![Figure 1-10](images/page_017_01.jpeg)
   - Figure 1-12: ![Figure 1-12](images/page_020_00.jpeg)
   - Figure 1-14: ![Figure 1-14](images/page_021_00.jpeg)
   - Figure 1-15: ![Figure 1-15](images/page_023_00.jpeg)
   - Figure 1-17: ![Figure 1-17](images/page_025_00.jpeg)
   - Figure 1-18: ![Figure 1-18](images/page_025_01.jpeg)
   - Figure 1-20: ![Figure 1-20](images/page_028_00.jpeg)
   - Figure 1-22: ![Figure 1-22](images/page_029_00.jpeg)
   - Figure 1-23: ![Figure 1-23](images/page_031_00.jpeg)
4. Định dạng Markdown trực quan, tiêu đề H2/H3 hợp lý, danh sách đánh số/gạch đầu dòng, bảng biểu, in đậm các ý chính.

Tài liệu kỹ thuật cần dịch:
{text}
"""
    cmd = ['C:\\Users\\tamda\\.gemini\\bin\\agy.exe', '--effort', 'low', '-p', prompt]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    out, err = p.communicate()
    if p.returncode != 0:
        raise Exception(f"Translation failed: {err}")
    return out.strip()

print("Bắt đầu dịch Chương 1 thành 5 phần song song / tuần tự...")
results = []
for idx, (sec_title, start_p, end_p) in enumerate(sections):
    chunk_text = ""
    for p in range(start_p, end_p + 1):
        chunk_text += f"\n--- Trang {p+1} ---\n" + doc[p].get_text()
    print(f"Đang dịch {sec_title} (Trang {start_p+1}-{end_p+1}, {len(chunk_text)} ký tự)...")
    trans = translate_chunk(sec_title, chunk_text)
    # Loại bỏ các đoạn dẫn dắt đầu ra nếu có
    if trans.startswith("Dưới đây là") or trans.startswith("Chắc chắn rồi"):
        trans = trans.split("\n", 2)[-1].strip()
        if trans.startswith("---"):
            trans = trans[3:].strip()
    results.append(trans)
    print(f"Xong phần {idx+1}/{len(sections)}")

header = """# Chương 01: Quy Mô Từ 0 Đến Hàng Triệu Người Dùng (Scale From Zero To Millions Of Users)

[← Lời Mở Đầu](00-loi-mo-dau.md) | [Mục lục](README.md) | [Chương 02: Ước lượng đại khái →](chuong-02-uoc-luong-dai-khai.md)

---
"""

footer = """
---

[← Lời Mở Đầu](00-loi-mo-dau.md) | [Mục lục](README.md) | [Chương 02: Ước lượng đại khái →](chuong-02-uoc-luong-dai-khai.md)
"""

full_content = header + "\n\n" + "\n\n---\n\n".join(results) + "\n\n" + footer
out_path = 'alex-xu-system-design-volume-1/chuong-01-scale-tu-0-den-trieu-nguoi-dung.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(full_content)

print(f"Hoàn thành và lưu vào {out_path} ({len(full_content)} ký tự)!")
