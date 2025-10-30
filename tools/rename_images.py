import os
import json
from natsort import natsorted
from pathlib import Path

def rename_images(images_folder, json_file, rename_files=True):
    images_folder = Path(images_folder)
    json_file = Path(json_file)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    old_filenames = []
    for item in data:
        if 'page_info' in item and 'image_path' in item['page_info']:
            old_filenames.append(item['page_info']['image_path'])
    
    sorted_filenames = natsorted(set(old_filenames))
    
    old_to_new = {}
    for idx, old_name in enumerate(sorted_filenames, start=1):
        ext = Path(old_name).suffix
        new_name = f"{idx}{ext}"
        old_to_new[old_name] = new_name
    
    if rename_files:
        print("开始重命名文件...")
        temp_mapping = {}
        for old_name in sorted_filenames:
            old_path = images_folder / old_name
            if old_path.exists():
                temp_name = f"temp_{old_name}"
                temp_path = images_folder / temp_name
                old_path.rename(temp_path)
                temp_mapping[temp_name] = old_to_new[old_name]
        
        for temp_name, new_name in temp_mapping.items():
            temp_path = images_folder / temp_name
            new_path = images_folder / new_name
            temp_path.rename(new_path)
        
        print(f"文件重命名完成: {len(temp_mapping)} 个文件")
    
    for item in data:
        if 'page_info' in item and 'image_path' in item['page_info']:
            old_filename = item['page_info']['image_path']
            if old_filename in old_to_new:
                item['page_info']['image_path'] = old_to_new[old_filename]
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"JSON更新完成: {len(old_to_new)} 个文件路径已更新")
    
    return old_to_new

if __name__ == "__main__":
    images_folder = "/mnt/disk1/chenkehao/parsing_bench_data/images"
    json_file = "/mnt/disk1/chenkehao/parsing_bench_data/OmniDocBench.json"
    
    mapping = rename_images(images_folder, json_file)
    print(f"\n前5个映射示例:")
    for i, (old, new) in enumerate(list(mapping.items())[:5]):
        print(f"  {old} -> {new}")

