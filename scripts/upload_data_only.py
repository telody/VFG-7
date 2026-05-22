"""仅上传数据文件到 HuggingFace（项目文件已上传）"""
from huggingface_hub import HfApi
from pathlib import Path
import time

REPO_ID = "Telody1220/VFG-7"
CLOUD = Path(r"\\JT-SVR1\jtgc\1 项目文件\田文康\交调计数系统\数据集\VFG7_opensource")

api = HfApi()

folders = [
    ("images/train", CLOUD / "images" / "train"),
    ("images/val", CLOUD / "images" / "val"),
    ("labels/train", CLOUD / "labels" / "train"),
    ("labels/val", CLOUD / "labels" / "val"),
]

t_start = time.time()
for remote_path, local_path in folders:
    if not local_path.exists():
        print(f"[跳过] {remote_path}")
        continue
    n = len(list(local_path.iterdir()))
    print(f"上传 {remote_path}/ ({n} files)...")
    t0 = time.time()
    api.upload_folder(
        folder_path=str(local_path),
        path_in_repo=remote_path,
        repo_id=REPO_ID,
        repo_type="dataset",
    )
    print(f"  ✓ {remote_path} ({time.time()-t0:.0f}s)")

# VLM annotations
vlm = CLOUD / "vlm_annotations.json"
if vlm.exists():
    print("上传 vlm_annotations.json...")
    api.upload_file(
        path_or_fileobj=str(vlm),
        path_in_repo="vlm_annotations.json",
        repo_id=REPO_ID,
        repo_type="dataset",
    )
    print("  ✓ vlm_annotations.json")

print(f"\n✓ 全部完成! 耗时 {(time.time()-t_start)/60:.1f} min")
print(f"  https://huggingface.co/datasets/{REPO_ID}")
