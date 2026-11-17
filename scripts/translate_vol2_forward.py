import sys
import os
from scripts.translate_vol2_common import CHAPTERS, process_chapter

if __name__ == "__main__":
    print("=== BẮT ĐẦU WORKER FORWARD: CHƯƠNG 1 ĐẾN 7 ===")
    for ch in CHAPTERS[1:8]:
        process_chapter(ch)
    print("=== WORKER FORWARD HOÀN TẤT! ===")
