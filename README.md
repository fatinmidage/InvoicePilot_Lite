# InvoicePilot Lite

本项目旨在实现一个可以自动读取 PDF 发票，并根据发票金额对文件进行重命名的工具。

## 功能特性

- ✅ 自动读取 PDF 格式的发票文件
- ✅ 识别并提取发票中的金额信息
- ✅ 根据发票金额自动重命名原始 PDF 文件，命名格式为"xx元_发票"
- ✅ 自动处理当前目录下的所有PDF文件
- ✅ 支持多种金额格式识别（金额、小写、合计、总计等）
- ✅ 自动处理文件名冲突
- ✅ 适配嵌入式Python环境，支持打包成可执行文件

## 安装依赖

```bash
# 使用 uv 安装依赖（推荐）
uv sync

# 或使用 pip 安装
pip install pdfplumber
```

## 使用方法

### 简单使用（推荐）

1. 将程序放在包含PDF发票的目录中
2. 双击运行程序或在命令行执行：
   ```bash
   python main.py
   ```
3. 程序会自动扫描当前目录下的所有PDF文件并处理

### Windows用户

Windows用户可以直接双击 `run.bat` 文件来运行程序。

### 命令行参数

- 无参数：自动处理当前目录下的所有PDF文件
- `-h`, `--help`, `/?`, `-?`：显示帮助信息

### 发票重命名格式示例

- `100.00元_发票.pdf`
- `1,234.56元_发票.pdf`
- `100.00元_发票_1.pdf` (当文件名冲突时自动添加序号)

## 支持的金额格式

程序可以识别以下格式的金额信息：

- `金额：¥100.00`
- `小写：¥100.00`
- `合计：¥100.00`
- `总计：¥100.00`
- `￥100.00`
- `¥100.00`
- `100.00元`

## 环境要求

- Python 3.8 及以上
- pdfplumber 0.10.0 及以上

## 项目结构

```
InvoicePilot_Lite/
├── main.py              # 主程序文件
├── build_config.py      # PyInstaller打包配置
├── run.bat              # Windows批处理脚本
├── pyproject.toml       # 项目配置文件
├── README.md            # 项目说明文档
└── uv.lock              # 依赖锁定文件
```

## 开发说明

程序使用 `pdfplumber` 库来提取PDF文本内容，然后通过正则表达式匹配金额信息。主要类和方法：

- `InvoiceProcessor`: 发票处理器主类
- `get_current_directory()`: 获取当前工作目录（适配嵌入式环境）
- `extract_text_from_pdf()`: 从PDF提取文本
- `extract_amount()`: 从文本中提取金额
- `process_invoice()`: 处理单个发票文件
- `process_current_directory()`: 自动处理当前目录中的所有文件

## 打包说明

程序已优化以适配嵌入式Python环境，可以使用以下工具打包：

### 使用 PyInstaller 打包

```bash
# 安装 PyInstaller
pip install pyinstaller

# 方法1：使用配置文件打包
python build_config.py

# 方法2：直接使用 PyInstaller 命令
pyinstaller --onefile --name InvoicePilot main.py
```

### 使用 cx_Freeze 打包

```bash
# 安装 cx_Freeze
pip install cx_Freeze

# 创建 setup.py
python setup.py build
```

## 注意事项

1. 确保PDF文件包含可提取的文本内容（非扫描图片）
2. 程序会直接重命名原文件，建议先备份重要文件
3. 如果目标文件名已存在，会自动添加序号避免覆盖
4. 支持处理包含逗号的金额格式（如 1,234.56）
5. 程序会自动检测运行环境，在嵌入式环境中使用可执行文件所在目录
6. 打包后的程序会自动处理当前目录下的所有PDF文件
7. Windows用户可以使用 `run.bat` 脚本简化操作
