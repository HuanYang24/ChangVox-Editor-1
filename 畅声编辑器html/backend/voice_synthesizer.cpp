// 畅声编辑器 - 声音合成器核心实现

#include "voice_synthesizer.h"
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <stdexcept>

// VoiceBank类实现
VoiceBank::VoiceBank() : name(""), version("") {
}

VoiceBank::~VoiceBank() {
    samples.clear();
    phonemeMap.clear();
}

bool VoiceBank::loadUTAUBank(const std::string& path) {
    try {
        // 在实际实现中，这里会解析UTAU声库的配置文件和音频样本
        // 这里仅作为示例框架
        
        // 1. 读取oto.ini文件
        std::string otoIniPath = path + "/oto.ini";
        std::ifstream otoFile(otoIniPath);
        
        if (!otoFile.is_open()) {
            std::cerr << "无法打开oto.ini文件: " << otoIniPath << std::endl;
            return false;
        }
        
        std::string line;
        while (std::getline(otoFile, line)) {
            // 解析oto.ini文件中的每一行
            // 格式通常为: 文件名=音素,偏移,辅音长度,元音长度,预音长度,重叠长度
            // 这里简化处理
            std::istringstream iss(line);
            std::string filename, phoneme;
            float offset = 0, consonant = 0, vowel = 0, preutter = 0, overlap = 0;
            
            // 实际解析逻辑需要根据UTAU规范进行
            // 这里仅作为示例
            if (std::getline(iss, filename, '=')) {
                if (std::getline(iss, phoneme, ',')) {
                    // 创建声库样本
                    auto sample = std::make_shared<VoiceSample>();
                    sample->phoneme = phoneme;
                    
                    // 这里应该读取实际的WAV文件并加载音频数据
                    std::string wavPath = path + "/" + filename;
                    // 简化示例，不实际加载WAV文件
                    
                    // 解析其他参数
                    iss >> offset >> consonant >> vowel >> preutter >> overlap;
                    
                    // 保存样本
                    samples[filename] = sample;
                }
            }
        }
        
        otoFile.close();
        
        // 2. 读取声库信息（通常在character.txt中）
        std::string charFilePath = path + "/character.txt";
        std::ifstream charFile(charFilePath);
        
        if (charFile.is_open()) {
            while (std::getline(charFile, line)) {
                // 解析character.txt文件
                // 这里简化处理
                if (line.find("name=") == 0) {
                    name = line.substr(5);
                } else if (line.find("version=") == 0) {
                    version = line.substr(8);
                }
            }
            charFile.close();
        }
        
        // 3. 构建音素映射
        // 这里简化处理
        for (const auto& pair : samples) {
            const auto& sample = pair.second;
            phonemeMap[sample->phoneme][sample->noteName] = 0.0f;
        }
        
        return true;
    } catch (const std::exception& e) {
        std::cerr << "加载声库时发生错误: " << e.what() << std::endl;
        return false;
    }
}

std::string VoiceBank::getName() const {
    return name;
}

std::string VoiceBank::getVersion() const {
    return version;
}

std::shared_ptr<VoiceSample> VoiceBank::getSample(const std::string& pitch, const std::string& phoneme) {
    // 在实际实现中，这里会根据音高和音素找到最合适的样本
    // 可能需要进行音高匹配和插值
    
    // 简化示例
    for (const auto& pair : samples) {
        const auto& sample = pair.second;
        if (sample->phoneme == phoneme) {
            return sample;
        }
    }
    
    // 如果找不到精确匹配，返回第一个可用的样本
    if (!samples.empty()) {
        return samples.begin()->second;
    }
    
    return nullptr;
}

const std::map<std::string, std::shared_ptr<VoiceSample>>& VoiceBank::getAllSamples() const {
    return samples;
}

// VoiceSynthesizer类实现
VoiceSynthesizer::VoiceSynthesizer(int sampleRate, int channels) 
    : sampleRate(sampleRate), channels(channels), bpm(120) {
}

