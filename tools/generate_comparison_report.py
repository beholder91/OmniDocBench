#!/usr/bin/env python3
import os
import json
import glob
from typing import Dict, List, Any


def load_model_results(result_dir: str) -> Dict[str, Dict]:
    """加载所有模型的结果文件"""
    model_results = {}
    pattern = os.path.join(result_dir, '*_quick_match_metric_result.json')
    
    for file_path in glob.glob(pattern):
        model_name = os.path.basename(file_path).replace('_quick_match_metric_result.json', '')
        with open(file_path, 'r', encoding='utf-8') as f:
            model_results[model_name] = json.load(f)
    
    return model_results


def format_value(value: Any, is_percentage: bool = True) -> str:
    """格式化数值"""
    if value is None or (isinstance(value, float) and (value != value)):  # NaN check
        return 'N/A'
    if isinstance(value, (int, float)):
        if is_percentage:
            return f"{value:.3f}"
        else:
            return f"{value:.3f}"
    return str(value)


def generate_overall_performance_table(model_results: Dict[str, Dict]) -> str:
    """生成整体性能对比表格"""
    md = "## 1. 整体性能对比\n\n"
    md += "各模型在核心任务上的整体表现。\n\n"
    
    headers = ["模型", "文本块 (1-Edit_dist)", "公式 (CDM)", "表格 (TEDS)", "表格结构 (TEDS_S)", "阅读顺序 (1-Edit_dist)", "综合得分"]
    md += "| " + " | ".join(headers) + " |\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for model_name, data in sorted(model_results.items()):
        text_block = data.get('text_block', {}).get('all', {}).get('Edit_dist', {}).get('ALL_page_avg', None)
        text_block_score = (1 - text_block) * 100 if text_block is not None else None
        
        display_formula = data.get('display_formula', {}).get('page', {}).get('CDM', {}).get('ALL', 0) * 100
        
        table_teds = data.get('table', {}).get('all', {}).get('TEDS', {}).get('all', None)
        table_teds_score = table_teds * 100 if table_teds is not None else None
        
        table_teds_s = data.get('table', {}).get('all', {}).get('TEDS_structure_only', {}).get('all', None)
        table_teds_s_score = table_teds_s * 100 if table_teds_s is not None else None
        
        reading_order = data.get('reading_order', {}).get('all', {}).get('Edit_dist', {}).get('ALL_page_avg', None)
        reading_order_score = (1 - reading_order) * 100 if reading_order is not None else None
        
        overall = None
        if text_block_score is not None and display_formula is not None and table_teds_score is not None:
            overall = (text_block_score + display_formula + table_teds_score) / 3
        
        md += f"| {model_name} | {format_value(text_block_score)} | {format_value(display_formula)} | "
        md += f"{format_value(table_teds_score)} | {format_value(table_teds_s_score)} | "
        md += f"{format_value(reading_order_score)} | {format_value(overall)} |\n"
    
    md += "\n"
    return md


def generate_datasource_table(model_results: Dict[str, Dict]) -> str:
    """生成数据源维度对比表格"""
    md = "## 2. 数据源维度对比\n\n"
    md += "不同数据源类型下的文本块识别性能 (1-Edit_dist，越高越好)。\n\n"
    
    datasources = [
        "data_source: book",
        "data_source: PPT2PDF", 
        "data_source: research_report",
        "data_source: colorful_textbook",
        "data_source: exam_paper",
        "data_source: magazine",
        "data_source: academic_literature",
        "data_source: note",
        "data_source: newspaper"
    ]
    
    headers = ["模型"] + [ds.replace("data_source: ", "") for ds in datasources]
    md += "| " + " | ".join(headers) + " |\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for model_name, data in sorted(model_results.items()):
        row = [model_name]
        page_data = data.get('text_block', {}).get('page', {}).get('Edit_dist', {})
        
        for ds in datasources:
            value = page_data.get(ds, None)
            score = (1 - value) * 100 if value is not None else None
            row.append(format_value(score))
        
        md += "| " + " | ".join(row) + " |\n"
    
    md += "\n"
    return md


