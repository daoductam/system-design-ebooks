import fitz
import subprocess
import os
import re
import time

doc = fitz.open('System-design-labs/system-design-questions.pdf')

days = []
for p in range(doc.page_count):
    txt = doc[p].get_text()
    m = re.search(r'DAY\s+(\d+)\s+[·•\-]\s+SYSTEM DESIGN', txt, re.IGNORECASE)
    if m:
        day_num = int(m.group(1))
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        title = lines[1] if len(lines) > 1 else f'Topic {day_num}'
        days.append((day_num, p+1, title))

day_list = []
for i in range(len(days)):
    d_num, s_page, title = days[i]
    e_page = days[i+1][1]-1 if i+1 < len(days) else doc.page_count
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    fn = f'day-{d_num:02d}-{slug}.md'
    prev_fn = f'day-{d_num-1:02d}-{re.sub(r"[^a-z0-9]+", "-", days[i-1][2].lower()).strip("-")}.md' if i > 0 else 'README.md'
    next_fn = f'day-{d_num+1:02d}-{re.sub(r"[^a-z0-9]+", "-", days[i+1][2].lower()).strip("-")}.md' if i+1 < len(days) else 'README.md'
    day_list.append({
        'day': d_num,
        'title': title,
        'start_page': s_page,
        'end_page': e_page,
        'file': fn,
        'prev': prev_fn,
        'next': next_fn
    })

def translate_day(item):
    out_file = os.path.join('60-days-of-system-design', item['file'])
    if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
        return
        
    s_p = item['start_page']
    e_p = item['end_page']
    
    txt = ""
    img_hints = []
    for p in range(s_p - 1, e_p):
        p_no = p + 1
        txt += f"\n--- Trang {p_no} ---\n" + doc[p].get_text()
        imgs = doc[p].get_images()
        for idx in range(len(imgs)):
            img_hints.append(f"   - Hình minh họa trang {p_no}: images/page_{p_no:03d}_{idx:02d}.png")
            
    hints_str = "\n".join(img_hints) if img_hints else "(Không có hình ảnh)"
    
    prompt = f"""Bạn là một Principal Software Architect và chuyên gia phỏng vấn System Design. Hãy dịch ĐẦY ĐỦ, NGUYÊN VĂN 100% tài liệu câu hỏi tình huống thực tế sau sang tiếng Việt chuẩn kỹ thuật theo định dạng Markdown GitHub.

Yêu cầu nghiêm ngặt:
1. DỊCH ĐẦY ĐỦ NGUYÊN VĂN 100%, KHÔNG TÓM TẮT, KHÔNG BỎ QUA BẤT KỲ CÂU NÀO: Đề bài tình huống (Scenario), Các phương án lựa chọn A/B/C/D, Câu trả lời đúng và Giải thích chi tiết (Why A wins, Why B is the trap answer, Why C/D is wrong).
2. Giữ nguyên các thuật ngữ kỹ thuật trong ngoặc hoặc song ngữ: API Gateway, BFF, Load Balancer, Token Bucket, Sliding Window, Idempotency Key, Sharding, Distributed Lock, CQRS, Saga Pattern, v.v.
3. Khi nhắc đến sơ đồ minh họa, hãy chèn cú pháp hình ảnh tương ứng:
{hints_str}
4. Định dạng Markdown trực quan, callout block `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`, bảng biểu, in đậm các điểm cốt lõi.

Văn bản gốc:
{txt}
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
                print(f"  Thử lại lần {attempt+1}/5 do lỗi: {err.strip()[:100]}")
                time.sleep(3 * (attempt + 1))
        except Exception as e:
            print(f"  Thử lại lần {attempt+1}/5 do ngoại lệ: {e}")
            time.sleep(3 * (attempt + 1))
    
    if not res:
        raise Exception(f"Failed after 5 attempts on Day {item['day']}")

    if res.startswith("Dưới đây là") or res.startswith("Chắc chắn rồi"):
        res = res.split("\n", 2)[-1].strip()
        if res.startswith("---"):
            res = res[3:].strip()
            
    header = f"""# Ngày {item['day']:02d}: {item['title']}

[← Ngày trước]({item['prev']}) | [Mục lục](README.md) | [Ngày tiếp theo →]({item['next']})

---
"""
    footer = f"""
---

[← Ngày trước]({item['prev']}) | [Mục lục](README.md) | [Ngày tiếp theo →]({item['next']})
"""
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(header + "\n\n" + res + "\n\n" + footer)
    print(f"Xong Ngày {item['day']:02d}: {item['title']} ({len(res)} ký tự)")

print(f"Bắt đầu dịch 60 Days of System Design ({len(day_list)} ngày)...")
for item in day_list:
    translate_day(item)
print("Hoàn thành toàn bộ 60 Days of System Design!")
