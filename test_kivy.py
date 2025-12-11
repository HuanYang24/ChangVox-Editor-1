#!/usr/bin/env python3
"""
Kivy测试脚本
"""

import sys
import subprocess

def test_kivy():
    """测试Kivy是否正常工作"""
    try:
        # 使用Python 3.6测试Kivy
        cmd = ["py", "-3.6-32", "-c", """
import kivy
from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return Label(text='Kivy测试成功！')

if __name__ == '__main__':
    TestApp().run()
"""]
        
        print("正在测试Kivy...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Kivy测试成功！")
            return True
        else:
            print("✗ Kivy测试失败")
            print("错误信息:", result.stderr)
            return False
            
    except Exception as e:
        print(f"测试过程中出错: {e}")
        return False

def test_kivymd():
    """测试KivyMD是否正常工作"""
    try:
        # 使用Python 3.6测试KivyMD
        cmd = ["py", "-3.6-32", "-c", """
import kivymd
print('KivyMD版本:', kivymd.__version__)
"""]
        
        print("正在测试KivyMD...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ KivyMD测试成功！")
            print("输出:", result.stdout)
            return True
        else:
            print("✗ KivyMD测试失败")
            print("错误信息:", result.stderr)
            return False
            
    except Exception as e:
        print(f"测试过程中出错: {e}")
        return False

if __name__ == '__main__':
    print("=== 畅声编辑器Kivy测试 ===")
    
    # 测试Kivy
    kivy_success = test_kivy()
    
    # 测试KivyMD
    kivymd_success = test_kivymd()
    
    if kivy_success and kivymd_success:
        print("\n✓ 所有测试通过！Kivy和KivyMD已准备就绪。")
    else:
        print("\n✗ 部分测试失败，请检查安装。")