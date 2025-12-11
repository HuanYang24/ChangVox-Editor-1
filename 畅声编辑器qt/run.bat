@echo off
REM 运行畅声编辑器 - 使用虚拟环境中的Python解释器
cd /d "%~dp0"
.venv\Scripts\python.exe main.py
echo 程序已退出，按任意键关闭窗口...
pause > nul