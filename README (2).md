# 畅声编辑器 (ChangVox Editor)

一个完全使用Python编写的跨平台歌声合成软件，支持DiffSinger AI声库。

## 特性

- 🎵 跨平台支持 (Windows, macOS, Linux, Android, iOS)
- 🤖 集成DiffSinger AI歌声合成引擎
- 🎼 支持音符编辑和参数调整
- 🔊 基于Synchrotron的高质量音频处理
- 📱 响应式Kivy GUI界面
- 🎚️ 实时音频预览和编辑

## 技术栈

- **GUI框架**: Kivy
- **AI推理**: PyTorch
- **音频引擎**: Synchrotron
- **架构**: 分层架构设计

## 项目结构

```
ChangVox Editor/
├── src/                    # 源代码目录
│   ├── presentation/       # 表现层 (GUI)
│   ├── business/           # 业务逻辑层
│   ├── services/           # 服务层
│   └── shared/             # 共享模块
├── assets/                 # 资源文件
├── models/                 # AI模型文件
├── docs/                   # 文档
└── tests/                  # 测试文件
```

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

## 开发计划

- [x] 项目架构设计
- [ ] GUI界面开发
- [ ] DiffSinger集成
- [ ] 音频引擎集成
- [ ] 跨平台测试

## 许可证

MIT License