def generate_layout_table(model_results: Dict[str, Dict]) -> str:
    """生成页面布局维度对比表格"""
    md = "## 3. 页面布局维度对比\n\n"
    md += "不同布局类型下的性能表现。\n\n"
    
    md += "### 3.1 文本块识别 (1-Edit_dist)\n\n"
    
    layouts = [
        "layout: single_column",
        "layout: double_column",
        "layout: three_column",
        "layout: 1andmore_column",
        "layout: other_layout"
    ]
    
    headers = ["模型"] + [l.replace("layout: ", "") for l in layouts]
    md += "| " + " | ".join(headers) + " |\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for model_name, data in sorted(model_results.items()):
        row = [model_name]
        page_data = data.get('text_block', {}).get('page', {}).get('Edit_dist', {})
        
        for layout in layouts:
            value = page_data.get(layout, None)
            score = (1 - value) * 100 if value is not None else None
            row.append(format_value(score))
        
        md += "| " + " | ".join(row) + " |\n"
    
    md += "\n### 3.2 阅读顺序 (1-Edit_dist)\n\n"
    md += "| " + " | ".join(headers) + " |\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for model_name, data in sorted(model_results.items()):
        row = [model_name]
        page_data = data.get('reading_order', {}).get('page', {}).get('Edit_dist', {})
        
        for layout in layouts:
            value = page_data.get(layout, None)
            score = (1 - value) * 100 if value is not None else None
            row.append(format_value(score))
        
        md += "| " + " | ".join(row) + " |\n"
    
    md += "\n"
    return md


def generate_language_table(model_results: Dict[str, Dict]) -> str:
    """生成语言维度对比表格"""
    md = "## 4. 语言维度对比\n\n"
    md += "不同语言类型下的文本块识别性能 (1-Edit_dist)。\n\n"
    
    languages = [
        "language: english",
        "language: simplified_chinese",
        "language: en_ch_mixed"
    ]
    
    headers = ["模型"] + [l.replace("language: ", "") for l in languages]
    md += "| " + " | ".join(headers) + " |\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for model_name, data in sorted(model_results.items()):
        row = [model_name]
        page_data = data.get('text_block', {}).get('page', {}).get('Edit_dist', {})
        
        for lang in languages:
            value = page_data.get(lang, None)
            score = (1 - value) * 100 if value is not None else None
            row.append(format_value(score))
        
        md += "| " + " | ".join(row) + " |\n"
    
    md += "\n"
    return md


def generate_table_attribute_table(model_results: Dict[str, Dict]) -> str:
    """生成表格属性维度对比表格"""
    md = "## 5. 表格属性维度对比\n\n"
    md += "不同表格属性下的识别性能 (TEDS)。\n\n"
    
    md += "### 5.1 线条类型\n\n"
    line_types = [
        "line: full_line",
        "line: less_line",
        "line: fewer_line",
        "line: wireless_line"
    ]
    
    headers = ["模型"] + [l.replace("line: ", "") for l in line_types]
    md += "| " + " | ".join(headers) + " |\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for model_name, data in sorted(model_results.items()):
        row = [model_name]
        group_data = data.get('table', {}).get('group', {}).get('TEDS', {})
        
        for line_type in line_types:
            value = group_data.get(line_type, None)
            score = value * 100 if value is not None else None
            row.append(format_value(score))
        
        md += "| " + " | ".join(row) + " |\n"
    
    md += "\n### 5.2 其他属性\n\n"
    
    other_attrs = [
        "with_span: True",
        "with_span: False",
        "include_equation: True",
        "include_equation: False",
        "include_background: True",
        "include_background: False",
        "table_layout: horizontal",
        "table_layout: vertical"
    ]
    
    headers = ["模型"] + [attr.replace(": ", "_") for attr in other_attrs]
    md += "| " + " | ".join(headers) + " |\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for model_name, data in sorted(model_results.items()):
        row = [model_name]
        group_data = data.get('table', {}).get('group', {}).get('TEDS', {})
        
        for attr in other_attrs:
            value = group_data.get(attr, None)
            score = value * 100 if value is not None else None
            row.append(format_value(score))
        
        md += "| " + " | ".join(row) + " |\n"
    
    md += "\n"
    return md


