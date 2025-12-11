"""
钢琴卷帘编辑器组件
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import ListProperty, ObjectProperty

class PianoRoll(BoxLayout):
    """钢琴卷帘编辑器"""
    
    notes = ListProperty([])
    on_notes_change = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # 钢琴卷帘参数
        self.octaves = 5  # 5个八度
        self.beats_per_measure = 4  # 每小节4拍
        self.measures = 8  # 8小节
        
        self._create_interface()
    
    def _create_interface(self):
        """创建界面"""
        # 标题
        title_label = Label(
            text='钢琴卷帘编辑器',
            size_hint_y=None,
            height=30,
            font_size='16sp',
            bold=True
        )
        self.add_widget(title_label)
        
        # 钢琴卷帘区域
        piano_roll_scroll = ScrollView()
        self.piano_roll_area = PianoRollArea(
            octaves=self.octaves,
            beats_per_measure=self.beats_per_measure,
            measures=self.measures
        )
        self.piano_roll_area.bind(on_notes_change=self._on_notes_change)
        piano_roll_scroll.add_widget(self.piano_roll_area)
        self.add_widget(piano_roll_scroll)
        
        # 控制按钮
        controls_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=40,
            spacing=10
        )
        
        add_note_btn = Button(text='添加音符')
        add_note_btn.bind(on_press=self._add_note)
        controls_layout.add_widget(add_note_btn)
        
        clear_notes_btn = Button(text='清空音符')
        clear_notes_btn.bind(on_press=self._clear_notes)
        controls_layout.add_widget(clear_notes_btn)
        
        self.add_widget(controls_layout)
    
    def _on_notes_change(self, instance, notes):
        """音符变化事件处理"""
        self.notes = notes
        if self.on_notes_change:
            self.on_notes_change(self, notes)
    
    def _add_note(self, instance):
        """添加音符"""
        # 默认添加一个C4音符
        new_note = {
            'pitch': 60,  # C4
            'duration': 1.0,
            'start_beat': 0.0,
            'velocity': 100
        }
        self.piano_roll_area.add_note(new_note)
    
    def _clear_notes(self, instance):
        """清空音符"""
        self.piano_roll_area.clear_notes()
    
    def get_notes(self):
        """获取音符列表"""
        return self.piano_roll_area.get_notes()
    
    def set_notes(self, notes):
        """设置音符列表"""
        self.piano_roll_area.set_notes(notes)


class PianoRollArea(GridLayout):
    """钢琴卷帘绘制区域"""
    
    notes = ListProperty([])
    on_notes_change = ObjectProperty(None)
    
    def __init__(self, octaves=5, beats_per_measure=4, measures=8, **kwargs):
        super().__init__(**kwargs)
        self.octaves = octaves
        self.beats_per_measure = beats_per_measure
        self.measures = measures
        
        self.cols = 1
        self.padding = 5
        self.spacing = 2
        
        self._create_piano_roll()
    
    def _create_piano_roll(self):
        """创建钢琴卷帘"""
        # 这里需要实现钢琴卷帘的绘制逻辑
        # 包括钢琴键盘、时间轴、音符块等
        
        # 临时显示信息
        info_label = Label(
            text=f'钢琴卷帘区域 - {self.octaves}个八度, {self.measures}小节',
            size_hint_y=None,
            height=200
        )
        self.add_widget(info_label)
    
    def add_note(self, note_data):
        """添加音符"""
        self.notes.append(note_data)
        if self.on_notes_change:
            self.on_notes_change(self, self.notes)
    
    def clear_notes(self):
        """清空音符"""
        self.notes = []
        if self.on_notes_change:
            self.on_notes_change(self, self.notes)
    
    def get_notes(self):
        """获取音符列表"""
        return self.notes.copy()
    
    def set_notes(self, notes):
        """设置音符列表"""
        self.notes = notes.copy()
        if self.on_notes_change:
            self.on_notes_change(self, self.notes)