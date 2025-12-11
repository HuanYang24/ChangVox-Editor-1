"""
主窗口 - Kivy GUI主界面
"""

import logging
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

from .lyrics_editor import LyricsEditor
from .piano_roll import PianoRoll
from .parameter_panel import ParameterPanel
from .audio_controls import AudioControls

class MainWindow(TabbedPanel):
    """主窗口类"""
    
    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        
        # 设置标签页样式
        self.default_tab_text = '编辑器'
        self.tab_width = 120
        
        # 创建界面组件
        self._create_interface()
        
        # 状态变量
        self.current_project = None
        self.is_playing = False
        
        logging.info("主窗口初始化完成")
    
    def _create_interface(self):
        """创建界面布局"""
        
        # 歌词编辑标签页
        lyrics_tab = BoxLayout(orientation='vertical')
        self.lyrics_editor = LyricsEditor()
        lyrics_tab.add_widget(self.lyrics_editor)
        self.add_widget(lyrics_tab)
        self.tab_list[-1].text = '歌词编辑'
        
        # 钢琴卷帘标签页
        piano_tab = BoxLayout(orientation='vertical')
        self.piano_roll = PianoRoll()
        piano_tab.add_widget(self.piano_roll)
        self.add_widget(piano_tab)
        self.tab_list[-1].text = '钢琴卷帘'
        
        # 参数调整标签页
        param_tab = BoxLayout(orientation='vertical')
        self.parameter_panel = ParameterPanel()
        param_tab.add_widget(self.parameter_panel)
        self.add_widget(param_tab)
        self.tab_list[-1].text = '参数调整'
        
        # 底部控制栏
        self.audio_controls = AudioControls()
        self.add_widget(self.audio_controls)
        
        # 连接事件
        self._connect_events()
    
    def _connect_events(self):
        """连接事件处理"""
        # 歌词编辑器事件
        self.lyrics_editor.bind(on_lyrics_change=self._on_lyrics_change)
        
        # 钢琴卷帘事件
        self.piano_roll.bind(on_notes_change=self._on_notes_change)
        
        # 参数面板事件
        self.parameter_panel.bind(on_parameters_change=self._on_parameters_change)
        
        # 音频控制事件
        self.audio_controls.bind(
            on_play=self._on_play,
            on_stop=self._on_stop,
            on_save=self._on_save,
            on_synthesize=self._on_synthesize
        )
    
    def update_ui(self, event_type, data):
        """更新UI界面
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        try:
            if event_type == 'synthesis_complete':
                self._on_synthesis_complete(data)
            elif event_type == 'audio_processed':
                self._on_audio_processed(data)
            elif event_type == 'project_updated':
                self._on_project_updated(data)
            elif event_type == 'synthesis_error':
                self._on_synthesis_error(data)
            
            # 在主线程中更新UI
            Clock.schedule_once(lambda dt: self._update_ui_threadsafe(event_type, data))
            
        except Exception as e:
            logging.error(f"UI更新错误: {e}")
    
    def _update_ui_threadsafe(self, event_type, data):
        """线程安全的UI更新"""
        if event_type == 'synthesis_complete':
            self.audio_controls.set_playback_ready(True)
            self.audio_controls.update_progress(100)
        elif event_type == 'synthesis_progress':
            self.audio_controls.update_progress(data.get('progress', 0))
    
    def _on_lyrics_change(self, instance, lyrics):
        """歌词变化事件处理"""
        if self.controller and self.current_project:
            self.controller.project_manager.update_lyrics(lyrics)
    
    def _on_notes_change(self, instance, notes):
        """音符变化事件处理"""
        if self.controller and self.current_project:
            self.controller.project_manager.update_notes(notes)
    
    def _on_parameters_change(self, instance, parameters):
        """参数变化事件处理"""
        if self.controller and self.current_project:
            self.controller.project_manager.update_parameters(parameters)
    
    def _on_play(self, instance):
        """播放按钮事件处理"""
        if self.controller:
            # 获取当前音频数据并播放
            # 这里需要从控制器获取音频数据
            pass
    
    def _on_stop(self, instance):
        """停止按钮事件处理"""
        if self.controller:
            self.controller.audio_service.stop()
    
    def _on_save(self, instance):
        """保存按钮事件处理"""
        if self.controller and self.current_project:
            # 实现文件保存对话框
            pass
    
    def _on_synthesize(self, instance):
        """合成按钮事件处理"""
        if self.controller:
            # 获取歌词、音符和参数
            lyrics = self.lyrics_editor.get_lyrics()
            notes = self.piano_roll.get_notes()
            parameters = self.parameter_panel.get_parameters()
            
            # 开始合成
            self.controller.synthesize_voice(lyrics, notes, parameters)
    
    def _on_synthesis_complete(self, data):
        """合成完成事件处理"""
        logging.info("歌声合成完成")
        self.audio_controls.set_synthesis_complete(True)
    
    def _on_audio_processed(self, data):
        """音频处理完成事件处理"""
        logging.info("音频处理完成")
    
    def _on_project_updated(self, data):
        """项目更新事件处理"""
        logging.info("项目已更新")
    
    def _on_synthesis_error(self, data):
        """合成错误事件处理"""
        error_msg = data.get('error', '未知错误')
        logging.error(f"合成错误: {error_msg}")
        # 显示错误消息
        self.audio_controls.show_error(error_msg)
    
    def new_project(self):
        """创建新项目"""
        if self.controller:
            # 实现新项目创建逻辑
            pass
    
    def open_project(self):
        """打开项目"""
        if self.controller:
            # 实现项目打开逻辑
            pass
    
    def save_project(self):
        """保存项目"""
        if self.controller and self.current_project:
            self.controller.save_project()