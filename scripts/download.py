"""
VFG-7 数据集下载脚本
自动从 HuggingFace 下载数据集到本地

用法: python scripts/download.py [--output ./VFG-7]
"""
import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Download VFG-7 dataset from HuggingFace")
    parser.add_argument("--output", default=".", help="Output directory (default: current dir)")
    parser.add_argument("--repo", default="Telody1220/VFG-7", help="HuggingFace repo ID")
    args = parser.parse_args()

    print("=" * 50)
    print("  VFG-7 Dataset Downloader")
    print("=" * 50)

    # Check huggingface_hub
    try:
        import huggingface_hub  # noqa: F401
    except ImportError:
        print("Installing huggingface_hub...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub"])

    from huggingface_hub import snapshot_download

    print(f"\nDownloading {args.repo} to {args.output} ...")
    path = snapshot_download(
        repo_id=args.repo,
        repo_type="dataset",
        local_dir=args.output,
    )
    print(f"\n✓ Dataset downloaded to: {path}")
    print("  To train: python -c \"from ultralytics import YOLO; YOLO('yolo11l.pt').train(data='data.yaml')\"")


if __name__ == "__main__":
    main()
