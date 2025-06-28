# InvoicePilot Lite

一个智能的PDF发票处理工具，可以自动读取PDF发票文件，提取金额信息，并根据金额对文件进行重命名。

## ✨ 功能特性

- ✅ 自动读取 PDF 格式的发票文件
- ✅ 智能判定PDF文件是否为发票（基于"发票号码"关键词识别）
- ✅ 识别并提取发票中的金额信息
- ✅ 根据发票金额自动重命名原始 PDF 文件，命名格式为"xx元_发票"
- ✅ 自动处理当前目录下的所有PDF文件
- ✅ 支持多种金额格式识别（金额、小写、合计、总计等）
- ✅ 自动处理文件名冲突
- ✅ 自动跳过非发票PDF文件，提高处理效率
- ✅ 适配嵌入式Python环境，支持打包成可执行文件

## 🚀 快速开始

### 方法一：使用 uv（推荐）

```bash
# 1. 安装 uv（如果还没有安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 克隆或下载项目
git clone <repository-url>
cd InvoicePilot_Lite

# 3. 安装依赖
uv sync

# 4. 运行程序
uv run python main.py
```

### 方法二：使用 pip

```bash
# 1. 安装依赖
pip install pdfplumber

# 2. 运行程序
python main.py
```

## 📦 安装说明

### 使用 uv（推荐）

uv 是一个快速的 Python 包管理器和安装器，提供更好的依赖管理和虚拟环境支持。

```bash
# 安装项目依赖
uv sync

# 运行程序
uv run python main.py

# 添加新的依赖
uv add package-name

# 在开发环境中运行
uv run --dev python main.py
```

### 使用 pip

```bash
# 安装依赖
pip install pdfplumber

# 运行程序
python main.py
```

## 🎯 使用方法

### 简单使用

1. 将程序放在包含PDF发票的目录中
2. 运行程序：
   ```bash
   # 使用 uv
   uv run python main.py
   
   # 或使用 pip
   python main.py
   ```
3. 程序会自动扫描当前目录下的所有PDF文件，智能识别发票文件并处理

### Windows用户

Windows用户可以直接双击 `run.bat` 文件来运行程序。

### 命令行参数

- 无参数：自动处理当前目录下的所有PDF文件
- `-h`, `--help`, `/?`, `-?`：显示帮助信息

### 发票重命名格式示例

- `100.00元_发票.pdf`
- `1,234.56元_发票.pdf`
- `100.00元_发票_1.pdf` (当文件名冲突时自动添加序号)

## 💰 支持的金额格式

程序可以识别以下格式的金额信息：

- `金额：¥100.00`
- `小写：¥100.00`
- `合计：¥100.00`
- `总计：¥100.00`
- `￥100.00`
- `¥100.00`
- `100.00元`

## 🔧 环境要求

- Python 3.8 及以上
- pdfplumber 0.10.0 及以上

## 📁 项目结构

```
InvoicePilot_Lite/
├── main.py              # 主程序文件
├── build_config.py      # PyInstaller打包配置
├── run.bat              # Windows批处理脚本
├── pyproject.toml       # 项目配置文件（uv支持）
├── uv.lock              # 依赖锁定文件（uv）
└── README.md            # 项目说明文档
```

## 🛠️ 开发说明

### 发票识别机制

程序在处理PDF文件时，会首先检查文档内容是否包含"发票号码"关键词：
- ✅ 包含"发票号码"：识别为发票文件，继续进行金额提取和重命名
- ❌ 不包含"发票号码"：跳过该文件，不进行处理

### 主要类和方法

- `InvoiceProcessor`: 发票处理器主类
- `get_current_directory()`: 获取当前工作目录（适配嵌入式环境）
- `extract_text_from_pdf()`: 从PDF提取文本
- `is_invoice_pdf()`: 判断PDF文件是否为发票（检查是否包含"发票号码"关键词）
- `extract_amount()`: 从文本中提取金额
- `process_invoice()`: 处理单个发票文件
- `process_current_directory()`: 自动处理当前目录中的所有文件

## 📦 打包说明

### 使用 uv + PyInstaller 打包（推荐）

```bash
# 1. 确保在项目目录中
cd InvoicePilot_Lite

# 2. 使用 uv 运行 PyInstaller（确保在项目虚拟环境中运行）
uv run --with pyinstaller pyinstaller main.spec

# 3. 等待完成，打包好的文件在 dist/InvoicePilot
```

**为什么推荐使用 uv？**
- uv 确保 PyInstaller 在项目虚拟环境中运行
- 自动解决模块找不到的问题（如 "No module named 'pdfplumber'"）
- 更好的依赖管理和环境隔离

### 使用传统方式打包

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

## ⚠️ 注意事项

1. **文件格式**：确保PDF文件包含可提取的文本内容（非扫描图片）
2. **发票识别**：程序只会处理包含"发票号码"关键词的PDF文件，其他PDF文件会被自动跳过
3. **文件备份**：程序会直接重命名原文件，建议先备份重要文件
4. **文件名冲突**：如果目标文件名已存在，会自动添加序号避免覆盖
5. **金额格式**：支持处理包含逗号的金额格式（如 1,234.56）
6. **环境适配**：程序会自动检测运行环境，在嵌入式环境中使用可执行文件所在目录
7. **批量处理**：打包后的程序会自动处理当前目录下的所有PDF文件
8. **Windows支持**：Windows用户可以使用 `run.bat` 脚本简化操作
9. **错误处理**：如果PDF文件不包含"发票号码"字段，程序会显示相应提示并跳过处理

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

本项目采用 MIT 许可证。
