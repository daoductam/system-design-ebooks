import os
import cv2
import time
import subprocess
from concurrent.futures import ProcessPoolExecutor
from rapidocr_onnxruntime import RapidOCR

ocr_engine = None

def init_worker():
    global ocr_engine
    ocr_engine = RapidOCR()

def ocr_single_page(p):
    global ocr_engine
    cache_path = f"alex-xu-system-design-volume-2/ocr_cache/page_{p:03d}.txt"
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 10:
        return p, True
    img_path = f"alex-xu-system-design-volume-2/images/page_{p:03d}.jpeg"
    if not os.path.exists(img_path):
        return p, False
    try:
        img = cv2.imread(img_path)
        img = cv2.resize(img, (0, 0), fx=0.75, fy=0.75)
        res, _ = ocr_engine(img)
        lines = [item[1] for item in res] if res else []
        text = "\n".join(lines)
        tmp_path = f"{cache_path}.tmp.{os.getpid()}"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp_path, cache_path)
        return p, True
    except Exception as e:
        print(f"Lỗi OCR trang {p}: {e}")
        return p, False

def ensure_ocr_pages(start_p, end_p, max_workers=2):
    missing = []
    for p in range(start_p, end_p + 1):
        cache_path = f"alex-xu-system-design-volume-2/ocr_cache/page_{p:03d}.txt"
        if not (os.path.exists(cache_path) and os.path.getsize(cache_path) > 10):
            missing.append(p)
    if not missing:
        return
    print(f"  [OCR] Cần nhận diện {len(missing)} trang ({missing[0]} -> {missing[-1]})...")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=max_workers, initializer=init_worker) as executor:
        list(executor.map(ocr_single_page, missing))
    print(f"  [OCR] Hoàn thành {len(missing)} trang trong {time.time() - t0:.1f}s.")

