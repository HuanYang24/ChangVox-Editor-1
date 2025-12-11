# 畅声编辑器 - 后端开发指南

## 项目结构

- `voice_synthesizer.h`: 声音合成器核心头文件，定义了主要的类和数据结构
- `voice_synthesizer.cpp`: 声音合成器的具体实现
- `main.cpp`: 程序入口点（待实现）
- `web_interface.cpp`: Web前端接口（待实现，用于WebAssembly集成）
- `CMakeLists.txt`: CMake构建配置文件（待实现）

## 核心类

### VoiceBank

负责加载和管理UTAU声库，包括解析声库配置文件和音频样本。

主要功能：
- 加载UTAU格式的声库文件
- 根据音高和音素查找合适的样本
- 管理声库元数据

### VoiceSynthesizer

负责使用声库样本进行歌声合成。

主要功能：
- 合成单个音符
- 合成多个音符并混合
- 音高转换和时长调整
- 应用各种声音效果（音量、张力、气息等）
- 导出为WAV文件

## 与前端集成

目前计划了两种集成方式：

### 1. WebAssembly方式

将C++代码编译为WebAssembly，可以直接在浏览器中运行。

优点：
- 用户体验好，无需安装额外软件
- 部署简单

缺点：
- WebAssembly性能可能不如原生应用
- 文件体积较大

### 2. 本地服务器方式

使用C++创建本地服务器，前端通过HTTP/WebSocket与后端通信。

优点：
- 性能更好
- 可以充分利用C++的优势

缺点：
- 用户需要安装额外的软件
- 部署稍复杂

## 编译指南

### 使用CMake构建

```bash
# 在backend目录下
mkdir build
cd build
cmake ..
make
```

### 编译为WebAssembly

需要安装Emscripten SDK：

```bash
# 设置Emscripten环境
source /path/to/emsdk/emsdk_env.sh

# 在backend目录下
mkdir wasm_build
cd wasm_build
emcmake cmake ..
emmake
```

## 开发路线图

1. 完成基础的声音合成功能
2. 实现UTAU声库的完整解析
3. 添加更高级的声音处理效果
4. 实现与前端的集成
5. 优化性能和用户体验

## 注意事项

- 目前的代码仅为框架实现，需要进一步完善
- 实际的声音合成算法需要更复杂的实现
- UTAU声库的解析需要严格遵循其格式规范
- 与前端的通信接口需要根据最终选择的集成方式进行调整