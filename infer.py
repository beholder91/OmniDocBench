import os
import subprocess
from pathlib import Path
from tqdm import tqdm

os.environ["MINERU_MODEL_SOURCE"] = "modelscope"

# === 配置部分 ===
input_dir = "images"  # 输入图片目录
output_root = "infer_output/mineru_pipeline"  # 输出目录
backend = "pipeline"
device = "cuda:0"

# === 运行逻辑 ===
def run_mineru(image_path: Path):
    output_dir = Path(output_root) / image_path.stem
    
    if output_dir.exists():
        return True
    
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "mineru",
        "-p", str(image_path),
        "-o", str(output_dir),
        "-b", backend,
        "-d", device,
    ]
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] 处理失败: {image_path.name} ({e})")
        return False

def main():
    input_dir_path = Path(input_dir)
    if not input_dir_path.exists():
        print(f"[ERROR] 输入目录不存在: {input_dir}")
        return

    image_files = sorted([p for p in input_dir_path.iterdir() if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tif"]])
    if not image_files:
        print(f"[WARN] 未找到图片文件。")
        return

    print(f"[INFO] 共找到 {len(image_files)} 张图片。")
    
    skipped = 0
    processed = 0
    failed = 0
    
    for img in tqdm(image_files, desc="处理进度"):
        output_dir = Path(output_root) / img.stem
        if output_dir.exists():
            skipped += 1
            continue
        
        success = run_mineru(img)
        if success:
            processed += 1
        else:
            failed += 1
    
    print(f"\n✅ 处理完成 | 已处理: {processed}, 跳过: {skipped}, 失败: {failed}")

if __name__ == "__main__":
    main()
    # run_mineru(Path("images/book_en_[#U642c#U4e66#U5320#20][HTML5 Canvas].2011.#U82f1#U6587#U7248_page_208.png"))