# 畅声编辑器 (ChangVox Editor) 安装指南

## 系统要求

### 最低要求
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+, Android 8.0+, iOS 13.0+
- **Python**: 3.8 或更高版本
- **内存**: 4GB RAM (推荐8GB)
- **存储空间**: 至少2GB可用空间

### 推荐配置
- **操作系统**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.9 或更高版本
- **内存**: 16GB RAM
- **GPU**: NVIDIA GPU (支持CUDA) 用于加速AI推理
- **存储空间**: 10GB可用空间 (用于模型文件)

## 安装步骤

### 1. 安装Python

确保已安装Python 3.8或更高版本：

```bash
python --version
# 或
python3 --version
```

如果未安装Python，请从[Python官网](https://www.python.org/downloads/)下载并安装。

### 2. 克隆或下载项目

```bash
# 如果使用Git
git clone <项目仓库地址>
cd ChangVox-Editor

# 或者直接下载ZIP文件并解压
```

### 3. 安装依赖

#### 方法一：使用pip安装

```bash
# 安装所有依赖
pip install -r requirements.txt

# 如果遇到权限问题，使用
pip install -r requirements.txt --user
```

#### 方法二：分步安装（推荐）

由于某些包可能有平台特定的要求，建议分步安装：

```bash
# 1. 安装Kivy (GUI框架)
pip install kivy[base] kivy_examples

# 2. 安装PyTorch (AI推理)
# 根据你的系统选择对应的命令：

# Windows (CUDA)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Windows (CPU only)
pip install torch torchaudio

# macOS
pip install torch torchaudio

# Linux (CUDA)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Linux (CPU only)
pip install torch torchaudio

# 3. 安装音频处理库
pip install librosa soundfile pydub numpy

# 4. 安装其他工具
pip install pyyaml pillow requests
```

### 4. 安装Synchrotron音频引擎

Synchrotron可能需要从源码编译或使用预编译版本：

```bash
# 尝试从PyPI安装
pip install synchrotron

# 如果不可用，可能需要从GitHub安装
pip install git+https://github.com/username/synchrotron.git
```

### 5. 下载DiffSinger模型

畅声编辑器需要DiffSinger模型文件才能进行歌声合成：

1. 从官方渠道下载DiffSinger模型文件
2. 将模型文件放置在 `models/diffsinger/` 目录下
3. 支持的格式：`.pt`, `.pth`, `.onnx`

### 6. 验证安装

运行测试脚本验证安装：

```bash
python test_structure.py
```

如果所有测试通过，说明安装成功。

## 平台特定说明

### Windows
- 确保已安装Visual C++ Redistributable
- 推荐使用Anaconda或Miniconda管理Python环境

### macOS
- 可能需要安装Xcode命令行工具：
  ```bash
  xcode-select --install
  ```
- 对于M1/M2芯片，使用PyTorch的MPS后端加速

### Linux (Ubuntu/Debian)
- 安装系统依赖：
  ```bash
  sudo apt update
  sudo apt install python3-dev python3-pip build-essential
  sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
  sudo apt install libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
  sudo apt install zlib1g-dev
  ```

### Android
- 需要使用Buildozer或Kivy Launcher
- 参考Kivy官方文档进行Android打包

### iOS
- 需要在macOS环境下使用Kivy iOS工具链
- 需要Apple开发者账号进行签名

## 故障排除

### 常见问题

1. **Kivy安装失败**
   - 确保已安装系统依赖
   - 尝试使用conda安装：`conda install kivy -c conda-forge`

2. **PyTorch安装失败**
   - 检查Python版本兼容性
   - 访问PyTorch官网获取正确的安装命令

3. **音频库问题**
   - 在Linux上可能需要安装额外的音频开发包
   - Windows用户确保已安装正确的音频编解码器

4. **模型加载失败**
   - 检查模型文件路径是否正确
   - 确保模型文件与当前PyTorch版本兼容

### 获取帮助

如果遇到问题，请：
1. 查看项目文档和README
2. 检查错误日志中的详细信息
3. 在项目Issue页面提交问题
4. 联系开发团队获取支持

## 首次运行

安装完成后，运行主程序：

```bash
python main.py
```

首次运行时会：
- 初始化项目目录结构
- 检查模型文件
- 加载默认配置

## 更新

要更新畅声编辑器：

```bash
# 更新代码
git pull

# 更新依赖
pip install -r requirements.txt --upgrade
```

## 卸载

要完全卸载畅声编辑器：

```bash
# 卸载Python包
pip uninstall -r requirements.txt

# 删除项目目录
rm -rf ChangVox-Editor
```