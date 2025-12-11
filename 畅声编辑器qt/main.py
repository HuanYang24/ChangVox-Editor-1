import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFileDialog, QLabel, QComboBox, QScrollArea, 
    QSplitter, QFrame, QGroupBox, QSlider, QGridLayout, QCheckBox,
    QTabWidget, QTextEdit, QMessageBox
)
from PyQt6.QtGui import QIcon, QPainter, QPen, QColor, QFont, QPalette
from PyQt6.QtCore import Qt, QRect, QPoint, QSize
import numpy as np
import librosa
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os
from utau_loader import UTAULoader

# 确保matplotlib使用PyQt6后端
import matplotlib
matplotlib.use('Qt5Agg')

# 设置matplotlib中文字体，使用系统可用字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "Arial Unicode MS"]
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

class SingingVoiceSynthesizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("畅声 - 虚拟歌声合成器")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        
        # 初始化音频相关变量
        self.audio_data = None
        self.sr = None
        self.current_track = 0
        self.tracks = [
            {"name": "未命名音轨", "data": None, "visible": True, "muted": False, "solo": False, "volume": 100, "singer": "默认歌手"},
        ]
        self.current_singer = "默认歌手"
        self.singers = ["默认歌手", "女高音", "男低音", "电音歌手"]
        
        # 添加播放控制相关变量
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0  # 当前播放位置
        self.playhead_position = 0
        self.is_playhead_moving = False
        
        # 初始化UTAU声库加载器
        self.utau_loader = UTAULoader()
        self.loaded_voicebanks = {}
        self.current_voicebank = None
        
        # 创建主部件和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建主分割器
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(self.main_splitter)
        self.main_splitter.setStyleSheet("QSplitter::handle { background-color: #333333; }")
        
        # 创建左侧音轨面板
        self.create_track_panel()
        
        # 创建中间主面板（钢琴卷帘和时间轴）
        self.create_main_panel()
        
        # 创建右侧参数面板
        self.create_parameter_panel()
        
        # 初始化PyAudio
        self.p = pyaudio.PyAudio()
        
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background-color: #2d2d2d; color: #ffffff;")
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        
        # 视图菜单
        view_menu = menu_bar.addMenu("视图")
        
        # 修改菜单
        modify_menu = menu_bar.addMenu("修改")
        
        # 自动处理菜单
        auto_menu = menu_bar.addMenu("自动处理")
        
        # 项目菜单
        project_menu = menu_bar.addMenu("项目")
        
        # 走带控制菜单
        control_menu = menu_bar.addMenu("走带控制")
        
        # 脚本菜单
        script_menu = menu_bar.addMenu("脚本")
        
        # 其他菜单
        other_menu = menu_bar.addMenu("其他")
        
    def create_tool_bar(self):
        tool_bar = self.addToolBar("工具栏")
        tool_bar.setStyleSheet("background-color: #252526; color: #ffffff;")
        
        # 设置按钮样式
        button_style = """
            QPushButton {
                background-color: #2d2d2d;
                color: #cccccc;
                border: 1px solid #3e3e42;
                padding: 4px 8px;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #4d4d4d;
            }
        """
        
        # 添加音轨按钮
        add_track_button = QPushButton("+")
        add_track_button.setStyleSheet(button_style)
        add_track_button.clicked.connect(self.add_track)
        tool_bar.addWidget(add_track_button)
        
        # 工具栏区域分隔
        tool_bar.addSeparator()
        
        # 显示工具栏区域标签
        toolbar_label = QLabel("编曲")
        toolbar_label.setStyleSheet("color: #ffffff;")
        tool_bar.addWidget(toolbar_label)
        
    def create_track_panel(self):
        # 创建左侧音轨面板
        self.track_panel = QWidget()
        self.track_panel.setMinimumWidth(150)
        self.track_panel.setMaximumWidth(200)
        self.track_panel.setStyleSheet("background-color: #252526;")
        track_panel_layout = QVBoxLayout(self.track_panel)
        track_panel_layout.setContentsMargins(0, 0, 0, 0)
        track_panel_layout.setSpacing(0)
        
        # 音轨面板标题
        track_title = QLabel("编曲")
        track_title.setStyleSheet("font-weight: bold; color: #ffffff; padding: 5px;")
        track_panel_layout.addWidget(track_title)
        
        # 创建音轨列表区域
        self.track_list_scroll = QScrollArea()
        self.track_list_scroll.setWidgetResizable(True)
        self.track_list_scroll.setStyleSheet("background-color: #252526;")
        
        self.track_list_widget = QWidget()
        self.track_list_layout = QVBoxLayout(self.track_list_widget)
        self.track_list_layout.setContentsMargins(0, 0, 0, 0)
        self.track_list_layout.setSpacing(1)
        
        self.track_list_scroll.setWidget(self.track_list_widget)
        track_panel_layout.addWidget(self.track_list_scroll)
        
        # 添加初始音轨
        self.update_track_list()
        
        # 将音轨面板添加到主分割器
        self.main_splitter.addWidget(self.track_panel)
        
    def create_main_panel(self):
        # 创建中间主面板
        self.main_panel = QWidget()
        main_panel_layout = QVBoxLayout(self.main_panel)
        main_panel_layout.setContentsMargins(0, 0, 0, 0)
        main_panel_layout.setSpacing(0)
        
        # 创建顶部小节/拍号显示
        self.time_signature_widget = QWidget()
        self.time_signature_widget.setMinimumHeight(30)
        self.time_signature_widget.setMaximumHeight(30)
        self.time_signature_widget.setStyleSheet("background-color: #252526;")
        time_signature_layout = QHBoxLayout(self.time_signature_widget)
        time_signature_layout.setContentsMargins(5, 0, 0, 0)
        
        # 小节/拍号标签
        time_signature_label = QLabel("1   4/4  120  |  2  ")
        time_signature_label.setStyleSheet("color: #cccccc;")
        time_signature_layout.addWidget(time_signature_label)
        
        # 钢琴卷帘工具栏
        piano_toolbar = QWidget()
        piano_toolbar.setMinimumHeight(30)
        piano_toolbar.setMaximumHeight(30)
        piano_toolbar.setStyleSheet("background-color: #2d2d2d;")
        piano_toolbar_layout = QHBoxLayout(piano_toolbar)
        piano_toolbar_layout.setContentsMargins(5, 0, 5, 0)
        
        # 钢琴卷帘工具按钮
        button_style = """
            QPushButton {
                background-color: #2d2d2d;
                color: #cccccc;
                border: 1px solid #3e3e42;
                padding: 2px 5px;
                border-radius: 2px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """
        
        piano_toolbar_layout.addWidget(QLabel("钢琴卷帘"))
        piano_toolbar_layout.addSpacing(10)
        
        piano_toolbar_layout.addWidget(QPushButton("▸"))
        piano_toolbar_layout.addWidget(QPushButton("✎"))
        piano_toolbar_layout.addWidget(QPushButton("="))
        piano_toolbar_layout.addWidget(QPushButton("↔"))
        piano_toolbar_layout.addWidget(QPushButton("♫"))
        piano_toolbar_layout.addWidget(QPushButton("🎵"))
        piano_toolbar_layout.addWidget(QPushButton("abc"))
        
        piano_toolbar_layout.addSpacing(10)
        piano_toolbar_layout.addWidget(QLabel("SNAP: 1/8个四分音符(32分音符)"))
        piano_toolbar_layout.addSpacing(10)
        
        # 播放控制按钮
        self.play_button = QPushButton("▶")
        self.play_button.setStyleSheet(button_style)
        self.play_button.clicked.connect(self.play_audio)
        piano_toolbar_layout.addWidget(self.play_button)
        
        self.pause_button = QPushButton("⏸")
        self.pause_button.setStyleSheet(button_style)
        self.pause_button.clicked.connect(self.pause_audio)
        piano_toolbar_layout.addWidget(self.pause_button)
        
        self.stop_button = QPushButton("⏹")
        self.stop_button.setStyleSheet(button_style)
        self.stop_button.clicked.connect(self.stop_audio)
        piano_toolbar_layout.addWidget(self.stop_button)
        
        self.rewind_button = QPushButton("⏮")
        self.rewind_button.setStyleSheet(button_style)
        self.rewind_button.clicked.connect(self.rewind_audio)
        piano_toolbar_layout.addWidget(self.rewind_button)
        
        self.fast_forward_button = QPushButton("⏭")
        self.fast_forward_button.setStyleSheet(button_style)
        self.fast_forward_button.clicked.connect(self.fast_forward_audio)
        piano_toolbar_layout.addWidget(self.fast_forward_button)
        
        # 伸展项，使按钮靠左
        piano_toolbar_layout.addStretch()
        
        # 创建钢琴卷帘控件
        self.piano_roll_widget = PianoRollWidget()
        
        # 添加到主面板布局
        main_panel_layout.addWidget(self.time_signature_widget)
        main_panel_layout.addWidget(piano_toolbar)
        main_panel_layout.addWidget(self.piano_roll_widget)
        
        # 将主面板添加到主分割器
        self.main_splitter.addWidget(self.main_panel)
        
    def create_parameter_panel(self):
        # 创建右侧参数面板
        self.parameter_panel = QWidget()
        self.parameter_panel.setMinimumWidth(250)
        self.parameter_panel.setMaximumWidth(350)
        self.parameter_panel.setStyleSheet("background-color: #252526;")
        parameter_panel_layout = QVBoxLayout(self.parameter_panel)
        parameter_panel_layout.setContentsMargins(0, 0, 0, 0)
        parameter_panel_layout.setSpacing(0)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(
            "QTabWidget::pane { background-color: #252526; border: none; }"
            "QTabBar::tab { background-color: #2d2d2d; color: #cccccc; padding: 5px 10px; border: 1px solid #3e3e42; }")
        
        # 歌声标签页
        vocals_tab = QWidget()
        vocals_layout = QVBoxLayout(vocals_tab)
        vocals_layout.setContentsMargins(5, 5, 5, 5)
        vocals_layout.setSpacing(10)
        
        # 歌手选择组
        singer_group = QGroupBox("歌声")
        singer_group.setStyleSheet("color: #ffffff; border: 1px solid #3e3e42; border-radius: 4px;")
        singer_layout = QVBoxLayout(singer_group)
        singer_layout.setContentsMargins(5, 5, 5, 5)
        singer_layout.setSpacing(8)
        
        # 当前声库下拉框
        singer_layout.addWidget(QLabel("当前声库(音域范围)"))
        self.singer_combo = QComboBox()
        self.singer_combo.addItem("(未设定)")
        self.singer_combo.addItems(self.singers)
        self.singer_combo.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555;")
        self.singer_combo.currentTextChanged.connect(self.change_singer)
        singer_layout.addWidget(self.singer_combo)
        
        # 加载UTAU声库按钮
        load_utau_button = QPushButton("加载UTAU声库")
        load_utau_button.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555;")
        load_utau_button.clicked.connect(self.load_utau_voicebank)
        singer_layout.addWidget(load_utau_button)
        
        # 声库版本下拉框
        singer_layout.addWidget(QLabel("声库版本"))
        self.singer_version_combo = QComboBox()
        self.singer_version_combo.addItem("(未设定)")
        self.singer_version_combo.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555;")
        singer_layout.addWidget(self.singer_version_combo)
        
        # 声库信息显示
        self.singer_info_label = QLabel("没有加载声库")
        self.singer_info_label.setStyleSheet("color: #cccccc; background-color: #2d2d2d; padding: 5px; border-radius: 3px;")
        self.singer_info_label.setWordWrap(True)
        singer_layout.addWidget(self.singer_info_label)
        
        # 加载/保存按钮
        load_save_layout = QHBoxLayout()
        load_button = QPushButton("载入保存预设...")
        load_button.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555; font-size: 10px;")
        reset_button = QPushButton("重置")
        reset_button.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555; font-size: 10px;")
        load_save_layout.addWidget(load_button)
        load_save_layout.addWidget(reset_button)
        singer_layout.addLayout(load_save_layout)
        
        # 语言设置组
        language_group = QGroupBox("语言")
        language_group.setStyleSheet("color: #ffffff; border: 1px solid #3e3e42; border-radius: 4px;")
        language_layout = QVBoxLayout(language_group)
        language_layout.setContentsMargins(5, 5, 5, 5)
        language_layout.setSpacing(5)
        
        # 使用以下语言歌唱下拉框
        language_layout.addWidget(QLabel("使用以下语言歌唱"))
        self.language_combo = QComboBox()
        self.language_combo.addItem("(未设定)")
        self.language_combo.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555;")
        language_layout.addWidget(self.language_combo)
        
        # 辅音使用松弛发音复选框
        consonant_checkbox = QCheckBox("辅音使用松弛发音")
        consonant_checkbox.setStyleSheet("color: #ffffff;")
        language_layout.addWidget(consonant_checkbox)
        
        # 声线设置组
        voice_group = QGroupBox("声线")
        voice_group.setStyleSheet("color: #ffffff; border: 1px solid #3e3e42; border-radius: 4px;")
        voice_layout = QVBoxLayout(voice_group)
        voice_layout.setContentsMargins(5, 5, 5, 5)
        voice_layout.setSpacing(5)
        
        # 预设下拉框
        voice_layout.addWidget(QLabel("预设"))
        self.voice_preset_combo = QComboBox()
        self.voice_preset_combo.addItem("(未设定)")
        self.voice_preset_combo.setStyleSheet("background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555;")
        voice_layout.addWidget(self.voice_preset_combo)
        
        # 参数设置组
        params_group = QGroupBox("参数")
        params_group.setStyleSheet("color: #ffffff; border: 1px solid #3e3e42; border-radius: 4px;")
        params_layout = QGridLayout(params_group)
        params_layout.setContentsMargins(5, 5, 5, 5)
        params_layout.setSpacing(5)
        
        # 响度参数
        params_layout.addWidget(QLabel("响度"), 0, 0)
        self.loudness_slider = QSlider(Qt.Orientation.Horizontal)
        self.loudness_slider.setRange(-24, 12)
        self.loudness_slider.setValue(0)
        self.loudness_slider.setStyleSheet("QSlider::groove:horizontal { background-color: #3c3c3c; } QSlider::handle:horizontal { background-color: #0e639c; }")
        params_layout.addWidget(self.loudness_slider, 0, 1)
        self.loudness_label = QLabel("0.00 dB")
        self.loudness_label.setStyleSheet("color: #cccccc;")
        params_layout.addWidget(self.loudness_label, 0, 2)
        
        # 张力参数
        params_layout.addWidget(QLabel("张力"), 1, 0)
        self.tension_slider = QSlider(Qt.Orientation.Horizontal)
        self.tension_slider.setRange(0, 100)
        self.tension_slider.setValue(0)
        self.tension_slider.setStyleSheet("QSlider::groove:horizontal { background-color: #3c3c3c; } QSlider::handle:horizontal { background-color: #0e639c; }")
        params_layout.addWidget(self.tension_slider, 1, 1)
        self.tension_label = QLabel("0.000")
        self.tension_label.setStyleSheet("color: #cccccc;")
        params_layout.addWidget(self.tension_label, 1, 2)
        
        # 气声参数
        params_layout.addWidget(QLabel("气声"), 2, 0)
        self.breathiness_slider = QSlider(Qt.Orientation.Horizontal)
        self.breathiness_slider.setRange(0, 100)
        self.breathiness_slider.setValue(0)
        self.breathiness_slider.setStyleSheet("QSlider::groove:horizontal { background-color: #3c3c3c; } QSlider::handle:horizontal { background-color: #0e639c; }")
        params_layout.addWidget(self.breathiness_slider, 2, 1)
        self.breathiness_label = QLabel("0.000")
        self.breathiness_label.setStyleSheet("color: #cccccc;")
        params_layout.addWidget(self.breathiness_label, 2, 2)
        
        # 添加到歌声标签页布局
        vocals_layout.addWidget(singer_group)
        vocals_layout.addWidget(language_group)
        vocals_layout.addWidget(voice_group)
        vocals_layout.addWidget(params_group)
        
        # 添加伸展项，使内容靠上
        vocals_layout.addStretch()
        
        # 添加标签页
        self.tab_widget.addTab(vocals_tab, "歌声")
        
        # 添加标签页控件到参数面板
        parameter_panel_layout.addWidget(self.tab_widget)
        
        # 将参数面板添加到主分割器
        self.main_splitter.addWidget(self.parameter_panel)
        
    def update_track_list(self):
        # 清空现有音轨列表
        for i in reversed(range(self.track_list_layout.count())):
            widget = self.track_list_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        # 添加音轨项
        for i, track in enumerate(self.tracks):
            track_item = TrackItem(i, track, self)
            self.track_list_layout.addWidget(track_item)
        
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开音频文件", "", "音频文件 (*.wav *.mp3 *.flac)"
        )
        
        if file_path:
            try:
                # 加载音频文件
                self.audio_data, self.sr = librosa.load(file_path, sr=None)
                
                # 将音频添加到当前轨道
                self.tracks[self.current_track]["data"] = self.audio_data
                
                # 更新音轨列表
                self.update_track_list()
                
            except Exception as e:
                print(f"加载音频文件失败: {e}")
                
    def add_track(self):
        track_number = len(self.tracks) + 1
        self.tracks.append({
            "name": f"未命名音轨", 
            "data": None, 
            "visible": True, 
            "muted": False, 
            "solo": False,
            "volume": 100,
            "singer": "默认歌手"
        })
        self.current_track = track_number - 1
        self.update_track_list()
        
    def change_track(self, index):
        self.current_track = index
        # 如果切换到已有音频的轨道，显示其波形
        if 0 <= index < len(self.tracks) and self.tracks[index]["data"] is not None:
            self.audio_data = self.tracks[index]["data"]
            
    def change_singer(self, singer_name):
        self.current_singer = singer_name
        
        # 检查是否为已加载的UTAU声库
        if singer_name in self.loaded_voicebanks:
            self.current_voicebank = self.loaded_voicebanks[singer_name]
            self.update_utau_singer_info(self.current_voicebank)
        else:
            # 否则使用默认的歌手信息
            self.update_singer_info()
        
    def update_singer_info(self):
        # 这里可以根据不同歌手显示不同的信息
        singer_info = {
            "默认歌手": "标准合成声音",
            "女高音": "明亮的高音女声",
            "男低音": "低沉的男声音色",
            "电音歌手": "具有电子效果的声音"
        }
        
        if self.current_singer in singer_info:
            self.singer_info_label.setText(singer_info[self.current_singer])
        
    def play_audio(self):
        """
        播放音频，使用UTAU声库生成音符对应的音频
        """
        try:
            import sounddevice as sd
            import numpy as np
            import threading
            import time
            
            # 如果是从暂停状态恢复，不需要重新生成音频
            if not self.is_paused:
                # 检查是否有加载的UTAU声库
                use_utau_voicebank = self.current_voicebank is not None
                
                # 生成音频数据
                if use_utau_voicebank:
                    # 使用UTAU声库生成音频
                    self.generate_audio_from_utau()
                else:
                    # 生成简单的示例音频
                    self.sample_rate = self.sr if self.sr else 44100  # 使用已加载的采样率或默认值
                    self.audio_data = np.sin(2 * np.pi * 440 * np.arange(self.sample_rate) / self.sample_rate)
            
            # 设置播放状态
            self.is_playing = True
            self.is_paused = False
            
            # 在单独的线程中播放音频，以允许UI响应
            def play_thread():
                try:
                    sample_rate = self.sr if self.sr else 44100  # 使用已加载的采样率或默认值
                    stream = sd.OutputStream(samplerate=sample_rate, channels=1, dtype='float32')
                    stream.start()
                    
                    # 播放音频数据
                    chunk_size = 1024
                    while self.is_playing and self.current_position < len(self.audio_data):
                        # 检查是否暂停
                        if self.is_paused:
                            # 暂停时等待一小段时间后再次检查
                            time.sleep(0.01)
                            continue
                        
                        chunk_end = min(self.current_position + chunk_size, len(self.audio_data))
                        stream.write(self.audio_data[self.current_position:chunk_end].astype(np.float32).tobytes())
                        self.current_position = chunk_end
                        # 更新播放指示器位置
                        self.playhead_position = self.current_position * self.piano_roll_widget.pixels_per_beat / sample_rate
                        self.piano_roll_widget.update()
                        
                        # 短暂休眠以减少CPU使用率
                        time.sleep(0.001)
                    
                    stream.stop()
                    stream.close()
                    
                    # 播放结束后重置状态
                    if self.is_playing:  # 如果播放完成而非被停止
                        self.is_playing = False
                        self.current_position = 0
                        self.playhead_position = 0
                        self.piano_roll_widget.update()
                    
                except Exception as e:
                    print(f"播放音频失败: {e}")
            
            # 启动播放线程
            self.playback_thread = threading.Thread(target=play_thread)
            self.playback_thread.daemon = True
            self.playback_thread.start()
            
        except Exception as e:
            print(f"播放音频失败: {e}")
            
    def generate_audio_from_utau(self):
        """
        使用UTAU声库和钢琴卷帘中的音符生成音频
        """
        import numpy as np
        
        # 检查是否有音符和UTAU声库
        if not hasattr(self, 'piano_roll_widget') or not self.piano_roll_widget.notes or not self.current_voicebank:
            print("没有音符或UTAU声库可用于生成音频")
            self.sample_rate = self.sr if self.sr else 44100  # 使用已加载的采样率或默认值
            self.audio_data = np.zeros(self.sample_rate)  # 生成静默
            return
        
        # 获取UTAU声库信息
        voicebank = self.current_voicebank
        
        # 估算总时长（以样本数计）
        max_note_end = max(note['time'] + note['duration'] for note in self.piano_roll_widget.notes)
        total_duration_seconds = max_note_end * 0.25 / self.piano_roll_widget.pixels_per_beat  # 假设每个像素代表一定的时间
        self.sample_rate = self.sr if self.sr else 44100  # 使用已加载的采样率或默认值
        total_samples = int(total_duration_seconds * self.sample_rate) + self.sample_rate  # 添加一点额外时间
        
        # 创建音频数据数组
        self.audio_data = np.zeros(total_samples)
        
        # 为每个音符生成音频
        for note in self.piano_roll_widget.notes:
            pitch = note['pitch']
            start_time = note['time'] * 0.25 / self.piano_roll_widget.pixels_per_beat  # 转换为秒
            duration = note['duration'] * 0.25 / self.piano_roll_widget.pixels_per_beat  # 转换为秒
            
            # 计算起始和结束样本索引
            start_sample = int(start_time * self.sample_rate)
            end_sample = min(start_sample + int(duration * self.sample_rate), total_samples)
            
            # 如果没有足够的空间，跳过此音符
            if start_sample >= total_samples:
                continue
            
            # 生成音符音频
            note_audio = self.generate_note_audio(pitch, duration)
            
            # 将音符音频添加到总音频中
            note_samples = len(note_audio)
            available_space = total_samples - start_sample
            copy_length = min(note_samples, available_space)
            
            # 淡入淡出以避免爆音
            fade_samples = int(0.01 * self.sample_rate)  # 10ms淡入淡出
            fade_in = np.linspace(0, 1, min(fade_samples, copy_length))
            fade_out = np.linspace(1, 0, min(fade_samples, copy_length))
            
            # 应用淡入淡出
            if copy_length > fade_samples:
                note_audio[:fade_samples] *= fade_in
                note_audio[-fade_samples:] *= fade_out
            else:
                # 如果音符太短，只应用一个淡入淡出
                fade = np.linspace(0, 1, copy_length) * np.linspace(1, 0, copy_length)
                note_audio *= fade
            
            # 添加到主音频
            self.audio_data[start_sample:start_sample+copy_length] += note_audio[:copy_length] * 0.5  # 衰减以避免削波
        
        # 归一化音频
        max_amplitude = np.max(np.abs(self.audio_data))
        if max_amplitude > 0:
            self.audio_data = self.audio_data / max_amplitude
        
    def generate_note_audio(self, pitch, duration):
        """
        生成指定音高和时长的音符音频，优先使用UTAU声库的采样文件
        
        参数:
            pitch: MIDI音高值
            duration: 音符时长（秒）
        """
        import numpy as np
        import librosa
        import soundfile as sf
        
        # 设置采样率
        self.sample_rate = self.sr if self.sr else 44100
        target_samples = int(duration * self.sample_rate)
        
        # 尝试使用UTAU声库的采样文件
        if self.current_voicebank and hasattr(self, 'utau_loader'):
            try:
                # 查找最匹配当前音高的采样文件
                sample_file = self.utau_loader.find_best_sample_for_pitch(self.current_voicebank, pitch)
                
                if sample_file and os.path.exists(sample_file):
                    # 加载采样文件
                    audio, sr = librosa.load(sample_file, sr=self.sample_rate, mono=True)
                    
                    # 计算目标频率
                    target_freq = 440.0 * (2.0 ** ((pitch - 69) / 12.0))
                    
                    # 估计采样的基频
                    # 简化实现：尝试从文件名估计频率
                    sample_name = os.path.basename(sample_file)
                    sample_freq = 0.0
                    
                    # 查找oto配置中对应的条目
                    for section, configs in self.current_voicebank.get('oto_configs', {}).items():
                        for config in configs:
                            if config['wav_file'] == sample_name or sample_name.endswith(config['wav_file']):
                                sample_freq = self.utau_loader._estimate_frequency_from_sample_name(config['alias'])
                                break
                        if sample_freq > 0:
                            break
                    
                    # 如果无法从文件名估计，使用简单的音高转换
                    if sample_freq > 0:
                        # 计算音高转换因子
                        pitch_factor = target_freq / sample_freq
                        # 进行音高转换
                        audio = librosa.effects.pitch_shift(audio, sr=self.sample_rate, n_steps=12 * np.log2(pitch_factor))
                    
                    # 调整时长
                    if len(audio) > target_samples:
                        # 如果采样太长，截断
                        audio = audio[:target_samples]
                    elif len(audio) < target_samples:
                        # 如果采样太短，循环或填充
                        # 这里使用简单的填充
                        padding = np.zeros(target_samples - len(audio))
                        audio = np.concatenate((audio, padding))
                    
                    # 添加包络
                    envelope = self.generate_envelope(len(audio), attack=0.01, decay=0.1, sustain=0.7, release=0.2)
                    audio *= envelope
                    
                    return audio
            except Exception as e:
                print(f"使用UTAU采样生成音符时出错: {e}")
        
        # 如果无法使用UTAU声库或出错，回退到正弦波
        t = np.linspace(0, duration, target_samples, False)
        frequency = 440.0 * (2.0 ** ((pitch - 69) / 12.0))
        audio = np.sin(2 * np.pi * frequency * t)
        
        # 添加包络
        envelope = self.generate_envelope(target_samples, attack=0.01, decay=0.1, sustain=0.7, release=0.2)
        audio *= envelope
        
        return audio
        
    def generate_envelope(self, length, attack=0.01, decay=0.1, sustain=0.7, release=0.2):
        """
        生成ADSR包络
        """
        import numpy as np
        
        self.sample_rate = self.sr if self.sr else 44100  # 使用已加载的采样率或默认值
        attack_samples = int(attack * self.sample_rate)
        decay_samples = int(decay * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        sustain_samples = length - attack_samples - decay_samples - release_samples
        
        if sustain_samples < 0:
            # 如果总时长太短，按比例缩小各阶段
            total_needed = attack_samples + decay_samples + release_samples
            scale = length / total_needed
            attack_samples = int(attack_samples * scale)
            decay_samples = int(decay_samples * scale)
            release_samples = length - attack_samples - decay_samples
            sustain_samples = 0
        
        envelope = np.zeros(length)
        
        # 攻击阶段
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # 衰减阶段
        envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, sustain, decay_samples)
        
        # 持续阶段
        envelope[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] = sustain
        
        # 释放阶段
        envelope[attack_samples+decay_samples+sustain_samples:] = np.linspace(sustain, 0, release_samples)
        
        return envelope
                
    def pause_audio(self):
        """
        暂停音频播放
        """
        self.is_paused = True
        # 不要设置is_playing=False，这样才能从暂停状态恢复
        print("音频已暂停")
        
    def stop_audio(self):
        """
        停止音频播放
        """
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0
        self.playhead_position = 0
        # 更新播放指示器
        self.piano_roll_widget.update()
        print("音频已停止")
        
    def rewind_audio(self):
        """
        倒带
        """
        self.current_position = max(0, self.current_position - self.sample_rate // 2)  # 倒回半秒
        self.playhead_position = self.current_position * self.piano_roll_widget.pixels_per_beat / self.sample_rate
        self.piano_roll_widget.update()
        print(f"倒带到位置: {self.current_position}")
        
    def fast_forward_audio(self):
        """
        快进
        """
        if self.audio_data is not None:
            self.current_position = min(len(self.audio_data) - 1, self.current_position + self.sample_rate // 2)  # 快进半秒
            self.playhead_position = self.current_position * self.piano_roll_widget.pixels_per_beat / self.sample_rate
            self.piano_roll_widget.update()
            print(f"快进到位置: {self.current_position}")
        
    def save_project(self):
        # 保存项目功能暂未实现
        print("保存项目功能暂未实现")
        
    def load_utau_voicebank(self):
        """
        加载UTAU声库
        """
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(
            self, "选择UTAU声库文件夹", "", QFileDialog.Option.ShowDirsOnly
        )
        
        if folder_path:
            # 使用UTAU加载器加载声库
            voicebank_info = self.utau_loader.load_voicebank(folder_path)
            
            if voicebank_info and voicebank_info['valid']:
                # 将加载的声库添加到已加载列表
                voicebank_name = voicebank_info['name']
                self.loaded_voicebanks[voicebank_name] = voicebank_info
                self.current_voicebank = voicebank_info
                
                # 更新歌手下拉框
                if voicebank_name not in [self.singer_combo.itemText(i) for i in range(self.singer_combo.count())]:
                    # 移除"(未设定)"项（如果存在）
                    if self.singer_combo.findText("(未设定)") >= 0:
                        self.singer_combo.removeItem(self.singer_combo.findText("(未设定)"))
                    
                    self.singer_combo.addItem(voicebank_name)
                    self.singer_combo.setCurrentText(voicebank_name)
                else:
                    self.singer_combo.setCurrentText(voicebank_name)
                
                # 更新声库版本下拉框
                self.singer_version_combo.clear()
                self.singer_version_combo.addItem("默认版本")
                self.singer_version_combo.setCurrentIndex(0)
                
                # 更新声库信息显示
                self.update_utau_singer_info(voicebank_info)
                
                # 显示成功消息
                QMessageBox.information(self, "加载成功", f"成功加载UTAU声库: {voicebank_name}")
            else:
                # 显示错误消息
                QMessageBox.warning(self, "加载失败", "无法加载所选文件夹作为UTAU声库。请确保选择的是有效的UTAU声库文件夹。")
    
    def update_utau_singer_info(self, voicebank_info):
        """
        更新UTAU声库信息显示
        
        参数:
            voicebank_info: 声库信息字典
        """
        # 构建声库信息文本
        info_text = f"声库名称: {voicebank_info['name']}\n"
        
        # 添加角色信息
        if 'character_info' in voicebank_info and voicebank_info['character_info']:
            for key, value in voicebank_info['character_info'].items():
                info_text += f"{key}: {value}\n"
        
        # 添加采样文件和配置信息
        info_text += f"\n采样文件数量: {len(voicebank_info['sample_files'])}\n"
        
        if 'oto_configs' in voicebank_info and voicebank_info['oto_configs']:
            config_count = 0
            for section, configs in voicebank_info['oto_configs'].items():
                config_count += len(configs)
            info_text += f"Oto配置条目数: {config_count}\n"
            
            # 添加oto配置的部分信息
            for section, configs in voicebank_info['oto_configs'].items():
                info_text += f"\n{section}部分配置示例:\n"
                # 只显示前5个配置作为示例
                for i, config in enumerate(configs[:5]):
                    info_text += f"  {config['alias']} ({config['wav_file']})\n"
                if len(configs) > 5:
                    info_text += f"  ... 还有{len(configs) - 5}个配置\n"
        
        # 更新标签文本
        self.singer_info_label.setText(info_text)

class TrackItem(QWidget):
    def __init__(self, index, track_data, parent):
        super().__init__()
        self.index = index
        self.track_data = track_data
        self.parent = parent
        
        self.setStyleSheet("background-color: #2d2d2d; border: 1px solid #3e3e42;")
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(2)
        
        # 音轨名称和控制按钮
        name_layout = QHBoxLayout()
        
        # 音轨图标
        self.track_icon = QPushButton("🎤")
        self.track_icon.setMaximumWidth(20)
        self.track_icon.setStyleSheet(
            "QPushButton { background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555; padding: 2px; font-size: 10px; }")
        name_layout.addWidget(self.track_icon)
        
        # 音轨名称
        self.name_label = QLabel(track_data["name"])
        self.name_label.setStyleSheet("color: #ffffff;")
        self.name_label.setMinimumWidth(60)
        name_layout.addWidget(self.name_label)
        
        # 选择按钮
        self.select_button = QPushButton("▶")
        self.select_button.setCheckable(True)
        self.select_button.setChecked(index == parent.current_track)
        self.select_button.setMaximumWidth(20)
        self.select_button.setStyleSheet(
            "QPushButton { background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555; padding: 2px; font-size: 10px; }"
            "QPushButton:checked { background-color: #0e639c; }")
        self.select_button.clicked.connect(self.on_select)
        name_layout.addWidget(self.select_button)
        
        # 静音按钮
        self.mute_button = QPushButton("M")
        self.mute_button.setCheckable(True)
        self.mute_button.setChecked(track_data["muted"])
        self.mute_button.setMaximumWidth(20)
        self.mute_button.setStyleSheet(
            "QPushButton { background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555; padding: 2px; font-size: 10px; }"
            "QPushButton:checked { background-color: #5a5a5a; color: #ff4444; }")
        self.mute_button.clicked.connect(self.on_mute)
        name_layout.addWidget(self.mute_button)
        
        # 独奏按钮
        self.solo_button = QPushButton("S")
        self.solo_button.setCheckable(True)
        self.solo_button.setChecked(track_data["solo"])
        self.solo_button.setMaximumWidth(20)
        self.solo_button.setStyleSheet(
            "QPushButton { background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555; padding: 2px; font-size: 10px; }"
            "QPushButton:checked { background-color: #5a5a5a; color: #ffff44; }")
        self.solo_button.clicked.connect(self.on_solo)
        name_layout.addWidget(self.solo_button)
        
        layout.addLayout(name_layout)
        
    def on_select(self):
        # 更新父窗口的当前轨道
        self.parent.change_track(self.index)
        # 更新所有轨道的选中状态
        for i in range(self.parent.track_list_layout.count()):
            track_item = self.parent.track_list_layout.itemAt(i).widget()
            if track_item is not None:
                track_item.select_button.setChecked(i == self.index)
        
    def on_mute(self):
        self.track_data["muted"] = self.mute_button.isChecked()
        
    def on_solo(self):
        self.track_data["solo"] = self.solo_button.isChecked()

class PianoRollWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1e1e1e;")
        self.notes = []
        self.is_dragging = False
        self.current_note = None
        self.note_height = 16
        self.note_width = 40
        self.pixels_per_beat = 60
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制钢琴卷帘背景
        painter.fillRect(self.rect(), QColor(30, 30, 30))
        
        # 绘制网格线
        self.draw_grid(painter)
        
        # 绘制播放指示器
        self.draw_playhead(painter)
        
        # 绘制音符
        self.draw_notes(painter)
        
    def draw_grid(self, painter):
        # 绘制垂直网格线（小节线）
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        
        width = self.width()
        height = self.height()
        
        # 绘制时间刻度
        for x in range(0, width, self.pixels_per_beat):
            # 每隔4个拍子绘制一条粗一点的线（小节线）
            if x % (self.pixels_per_beat * 4) == 0:
                painter.setPen(QPen(QColor(80, 80, 80), 1.5))
                # 绘制小节标记
                painter.setFont(QFont("Arial", 8))
                painter.setPen(QPen(QColor(150, 150, 150), 1))
                bar_num = x // (self.pixels_per_beat * 4) + 1
                painter.drawText(x + 2, 12, str(bar_num))
                painter.setPen(QPen(QColor(80, 80, 80), 1.5))
            else:
                painter.setPen(QPen(QColor(60, 60, 60), 1))
            painter.drawLine(x, 0, x, height)
        
        # 绘制水平网格线（音高线）
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        for y in range(0, height, self.note_height):
            painter.drawLine(0, y, width, y)
        
        # 绘制音符标签
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        painter.setFont(QFont("Arial", 8))
        
        # 音符名称
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        for i in range(0, height, self.note_height * 12):
            for j in range(12):
                y = i + j * self.note_height
                if y < height:
                    # 只在左侧显示音符名称
                    note_name = note_names[j] + str(8 - (i // (self.note_height * 12)))
                    painter.drawText(5, y + 12, note_name)
        
    def draw_playhead(self, painter):
        # 绘制播放指示器
        parent = self.parent().parent()  # 获取SingingVoiceSynthesizer主窗口
        if hasattr(parent, 'playhead_position'):
            playhead_x = parent.playhead_position
            # 绘制播放头垂直线
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(int(playhead_x), 0, int(playhead_x), self.height())
            # 绘制播放头三角形
            triangle_points = [
                QPoint(int(playhead_x), 0),
                QPoint(int(playhead_x - 5), 10),
                QPoint(int(playhead_x + 5), 10)
            ]
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            painter.drawPolygon(triangle_points)
    
    def draw_notes(self, painter):
        # 绘制音符
        for note in self.notes:
            # 绘制音符主体
            painter.fillRect(note['rect'], QColor(14, 99, 156, 200))
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.drawRect(note['rect'])
            
            # 在音符上显示音高信息，使用较小的字体避免重叠
            note_name = self.get_note_name_from_pitch(note['pitch'])
            font = painter.font()
            font.setPointSize(7)  # 减小字体大小
            painter.setFont(font)
            painter.drawText(note['rect'], Qt.AlignmentFlag.AlignCenter, note_name)
        
    def get_note_name_from_pitch(self, pitch):
        # 根据音高值获取音符名称
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = pitch // 12 - 1
        note_index = pitch % 12
        return note_names[note_index] + str(octave)
        
    def mousePressEvent(self, event):
        # 鼠标按下事件，创建新音符或选择已有音符
        if event.button() == Qt.MouseButton.LeftButton:
            # 检查是否点击了现有音符
            for note in reversed(self.notes):
                if note['rect'].contains(event.pos()):
                    self.is_dragging = True
                    self.current_note = note
                    return
            
            # 创建新音符
            x = event.pos().x()
            y = event.pos().y()
            
            # 对齐到网格
            x = (x // self.pixels_per_beat) * self.pixels_per_beat
            y = (y // self.note_height) * self.note_height
            
            # 确保在可绘制区域内
            if y < self.height():
                new_note = {
                    'rect': QRect(x, y, self.note_width, self.note_height),
                    'pitch': self.get_pitch_from_position(y),
                    'time': x,
                    'duration': self.note_width
                }
                self.notes.append(new_note)
                self.update()
        
    def mouseMoveEvent(self, event):
        # 鼠标移动事件，拖动音符
        if self.is_dragging and self.current_note is not None:
            # 对齐到网格
            target_x = (event.pos().x() // self.pixels_per_beat) * self.pixels_per_beat
            target_y = (event.pos().y() // self.note_height) * self.note_height
            
            # 确保在可绘制区域内
            if target_y >= 0 and target_y < self.height():
                # 计算偏移量
                dx = target_x - self.current_note['rect'].x()
                dy = target_y - self.current_note['rect'].y()
                
                self.current_note['rect'].translate(dx, dy)
                self.current_note['time'] = target_x
                
                self.update()
        
    def mouseReleaseEvent(self, event):
        # 鼠标释放事件，结束拖动
        self.is_dragging = False
        self.current_note = None
        
    def get_pitch_from_position(self, y):
        # 根据Y坐标计算音高 (MIDI 音高 0-127)
        return 127 - int(y / self.height() * 127)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 设置应用程序样式
    app.setStyle("Fusion")
    window = SingingVoiceSynthesizer()
    window.show()
    sys.exit(app.exec())