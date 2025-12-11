"""
畅声编辑器应用主类
"""

import logging
from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config

from .business.controller import MainController
from .presentation.main_window import MainWindow

class ChangVoxApp(App):
    """主应用类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "畅声编辑器 (ChangVox Editor)"
        self.controller = None
        self.main_window = None
        
        # 配置应用
        self._configure_app()
    
    def _configure_app(self):
        """配置应用设置"""
        # Kivy配置
        Config.set('graphics', 'width', '1200')
        Config.set('graphics', 'height', '800')
        Config.set('graphics', 'minimum_width', '800')
        Config.set('graphics', 'minimum_height', '600')
        
        # 设置窗口图标（如果有）
        # Config.set('kivy', 'window_icon', 'assets/icon.png')
        
        logging.info("应用配置完成")
    
    def build(self):
        """构建应用界面"""
        try:
            # 初始化控制器
            self.controller = MainController()
            
            # 创建主窗口
            self.main_window = MainWindow(controller=self.controller)
            
            # 设置控制器回调
            self.controller.set_ui_callback(self.main_window.update_ui)
            
            logging.info("应用构建完成")
            return self.main_window
            
        except Exception as e:
            logging.error(f"构建应用时出错: {e}")
            raise
    
    def on_stop(self):
        """应用退出时的清理工作"""
        if self.controller:
            self.controller.cleanup()
        logging.info("应用已退出")