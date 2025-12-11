// 畅声编辑器 - 示例数据

const SampleData = {
    // 示例声库数据
    voiceBanks: [
        {
            id: 1,
            name: '示例女声',
            version: '1.0.0',
            description: '一个示例女声虚拟歌手声库',
            language: '中文'
        },
        {
            id: 2,
            name: '示例男声',
            version: '1.0.0',
            description: '一个示例男声虚拟歌手声库',
            language: '中文'
        }
    ],
    
    // 示例项目数据
    projects: [
        {
            id: 1,
            name: '示例项目1',
            tracks: [
                {
                    id: 101,
                    name: '主音轨',
                    voiceBankId: 1,
                    notes: [
                        {
                            id: 1001,
                            pitch: 'C4',
                            startTime: 0, 
                            duration: 1,
                            lyric: '你',
                            parameters: {
                                volume: 0,
                                tension: 0.3,
                                breathiness: 0.1
                            }
                        },
                        {
                            id: 1002,
                            pitch: 'D4',
                            startTime: 1,
                            duration: 1,
                            lyric: '好',
                            parameters: {
                                volume: 0,
                                tension: 0.2,
                                breathiness: 0.15
                            }
                        },
                        {
                            id: 1003,
                            pitch: 'E4',
                            startTime: 2,
                            duration: 2,
                            lyric: '世',
                            parameters: {
                                volume: 0,
                                tension: 0.4,
                                breathiness: 0.1
                            }
                        },
                        {
                            id: 1004,
                            pitch: 'C4',
                            startTime: 4,
                            duration: 2,
                            lyric: '界',
                            parameters: {
                                volume: 0,
                                tension: 0.5,
                                breathiness: 0.2
                            }
                        }
                    ]
                }
            ],
            bpm: 120,
            timeSignature: '4/4'
        }
    ],
    
    // 示例预设参数
    presets: [
        {
            id: 1,
            name: '清澈',
            parameters: {
                volume: 0,
                tension: 0.2,
                breathiness: 0.1
            }
        },
        {
            id: 2,
            name: '有力',
            parameters: {
                volume: 3,
                tension: 0.6,
                breathiness: 0.05
            }
        },
        {
            id: 3,
            name: '温柔',
            parameters: {
                volume: -2,
                tension: 0.1,
                breathiness: 0.3
            }
        }
    ],
    
    // 获取示例项目
    getSampleProject() {
        return this.projects[0];
    },
    
    // 获取所有声库
    getAllVoiceBanks() {
        return this.voiceBanks;
    },
    
    // 获取所有预设
    getAllPresets() {
        return this.presets;
    },
    
    // 根据ID获取声库
    getVoiceBankById(id) {
        return this.voiceBanks.find(bank => bank.id === id);
    },
    
    // 根据ID获取预设
    getPresetById(id) {
        return this.presets.find(preset => preset.id === id);
    }
};

// 在浏览器环境中导出数据
try {
    if (typeof window !== 'undefined') {
        window.SampleData = SampleData;
    }
} catch (e) {
    console.error('无法导出SampleData到全局对象', e);
}

// 在Node.js环境中导出数据
try {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = SampleData;
    }
} catch (e) {
    // 忽略Node.js特定的导出错误
}