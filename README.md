**中文** | [English](README_en.md)

# VFG-7：细粒度 7 类车辆检测数据集

### VFG-7 Dataset

<p align="center">
  <img src="assets/overview_grid.jpg" alt="VFG-7 数据集总览" width="100%">
</p>

**VFG-7** 是由 **VFG-7 Dataset** 整理的 7 类细粒度车辆检测数据集，来源于中国东莞城市交通量调查项目。开源版本从总计 **50,000+ 张**原始交通图像中精选 **3,600 张**，约占完整数据量的 **7%**，包含约 50,000 个标注框及 10,784 条 AI 结构化描述。

采集场景覆盖白天/夜间、路侧监控、路测手机拍摄、无人机航拍等多种视角。如需获取完整数据集，请联系作者：**tianwenkang123@163.com**。

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Dataset on HuggingFace](https://img.shields.io/badge/🤗-Dataset-yellow.svg)](https://huggingface.co/datasets/Telody1220/VFG-7)
[![ModelScope](https://img.shields.io/badge/ModelScope-Dataset-blue.svg)](https://www.modelscope.cn/datasets/Telody/VFG-7)

---

## 亮点

- **7 类细粒度车辆分类** — 超越传统"大车/小车"粗分类
- **AI 富文本标注** — 每个检测框附带结构化描述（车辆类型、颜色、车身结构等）
- **真实交通场景** — 来源于中国东莞城市交通量调查项目，覆盖白天/夜间及多种采集视角
- **YOLO 即用** — 标准 YOLO 格式，Ultralytics 即插即用

---

## 类别定义

| ID | 类别 | 英文名 | 包含车型 |
|----|------|--------|----------|
| 0 | 小客车 | small_vehicle | 轿车、SUV、MPV、面包车、皮卡、微型货车 |
| 1 | 中型货车 | medium_truck | 蓝牌货车、轻卡、轻型厢式货车 |
| 2 | 重型厢式货车 | heavy_box_truck | 黄牌厢式货车、集装箱运输车 |
| 3 | 自卸车 | dump_truck | 渣土车、工程自卸车 |
| 4 | 罐体车 | tanker | 油罐车、液化气车、混凝土搅拌车 |
| 5 | 半挂车 | semi_trailer | 半挂集装箱车、半挂平板车、轿运车 |
| 6 | 大客车 | bus | 公交车、长途大巴、旅游客车 |

### 为什么划分 7 类？

交通工程中的 **PCU（当量小客车系数）** 因车型不同差异巨大：

| 车型 | PCU 系数 |
|------|----------|
| 小客车 | 1.0 |
| 中型货车 | 1.5 |
| 大型货车/自卸车 | 2.0 |
| 半挂车 | 3.0 |

传统"大车/小车"粗分类无法区分 PCU 1.5 的中型货车和 PCU 3.0 的半挂车，导致交通量估算偏差 50-100%。本数据集的 7 类细粒度划分直接对应不同 PCU 系数，可显著提升交调精度。

---

## 数据统计

| 数据划分 | 图片数 | 标注框数 | 格式 |
|----------|--------|----------|------|
| 训练集 | 3,000 | ~42,000 | YOLO |
| 验证集 | 600 | ~8,000 | YOLO |
| **开源合计** | **3,600** | **~50,000** | 完整数据 50,000+ 张中的精选子集（约 7%） |

| 附加数据 | 数量 |
|----------|------|
| AI 结构化描述 | 10,784 条 |

### 各类别分布

| 类别 | 训练集（张） | 验证集（张） |
|------|-------------|-------------|
| 小客车 | 429 | 236 |
| 中型货车 | 600 | 73 |
| 重型厢式货车 | 434 | 117 |
| 自卸车 | 429 | 35 |
| 罐体车 | 64 | 16 |
| 半挂车 | 570 | 87 |
| 大客车 | 474 | 36 |

---

## 目录结构

```
VFG-7/
├── images/
│   ├── train/   (3,000 张图像, 1920×1080 JPEG)
│   └── val/     (600 张图像)
├── labels/
│   ├── train/   (YOLO 格式 .txt)
│   └── val/
├── vlm_annotations.json   (AI 结构化描述)
├── data.yaml              (YOLO 配置文件)
├── README.md
└── LICENSE
```

---

## 标注方法

本数据集采用 **AI 辅助 + 人工审核** 的混合标注方案，对多视角交通图像进行车辆检测、细粒度类别标注与质量复核。公开文档仅介绍总体流程，不展开内部实现细节。

### 标注优势

| 对比项 | 传统人工标注 | AI 辅助标注 |
|--------|-------------|-------------|
| 标注一致性 | 标注员主观差异大 | 多视角结果校验，标准更统一 |
| 标注效率 | 人工逐框处理 | 自动化辅助后人工复核 |
| 标签丰富度 | 仅类别 + 边界框 | 结构化描述 + 自然语言 |
| 可扩展性 | 人力线性增长 | 适合大规模数据处理 |

---

## AI 描述示例

`vlm_annotations.json` 中每条记录包含：

```json
{
  "vehicle_type": "混凝土搅拌车",
  "color": "白色",
  "body_structure": "罐体式",
  "cargo_type": "混凝土",
  "desc": "白色混凝土搅拌车，罐体旋转中，行驶于最右车道",
  "agreement": 1.0
}
```

可用于多模态模型训练、标签质量审核、数据增强等场景。

---

## 快速上手

### 下载数据集

```bash
# 方式一：ModelScope 魔搭（国内推荐）
pip install modelscope
modelscope download --dataset Telody/VFG-7 --local_dir ./VFG-7

# 方式二：HuggingFace（海外推荐）
pip install huggingface_hub
huggingface-cli download Telody1220/VFG-7 --repo-type dataset --local-dir ./VFG-7
```

### 训练模型

```python
from ultralytics import YOLO

model = YOLO("yolo11l.pt")
model.train(data="VFG-7/data.yaml", epochs=50, imgsz=1280, batch=8)
```

### 基线指标（YOLO11L，imgsz=1280）

| 指标 | 数值 |
|------|------|
| mAP50 | 0.673 |
| mAP50-95 | 0.521 |
| 精确率 P | 0.68 |
| 召回率 R | 0.65 |

---

## 相关链接

| 平台 | 链接 |
|------|------|
| GitHub | https://github.com/telody/VFG-7 |
| Gitee | https://gitee.com/telody/vfg-7 |
| HuggingFace | https://huggingface.co/datasets/Telody1220/VFG-7 |
| ModelScope 魔搭 | https://www.modelscope.cn/datasets/Telody/VFG-7 |

---

## 引用

```bibtex
@dataset{vfg7_2026,
  title={VFG-7: Vehicle Fine-Grained 7-Class Detection Dataset},
  author={VFG-7 Dataset},
  year={2026},
  url={https://github.com/telody/VFG-7},
  license={CC BY-NC 4.0}
}
```

---

## 许可证

本数据集采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 许可。

- **署名** — 使用时须注明出处
- **非商业** — 不得用于商业目的

---

## 致谢

本数据集由 **VFG-7 Dataset** 整理，用于推动交通工程领域的智能化发展。

- 车辆检测框架：[Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- AI 辅助标注：用于提升细粒度车辆标注效率与一致性
- 数据来源：中国东莞城市交通量调查项目
