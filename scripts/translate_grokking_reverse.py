import fitz
import subprocess
import os
import glob
import re
import time

pdf_files = sorted(glob.glob('Grokking-Modern-System-Design-Interview-for-Engineers-Managers/*.pdf'))
readme = open('grokking-modern-system-design/README.md', encoding='utf-8').read()
md_links = re.findall(r'\[([^\]]+)\]\((0\d\d-[^)]+\.md)\)', readme)

mapping = []
for i in range(min(len(pdf_files), len(md_links))):
    pdf = pdf_files[i]
    title, md = md_links[i]
    prev_md = md_links[i-1][1] if i > 0 else 'README.md'
    next_md = md_links[i+1][1] if i+1 < len(md_links) else 'README.md'
    prefix = os.path.basename(pdf)[:3]
    mapping.append({
        'pdf': pdf,
        'prefix': prefix,
        'title': title,
        'file': md,
        'prev': prev_md,
        'next': next_md
    })

def translate_chunk_api(chunk_text, img_hints):
    prompt = f"""Bạn là một Principal Software Architect và chuyên gia cao cấp về thiết kế hệ thống phân tán (Distributed Systems). Hãy dịch TOÀN BỘ tài liệu kỹ thuật sau sang tiếng Việt chuẩn kỹ thuật, chính xác 100%, định dạng Markdown chuẩn GitHub.

Yêu cầu nghiêm ngặt:
1. DỊCH ĐẦY ĐỦ NGUYÊN VĂN 100%, TUYỆT ĐỐI KHÔNG TÓM TẮT, KHÔNG CẮT BỚT BẤT KỲ CÂU, DÒNG HAY CHI TIẾT KỸ THUẬT NÀO.
2. Giữ nguyên thuật ngữ kỹ thuật trong ngoặc hoặc dùng song ngữ: High Availability, Scalability, Fault Tolerance, Latency, Throughput, DNS, Anycast, Consistent Hashing, Sharding, Replication Lag, Quorum, v.v.
3. Khi nhắc đến hình ảnh hoặc sơ đồ, hãy chèn đúng cú pháp Markdown hình ảnh:
{img_hints}
4. Định dạng Markdown trực quan, tiêu đề rõ ràng, bảng biểu, callout box `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, in đậm các ý chính.

Tài liệu kỹ thuật cần dịch:
{chunk_text}
"""
    cmd = ['C:\\Users\\tamda\\.gemini\\bin\\agy.exe', '--effort', 'low', '-p', prompt]
    res = ""
    for attempt in range(5):
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            out, err = p.communicate()
            if p.returncode == 0 and len(out.strip()) > 100:
                res = out.strip()
                break
            else:
                print(f"    Thử lại chunk lần {attempt+1}/5 do lỗi: {err.strip()[:100]}")
                time.sleep(3 * (attempt + 1))
        except Exception as e:
            print(f"    Thử lại chunk lần {attempt+1}/5 do ngoại lệ: {e}")
            time.sleep(3 * (attempt + 1))
    
    if not res:
        raise Exception("Translation failed after 5 attempts")
    if res.startswith("Dưới đây là") or res.startswith("Chắc chắn rồi"):
        res = res.split("\n", 2)[-1].strip()
        if res.startswith("---"):
            res = res[3:].strip()
    return res

def process_grokking_item(item):
    out_file = os.path.join('grokking-modern-system-design', item['file'])
    if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
        return
        
    doc = fitz.open(item['pdf'])
    print(f"\n>>> Đang xử lý Grokking [{item['prefix']}]: {item['title']} ({doc.page_count} trang)...")
    
    # Chia trang theo chunk 6 trang
    page_chunks = []
    curr = 0
    while curr < doc.page_count:
        end = min(curr + 6, doc.page_count)
        page_chunks.append((curr, end))
        curr = end
        
    results = []
    for c_start, c_end in page_chunks:
        chunk_text = ""
        img_hints = []
        for p in range(c_start, c_end):
            p_no = p + 1
            chunk_text += f"\n--- Trang {p_no} ---\n" + doc[p].get_text()
            imgs = doc[p].get_images()
            for idx in range(len(imgs)):
                for ext in ['png', 'jpeg', 'jpg']:
                    fpath = f"images/topic_{item['prefix']}_p{p_no:03d}_{idx:02d}.{ext}"
                    if os.path.exists(os.path.join('grokking-modern-system-design', fpath)):
                        img_hints.append(f"   - ![{item['title']}]({fpath})")
                        break
                
        hints_str = "\n".join(img_hints[:15]) if img_hints else "(Không có hình ảnh sơ đồ trong đoạn này)"
        chunk_text = chunk_text.replace('\x00', '')
        print(f"  Dịch trang {c_start+1}-{c_end} ({len(chunk_text)} ký tự)...")
        trans = translate_chunk_api(chunk_text, hints_str)
        results.append(trans)
        
    header = f"""# {item['title']}

[← Bài trước]({item['prev']}) | [Mục lục](README.md) | [Bài tiếp theo →]({item['next']})

---
"""
    footer = f"""
---

[← Bài trước]({item['prev']}) | [Mục lục](README.md) | [Bài tiếp theo →]({item['next']})
"""
    final_content = header + "\n\n" + "\n\n---\n\n".join(results) + "\n\n" + footer
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Hoàn thành {item['file']} ({len(final_content)} ký tự)!")

print(f"Bắt đầu dịch Grokking Modern System Design [Worker 2 - Từ cuối lên]...")
for item in reversed(mapping):
    process_grokking_item(item)
print("Hoàn thành toàn bộ Grokking Modern System Design [Worker 2]!")
