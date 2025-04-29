<h1 align="center"> AI-Novel_Editor-DeepSeek-R1 </h1>
<h4 align="center">The AI Novel Editing System is an intelligent fiction processing tool built upon the DeepSeek API. </h4>
This system is designed to help users automatically analyze and comprehend novel texts, while generating structured output files.  

Acknowledgments: We extend our gratitude to DeepSeek and the ShenDu QiuSuo (深度求索) team for creating such exceptional
AI technologies.
<p  align="center">
<a href="https://www.gnu.org/licenses/quick-guide-gplv3.zh-cn.html"><img src="https://img.shields.io/pypi/l/azurlanetoollib?color=green"></a>
</p>
<hr />

# AI 小说编辑系统 (DeepSeek 版本)

AI 小说编辑系统是一个基于 DeepSeek API 的智能小说处理工具。该系统旨在帮助用户自动处理和理解小说文段，并生成结构化的输出文件。

## 功能特点

- **日志记录**：系统会详细记录操作日志，便于追踪和调试。
- **模块化设计**：核心逻辑和 API 调用分离，易于维护和扩展。
- **用户友好的交互菜单**：提供简单直观的命令行界面，方便用户操作。
- **自动化处理**：能够自动读取用户输入内容，调用 DeepSeek API 进行处理，并将结果保存到文件中。

## 目录结构

```

AI-Novel_Editor-DeepSeek-R1
├── .venv                     # Python虚拟环境
├── config                    # 配置文件目录
│   └── api_key.txt           # 存储DeepSeek API密钥
├── css                       # 样式文件目录
│   └── MarkdownA.css         # Markdown样式文件
├── data                      # 输入数据目录
├── logs                      # 系统日志目录
├── mode                      # 模块目录
│   └── mode_DPSK_Apic.py     # DeepSeek API处理模块
├── results                   # 处理结果目录
├── text                      # 系统提示目录
│   └── text_SYST_Inst.md     # 提示文件
└── main.py                   # 主程序入口
```

## 安装和配置

### 前提条件

- Python 3.11.9
- virtualenv

### 安装步骤

1. 克隆项目仓库：
   ```bash
   git clone https://github.com/yourusername/AI-Novel_Editor-DeepSeek-R1.git
   cd AI-Novel_Editor-DeepSeek-R1
   ```

2. 创建并激活虚拟环境：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

4. 配置API密钥：
   - 创建 `config/api_key.txt` 文件并将你的 DeepSeek API 密钥写入其中。
   - 或者，设置环境变量 `DEEPSEEK_API_KEY`。

### 使用方法

运行主程序：

```
bash
python main.py
```

程序启动后，会显示一个交互菜单，用户可以选择不同的操作选项：

```

 DeepSeek小说编辑系统 
[1] 💬 文段理解处理。
[0] ❗ 退出系统。
```

选择相应的编号即可执行对应的操作。

## 示例

### 输入文件格式

输入文件应位于 `data/data_MAIN_Info.md`，并且应以 Markdown 标题开头，例如：

```markdown
# 示例小说文段

这是示例小说文段的内容。
```

### 输出文件格式

处理后的结果将保存在 `results` 目录下，文件名格式为 `Result_YYYY-MM-DD_HH-MM-SS.md`。

## 日志

所有操作的日志会记录在 `logs` 目录下，文件名格式为 `logs_MMDD_HHMM.log`。

## 错误处理

系统对各种异常进行了全面的捕获和处理，确保用户能够获得详细的错误信息。常见错误包括但不限于：

- 文件未找到
- 配置文件缺少必要键
- API连接失败
- API返回无效数据

## 贡献

欢迎贡献代码和提出问题！请遵循以下步骤：

1. Fork 项目
2. 创建新分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 [GNU General Public License v3.0 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.html)
许可证。详情请参阅 [LICENSE](LICENSE) 文件。

