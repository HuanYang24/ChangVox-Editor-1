"""
歌词编辑器组件
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ObjectProperty

class LyricsEditor(BoxLayout):
    """歌词编辑器"""
    
    lyrics_text = StringProperty('')
    on_lyrics_change = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        self._create_interface()
    
    def _create_interface(self):
        """创建界面"""
        # 标题
        title_label = Label(
            text='歌词编辑器',
            size_hint_y=None,
            height=30,
            font_size='16sp',
            bold=True
        )
        self.add_widget(title_label)
        
        # 歌词输入区域
        lyrics_scroll = ScrollView()
        self.lyrics_input = TextInput(
            text=self.lyrics_text,
            multiline=True,
            hint_text='请输入歌词...',
            size_hint_y=None
        )
        self.lyrics_input.bind(text=self._on_text_change)
        lyrics_scroll.add_widget(self.lyrics_input)
        self.add_widget(lyrics_scroll)
        
        # 歌词统计信息
        self.stats_label = Label(
            text='字符数: 0  行数: 0',
            size_hint_y=None,
            height=25,
            font_size='12sp'
        )
        self.add_widget(self.stats_label)
    
    def _on_text_change(self, instance, value):
        """文本变化事件处理"""
        self.lyrics_text = value
        self._update_stats()
        
        # 触发歌词变化事件
        if self.on_lyrics_change:
            self.on_lyrics_change(self, value)
    
    def _update_stats(self):
        """更新统计信息"""
        char_count = len(self.lyrics_text)
        line_count = len(self.lyrics_text.split('\n'))
        self.stats_label.text = f'字符数: {char_count}  行数: {line_count}'
    
    def get_lyrics(self):
        """获取歌词文本"""
        return self.lyrics_text
    
    def set_lyrics(self, lyrics):
        """设置歌词文本"""
        self.lyrics_text = lyrics
        self.lyrics_input.text = lyrics
        self._update_stats()
    
    def clear_lyrics(self):
        """清空歌词"""
        self.lyrics_text = ''
        self.lyrics_input.text = ''
        self._update_stats()