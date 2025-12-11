"""
主控制器 - 协调各个服务模块
"""

import logging
from typing import Optional, Callable

from ..services.diffsinger_service import DiffSingerService
from ..services.audio_service import AudioService
from ..services.project_manager import ProjectManager
from .event_bus import EventBus

class MainController:
    """主控制器类"""
    
    def __init__(self):
        self.ui_callback: Optional[Callable] = None
        self.event_bus = EventBus()
        
        # 初始化服务
        self.diffsinger_service = DiffSingerService(self.event_bus)
        self.audio_service = AudioService(self.event_bus)
        self.project_manager = ProjectManager(self.event_bus)
        
        # 设置事件监听
        self._setup_event_listeners()
        
        logging.info("主控制器初始化完成")
    
    def _setup_event_listeners(self):
        """设置事件监听器"""
        # 监听合成完成事件
        self.event_bus.subscribe('synthesis_complete', self._on_synthesis_complete)
        # 监听音频处理完成事件
        self.event_bus.subscribe('audio_processed', self._on_audio_processed)
        # 监听项目状态变化
        self.event_bus.subscribe('project_updated', self._on_project_updated)
    
    def set_ui_callback(self, callback: Callable):
        """设置UI更新回调"""
        self.ui_callback = callback
    
    def synthesize_voice(self, lyrics: str, notes: list, parameters: dict):
        """合成歌声
        
        Args:
            lyrics: 歌词文本
            notes: 音符列表
            parameters: 合成参数
        """
        try:
            # 尝试使用演示模式合成
            spectrogram = self.diffsinger_service.synthesize_demo(lyrics, notes, parameters)
            
            # 通过音频服务生成音频
            audio_data = self.audio_service.synthesize_audio(spectrogram)
            
            # 发布合成完成事件
            self.event_bus.publish('synthesis_complete', {
                'audio_data': audio_data,
                'spectrogram': spectrogram,
                'lyrics': lyrics,
                'notes': notes,
                'parameters': parameters
            })
            
            logging.info("歌声合成请求已处理")
            
        except Exception as e:
            logging.error(f"歌声合成失败: {e}")
            self.event_bus.publish('synthesis_error', {'error': str(e)})
    
    def play_audio(self, audio_data):
        """播放音频"""
        self.audio_service.play(audio_data)
    
    def save_project(self, file_path: str):
        """保存项目"""
        self.project_manager.save(file_path)
    
    def load_project(self, file_path: str):
        """加载项目"""
        self.project_manager.load(file_path)
    
    def _on_synthesis_complete(self, data):
        """处理合成完成事件"""
        if self.ui_callback:
            self.ui_callback('synthesis_complete', data)
    
    def _on_audio_processed(self, data):
        """处理音频处理完成事件"""
        if self.ui_callback:
            self.ui_callback('audio_processed', data)
    
    def _on_project_updated(self, data):
        """处理项目更新事件"""
        if self.ui_callback:
            self.ui_callback('project_updated', data)
    
    def cleanup(self):
        """清理资源"""
        self.diffsinger_service.cleanup()
        self.audio_service.cleanup()
        logging.info("控制器资源清理完成")