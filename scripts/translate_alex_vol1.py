import fitz
import subprocess
import os
import re
from concurrent.futures import ThreadPoolExecutor

doc = fitz.open('design.interview.alex/System Design Interview VOL 1 BUY.pdf')

chapters = [
    {
        'id': 2,
        'title': 'Chương 02: Ước lượng đại khái (Back-of-the-envelope Estimation)',
        'file': 'chuong-02-uoc-luong-dai-khai.md',
        'prev': 'chuong-01-scale-tu-0-den-trieu-nguoi-dung.md',
        'next': 'chuong-03-khung-suon-phong-van-system-design.md',
        'pages': (34, 41)
    },
    {
        'id': 3,
        'title': 'Chương 03: Khung sườn phỏng vấn System Design (A Framework For System Design Interviews)',
        'file': 'chuong-03-khung-suon-phong-van-system-design.md',
        'prev': 'chuong-02-uoc-luong-dai-khai.md',
        'next': 'chuong-04-thiet-ke-rate-limiter.md',
        'pages': (42, 50)
    },
    {
        'id': 4,
        'title': 'Chương 04: Thiết kế Bộ giới hạn tốc độ (Design A Rate Limiter)',
        'file': 'chuong-04-thiet-ke-rate-limiter.md',
        'prev': 'chuong-03-khung-suon-phong-van-system-design.md',
        'next': 'chuong-05-thiet-ke-consistent-hashing.md',
        'pages': (51, 70)
    },
    {
        'id': 5,
        'title': 'Chương 05: Thiết kế Băm nhất quán (Design Consistent Hashing)',
        'file': 'chuong-05-thiet-ke-consistent-hashing.md',
        'prev': 'chuong-04-thiet-ke-rate-limiter.md',
        'next': 'chuong-06-thiet-ke-key-value-store.md',
        'pages': (71, 86)
    },
    {
        'id': 6,
        'title': 'Chương 06: Thiết kế Kho lưu trữ Key-Value (Design A Key-Value Store)',
        'file': 'chuong-06-thiet-ke-key-value-store.md',
        'prev': 'chuong-05-thiet-ke-consistent-hashing.md',
        'next': 'chuong-07-thiet-ke-unique-id-generator-phan-tan.md',
        'pages': (87, 109)
    },
    {
        'id': 7,
        'title': 'Chương 07: Thiết kế Trình tạo ID duy nhất trong hệ thống phân tán (Design Unique ID Generator)',
        'file': 'chuong-07-thiet-ke-unique-id-generator-phan-tan.md',
        'prev': 'chuong-06-thiet-ke-key-value-store.md',
        'next': 'chuong-08-thiet-ke-url-shortener.md',
        'pages': (110, 118)
    },
    {
        'id': 8,
        'title': 'Chương 08: Thiết kế Hệ thống rút gọn URL (Design A URL Shortener)',
        'file': 'chuong-08-thiet-ke-url-shortener.md',
        'prev': 'chuong-07-thiet-ke-unique-id-generator-phan-tan.md',
        'next': 'chuong-09-thiet-ke-web-crawler.md',
        'pages': (119, 131)
    },
    {
        'id': 9,
        'title': 'Chương 09: Thiết kế Trình thu thập dữ liệu Web (Design A Web Crawler)',
        'file': 'chuong-09-thiet-ke-web-crawler.md',
        'prev': 'chuong-08-thiet-ke-url-shortener.md',
        'next': 'chuong-10-thiet-ke-he-thong-thong-bao.md',
        'pages': (132, 150)
    },
    {
        'id': 10,
        'title': 'Chương 10: Thiết kế Hệ thống thông báo (Design A Notification System)',
        'file': 'chuong-10-thiet-ke-he-thong-thong-bao.md',
        'prev': 'chuong-09-thiet-ke-web-crawler.md',
        'next': 'chuong-11-thiet-ke-news-feed-system.md',
        'pages': (151, 165)
    },
    {
        'id': 11,
        'title': 'Chương 11: Thiết kế Hệ thống Bảng tin (Design A News Feed System)',
        'file': 'chuong-11-thiet-ke-news-feed-system.md',
        'prev': 'chuong-10-thiet-ke-he-thong-thong-bao.md',
        'next': 'chuong-12-thiet-ke-chat-system.md',
        'pages': (166, 177)
    },
    {
        'id': 12,
        'title': 'Chương 12: Thiết kế Hệ thống Chat (Design A Chat System)',
        'file': 'chuong-12-thiet-ke-chat-system.md',
        'prev': 'chuong-11-thiet-ke-news-feed-system.md',
        'next': 'chuong-13-thiet-ke-search-autocomplete.md',
        'pages': (178, 199)
    },
    {
        'id': 13,
        'title': 'Chương 13: Thiết kế Hệ thống gợi ý tìm kiếm (Design Search Autocomplete)',
        'file': 'chuong-13-thiet-ke-search-autocomplete.md',
        'prev': 'chuong-12-thiet-ke-chat-system.md',
        'next': 'chuong-14-thiet-ke-youtube.md',
        'pages': (200, 219)
    },
    {
        'id': 14,
        'title': 'Chương 14: Thiết kế YouTube (Design YouTube)',
        'file': 'chuong-14-thiet-ke-youtube.md',
        'prev': 'chuong-13-thiet-ke-search-autocomplete.md',
        'next': 'chuong-15-thiet-ke-google-drive.md',
        'pages': (220, 243)
    },
    {
        'id': 15,
        'title': 'Chương 15: Thiết kế Google Drive (Design Google Drive)',
        'file': 'chuong-15-thiet-ke-google-drive.md',
        'prev': 'chuong-14-thiet-ke-youtube.md',
        'next': 'chuong-16-hanh-trinh-hoc-tap-tiep-dien.md',
        'pages': (244, 263)
    },
    {
        'id': 16,
        'title': 'Chương 16: Hành trình học tập tiếp diễn & Lời bạt (The Learning Continues & Afterword)',
        'file': 'chuong-16-hanh-trinh-hoc-tap-tiep-dien.md',
        'prev': 'chuong-15-thiet-ke-google-drive.md',
        'next': 'README.md',
        'pages': (264, 269)
    }
]

