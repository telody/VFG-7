"""
生成 VFG-7 数据集可视化样本图，用于 GitHub README 展示。
从每个类别各选一张代表性图片，画上标注框+类别名。
"""
import cv2
import numpy as np
import json
from pathlib import Path
from collections import defaultdict

CLOUD_DATASET = Path(r"\\JT-SVR1\jtgc\1 项目文件\田文康\交调计数系统\数据集\VFG7_opensource")
OUTPUT_DIR = Path(r"D:\002车辆训练图片\VFG7\assets")

CLASS_NAMES = {
    0: "small_vehicle",
    1: "medium_truck",
    2: "heavy_box_truck",
    3: "dump_truck",
    4: "tanker",
    5: "semi_trailer",
    6: "bus",
}

CLASS_NAMES_CN = {
    0: "小客车",
    1: "中型货车",
    2: "重型厢式货车",
    3: "自卸车",
    4: "罐体车",
    5: "半挂车",
    6: "大客车",
}

# 每个类别一个颜色 (BGR)
COLORS = {
    0: (0, 200, 0),      # 绿
    1: (255, 150, 0),    # 蓝橙
    2: (0, 100, 255),    # 橙红
    3: (0, 0, 255),      # 红
    4: (255, 0, 200),    # 紫
    5: (255, 255, 0),    # 青
    6: (0, 255, 255),    # 黄
}


def parse_yolo_label(label_path, img_w, img_h):
    """解析 YOLO 标签文件，返回 [(cls, x1, y1, x2, y2), ...]"""
    boxes = []
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            cls = int(parts[0])
            cx, cy, w, h = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
            x1 = int((cx - w / 2) * img_w)
            y1 = int((cy - h / 2) * img_h)
            x2 = int((cx + w / 2) * img_w)
            y2 = int((cy + h / 2) * img_h)
            boxes.append((cls, x1, y1, x2, y2))
    return boxes


def draw_boxes(img, boxes):
    """在图片上绘制标注框"""
    for cls, x1, y1, x2, y2 in boxes:
        color = COLORS.get(cls, (200, 200, 200))
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{CLASS_NAMES.get(cls, '?')} ({CLASS_NAMES_CN.get(cls, '?')})"
        # 标签背景
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
        cv2.putText(img, label, (x1 + 2, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return img


def find_best_samples():
    """每类选择包含该类最多目标的图片"""
    img_dir = CLOUD_DATASET / "images" / "train"
    lbl_dir = CLOUD_DATASET / "labels" / "train"

    cls_candidates = defaultdict(list)  # cls -> [(stem, count, total_boxes)]

    for lbl_file in lbl_dir.glob("*.txt"):
        stem = lbl_file.stem
        cls_count = defaultdict(int)
        total = 0
        with open(lbl_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    cls_count[int(parts[0])] += 1
                    total += 1

        for cls_id, count in cls_count.items():
            # 优先选有多种类别的丰富图片
            cls_candidates[cls_id].append((stem, count, total))

    # 每类选目标数最多的图
    best = {}
    for cls_id in range(7):
        candidates = cls_candidates.get(cls_id, [])
        if candidates:
            # 按总框数排序（选内容丰富的），然后按该类数排序
            candidates.sort(key=lambda x: (x[2], x[1]), reverse=True)
            best[cls_id] = candidates[0][0]

    return best


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    img_dir = CLOUD_DATASET / "images" / "train"
    lbl_dir = CLOUD_DATASET / "labels" / "train"

    print("选择各类别代表样本...")
    best = find_best_samples()
    for cls_id, stem in best.items():
        print(f"  cls{cls_id} {CLASS_NAMES[cls_id]:20s} → {stem}")

    # 生成单类展示图 (每类一张)
    print("\n生成单类展示图...")
    for cls_id, stem in best.items():
        img_path = img_dir / f"{stem}.jpg"
        lbl_path = lbl_dir / f"{stem}.txt"
        buf = np.fromfile(str(img_path), dtype=np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        if img is None:
            print(f"  [跳过] 无法读取 {img_path}")
            continue
        h, w = img.shape[:2]
        boxes = parse_yolo_label(lbl_path, w, h)
        img = draw_boxes(img, boxes)
        out_path = OUTPUT_DIR / f"sample_cls{cls_id}_{CLASS_NAMES[cls_id]}.jpg"
        _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
        buf.tofile(str(out_path))
        print(f"  ✓ {out_path.name} ({len(boxes)} boxes)")

    # 生成综合拼图 (2x4 grid)
    print("\n生成综合展示拼图...")
    grid_imgs = []
    target_h, target_w = 360, 640
    for cls_id in range(7):
        stem = best.get(cls_id)
        if not stem:
            grid_imgs.append(np.zeros((target_h, target_w, 3), dtype=np.uint8))
            continue
        img_path = img_dir / f"{stem}.jpg"
        lbl_path = lbl_dir / f"{stem}.txt"
        buf = np.fromfile(str(img_path), dtype=np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        h, w = img.shape[:2]
        boxes = parse_yolo_label(lbl_path, w, h)
        img = draw_boxes(img, boxes)
        img = cv2.resize(img, (target_w, target_h))
        # 类别标签
        cv2.putText(img, f"cls{cls_id}: {CLASS_NAMES[cls_id]}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        grid_imgs.append(img)

    # 补一个空白+统计信息
    info_img = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    cv2.putText(info_img, "VFG-7 Dataset", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 200, 255), 2)
    cv2.putText(info_img, "7 classes | 3600 images", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    cv2.putText(info_img, "VLM-assisted annotation", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    cv2.putText(info_img, "CC BY-NC 4.0", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    grid_imgs.append(info_img)

    # 2x4 grid
    row1 = np.hstack(grid_imgs[0:4])
    row2 = np.hstack(grid_imgs[4:8])
    grid = np.vstack([row1, row2])

    out_path = OUTPUT_DIR / "overview_grid.jpg"
    _, buf = cv2.imencode(".jpg", grid, [cv2.IMWRITE_JPEG_QUALITY, 92])
    buf.tofile(str(out_path))
    print(f"  ✓ {out_path.name} ({grid.shape[1]}x{grid.shape[0]})")

    print(f"\n✓ 所有样本图已保存到 {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
