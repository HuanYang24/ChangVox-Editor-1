// 畅声编辑器 - 声音合成器核心头文件

#ifndef VOICE_SYNTHESIZER_H
#define VOICE_SYNTHESIZER_H

#include <string>
#include <vector>
#include <map>
#include <memory>

// 音符数据结构
struct Note {
    std::string pitch;        // 音高，如 C4, D#5 等
    float startTime;          // 开始时间（秒）
    float duration;           // 持续时间（秒）
    std::string lyric;        // 歌词或音节
    float volume;             // 音量参数
    float tension;            // 张力参数
    float breathiness;        // 气息参数
};

// 声库样本数据结构
struct VoiceSample {
    std::string noteName;     // 音符名称
    std::string phoneme;      // 音素
    float pitch;              // 音高（Hz）
    std::vector<float> audioData; // 音频样本数据
    int sampleRate;           // 采样率
};

// 声库类，用于加载和管理UTAU声库
class VoiceBank {
private:
    std::string name;                          // 声库名称
    std::string version;                       // 声库版本
    std::map<std::string, std::shared_ptr<VoiceSample>> samples; // 声库样本
    std::map<std::string, std::map<std::string, float>> phonemeMap; // 音素映射

public:
    VoiceBank();
    ~VoiceBank();
    
    // 加载UTAU声库
    bool loadUTAUBank(const std::string& path);
    
    // 获取声库名称
    std::string getName() const; 
    
    // 获取声库版本
    std::string getVersion() const; 
    
    // 根据音高和音素获取样本
    std::shared_ptr<VoiceSample> getSample(const std::string& pitch, const std::string& phoneme);
    
    // 获取所有样本
    const std::map<std::string, std::shared_ptr<VoiceSample>>& getAllSamples() const;
};

// 声音合成器类
class VoiceSynthesizer {
private:
    std::shared_ptr<VoiceBank> currentVoiceBank; // 当前使用的声库
    float bpm;                                  // 每分钟节拍数
    int sampleRate;                             // 输出采样率
    int channels;                               // 通道数
    
    // 内部合成方法
    std::vector<float> synthesizeNoteInternal(const Note& note);
    
    // 音高转换
    void pitchShift(std::vector<float>& audioData, float targetPitch, float sourcePitch);
    
    // 时长调整
    void timeStretch(std::vector<float>& audioData, float stretchFactor);
    
    // 应用效果
    void applyEffects(std::vector<float>& audioData, const Note& note);

public:
    VoiceSynthesizer(int sampleRate = 44100, int channels = 1);
    ~VoiceSynthesizer();
    
    // 设置声库
    void setVoiceBank(std::shared_ptr<VoiceBank> voiceBank);
    
    // 设置BPM
    void setBPM(float newBPM);
    
    // 合成单个音符
    std::vector<float> synthesizeNote(const Note& note);
    
    // 合成多个音符
    std::vector<float> synthesizeNotes(const std::vector<Note>& notes);
    
    // 导出为WAV文件
    bool exportToWav(const std::vector<float>& audioData, const std::string& filePath);
    
    // 从UTAU声库路径创建合成器
    static std::shared_ptr<VoiceSynthesizer> createFromUTAUBank(const std::string& voiceBankPath);
};

#endif // VOICE_SYNTHESIZER_H