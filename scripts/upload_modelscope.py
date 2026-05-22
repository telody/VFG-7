"""上传 VFG-7 数据集到 ModelScope（魔搭）"""
from modelscope.hub.api import HubApi
from pathlib import Path
import time

REPO_ID = "Telody/VFG-7"
CLOUD = Path(r"\\JT-SVR1\jtgc\1 项目文件\田文康\交调计数系统\数据集\VFG7_opensource")
LOCAL_PROJECT = Path(r"D:\002车辆训练图片\VFG7")

api = HubApi()

# 先上传项目文件
print("=" * 50)
print("Step 1: 上传项目文件...")
print("=" * 50)

project_files = [
    (LOCAL_PROJECT / "README.md", "README.md"),
    (LOCAL_PROJECT / "LICENSE", "LICENSE"),
    (LOCAL_PROJECT / "data.yaml", "data.yaml"),
]

for local_path, remote_path in project_files:
    print(f"  上传 {remote_path}...")
    api.upload_file(
        repo_id=REPO_ID,
        file_path=str(local_path),
        path_in_repo=remote_path,
        repo_type="dataset",
    )

# 上传 assets
for f in (LOCAL_PROJECT / "assets").glob("*.jpg"):
    print(f"  上传 assets/{f.name}...")
    api.upload_file(
        repo_id=REPO_ID,
        file_path=str(f),
        path_in_repo=f"assets/{f.name}",
        repo_type="dataset",
    )

print("  ✓ 项目文件完成\n")

# Step 2: 上传数据文件
print("=" * 50)
print("Step 2: 上传数据文件 (~2.6 GB)...")
print("=" * 50)

t_start = time.time()

folders = [
    ("images/train", CLOUD / "images" / "train"),
    ("images/val", CLOUD / "images" / "val"),
    ("labels/train", CLOUD / "labels" / "train"),
    ("labels/val", CLOUD / "labels" / "val"),
]

for remote_dir, local_dir in folders:
    if not local_dir.exists():
        print(f"  [跳过] {remote_dir}")
        continue
    files = list(local_dir.iterdir())
    print(f"  上传 {remote_dir}/ ({len(files)} files)...")
    t0 = time.time()
    api.upload_folder(
        repo_id=REPO_ID,
        folder_path=str(local_dir),
        path_in_repo=remote_dir,
        repo_type="dataset",
    )
    print(f"    ✓ ({time.time()-t0:.0f}s)")

# VLM annotations
vlm = CLOUD / "vlm_annotations.json"
if vlm.exists():
    print("  上传 vlm_annotations.json...")
    api.upload_file(
        repo_id=REPO_ID,
        file_path=str(vlm),
        path_in_repo="vlm_annotations.json",
        repo_type="dataset",
    )

print(f"\n✓ 全部完成! 耗时 {(time.time()-t_start)/60:.1f} min")
print(f"  https://www.modelscope.cn/datasets/{REPO_ID}")
