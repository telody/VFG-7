"""上传 VFG-7 到 ModelScope"""
from modelscope.hub.api import HubApi
from pathlib import Path
import time

api = HubApi()
api.login('***REDACTED***')

REPO_ID = 'Telody/VFG-7'
LOCAL = Path(r'D:\002车辆训练图片\VFG7')
CLOUD = Path(r'\\JT-SVR1\jtgc\1 项目文件\田文康\交调计数系统\数据集\VFG7_opensource')

# Step 1: 上传项目文件
print("=" * 50)
print("Step 1: 上传项目文件...")
print("=" * 50)

for fname in ['README.md', 'LICENSE', 'data.yaml']:
    print(f"  上传 {fname}...")
    api.upload_file(
        path_or_fileobj=str(LOCAL / fname),
        path_in_repo=fname,
        repo_id=REPO_ID,
        repo_type='dataset',
    )

# assets
print("  上传 assets/...")
api.upload_folder(
    repo_id=REPO_ID,
    folder_path=str(LOCAL / 'assets'),
    path_in_repo='assets',
    repo_type='dataset',
)
print("  ✓ 项目文件完成\n")

# Step 2: 上传数据
print("=" * 50)
print("Step 2: 上传数据文件 (~2.6 GB)...")
print("=" * 50)

t_start = time.time()

for subdir in ['images/train', 'images/val', 'labels/train', 'labels/val']:
    src = CLOUD / subdir.replace('/', '\\')
    if not src.exists():
        print(f"  [跳过] {subdir}")
        continue
    n = len(list(src.iterdir()))
    print(f"  上传 {subdir}/ ({n} files)...")
    t0 = time.time()
    api.upload_folder(
        repo_id=REPO_ID,
        folder_path=str(src),
        path_in_repo=subdir,
        repo_type='dataset',
    )
    print(f"    ✓ ({time.time()-t0:.0f}s)")

# VLM annotations
vlm = CLOUD / 'vlm_annotations.json'
if vlm.exists():
    print("  上传 vlm_annotations.json...")
    api.upload_file(
        path_or_fileobj=str(vlm),
        path_in_repo='vlm_annotations.json',
        repo_id=REPO_ID,
        repo_type='dataset',
    )

print(f"\n✓ 全部完成! 耗时 {(time.time()-t_start)/60:.1f} min")
print(f"  https://www.modelscope.cn/datasets/{REPO_ID}")
