import sys
import os
sys.path.insert(0, os.path.abspath("."))
from scripts.translate_vol2_common import CHAPTERS, process_chapter

if __name__ == "__main__":
    print("=== BẮT ĐẦU WORKER REVERSE: CHƯƠNG 14 VỀ 8 ===")
    for ch in CHAPTERS[14:7:-1]:
        process_chapter(ch)
    print("=== WORKER REVERSE HOÀN TẤT! ===")
