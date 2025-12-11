"""
音频控制组件
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.properties import BooleanProperty, NumericProperty, StringProperty

class AudioControls(BoxLayout):
    """音频控制面板"""
    
    # 属性
    is_playing = BooleanProperty(False)
    is_synthesis_complete = BooleanProperty(False)
    progress = NumericProperty(0)
    status_text = StringProperty('就绪')
    
    # 事件
    on_play = None
    on_stop = None
    on_save = None
    on_synthesize = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = 10
        self.spacing = 10
        self.size_hint_y = None
        self.height = 60
        
        self._create_interface()
    
    def _create_interface(self):
        """创建界面"""
        
        # 播放控制区域
        play_controls = BoxLayout(
            orientation='horizontal',
            size_hint_x=None,
            width=150,
            spacing=5
        )
        
        self.play_btn = Button(
            text='播放',
            disabled=True
        )
        self.play_btn.bind(on_press=self._on_play)
        play_controls.add_widget(self.play_btn)
        
        self.stop_btn = Button(
            text='停止',
            disabled=True
        )
        self.stop_btn.bind(on_press=self._on_stop)
        play_controls.add_widget(self.stop_btn)
        
        self.add_widget(play_controls)
        
        # 进度显示区域
        progress_area = BoxLayout(
            orientation='vertical',
            spacing=5
        )
        
        self.status_label = Label(
            text=self.status_text,
            size_hint_y=None,
            height=20
        )
        progress_area.add_widget(self.status_label)
        
        self.progress_bar = ProgressBar(
            max=100,
            value=self.progress,
            size_hint_y=None,
            height=20
        )
        progress_area.add_widget(self.progress_bar)
        
        self.add_widget(progress_area)
        
        # 合成控制区域
        synth_controls = BoxLayout(
            orientation='horizontal',
            size_hint_x=None,
            width=200,
            spacing=5
        )
        
        self.synthesize_btn = Button(
            text='开始合成',
            background_color=(0.2, 0.8, 0.2, 1)  # 绿色
        )
        self.synthesize_btn.bind(on_press=self._on_synthesize)
        synth_controls.add_widget(self.synthesize_btn)
        
        self.save_btn = Button(
            text='保存音频',
            disabled=True
        )
        self.save_btn.bind(on_press=self._on_save)
        synth_controls.add_widget(self.save_btn)
        
        self.add_widget(synth_controls)
    
    def _on_play(self, instance):
        """播放按钮事件"""
        if self.on_play:
            self.on_play(self)
        
        self.is_playing = True
        self.play_btn.disabled = True
        self.stop_btn.disabled = False
        self.status_text = '播放中...'
    
    def _on_stop(self, instance):
        """停止按钮事件"""
        if self.on_stop:
            self.on_stop(self)
        
        self.is_playing = False
        self.play_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_text = '已停止'
    
    def _on_save(self, instance):
        """保存按钮事件"""
        if self.on_save:
            self.on_save(self)
    
    def _on_synthesize(self, instance):
        """合成按钮事件"""
        if self.on_synthesize:
            self.on_synthesize(self)
        
        self.status_text = '合成中...'
        self.synthesize_btn.disabled = True
        self.progress = 0
    
    def set_playback_ready(self, ready):
        """设置播放就绪状态"""
        self.play_btn.disabled = not ready
        self.save_btn.disabled = not ready
    
    def set_synthesis_complete(self, complete):
        """设置合成完成状态"""
        self.is_synthesis_complete = complete
        self.synthesize_btn.disabled = False
        
        if complete:
            self.status_text = '合成完成'
            self.set_playback_ready(True)
    
    def update_progress(self, progress):
        """更新进度"""
        self.progress = progress
        self.progress_bar.value = progress
        
        if progress < 100:
            self.status_text = f'合成中... {progress}%'
    
    def show_error(self, error_message):
        """显示错误信息"""
        self.status_text = f'错误: {error_message}'
        self.synthesize_btn.disabled = False
        self.progress = 0
    
    def reset(self):
        """重置控制面板"""
        self.is_playing = False
        self.is_synthesis_complete = False
        self.progress = 0
        self.status_text = '就绪'
        
        self.play_btn.disabled = True
        self.stop_btn.disabled = True
        self.save_btn.disabled = True
        self.synthesize_btn.disabled = False