"""
参数调整面板组件
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.properties import DictProperty, ObjectProperty

class ParameterPanel(BoxLayout):
    """参数调整面板"""
    
    parameters = DictProperty({})
    on_parameters_change = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # 默认参数
        self.default_parameters = {
            'speed': {'min': 0.5, 'max': 2.0, 'default': 1.0, 'value': 1.0},
            'pitch': {'min': -12, 'max': 12, 'default': 0, 'value': 0},
            'energy': {'min': 0.0, 'max': 2.0, 'default': 1.0, 'value': 1.0},
            'breathiness': {'min': 0.0, 'max': 1.0, 'default': 0.5, 'value': 0.5},
            'tension': {'min': 0.0, 'max': 1.0, 'default': 0.5, 'value': 0.5},
            'vibrato': {'min': 0.0, 'max': 1.0, 'default': 0.3, 'value': 0.3}
        }
        
        self.parameters = {key: param['value'] for key, param in self.default_parameters.items()}
        
        self._create_interface()
    
    def _create_interface(self):
        """创建界面"""
        # 标题
        title_label = Label(
            text='合成参数调整',
            size_hint_y=None,
            height=30,
            font_size='16sp',
            bold=True
        )
        self.add_widget(title_label)
        
        # 参数网格
        param_grid = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None
        )
        param_grid.bind(minimum_height=param_grid.setter('height'))
        
        # 创建参数控件
        self.param_widgets = {}
        
        for param_name, param_config in self.default_parameters.items():
            # 参数标签
            label = Label(
                text=f"{param_name}: {param_config['value']}",
                size_hint_y=None,
                height=30
            )
            param_grid.add_widget(label)
            
            # 参数滑块
            slider = Slider(
                min=param_config['min'],
                max=param_config['max'],
                value=param_config['value'],
                step=0.01 if isinstance(param_config['value'], float) else 1,
                size_hint_y=None,
                height=30
            )
            slider.bind(value=self._create_slider_callback(param_name, label))
            param_grid.add_widget(slider)
            
            self.param_widgets[param_name] = {'slider': slider, 'label': label}
        
        self.add_widget(param_grid)
        
        # 预设按钮
        preset_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=40,
            spacing=10
        )
        
        from kivy.uix.button import Button
        
        default_preset_btn = Button(text='默认预设')
        default_preset_btn.bind(on_press=self._load_default_preset)
        preset_layout.add_widget(default_preset_btn)
        
        soft_preset_btn = Button(text='柔和预设')
        soft_preset_btn.bind(on_press=self._load_soft_preset)
        preset_layout.add_widget(soft_preset_btn)
        
        powerful_preset_btn = Button(text='强力预设')
        powerful_preset_btn.bind(on_press=self._load_powerful_preset)
        preset_layout.add_widget(powerful_preset_btn)
        
        self.add_widget(preset_layout)
    
    def _create_slider_callback(self, param_name, label):
        """创建滑块回调函数"""
        def on_slider_value(instance, value):
            # 更新参数值
            self.parameters[param_name] = value
            
            # 更新标签显示
            label.text = f"{param_name}: {value:.2f}" if isinstance(value, float) else f"{param_name}: {value}"
            
            # 触发参数变化事件
            if self.on_parameters_change:
                self.on_parameters_change(self, self.parameters)
        
        return on_slider_value
    
    def _load_default_preset(self, instance):
        """加载默认预设"""
        for param_name, param_config in self.default_parameters.items():
            default_value = param_config['default']
            self.param_widgets[param_name]['slider'].value = default_value
            self.parameters[param_name] = default_value
    
    def _load_soft_preset(self, instance):
        """加载柔和预设"""
        soft_preset = {
            'speed': 0.8,
            'pitch': -2,
            'energy': 0.7,
            'breathiness': 0.8,
            'tension': 0.3,
            'vibrato': 0.4
        }
        
        for param_name, value in soft_preset.items():
            if param_name in self.param_widgets:
                self.param_widgets[param_name]['slider'].value = value
                self.parameters[param_name] = value
    
    def _load_powerful_preset(self, instance):
        """加载强力预设"""
        powerful_preset = {
            'speed': 1.2,
            'pitch': 2,
            'energy': 1.5,
            'breathiness': 0.2,
            'tension': 0.8,
            'vibrato': 0.6
        }
        
        for param_name, value in powerful_preset.items():
            if param_name in self.param_widgets:
                self.param_widgets[param_name]['slider'].value = value
                self.parameters[param_name] = value
    
    def get_parameters(self):
        """获取当前参数"""
        return self.parameters.copy()
    
    def set_parameters(self, parameters):
        """设置参数"""
        for param_name, value in parameters.items():
            if param_name in self.param_widgets:
                self.param_widgets[param_name]['slider'].value = value
                self.parameters[param_name] = value