def generate_text_attribute_table(model_results: Dict[str, Dict]) -> str:
    """生成文本属性维度对比表格"""
    md = "## 6. 文本属性维度对比\n\n"
    md += "不同文本属性下的识别性能 (1-Edit_dist)。\n\n"
    
    md += "### 6.1 文本背景\n\n"
    
    backgrounds = [
        "text_background: white",
        "text_background: single_colored",
        "text_background: multi_colored"
    ]
    
    headers = ["模型"] + [b.replace("text_background: ", "") for b in backgrounds]
    md += "| " + " | ".join(headers) + " |\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for model_name, data in sorted(model_results.items()):
        row = [model_name]
        group_data = data.get('text_block', {}).get('group', {}).get('Edit_dist', {})
        
        for bg in backgrounds:
            value = group_data.get(bg, None)
            score = (1 - value) * 100 if value is not None else None
            row.append(format_value(score))
        
        md += "| " + " | ".join(row) + " |\n"
    
    md += "\n### 6.2 文本旋转\n\n"
    
    rotations = [
        "text_rotate: normal",
        "text_rotate: horizontal",
        "text_rotate: rotate270"
    ]
    
    headers = ["模型"] + [r.replace("text_rotate: ", "") for r in rotations]
    md += "| " + " | ".join(headers) + " |\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for model_name, data in sorted(model_results.items()):
        row = [model_name]
        group_data = data.get('text_block', {}).get('group', {}).get('Edit_dist', {})
        
        for rot in rotations:
            value = group_data.get(rot, None)
            score = (1 - value) * 100 if value is not None else None
            row.append(format_value(score))
        
        md += "| " + " | ".join(row) + " |\n"
    
    md += "\n"
    return md


def generate_special_issues_table(model_results: Dict[str, Dict]) -> str:
    """生成页面特殊问题对比表格"""
    md = "## 7. 页面特殊问题对比\n\n"
    md += "特殊场景下的文本块识别性能 (1-Edit_dist)。\n\n"
    
    issues = ["fuzzy_scan", "watermark", "colorful_backgroud"]
    
    headers = ["模型"] + issues
    md += "| " + " | ".join(headers) + " |\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    for model_name, data in sorted(model_results.items()):
        row = [model_name]
        page_data = data.get('text_block', {}).get('page', {}).get('Edit_dist', {})
        
        for issue in issues:
            value = page_data.get(issue, None)
            score = (1 - value) * 100 if value is not None else None
            row.append(format_value(score))
        
        md += "| " + " | ".join(row) + " |\n"
    
    md += "\n"
    return md


def generate_markdown_report(result_dir: str, output_file: str):
    """生成完整的 Markdown 报表"""
    model_results = load_model_results(result_dir)
    
    if not model_results:
        print(f"错误：在 {result_dir} 目录下未找到任何模型结果文件")
        return
    
    print(f"找到 {len(model_results)} 个模型：{', '.join(model_results.keys())}")
    
    md_content = "# 模型性能对比报表\n\n"
    md_content += f"本报表对比了 {len(model_results)} 个模型在多个维度上的性能表现。\n\n"
    
    md_content += generate_overall_performance_table(model_results)
    md_content += generate_datasource_table(model_results)
    md_content += generate_layout_table(model_results)
    md_content += generate_language_table(model_results)
    md_content += generate_table_attribute_table(model_results)
    md_content += generate_text_attribute_table(model_results)
    md_content += generate_special_issues_table(model_results)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"报表已生成：{output_file}")


if __name__ == "__main__":
    import sys
    
    result_dir = sys.argv[1] if len(sys.argv) > 1 else "../result"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "model_comparison_report.md"
    
    if not os.path.isabs(result_dir):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        result_dir = os.path.normpath(os.path.join(script_dir, result_dir))
    
    if not os.path.isabs(output_file):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, output_file)
    
    generate_markdown_report(result_dir, output_file)

