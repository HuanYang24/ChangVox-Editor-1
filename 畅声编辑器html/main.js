// 畅声编辑器主逻辑文件

class VoiceEditor {
    constructor() {
        // 初始化编辑器状态
        this.project = {
            tracks: [],
            currentTrack: null,
            bpm: 120,
            timeSignature: '4/4',
            voiceBank: null
        };
        
        // 初始化UI元素引用
        this.ui = {
            pianoRoll: null,
            pianoKeys: null,
            timeline: null,
            transportControls: {
                play: null,
                pause: null,
                stop: null,
                prev: null,
                next: null
            },
            sliders: [],
            voiceBankSelector: null,
            loadVoiceBankButton: null,
            timeDisplay: null,
            bpmInput: null,
            timeSignatureSelect: null
        };
        
        // 当前选中的音符
        this.selectedNote = null;
        
        // 示例数据（将在DOM加载完成后初始化）
        this.sampleData = null;
        
        // 初始化编辑器
        this.init();
    }
    
    // 初始化编辑器
    init() {
        this.initUIReferences();
        this.initEventListeners();
        this.createDefaultTrack();
        this.renderPianoKeys();
        
        // 等待示例数据加载完成
        setTimeout(() => {
            this.loadSampleData();
            this.loadSampleProject();
        }, 100);
    }
    
    // 获取UI元素引用
    initUIReferences() {
        this.ui.pianoRoll = document.querySelector('.piano-roll');
        this.ui.pianoKeys = document.querySelector('.piano-keys');
        this.ui.timeline = document.querySelector('.timeline');
        this.ui.transportControls.play = document.querySelector('.transport-btn.play');
        this.ui.transportControls.pause = document.querySelector('.transport-btn:nth-child(3)');
        this.ui.transportControls.stop = document.querySelector('.transport-btn:nth-child(4)');
        this.ui.transportControls.prev = document.querySelector('.transport-btn:nth-child(1)');
        this.ui.transportControls.next = document.querySelector('.transport-btn:nth-child(5)');
        this.ui.sliders = document.querySelectorAll('.slider');
        this.ui.voiceBankSelector = document.querySelector('select');
        this.ui.loadVoiceBankButton = document.querySelector('.button:not(.secondary)');
        this.ui.timeDisplay = document.querySelector('.time-display');
        this.ui.bpmInput = document.querySelector('input[type="number"]');
        this.ui.timeSignatureSelect = document.querySelector('select[style*="width: 80px"]');
    }
    