VoiceSynthesizer::~VoiceSynthesizer() {
}

void VoiceSynthesizer::setVoiceBank(std::shared_ptr<VoiceBank> voiceBank) {
    currentVoiceBank = voiceBank;
}

void VoiceSynthesizer::setBPM(float newBPM) {
    if (newBPM > 0) {
        bpm = newBPM;
    }
}

std::vector<float> VoiceSynthesizer::synthesizeNoteInternal(const Note& note) {
    if (!currentVoiceBank) {
        throw std::runtime_error("未设置声库");
    }
    
    // 获取适合的样本
    auto sample = currentVoiceBank->getSample(note.pitch, note.lyric);
    
    if (!sample) {
        throw std::runtime_error("找不到适合的样本");
    }
    
    // 创建样本的副本进行处理
    std::vector<float> audioData = sample->audioData;
    
    // 音高转换
    float targetPitch = 440.0f; // 默认A4音高，实际应该根据note.pitch计算
    float sourcePitch = sample->pitch;
    pitchShift(audioData, targetPitch, sourcePitch);
    
    // 时长调整
    float targetDuration = note.duration;
    float currentDuration = audioData.size() / (float)sampleRate;
    float stretchFactor = targetDuration / currentDuration;
    timeStretch(audioData, stretchFactor);
    
    // 应用效果
    applyEffects(audioData, note);
    
    return audioData;
}

void VoiceSynthesizer::pitchShift(std::vector<float>& audioData, float targetPitch, float sourcePitch) {
    // 音高转换算法实现
    // 这里仅作为示例框架，实际实现需要使用更复杂的算法如PSOLA
    
    float pitchRatio = targetPitch / sourcePitch;
    int newLength = static_cast<int>(audioData.size() / pitchRatio);
    std::vector<float> result(newLength);
    
    // 简化的线性插值实现（实际效果不佳，仅作为示例）
    for (int i = 0; i < newLength; i++) {
        float pos = i * pitchRatio;
        int posFloor = static_cast<int>(pos);
        int posCeil = std::min(posFloor + 1, static_cast<int>(audioData.size() - 1));
        
        if (posFloor < audioData.size()) {
            float alpha = pos - posFloor;
            result[i] = audioData[posFloor] * (1 - alpha) + audioData[posCeil] * alpha;
        }
    }
    
    audioData = std::move(result);
}

void VoiceSynthesizer::timeStretch(std::vector<float>& audioData, float stretchFactor) {
    // 时长调整算法实现
    // 这里仅作为示例框架，实际实现需要使用更复杂的算法
    
    int newLength = static_cast<int>(audioData.size() * stretchFactor);
    std::vector<float> result(newLength);
    
    // 简化的线性插值实现
    for (int i = 0; i < newLength; i++) {
        float pos = i / stretchFactor;
        int posFloor = static_cast<int>(pos);
        int posCeil = std::min(posFloor + 1, static_cast<int>(audioData.size() - 1));
        
        if (posFloor < audioData.size()) {
            float alpha = pos - posFloor;
            result[i] = audioData[posFloor] * (1 - alpha) + audioData[posCeil] * alpha;
        }
    }
    
    audioData = std::move(result);
}

void VoiceSynthesizer::applyEffects(std::vector<float>& audioData, const Note& note) {
    // 应用各种效果
    
    // 1. 音量调整
    float volumeFactor = std::pow(10.0f, note.volume / 20.0f); // 将dB转换为线性因子
    for (auto& sample : audioData) {
        sample *= volumeFactor;
    }
    
    // 2. 张力调整（简化实现）
    // 实际实现可能需要更复杂的处理
    
    // 3. 气息调整（简化实现）
    // 实际实现可能需要添加噪声或调整频谱
}

