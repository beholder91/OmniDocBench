# 模型性能对比报表

本报表对比了 2 个模型在多个维度上的性能表现。

## 1. 整体性能对比

各模型在核心任务上的整体表现。

| 模型 | 文本块 (1-Edit_dist) | 公式 (CDM) | 表格 (TEDS) | 表格结构 (TEDS_S) | 阅读顺序 (1-Edit_dist) | 综合得分 |
|---|---|---|---|---|---|---|
| mineru_pipeline | 92.406 | 0.000 | 74.054 | 80.088 | 90.603 | 55.487 |
| mineru_vlm | 94.642 | 0.000 | 86.963 | 91.289 | 94.843 | 60.535 |

## 2. 数据源维度对比

不同数据源类型下的文本块识别性能 (1-Edit_dist，越高越好)。

| 模型 | book | PPT2PDF | research_report | colorful_textbook | exam_paper | magazine | academic_literature | note | newspaper |
|---|---|---|---|---|---|---|---|---|---|
| mineru_pipeline | 96.098 | 94.029 | 97.285 | 89.331 | 91.959 | 93.605 | 97.701 | 76.215 | 93.992 |
| mineru_vlm | 96.330 | 96.505 | 98.787 | 92.523 | 94.235 | 95.632 | 97.502 | 86.118 | 93.765 |

## 3. 页面布局维度对比

不同布局类型下的性能表现。

### 3.1 文本块识别 (1-Edit_dist)

| 模型 | single_column | double_column | three_column | 1andmore_column | other_layout |
|---|---|---|---|---|---|
| mineru_pipeline | 91.204 | 95.665 | 92.655 | 96.571 | 90.894 |
| mineru_vlm | 95.103 | 95.994 | 93.362 | 96.545 | 92.228 |

### 3.2 阅读顺序 (1-Edit_dist)

| 模型 | single_column | double_column | three_column | 1andmore_column | other_layout |
|---|---|---|---|---|---|
| mineru_pipeline | 94.619 | 93.982 | 87.046 | 94.023 | 79.572 |
| mineru_vlm | 96.907 | 96.440 | 90.553 | 97.134 | 89.387 |

## 4. 语言维度对比

不同语言类型下的文本块识别性能 (1-Edit_dist)。

| 模型 | english | simplified_chinese | en_ch_mixed |
|---|---|---|---|
| mineru_pipeline | 95.072 | 91.588 | 80.213 |
| mineru_vlm | 96.076 | 94.093 | 88.790 |

## 5. 表格属性维度对比

不同表格属性下的识别性能 (TEDS)。

### 5.1 线条类型

| 模型 | full_line | less_line | fewer_line | wireless_line |
|---|---|---|---|---|
| mineru_pipeline | 76.550 | 79.103 | 80.243 | 31.537 |
| mineru_vlm | 88.342 | 90.067 | 88.686 | 69.255 |

### 5.2 其他属性

| 模型 | with_span_True | with_span_False | include_equation_True | include_equation_False | include_background_True | include_background_False | table_layout_horizontal | table_layout_vertical |
|---|---|---|---|---|---|---|---|---|
| mineru_pipeline | 76.414 | 72.991 | 72.437 | 74.389 | 70.195 | 75.761 | 74.166 | 65.968 |
| mineru_vlm | 87.010 | 86.942 | 83.990 | 87.580 | 86.062 | 87.362 | 87.072 | 79.105 |

## 6. 文本属性维度对比

不同文本属性下的识别性能 (1-Edit_dist)。

### 6.1 文本背景

| 模型 | white | single_colored | multi_colored |
|---|---|---|---|
| mineru_pipeline | 94.018 | 89.471 | 84.562 |
| mineru_vlm | 95.292 | 93.060 | 91.835 |

### 6.2 文本旋转

| 模型 | normal | horizontal | rotate270 |
|---|---|---|---|
| mineru_pipeline | 93.476 | 31.451 | 3.226 |
| mineru_vlm | 95.038 | 69.983 | 58.788 |

## 7. 页面特殊问题对比

特殊场景下的文本块识别性能 (1-Edit_dist)。

| 模型 | fuzzy_scan | watermark | colorful_backgroud |
|---|---|---|---|
| mineru_pipeline | 90.597 | 89.778 | 92.426 |
| mineru_vlm | 95.138 | 93.075 | 95.274 |

