#!/usr/bin/env python3
"""
项目结构测试脚本 - 验证所有模块是否正确导入
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试所有模块的导入"""
    print("=== 畅声编辑器项目结构测试 ===")
    
    modules_to_test = [
        # 主应用
        ("src.app", "ChangVoxApp"),
        
        # 业务逻辑层
        ("src.business.controller", "MainController"),
        ("src.business.event_bus", "EventBus"),
        
        # 服务层
        ("src.services.diffsinger_service", "DiffSingerService"),
        ("src.services.audio_service", "AudioService"),
        ("src.services.project_manager", "ProjectManager"),
        
        # 表现层
        ("src.presentation.main_window", "MainWindow"),
        ("src.presentation.lyrics_editor", "LyricsEditor"),
        ("src.presentation.piano_roll", "PianoRoll"),
        ("src.presentation.parameter_panel", "ParameterPanel"),
        ("src.presentation.audio_controls", "AudioControls"),
    ]
    
    all_passed = True
    
    for module_path, class_name in modules_to_test:
        try:
            # 动态导入模块和类
            module = __import__(module_path, fromlist=[class_name])
            class_obj = getattr(module, class_name)
            
            # 尝试创建实例（如果可能）
            if class_name in ['EventBus', 'LyricsEditor', 'ParameterPanel', 'AudioControls']:
                instance = class_obj()
                print(f"✓ {module_path}.{class_name} - 导入和实例化成功")
            else:
                print(f"✓ {module_path}.{class_name} - 导入成功")
                
        except ImportError as e:
            print(f"✗ {module_path}.{class_name} - 导入失败: {e}")
            all_passed = False
        except Exception as e:
            print(f"? {module_path}.{class_name} - 导入成功但实例化失败: {e}")
    
    print(f"\n测试结果: {'全部通过' if all_passed else '部分失败'}")
    return all_passed

def test_file_structure():
    """测试文件结构"""
    print("\n=== 文件结构检查 ===")
    
    required_files = [
        "README.md",
        "requirements.txt",
        "main.py",
        "src/__init__.py",
        "src/app.py",
        "src/business/__init__.py",
        "src/business/controller.py",
        "src/business/event_bus.py",
        "src/services/__init__.py",
        "src/services/diffsinger_service.py",
        "src/services/audio_service.py",
        "src/services/project_manager.py",
        "src/presentation/__init__.py",
        "src/presentation/main_window.py",
        "src/presentation/lyrics_editor.py",
        "src/presentation/piano_roll.py",
        "src/presentation/parameter_panel.py",
        "src/presentation/audio_controls.py",
    ]
    
    all_exist = True
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✓ {file_path} - 存在")
        else:
            print(f"✗ {file_path} - 不存在")
            all_exist = False
    
    print(f"\n文件结构: {'完整' if all_exist else '不完整'}")
    return all_exist

def test_requirements():
    """测试依赖文件"""
    print("\n=== 依赖文件检查 ===")
    
    requirements_file = project_root / "requirements.txt"
    
    if requirements_file.exists():
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_packages = [
                "kivy", "torch", "librosa", "soundfile", "pydub", "numpy"
            ]
            
            missing_packages = []
            for package in required_packages:
                if package in content:
                    print(f"✓ {package} - 在依赖文件中")
                else:
                    print(f"✗ {package} - 不在依赖文件中")
                    missing_packages.append(package)
            
            if missing_packages:
                print(f"\n缺少的包: {', '.join(missing_packages)}")
                return False
            else:
                print("\n所有必需依赖项都存在")
                return True
                
        except Exception as e:
            print(f"读取依赖文件失败: {e}")
            return False
    else:
        print("依赖文件不存在")
        return False

if __name__ == "__main__":
    print("畅声编辑器项目结构验证")
    print("=" * 50)
    
    # 运行测试
    import_ok = test_imports()
    structure_ok = test_file_structure()
    requirements_ok = test_requirements()
    
    print("\n" + "=" * 50)
    
    if import_ok and structure_ok and requirements_ok:
        print("🎉 项目结构验证通过！")
        print("\n下一步:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 运行应用: python main.py")
        print("3. 集成DiffSinger模型")
        print("4. 测试音频功能")
    else:
        print("❌ 项目结构验证失败，请检查上述错误")
    
    sys.exit(0 if (import_ok and structure_ok and requirements_ok) else 1)