std::vector<float> VoiceSynthesizer::synthesizeNote(const Note& note) {
    try {
        return synthesizeNoteInternal(note);
    } catch (const std::exception& e) {
        std::cerr << "合成音符时发生错误: " << e.what() << std::endl;
        return {};
    }
}

std::vector<float> VoiceSynthesizer::synthesizeNotes(const std::vector<Note>& notes) {
    try {
        // 计算总时长
        float totalDuration = 0;
        for (const auto& note : notes) {
            totalDuration = std::max(totalDuration, note.startTime + note.duration);
        }
        
        // 创建输出缓冲区
        int totalSamples = static_cast<int>(totalDuration * sampleRate * channels);
        std::vector<float> result(totalSamples, 0.0f);
        
        // 合成每个音符并混合
        for (const auto& note : notes) {
            auto noteAudio = synthesizeNoteInternal(note);
            int startSample = static_cast<int>(note.startTime * sampleRate * channels);
            
            // 混合到输出缓冲区
            for (size_t i = 0; i < noteAudio.size() && (startSample + i) < result.size(); i++) {
                result[startSample + i] += noteAudio[i];
                // 简单的限幅处理
                result[startSample + i] = std::max(-1.0f, std::min(1.0f, result[startSample + i]));
            }
        }
        
        return result;
    } catch (const std::exception& e) {
        std::cerr << "合成多个音符时发生错误: " << e.what() << std::endl;
        return {};
    }
}

bool VoiceSynthesizer::exportToWav(const std::vector<float>& audioData, const std::string& filePath) {
    try {
        // WAV文件头结构
        struct WavHeader {
            char riff[4] = {'R', 'I', 'F', 'F'};
            uint32_t chunkSize;
            char wave[4] = {'W', 'A', 'V', 'E'};
            char fmt[4] = {'f', 'm', 't', ' '};
            uint32_t subchunk1Size = 16;
            uint16_t audioFormat = 1;
            uint16_t numChannels;
            uint32_t sampleRate;
            uint32_t byteRate;
            uint16_t blockAlign;
            uint16_t bitsPerSample = 16;
            char data[4] = {'d', 'a', 't', 'a'};
            uint32_t subchunk2Size;
        } header;
        
        // 填充WAV头
        header.numChannels = channels;
        header.sampleRate = sampleRate;
        header.byteRate = sampleRate * channels * 2; // 16位PCM
        header.blockAlign = channels * 2;
        header.subchunk2Size = audioData.size() * 2;
        header.chunkSize = 36 + header.subchunk2Size;
        
        // 打开文件
        std::ofstream file(filePath, std::ios::binary);
        if (!file.is_open()) {
            return false;
        }
        
        // 写入WAV头
        file.write(reinterpret_cast<const char*>(&header), sizeof(header));
        
        // 写入音频数据（转换为16位PCM）
        for (float sample : audioData) {
            // 将[-1,1]范围的浮点数转换为[-32768,32767]范围的16位整数
            int16_t pcmSample = static_cast<int16_t>(sample * 32767.0f);
            file.write(reinterpret_cast<const char*>(&pcmSample), sizeof(pcmSample));
        }
        
        file.close();
        return true;
    } catch (const std::exception& e) {
        std::cerr << "导出WAV文件时发生错误: " << e.what() << std::endl;
        return false;
    }
}

std::shared_ptr<VoiceSynthesizer> VoiceSynthesizer::createFromUTAUBank(const std::string& voiceBankPath) {
    try {
        auto voiceBank = std::make_shared<VoiceBank>();
        if (!voiceBank->loadUTAUBank(voiceBankPath)) {
            return nullptr;
        }
        
        auto synthesizer = std::make_shared<VoiceSynthesizer>();
        synthesizer->setVoiceBank(voiceBank);
        
        return synthesizer;
    } catch (const std::exception& e) {
        std::cerr << "从UTAU声库创建合成器时发生错误: " << e.what() << std::endl;
        return nullptr;
    }
}