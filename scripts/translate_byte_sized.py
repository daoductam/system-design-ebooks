import fitz
import subprocess
import os

doc = fitz.open('design.interview.alex/System Design Interview VOL 0 FREE.pdf')

topics = [
    {
        'file': '01-database-isolation-levels.md',
        'title': 'Cấp độ cô lập trong Cơ sở dữ liệu (Database Isolation Levels)',
        'pages': [5, 6]
    },
    {
        'file': '02-iaas-paas-saas.md',
        'title': 'Phân biệt Điện toán đám mây IaaS, PaaS và SaaS',
        'pages': [7]
    },
    {
        'file': '03-http-evolution.md',
        'title': 'Sự tiến hóa của giao thức HTTP (HTTP/1.0 -> HTTP/1.1 -> HTTP/2.0 -> HTTP/3.0 QUIC)',
        'pages': [3, 54, 55, 56]
    },
    {
        'file': '04-sso-single-sign-on.md',
        'title': 'Cơ chế xác thực một lần Single Sign-On (SSO)',
        'pages': [12, 13]
    },
    {
        'file': '05-password-storage-security.md',
        'title': 'Lưu trữ mật khẩu an toàn trong Cơ sở dữ liệu (Password Hashing & Salting)',
        'pages': [14, 15, 16]
    },
    {
        'file': '06-read-replica-pattern.md',
        'title': 'Mô hình bản sao đọc (Read Replica Pattern)',
        'pages': [4, 105, 106]
    },
    {
        'file': '07-email-receiving-flow.md',
        'title': 'Quy trình tiếp nhận và phân loại Email (Email Receiving Architecture)',
        'pages': [107, 108]
    }
]

def translate_topic(t):
    out_path = os.path.join('alex-xu-system-design-byte-sized', t['file'])
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"Skipping {t['file']}")
        return

    txt = ""
    img_hints = []
    for p in t['pages']:
        p_idx = p - 1
        txt += f"\n--- Trang {p} ---\n" + doc[p_idx].get_text()
        imgs = doc[p_idx].get_images()
        for idx in range(len(imgs)):
            img_hints.append(f"   - images/page_{p:03d}_{idx:02d}.jpeg")
            
    hints_str = "\n".join(img_hints) if img_hints else "(Không có hình ảnh)"
    prompt = f"""Bạn là Principal Software Architect. Hãy dịch TOÀN BỘ tài liệu kỹ thuật sau từ tuyển tập kiến trúc cô đọng của Alex Xu sang tiếng Việt định dạng Markdown chuẩn GitHub.

Yêu cầu nghiêm ngặt:
1. DỊCH ĐẦY ĐỦ NGUYÊN VĂN 100%, KHÔNG TÓM TẮT, KHÔNG CẮT BỚT BẤT KỲ CÂU HOẶC CHI TIẾT NÀO.
2. Giữ nguyên thuật ngữ kỹ thuật trong ngoặc hoặc song ngữ: MVCC, Dirty Read, Phantom Read, Repeatable Read, Serializable, OAuth2, SAML, IaaS, PaaS, SaaS, QUIC, Head-of-line Blocking, Salt, Bcrypt, Argon2, v.v.
3. Khi nhắc đến sơ đồ minh họa, hãy chèn cú pháp Markdown hình ảnh:
{hints_str}
4. Định dạng Markdown trực quan, chuyên nghiệp, bảng biểu, in đậm các điểm cốt lõi.

Văn bản cần dịch:
{txt}
"""
    cmd = ['C:\\Users\\tamda\\.gemini\\bin\\agy.exe', '--effort', 'low', '-p', prompt]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    out, err = p.communicate()
    if p.returncode != 0:
        raise Exception(f"Failed: {err}")
    res = out.strip()
    if res.startswith("Dưới đây là") or res.startswith("Chắc chắn rồi"):
        res = res.split("\n", 2)[-1].strip()
        if res.startswith("---"):
            res = res[3:].strip()
            
    header = f"# {t['title']}\n\n[← Mục lục](README.md)\n\n---\n\n"
    footer = f"\n\n---\n\n[← Mục lục](README.md)\n"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(header + res + footer)
    print(f"Hoàn thành {t['file']} ({len(res)} ký tự)!")

for t in topics:
    print(f"Đang xử lý {t['title']}...")
    translate_topic(t)
