#!/usr/bin/env python3
"""
畅声编辑器 (ChangVox Editor) - 主入口文件
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """主函数"""
    try:
        from src.app import ChangVoxApp
        
        # 创建并运行应用
        app = ChangVoxApp()
        app.run()
        
    except ImportError as e:
        logging.error(f"导入错误: {e}")
        print("请确保所有依赖已正确安装")
        sys.exit(1)
    except Exception as e:
        logging.error(f"应用启动错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()