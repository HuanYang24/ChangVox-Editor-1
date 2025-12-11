# 畅声编辑器

畅声编辑器是一个功能强大的人声合成编辑工具，提供直观的界面用于创建和编辑音轨、音符和参数设置。

## 项目功能

- **多轨音频编辑**：支持创建和管理多个音轨
- **钢琴卷帘界面**：直观地编辑音符和旋律
- **参数控制面板**：调整各种音频参数
- **时间轴控制**：精确控制音频时间
- **歌手选择功能**：切换不同的合成声音

## 环境配置

项目使用Python 3.13开发，主要依赖包已在requirements.txt中列出：

- PyQt6
- numpy
- librosa
- pyaudio
- scipy
- matplotlib

## 如何运行程序

### 方法一：使用批处理文件（推荐）

1. 直接双击项目根目录下的 `run.bat` 文件
2. 程序将自动使用虚拟环境中的Python解释器运行

### 方法二：手动命令行运行

1. 打开命令提示符（cmd）
2. 导航到项目目录：`cd G:\编程工程\畅声编辑器`
3. 使用虚拟环境运行：`.venv\Scripts\python.exe main.py`

### 注意事项

- 程序运行时可能会显示一些关于字体缺失的警告信息（如WenQuanYi Micro Hei、Heiti TC等），这些警告不会影响程序功能
- 如果直接点击Python文件运行，可能会使用系统Python解释器而非虚拟环境，导致缺少依赖的错误

## 虚拟环境管理

如果需要重新安装依赖或更新包：

1. 使用虚拟环境中的pip：`.venv\Scripts\pip.exe install -r requirements.txt`
2. 安装新包：`.venv\Scripts\pip.exe install 包名`

## 常见问题解决

- **错误：ModuleNotFoundError: No module named 'PyQt6'**
  - 这是因为使用了未安装依赖的Python解释器
  - 解决方案：使用虚拟环境中的Python解释器（.venv\Scripts\python.exe）

- **字体警告**
  - 程序可能会显示字体缺失的警告，但这些警告不影响功能
  - 如果需要解决这些警告，可以安装缺失的字体

## 项目结构

```
├── .venv\        # Python虚拟环境
├── main.py       # 主程序文件
├── requirements.txt # 项目依赖
├── run.bat       # 运行脚本
└── README.md     # 项目说明文档
```