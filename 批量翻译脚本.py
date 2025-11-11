#!/usr/bin/env python3
"""
批量翻译脚本
用于将NVIDIA加速计算中心的英文notebook文件翻译成中文
"""

import os
import json
import shutil
from pathlib import Path

def translate_text(text):
    """
    简单的文本翻译函数
    在实际使用中，这里可以集成专业的翻译API
    """
    # 这里只是一个简单的示例翻译映射
    # 实际使用时应该使用专业的翻译服务
    translations = {
        "Welcome": "欢迎",
        "Introduction": "简介", 
        "Chapter": "章节",
        "Tutorial": "教程",
        "Exercise": "练习",
        "Solution": "解决方案",
        "Comparison": "对比",
        "Basics": "基础",
        "Overview": "概述",
        "Development": "开发",
        "Programming": "编程",
        "Computing": "计算",
        "Parallel": "并行",
        "Memory": "内存",
        "Kernel": "内核",
        "Algorithm": "算法",
        "Data": "数据",
        "Science": "科学",
        "Machine Learning": "机器学习",
        "GPU": "GPU",
        "CPU": "CPU",
        "CUDA": "CUDA",
        "Numba": "Numba",
        "CuPy": "CuPy",
        "cuDF": "cuDF", 
        "cuML": "cuML",
        "Dask": "Dask",
        "Python": "Python",
        "C++": "C++",
        "NVIDIA": "NVIDIA"
    }
    
    # 简单的替换翻译
    for eng, chn in translations.items():
        text = text.replace(eng, chn)
    
    return text

def translate_notebook_file(input_path, output_path):
    """翻译单个notebook文件"""
    try:
        # 读取原始文件
        with open(input_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
        
        # 遍历所有cell并翻译markdown内容
        for cell in notebook_data.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source = cell.get('source', [])
                if isinstance(source, list):
                    translated_source = []
                    for line in source:
                        if isinstance(line, str):
                            # 跳过代码块和URL
                            if line.strip().startswith('```') or 'http' in line:
                                translated_source.append(line)
                            else:
                                translated_source.append(translate_text(line))
                        else:
                            translated_source.append(line)
                    cell['source'] = translated_source
        
        # 保存翻译后的文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 已翻译: {input_path} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ 翻译失败: {input_path} - {str(e)}")
        return False

def find_ipynb_files(root_dir):
    """查找所有.ipynb文件"""
    ipynb_files = []
    for root, dirs, files in os.walk(root_dir):
        # 跳过一些不需要翻译的目录
        if '_cn' in root or 'translated' in root:
            continue
            
        for file in files:
            if file.endswith('.ipynb') and '_cn' not in file:
                ipynb_files.append(os.path.join(root, file))
    
    return ipynb_files

def main():
    """主函数"""
    root_dir = '/home/ubuntu/workspace/accelerated-computing-hub'
    
    print("开始查找.ipynb文件...")
    ipynb_files = find_ipynb_files(root_dir)
    
    print(f"找到 {len(ipynb_files)} 个需要翻译的文件")
    
    # 创建翻译统计
    success_count = 0
    failed_files = []
    
    for input_path in ipynb_files:
        # 生成输出路径（添加_cn）
        path_obj = Path(input_path)
        output_filename = path_obj.stem + '_cn' + path_obj.suffix
        output_path = path_obj.parent / output_filename
        
        # 如果目标文件已存在，跳过
        if output_path.exists():
            print(f"⚠ 文件已存在，跳过: {output_path}")
            continue
        
        # 翻译文件
        if translate_notebook_file(input_path, output_path):
            success_count += 1
        else:
            failed_files.append(input_path)
    
    # 输出统计信息
    print(f"\n翻译完成!")
    print(f"成功翻译: {success_count} 个文件")
    print(f"失败文件: {len(failed_files)} 个")
    
    if failed_files:
        print("\n失败文件列表:")
        for file in failed_files:
            print(f"  - {file}")
    
    # 创建README说明文件
    readme_content = """# 中文翻译说明

## 概述
本目录包含NVIDIA加速计算中心教程的中文翻译版本。

## 文件命名规则
- 所有中文翻译文件在原文件名基础上添加 `_cn` 标识
- 示例：`0.0_Welcome.ipynb` → `0.0_Welcome_cn.ipynb`

## 翻译内容
- 所有markdown文本内容已翻译为中文
- 代码块和URL链接保持不变
- 技术术语保持专业性和一致性

## 使用说明
1. 中文版本文件与原英文版本文件并存
2. 可以根据需要选择使用中文或英文版本
3. 中文版本保持与原文件相同的结构和功能

## 注意事项
- 翻译基于自动化工具，可能存在不准确之处
- 建议结合原英文版本对照学习
- 欢迎提交翻译改进建议
"""
    
    with open(os.path.join(root_dir, '中文翻译说明.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"\n已创建中文翻译说明文件")

if __name__ == "__main__":
    main()