CHAPTERS = [
    {
        "idx": 0,
        "id": "00-loi-mo-dau",
        "title": "Lời Mở Đầu & Mục Lục (Foreword & Contents)",
        "start_page": 1,
        "end_page": 7,
        "file": "00-loi-mo-dau.md",
        "prev": None,
        "next": "chuong-01-proximity-service.md"
    },
    {
        "idx": 1,
        "id": "chuong-01-proximity-service",
        "title": "Chương 1: Dịch Vụ Định Vị Lân Cận (Proximity Service)",
        "start_page": 8,
        "end_page": 41,
        "file": "chuong-01-proximity-service.md",
        "prev": "00-loi-mo-dau.md",
        "next": "chuong-02-nearby-friends.md"
    },
    {
        "idx": 2,
        "id": "chuong-02-nearby-friends",
        "title": "Chương 2: Tìm Bạn Bè Gần Đây (Nearby Friends)",
        "start_page": 42,
        "end_page": 65,
        "file": "chuong-02-nearby-friends.md",
        "prev": "chuong-01-proximity-service.md",
        "next": "chuong-03-google-maps.md"
    },
    {
        "idx": 3,
        "id": "chuong-03-google-maps",
        "title": "Chương 3: Google Maps",
        "start_page": 66,
        "end_page": 97,
        "file": "chuong-03-google-maps.md",
        "prev": "chuong-02-nearby-friends.md",
        "next": "chuong-04-distributed-message-queue.md"
    },
    {
        "idx": 4,
        "id": "chuong-04-distributed-message-queue",
        "title": "Chương 4: Hàng Đợi Tin Nhắn Phân Tán (Distributed Message Queue)",
        "start_page": 98,
        "end_page": 137,
        "file": "chuong-04-distributed-message-queue.md",
        "prev": "chuong-03-google-maps.md",
        "next": "chuong-05-metrics-monitoring-and-alerting-system.md"
    },
    {
        "idx": 5,
        "id": "chuong-05-metrics-monitoring-and-alerting-system",
        "title": "Chương 5: Hệ Thống Giám Sát Chỉ Số và Cảnh Báo (Metrics Monitoring & Alerting)",
        "start_page": 138,
        "end_page": 162,
        "file": "chuong-05-metrics-monitoring-and-alerting-system.md",
        "prev": "chuong-04-distributed-message-queue.md",
        "next": "chuong-06-ad-click-event-aggregation.md"
    },
    {
        "idx": 6,
        "id": "chuong-06-ad-click-event-aggregation",
        "title": "Chương 6: Tổng Hợp Sự Kiện Nhấp Chuột Quảng Cáo (Ad Click Event Aggregation)",
        "start_page": 163,
        "end_page": 198,
        "file": "chuong-06-ad-click-event-aggregation.md",
        "prev": "chuong-05-metrics-monitoring-and-alerting-system.md",
        "next": "chuong-07-hotel-reservation-system.md"
    },
    {
        "idx": 7,
        "id": "chuong-07-hotel-reservation-system",
        "title": "Chương 7: Hệ Thống Đặt Phòng Khách Sạn (Hotel Reservation System)",
        "start_page": 199,
        "end_page": 227,
        "file": "chuong-07-hotel-reservation-system.md",
        "prev": "chuong-06-ad-click-event-aggregation.md",
        "next": "chuong-08-distributed-email-service.md"
    },
    {
        "idx": 8,
        "id": "chuong-08-distributed-email-service",
        "title": "Chương 8: Dịch Vụ Email Phân Tán (Distributed Email Service)",
        "start_page": 228,
        "end_page": 254,
        "file": "chuong-08-distributed-email-service.md",
        "prev": "chuong-07-hotel-reservation-system.md",
        "next": "chuong-09-s3-like-object-storage.md"
    },
    {
        "idx": 9,
        "id": "chuong-09-s3-like-object-storage",
        "title": "Chương 9: Lưu Trữ Đối Tượng Tương Tự S3 (S3-like Object Storage)",
        "start_page": 255,
        "end_page": 289,
        "file": "chuong-09-s3-like-object-storage.md",
        "prev": "chuong-08-distributed-email-service.md",
        "next": "chuong-10-real-time-gaming-leaderboard.md"
    },
    {
        "idx": 10,
        "id": "chuong-10-real-time-gaming-leaderboard",
        "title": "Chương 10: Bảng Xếp Hạng Game Thời Gian Thực (Real-time Gaming Leaderboard)",
        "start_page": 290,
        "end_page": 315,
        "file": "chuong-10-real-time-gaming-leaderboard.md",
        "prev": "chuong-09-s3-like-object-storage.md",
        "next": "chuong-11-payment-system.md"
    },
    {
        "idx": 11,
        "id": "chuong-11-payment-system",
        "title": "Chương 11: Hệ Thống Thanh Toán (Payment System)",
        "start_page": 316,
        "end_page": 341,
        "file": "chuong-11-payment-system.md",
        "prev": "chuong-10-real-time-gaming-leaderboard.md",
        "next": "chuong-12-digital-wallet.md"
    },
    {
        "idx": 12,
        "id": "chuong-12-digital-wallet",
        "title": "Chương 12: Ví Điện Tử (Digital Wallet)",
        "start_page": 342,
        "end_page": 385,
        "file": "chuong-12-digital-wallet.md",
        "prev": "chuong-11-payment-system.md",
        "next": "chuong-13-stock-exchange.md"
    },
    {
        "idx": 13,
        "id": "chuong-13-stock-exchange",
        "title": "Chương 13: Sàn Giao Dịch Chứng Khoán (Stock Exchange)",
        "start_page": 386,
        "end_page": 415,
        "file": "chuong-13-stock-exchange.md",
        "prev": "chuong-12-digital-wallet.md",
        "next": "14-loi-ket-va-index.md"
    },
    {
        "idx": 14,
        "id": "14-loi-ket-va-index",
        "title": "Lời Kết & Chỉ Mục (Afterword & Index)",
        "start_page": 416,
        "end_page": 427,
        "file": "14-loi-ket-va-index.md",
        "prev": "chuong-13-stock-exchange.md",
        "next": None
    }
]