    // 初始化事件监听器
    initEventListeners() {
        // 播放控制
        this.ui.transportControls.play.addEventListener('click', () => this.play());
        this.ui.transportControls.pause.addEventListener('click', () => this.pause());
        this.ui.transportControls.stop.addEventListener('click', () => this.stop());
        
        // 参数控制
        this.ui.sliders.forEach(slider => {
            slider.addEventListener('input', (e) => this.updateParameter(slider, e.target.value));
        });
        
        // 加载声库
        this.ui.loadVoiceBankButton.addEventListener('click', () => this.loadVoiceBank());
        
        // 钢琴卷帘交互
        this.ui.pianoRoll.addEventListener('mousedown', (e) => this.startCreatingNote(e));
        
        // BPM和拍号变化
        this.ui.bpmInput.addEventListener('change', (e) => this.changeBPM(parseInt(e.target.value)));
        
        this.ui.timeSignatureSelect.addEventListener('change', (e) => this.changeTimeSignature(e.target.value));
        
        // 右键菜单支持
        this.ui.pianoRoll.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            // 在实际项目中这里会显示右键菜单
        });
        
        // 键盘快捷键
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
    }
    
    // 创建默认音轨
    createDefaultTrack() {
        const track = {
            id: Date.now(),
            name: '未命名音轨',
            notes: [],
            parameters: {
                volume: 0,
                tension: 0,
                breathiness: 0
            }
        };
        
        this.project.tracks.push(track);
        this.project.currentTrack = track;
    }
    
    // 渲染钢琴键盘
    renderPianoKeys() {
        // 清空现有键盘
        this.ui.pianoKeys.innerHTML = '';
        
        // 创建从C4到C5的音符键
        const notes = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5'];
        
        notes.forEach(note => {
            const key = document.createElement('div');
            key.className = 'key';
            key.textContent = note;
            key.dataset.note = note;
            this.ui.pianoKeys.appendChild(key);
        });
    }
    
    // 开始创建音符
    startCreatingNote(event) {
        // 确保点击的是钢琴卷帘区域而不是钢琴键
        if (event.target === this.ui.pianoRoll || event.target === this.ui.timeline) {
            const rect = this.ui.pianoRoll.getBoundingClientRect();
            const x = event.clientX - rect.left - 50; // 减去钢琴键宽度
            const y = event.clientY - rect.top;
            
            // 计算音符位置和音高
            const startTime = this.calculateTimeFromX(x);
            const notePitch = this.calculatePitchFromY(y);
            
            if (notePitch) {
                // 创建临时音符
                this.createNote(startTime, 1, notePitch);
                
                // 添加鼠标移动和释放事件监听
                let isDragging = true;
                
                const mouseMoveHandler = (e) => {
                    if (isDragging) {
                        const moveX = e.clientX - rect.left - 50 - x;
                        const duration = Math.max(0.25, this.calculateTimeFromX(x + moveX) - startTime);
                        
                        // 更新最后创建的音符的时长
                        if (this.project.currentTrack.notes.length > 0) {
                            const lastNote = this.project.currentTrack.notes[this.project.currentTrack.notes.length - 1];
                            lastNote.duration = duration;
                            this.updateNoteElement(lastNote);
                        }
                    }
                };
                
                const mouseUpHandler = () => {
                    isDragging = false;
                    document.removeEventListener('mousemove', mouseMoveHandler);
                    document.removeEventListener('mouseup', mouseUpHandler);
                };
                
                document.addEventListener('mousemove', mouseMoveHandler);
                document.addEventListener('mouseup', mouseUpHandler);
            }
        }
    }
    
    // 创建音符
    createNote(startTime, duration, pitch) {
        const note = {
            id: Date.now(),
            startTime,
            duration,
            pitch,
            lyric: 'あ', // 默认音节
            parameters: {
                volume: 0,
                tension: 0,
                breathiness: 0
            }
        };
        
        this.project.currentTrack.notes.push(note);
        this.renderNote(note);
        
        // 在实际项目中，这里会通知后端进行音符合成
        this.synthesizeNote(note);
    }
    
    // 渲染音符到钢琴卷帘
    renderNote(note) {
        const noteElement = document.createElement('div');
        noteElement.className = 'note-block';
        noteElement.dataset.noteId = note.id;
        
        // 计算音符位置和大小
        const x = this.calculateXFromTime(note.startTime);
        const width = this.calculateXFromTime(note.duration);
        const y = this.calculateYFromPitch(note.pitch);
        const height = 24; // 音符高度
        
        // 设置音符样式
        noteElement.style.left = x + 'px';
        noteElement.style.top = y + 'px';
        noteElement.style.width = width + 'px';
        noteElement.style.height = height + 'px';
        noteElement.style.zIndex = 10;
        
        // 添加歌词显示
        if (note.lyric) {
            const lyricSpan = document.createElement('span');
            lyricSpan.textContent = note.lyric;
            lyricSpan.style.fontSize = '11px';
            lyricSpan.style.color = 'white';
            lyricSpan.style.display = 'block';
            lyricSpan.style.textAlign = 'center';
            lyricSpan.style.lineHeight = height + 'px';
            noteElement.appendChild(lyricSpan);
        }
        
        // 添加音符到钢琴卷帘
        this.ui.pianoRoll.appendChild(noteElement);
        
        // 添加音符交互
        noteElement.addEventListener('mousedown', (e) => {
            e.stopPropagation();
            this.selectNote(note.id);
        });
    }
    
    // 加载示例数据
    loadSampleData() {
        try {
            // 尝试获取全局的SampleData对象
            this.sampleData = window.SampleData || null;
            
            if (this.sampleData) {
                // 更新声库下拉列表
                const voiceBanks = this.sampleData.getAllVoiceBanks();
                const voiceBankSelects = document.querySelectorAll('select');
                
                voiceBankSelects.forEach(select => {
                    if (select.options[0].textContent.includes('未选择') || 
                        select.options[0].textContent.includes('未设定') ||
                        select.options[0].textContent.includes('N/A')) {
                        select.innerHTML = '';
                        voiceBanks.forEach(bank => {
                            const option = document.createElement('option');
                            option.value = bank.id;
                            option.textContent = bank.name;
                            select.appendChild(option);
                        });
                    }
                });
            }
        } catch (e) {
            console.error('加载示例数据时出错:', e);
        }
    }
    
    // 加载示例项目
    loadSampleProject() {
        if (this.sampleData) {
            try {
                const sampleProject = this.sampleData.getSampleProject();
                
                if (sampleProject) {
                    // 清空当前项目
                    this.project.tracks = [];
                    this.project.bpm = sampleProject.bpm;
                    this.project.timeSignature = sampleProject.timeSignature;
                    
                    // 更新UI
                    this.ui.bpmInput.value = sampleProject.bpm;
                    this.ui.timeSignatureSelect.value = sampleProject.timeSignature;
                    
                    // 加载音轨和音符
                    sampleProject.tracks.forEach(track => {
                        const newTrack = {
                            id: track.id,
                            name: track.name,
                            notes: [...track.notes],
                            parameters: track.parameters || {
                                volume: 0,
                                tension: 0,
                                breathiness: 0
                            }
                        };
                        
                        this.project.tracks.push(newTrack);
                        
                        // 如果是第一个音轨，设为当前音轨
                        if (!this.project.currentTrack) {
                            this.project.currentTrack = newTrack;
                        }
                        
                        // 渲染音符
                        newTrack.notes.forEach(note => {
                            this.renderNote(note);
                        });
                    });
                }
            } catch (e) {
                console.error('加载示例项目时出错:', e);
            }
        }
    }
    
    // 处理键盘快捷键
    handleKeyPress(e) {
        // 在实际项目中这里会实现各种键盘快捷键
        switch (e.key.toLowerCase()) {
            case 'delete':
                if (this.selectedNote) {
                    this.deleteNote(this.selectedNote);
                }
                break;
            // 可以添加更多快捷键
        }
    }
    
    // 删除音符
    deleteNote(noteId) {
        if (this.project.currentTrack) {
            const noteIndex = this.project.currentTrack.notes.findIndex(note => note.id === noteId);
            
            if (noteIndex !== -1) {
                // 从数据中删除
                this.project.currentTrack.notes.splice(noteIndex, 1);
                
                // 从UI中删除
                const noteElement = document.querySelector(`.note-block[data-note-id="${noteId}"]`);
                if (noteElement) {
                    noteElement.remove();
                }
                
                // 清除选中状态
                this.selectedNote = null;
            }
        }
    }
    
    // 更新音符元素
    updateNoteElement(note) {
        const noteElement = document.querySelector(`.note-block[data-note-id="${note.id}"]`);
        if (noteElement) {
            const x = this.calculateXFromTime(note.startTime);
            const width = this.calculateXFromTime(note.duration);
            const y = this.calculateYFromPitch(note.pitch);
            
            noteElement.style.left = x + 'px';
            noteElement.style.top = y + 'px';
            noteElement.style.width = width + 'px';
        }
    }
    
    // 选择音符
    selectNote(noteId) {
        // 在实际项目中，这里会高亮选中的音符并显示其属性
        console.log('选中音符:', noteId);
    }
    
    // 从X坐标计算时间
    calculateTimeFromX(x) {
        // 简化版：假设每个四分音符对应40像素
        const pixelsPerQuarterNote = 40;
        return (x / pixelsPerQuarterNote) * (60 / this.project.bpm);
    }
    
    // 从时间计算X坐标
    calculateXFromTime(time) {
        // 简化版：假设每个四分音符对应40像素
        const pixelsPerQuarterNote = 40;
        return (time * this.project.bpm / 60) * pixelsPerQuarterNote;
    }
    
    // 从Y坐标计算音高
    calculatePitchFromY(y) {
        const rect = this.ui.pianoKeys.getBoundingClientRect();
        const pianoRollRect = this.ui.pianoRoll.getBoundingClientRect();
        const relativeY = (y + pianoRollRect.top) / rect.height;
        const keys = Array.from(this.ui.pianoKeys.children);
        const keyIndex = Math.floor((1 - relativeY) * keys.length);
        
        if (keyIndex >= 0 && keyIndex < keys.length) {
            return keys[keyIndex].dataset.note;
        }
        
        return null;
    }
    
    // 从音高计算Y坐标
    calculateYFromPitch(pitch) {
        const keys = Array.from(this.ui.pianoKeys.children);
        const keyIndex = keys.findIndex(key => key.dataset.note === pitch);
        
        if (keyIndex !== -1) {
            const rect = this.ui.pianoKeys.getBoundingClientRect();
            const keyHeight = rect.height / keys.length;
            // 确保音符在钢琴键的中间位置
            return keyIndex * keyHeight + keyHeight / 2 - 12; // 12是音符高度的一半
        }
        
        return 0;
    }
    
    // 更新参数
    updateParameter(slider, value) {
        // 在实际项目中，这里会更新对应的声音参数并通知后端
        const label = slider.previousElementSibling;
        if (label && label.classList.contains('control-label')) {
            const paramName = label.textContent.split(':')[0].trim();
            label.textContent = `${paramName}: ${parseFloat(value).toFixed(3)}`;
        }
        
        // 更新当前音轨的参数
        if (this.project.currentTrack) {
            // 根据滑块位置确定参数类型
            const sliderIndex = Array.from(this.ui.sliders).indexOf(slider);
            switch (sliderIndex) {
                case 0:
                    this.project.currentTrack.parameters.volume = parseFloat(value);
                    break;
                case 1:
                    this.project.currentTrack.parameters.tension = parseFloat(value);
                    break;
                case 2:
                    this.project.currentTrack.parameters.breathiness = parseFloat(value);
                    break;
            }
        }
    }
    
    // 加载声库
    loadVoiceBank() {
        // 在实际项目中，这里会打开文件选择器让用户选择UTAU声库文件
        alert('加载声库功能将在完整版本中实现');
        
        // 模拟加载声库
        this.project.voiceBank = {
            name: '示例声库',
            version: '1.0',
            samples: []
        };
        
        // 更新UI
        const voiceBankSelects = document.querySelectorAll('select');
        voiceBankSelects.forEach(select => {
            if (select.options[0].textContent.includes('未选择') || select.options[0].textContent.includes('未设定')) {
                select.innerHTML = '<option>示例声库</option>';
            }
        });
    }
    
    // 播放
    play() {
        // 在实际项目中，这里会触发后端进行实时合成和播放
        alert('播放功能将在完整版本中实现');
    }
    
    // 暂停
    pause() {
        // 在实际项目中，这里会暂停播放
        alert('暂停功能将在完整版本中实现');
    }
    
    // 停止
    stop() {
        // 在实际项目中，这里会停止播放并重置播放头
        alert('停止功能将在完整版本中实现');
    }
    
    // 改变BPM
    changeBPM(bpm) {
        this.project.bpm = bpm;
        // 在实际项目中，这里会更新时间线显示和影响播放速度
    }
    
    // 改变拍号
    changeTimeSignature(signature) {
        this.project.timeSignature = signature;
        // 在实际项目中，这里会更新时间线的小节显示
    }
    
    // 合成音符（模拟与C++后端的交互）
    synthesizeNote(note) {
        // 在实际项目中，这里会通过WebAssembly或本地服务器与C++后端通信
        console.log('请求合成音符:', note);
    }
}

// 当页面加载完成后初始化编辑器
document.addEventListener('DOMContentLoaded', function() {
    const editor = new VoiceEditor();
    
    // 暴露编辑器实例给全局，便于调试
    window.voiceEditor = editor;
});