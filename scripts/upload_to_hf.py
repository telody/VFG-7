"""上传 VFG-7 数据集到 HuggingFace"""
from huggingface_hub import HfApi
from pathlib import Path
import time

REPO_ID = "Telody1220/VFG-7"
LOCAL_PROJECT = Path(r"D:\002车辆训练图片\VFG7")
CLOUD_DATASET = Path(r"\\JT-SVR1\jtgc\1 项目文件\田文康\交调计数系统\数据集\VFG7_opensource")

api = HfApi()

# Step 1: 上传项目文件（README, LICENSE, data.yaml, assets）
print("=" * 50)
print("Step 1: 上传项目文件...")
print("=" * 50)

small_files = [
    ("README.md", LOCAL_PROJECT / "README.md"),
    ("LICENSE", LOCAL_PROJECT / "LICENSE"),
    ("data.yaml", LOCAL_PROJECT / "data.yaml"),
]

for remote_name, local_path in small_files:
    print(f"  上传 {remote_name}...")
    api.upload_file(
        path_or_fileobj=str(local_path),
        path_in_repo=remote_name,
        repo_id=REPO_ID,
        repo_type="dataset",
    )

# 上传 assets 目录
print("  上传 assets/...")
api.upload_folder(
    folder_path=str(LOCAL_PROJECT / "assets"),
    path_in_repo="assets",
    repo_id=REPO_ID,
    repo_type="dataset",
)

print("  ✓ 项目文件上传完成\n")

# Step 2: 上传数据集大文件（images, labels, vlm_annotations）
print("=" * 50)
print("Step 2: 上传数据集文件 (~2.6 GB)...")
print("=" * 50)

for subdir in ["images/train", "images/val", "labels/train", "labels/val"]:
    src = CLOUD_DATASET / subdir
    if not src.exists():
        print(f"  [跳过] {subdir} 不存在")
        continue
    file_count = len(list(src.iterdir()))
    print(f"  上传 {subdir}/ ({file_count} files)...")
    t0 = time.time()
    api.upload_folder(
        folder_path=str(src),
        path_in_repo=subdir,
        repo_id=REPO_ID,
        repo_type="dataset",
    )
    elapsed = time.time() - t0
    print(f"    ✓ 完成 ({elapsed:.0f}s)")

# VLM annotations
vlm_file = CLOUD_DATASET / "vlm_annotations.json"
if vlm_file.exists():
    print(f"  上传 vlm_annotations.json...")
    api.upload_file(
        path_or_fileobj=str(vlm_file),
        path_in_repo="vlm_annotations.json",
        repo_id=REPO_ID,
        repo_type="dataset",
    )

print("\n" + "=" * 50)
print("✓ 全部上传完成!")
print(f"  https://huggingface.co/datasets/{REPO_ID}")
print("=" * 50)
