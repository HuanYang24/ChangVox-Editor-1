"""
音频服务 - 基于Synchrotron的音频处理引擎
"""

import logging
import numpy as np
from typing import Optional, Union
from pathlib import Path

# 尝试导入Synchrotron，如果不可用则使用替代方案
try:
    import synchrotron
    SYNCHROTRON_AVAILABLE = True
except ImportError:
    SYNCHROTRON_AVAILABLE = False
    logging.warning("Synchrotron不可用，将使用替代音频处理方案")

# 备用音频处理库
try:
    import librosa
    import soundfile as sf
    import pydub
    AUDIO_LIBS_AVAILABLE = True
except ImportError:
    AUDIO_LIBS_AVAILABLE = False
    logging.warning("备用音频库不可用")

class AudioService:
    """音频处理服务"""
    
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.sample_rate = 44100
        self.audio_engine = None
        self.is_playing = False
        
        self._initialize_audio_engine()
        logging.info("音频服务初始化完成")
    
    def _initialize_audio_engine(self):
        """初始化音频引擎"""
        if SYNCHROTRON_AVAILABLE:
            try:
                self.audio_engine = synchrotron.AudioEngine(sample_rate=self.sample_rate)
                logging.info("使用Synchrotron音频引擎")
            except Exception as e:
                logging.error(f"初始化Synchrotron失败: {e}")
                self.audio_engine = None
        
        if not self.audio_engine and AUDIO_LIBS_AVAILABLE:
            logging.info("使用备用音频处理方案")
    
    def synthesize_audio(self, spectrogram: np.ndarray) -> np.ndarray:
        """从频谱合成音频
        
        Args:
            spectrogram: 频谱数据
            
        Returns:
            音频数据
        """
        try:
            if self.audio_engine and SYNCHROTRON_AVAILABLE:
                # 使用Synchrotron合成音频
                audio_data = self.audio_engine.synthesize(spectrogram)
            else:
                # 使用备用方案（Griffin-Lim算法）
                audio_data = self._griffin_lim_synthesis(spectrogram)
            
            # 后处理音频
            processed_audio = self._postprocess_audio(audio_data)
            
            # 发布音频处理完成事件
            self.event_bus.publish('audio_processed', {
                'audio_data': processed_audio,
                'sample_rate': self.sample_rate
            })
            
            logging.info("音频合成完成")
            return processed_audio
            
        except Exception as e:
            logging.error(f"音频合成失败: {e}")
            raise
    
    def _griffin_lim_synthesis(self, spectrogram: np.ndarray, n_iter: int = 100) -> np.ndarray:
        """Griffin-Lim算法频谱反演（备用方案）
        
        Args:
            spectrogram: 频谱数据
            n_iter: 迭代次数
            
        Returns:
            音频数据
        """
        if not AUDIO_LIBS_AVAILABLE:
            raise RuntimeError("音频处理库不可用")
        
        # 使用librosa实现Griffin-Lim算法
        magnitude = np.abs(spectrogram)
        
        # 随机相位初始化
        angles = np.exp(2j * np.pi * np.random.rand(*magnitude.shape))
        complex_spec = magnitude * angles
        
        # 迭代重建
        for _ in range(n_iter):
            # 逆STFT
            audio = librosa.istft(complex_spec)
            # 正向STFT
            stft_audio = librosa.stft(audio)
            # 保持幅度，更新相位
            complex_spec = magnitude * np.exp(1j * np.angle(stft_audio))
        
        # 最终逆STFT
        audio = librosa.istft(complex_spec)
        return audio
    
    def _postprocess_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """后处理音频数据
        
        Args:
            audio_data: 原始音频数据
            
        Returns:
            处理后的音频数据
        """
        # 归一化
        if np.max(np.abs(audio_data)) > 0:
            audio_data = audio_data / np.max(np.abs(audio_data))
        
        # 限制动态范围
        audio_data = np.clip(audio_data, -1.0, 1.0)
        
        return audio_data
    
    def play(self, audio_data: np.ndarray):
        """播放音频
        
        Args:
            audio_data: 音频数据
        """
        if self.is_playing:
            self.stop()
        
        try:
            # 这里需要根据平台选择合适的音频播放方式
            # 可以使用pygame, pyaudio等库
            self.is_playing = True
            
            # 发布播放开始事件
            self.event_bus.publish('audio_play_start', {})
            
            # 模拟播放（实际实现需要具体音频库）
            logging.info("音频播放开始")
            
            # 发布播放完成事件
            self.event_bus.publish('audio_play_complete', {})
            self.is_playing = False
            
        except Exception as e:
            logging.error(f"音频播放失败: {e}")
            self.is_playing = False
            self.event_bus.publish('audio_play_error', {'error': str(e)})
    
    def stop(self):
        """停止播放"""
        self.is_playing = False
        self.event_bus.publish('audio_play_stop', {})
        logging.info("音频播放停止")
    
    def save_audio(self, audio_data: np.ndarray, file_path: str, format: str = 'wav'):
        """保存音频文件
        
        Args:
            audio_data: 音频数据
            file_path: 文件路径
            format: 文件格式
        """
        try:
            if AUDIO_LIBS_AVAILABLE:
                sf.write(file_path, audio_data, self.sample_rate, format=format)
                logging.info(f"音频文件已保存: {file_path}")
            else:
                raise RuntimeError("音频保存功能不可用")
        except Exception as e:
            logging.error(f"保存音频文件失败: {e}")
            raise
    
    def load_audio(self, file_path: str) -> np.ndarray:
        """加载音频文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            音频数据
        """
        try:
            if AUDIO_LIBS_AVAILABLE:
                audio_data, sample_rate = librosa.load(file_path, sr=self.sample_rate)
                return audio_data
            else:
                raise RuntimeError("音频加载功能不可用")
        except Exception as e:
            logging.error(f"加载音频文件失败: {e}")
            raise
    
    def get_supported_formats(self) -> list:
        """获取支持的音频格式"""
        return ['wav', 'mp3', 'flac', 'ogg'] if AUDIO_LIBS_AVAILABLE else []
    
    def cleanup(self):
        """清理资源"""
        self.stop()
        if self.audio_engine:
            del self.audio_engine
        logging.info("音频服务资源清理完成")