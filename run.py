#!/usr/bin/env python3
"""
畅声编辑器启动脚本 - 使用Python 3.6环境
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """主启动函数"""
    try:
        # 获取项目根目录
        project_root = Path(__file__).parent
        
        # 检查Python 3.6是否可用
        try:
            result = subprocess.run(["py", "-3.6-32", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                python_cmd = "py -3.6-32"
                logging.info("使用Python 3.6-32环境")
            else:
                # 尝试直接使用python3.6
                result = subprocess.run(["python3.6", "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    python_cmd = "python3.6"
                    logging.info("使用python3.6环境")
                else:
                    logging.error("未找到Python 3.6环境")
                    print("错误: 请确保Python 3.6已安装")
                    sys.exit(1)
        except Exception as e:
            logging.error(f"检查Python环境时出错: {e}")
            sys.exit(1)
        
        # 运行主应用 - 使用更安全的方式处理路径
        main_script = str(project_root / "main.py")
        
        # 使用列表形式传递参数，避免路径编码问题
        cmd = [python_cmd.split()[0], python_cmd.split()[1] if len(python_cmd.split()) > 1 else "", main_script]
        cmd = [c for c in cmd if c]  # 移除空字符串
        
        logging.info(f"启动命令: {' '.join(cmd)}")
        print(f"启动畅声编辑器...")
        
        # 执行命令
        result = subprocess.run(cmd, cwd=str(project_root))
        if result.returncode != 0:
            logging.error(f"应用启动失败，退出码: {result.returncode}")
            sys.exit(result.returncode)
        
    except Exception as e:
        logging.error(f"启动应用时出错: {e}")
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()