def translate_chunk_api(chunk_text, img_hints, chapter_title):
    prompt = f"""Bạn là một Principal Software Architect và chuyên gia cao cấp về thiết kế hệ thống phân tán (Distributed Systems).
Hãy dịch TOÀN BỘ tài liệu kiến trúc kỹ thuật sau sang tiếng Việt chuẩn kỹ thuật cao cấp, chính xác 100%, định dạng Markdown chuẩn GitHub.

Chủ đề: {chapter_title}

Yêu cầu nghiêm ngặt:
1. DỊCH ĐẦY ĐỦ NGUYÊN VĂN 100%, TUYỆT ĐỐI KHÔNG TÓM TẮT, KHÔNG CẮT BỚT BẤT KỲ CÂU, DÒNG, CÔNG THỨC HAY CHI TIẾT KỸ THUẬT NÀO.
2. Giữ nguyên thuật ngữ kỹ thuật trong ngoặc hoặc dùng song ngữ: High Availability, Scalability, Fault Tolerance, Latency, Throughput, Consistent Hashing, Sharding, Replication Lag, Quorum, Quadtree, Geohash, Write-Ahead Log (WAL), Raft, 2PC, Saga, v.v.
3. Khi nhắc đến hình ảnh, sơ đồ kiến trúc hoặc minh họa trang tài liệu, hãy chèn đúng cú pháp Markdown hình ảnh:
{img_hints}
4. Định dạng Markdown trực quan, tiêu đề rõ ràng, bảng biểu, callout box GitHub `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, in đậm các ý chính.

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
                txt = out.strip()
                if any(bad in txt[:100] for bad in ["Tôi không thể", "Tôi rất tiếc", "I cannot", "I'm sorry"]):
                    print(f"    Phát hiện câu trả lời từ chối, thử lại lần {attempt+1}/5...")
                    time.sleep(3 * (attempt + 1))
                    continue
                res = txt
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

def process_chapter(ch):
    out_file = os.path.join("alex-xu-system-design-volume-2", ch["file"])
    if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
        print(f"Bỏ qua {ch['id']} (đã hoàn thành)")
        return
        
    print(f"\n=======================================================")
    print(f">>> Đang xử lý: {ch['title']} (Trang {ch['start_page']} -> {ch['end_page']})...")
    print(f"=======================================================")
    
    # 1. Đảm bảo OCR đầy đủ
    ensure_ocr_pages(ch["start_page"], ch["end_page"])
    
    # 2. Phân chia chunks (~5-6 trang mỗi chunk)
    chunks = []
    curr = ch["start_page"]
    while curr <= ch["end_page"]:
        end = min(curr + 5, ch["end_page"])
        chunks.append((curr, end))
        curr = end + 1
        
    translated_parts = []
    for c_start, c_end in chunks:
        chunk_text = ""
        img_hints = []
        for p in range(c_start, c_end + 1):
            cache_file = f"alex-xu-system-design-volume-2/ocr_cache/page_{p:03d}.txt"
            p_text = open(cache_file, encoding="utf-8").read() if os.path.exists(cache_file) else ""
            chunk_text += f"\n--- Trang {p} ---\n" + p_text
            img_hints.append(f"   - ![Sơ đồ trang {p}](images/page_{p:03d}.jpeg)")
            
        hints_str = "\n".join(img_hints)
        chunk_text = chunk_text.replace('\x00', '')
        print(f"  [Dịch] Trang {c_start} - {c_end} ({len(chunk_text)} ký tự)...")
        t_trans = translate_chunk_api(chunk_text, hints_str, ch["title"])
        translated_parts.append(t_trans)
        
    # 3. Tạo thanh điều hướng
    prev_link = f"[{ch['prev']}]({ch['prev']})" if ch["prev"] else "[Mục lục](README.md)"
    next_link = f"[{ch['next']}]({ch['next']})" if ch["next"] else "[Mục lục](README.md)"
    
    top_nav = f"[← Chương trước]({ch['prev'] if ch['prev'] else 'README.md'}) | [Mục lục](README.md) | [Chương tiếp theo →]({ch['next'] if ch['next'] else 'README.md'})\n\n---\n\n"
    bottom_nav = f"\n\n---\n\n## Điều hướng\n\n- {prev_link}\n- [Mục lục](README.md)\n- {next_link}\n"
    
    full_content = top_nav + "\n\n".join(translated_parts) + bottom_nav
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(full_content)
    print(f"[HOÀN THÀNH] {ch['file']} ({os.path.getsize(out_file)} bytes)")
