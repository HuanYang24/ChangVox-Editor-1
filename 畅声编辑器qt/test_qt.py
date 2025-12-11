import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

print("PyQt5模块导入成功")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("PyQt5测试")
    window.setGeometry(100, 100, 300, 200)
    
    label = QLabel("PyQt5测试成功!", window)
    label.setGeometry(50, 50, 200, 30)
    
    window.show()
    sys.exit(app.exec_())