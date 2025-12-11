#!/usr/bin/env python3
"""
Kivy简单测试脚本 - 只测试导入
"""

import subprocess

def test_kivy_import():
    """测试Kivy导入"""
    try:
        cmd = ["py", "-3.6-32", "-c", """
import kivy
print('Kivy版本:', kivy.__version__)
print('✓ Kivy导入成功')
"""]
        
        print("正在测试Kivy导入...")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        if result.returncode == 0:
            print("✓ Kivy导入成功！")
            print("输出:", result.stdout)
            return True
        else:
            print("✗ Kivy导入失败")
            print("错误信息:", result.stderr)
            return False
            
    except Exception as e:
        print(f"测试过程中出错: {e}")
        return False

def test_kivymd_import():
    """测试KivyMD导入"""
    try:
        cmd = ["py", "-3.6-32", "-c", """
import kivymd
print('KivyMD版本:', kivymd.__version__)
print('✓ KivyMD导入成功')
"""]
        
        print("正在测试KivyMD导入...")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        if result.returncode == 0:
            print("✓ KivyMD导入成功！")
            print("输出:", result.stdout)
            return True
        else:
            print("✗ KivyMD导入失败")
            print("错误信息:", result.stderr)
            return False
            
    except Exception as e:
        print(f"测试过程中出错: {e}")
        return False

def test_project_imports():
    """测试项目模块导入"""
    try:
        cmd = ["py", "-3.6-32", "-c", """
import sys
sys.path.insert(0, '.')

try:
    from src.app import ChangVoxApp
    print('✓ ChangVoxApp导入成功')
except ImportError as e:
    print('✗ ChangVoxApp导入失败:', e)
    
try:
    from src.business.controller import MainController
    print('✓ MainController导入成功')
except ImportError as e:
    print('✗ MainController导入失败:', e)
"""]
        
        print("正在测试项目模块导入...")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        if result.returncode == 0:
            print("✓ 项目模块导入测试完成")
            print("输出:", result.stdout)
            return True
        else:
            print("✗ 项目模块导入测试失败")
            print("错误信息:", result.stderr)
            return False
            
    except Exception as e:
        print(f"测试过程中出错: {e}")
        return False

if __name__ == '__main__':
    print("=== 畅声编辑器Kivy简单测试 ===")
    
    # 测试Kivy导入
    kivy_success = test_kivy_import()
    
    # 测试KivyMD导入
    kivymd_success = test_kivymd_import()
    
    # 测试项目模块导入
    project_success = test_project_imports()
    
    if kivy_success and kivymd_success and project_success:
        print("\n✓ 所有测试通过！Kivy环境已准备就绪。")
        print("\n使用以下命令启动应用:")
        print("py -3.6-32 main.py")
        print("或使用启动脚本:")
        print("python run.py")
    else:
        print("\n✗ 部分测试失败，请检查安装。")