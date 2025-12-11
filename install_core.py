#!/usr/bin/env python3
"""
核心依赖安装脚本
用于逐步安装ChangVox Editor的核心依赖包
"""

import subprocess
import sys

def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_package(package_name):
    """安装单个包"""
    print(f"正在安装 {package_name}...")
    success, stdout, stderr = run_command(f"{sys.executable} -m pip install {package_name}")
    
    if success:
        print(f"✓ {package_name} 安装成功")
        return True
    else:
        print(f"✗ {package_name} 安装失败")
        print(f"错误信息: {stderr}")
        return False

def main():
    print("开始安装ChangVox Editor核心依赖包...")
    print("=" * 50)
    
    # 核心依赖包列表（按依赖顺序）
    core_packages = [
        "numpy",
        "pillow",
        "requests",
        "pyyaml",
        "soundfile",
        "pydub",
        "librosa",
        "kivy",
        "kivymd"
    ]
    
    # 安装核心包
    for package in core_packages:
        if not install_package(package):
            print(f"安装 {package} 失败，跳过后续安装")
            break
    
    print("=" * 50)
    print("核心依赖安装完成！")
    print("\n接下来需要安装PyTorch，请运行以下命令：")
    print("pip install torch torchaudio")

if __name__ == "__main__":
    main()