def translate_chunk_api(chunk_text, img_hints):
    prompt = f"""Bạn là một Principal Software Architect và chuyên gia kỹ thuật dịch thuật công nghệ cao cấp. Hãy dịch TOÀN BỘ tài liệu kỹ thuật sau sang tiếng Việt chuẩn kỹ thuật, văn phong rõ ràng, chuyên nghiệp theo định dạng Markdown chuẩn GitHub.

Yêu cầu nghiêm ngặt:
1. DỊCH ĐẦY ĐỦ NGUYÊN VĂN 100%, TUYỆT ĐỐI KHÔNG TÓM TẮT, KHÔNG CẮT BỚT BẤT KỲ CÂU, DÒNG HAY CHI TIẾT NÀO.
2. Giữ nguyên các thuật ngữ kỹ thuật trong ngoặc hoặc dùng thuật ngữ chuẩn: Rate Limiter, Consistent Hashing, Virtual Nodes, Key-Value Store, Vector Clock, Gossip Protocol, Snowflake ID, Base62, Bloom Filter, v.v.
3. Khi gặp hình ảnh minh họa (Figure X-Y) trong văn bản, hãy chèn đúng cú pháp Markdown hình ảnh dựa trên các hình trích xuất có sẵn sau đây nếu có:
{img_hints}
4. Định dạng Markdown trực quan, bảng biểu đẹp, in đậm các ý quan trọng, công thức toán học KaTeX nếu có.

Tài liệu kỹ thuật cần dịch:
{chunk_text}
"""
    cmd = ['C:\\Users\\tamda\\.gemini\\bin\\agy.exe', '--effort', 'low', '-p', prompt]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    out, err = p.communicate()
    if p.returncode != 0:
        raise Exception(f"Translation failed: {err}")
    res = out.strip()
    if res.startswith("Dưới đây là") or res.startswith("Chắc chắn rồi"):
        res = res.split("\n", 2)[-1].strip()
        if res.startswith("---"):
            res = res[3:].strip()
    return res

def process_chapter(ch):
    start_p, end_p = ch['pages']
    out_file = os.path.join('alex-xu-system-design-volume-1', ch['file'])
    if os.path.exists(out_file) and os.path.getsize(out_file) > 2000:
        print(f"Skipping {ch['file']} (already exists)")
        return
    
    print(f"\n>>> Bắt đầu xử lý {ch['title']} (Trang {start_p}-{end_p})...")
    
    # Chia thành các chunk ~ 5-7 trang
    page_chunks = []
    curr = start_p
    while curr <= end_p:
        chunk_end = min(curr + 5, end_p)
        page_chunks.append((curr, chunk_end))
        curr = chunk_end + 1
        
    chunk_results = []
    for c_start, c_end in page_chunks:
        chunk_text = ""
        img_hints = []
        for p in range(c_start - 1, c_end):
            p_no = p + 1
            chunk_text += f"\n--- Trang {p_no} ---\n" + doc[p].get_text()
            imgs = doc[p].get_images()
            for idx in range(len(imgs)):
                img_hints.append(f"   - Hình trang {p_no}: images/page_{p_no:03d}_{idx:02d}.jpeg")
        
        hints_str = "\n".join(img_hints) if img_hints else "   (Không có hình ảnh ở các trang này)"
        print(f"  Dịch trang {c_start}-{c_end} ({len(chunk_text)} ký tự)...")
        translated_text = translate_chunk_api(chunk_text, hints_str)
        chunk_results.append(translated_text)
        
    header = f"""# {ch['title']}

[← Chương trước]({ch['prev']}) | [Mục lục](README.md) | [Chương tiếp theo →]({ch['next']})

---
"""
    footer = f"""
---

[← Chương trước]({ch['prev']}) | [Mục lục](README.md) | [Chương tiếp theo →]({ch['next']})
"""
    final_content = header + "\n\n" + "\n\n---\n\n".join(chunk_results) + "\n\n" + footer
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Hoàn thành {ch['file']} ({len(final_content)} ký tự)!")

for ch in chapters:
    process_chapter(ch)
