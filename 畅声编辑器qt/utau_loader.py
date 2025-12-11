import os
import re
import configparser

class UTAULoader:
    """
    UTAU声库加载器类，用于解析和加载UTAU声库
    """
    def __init__(self):
        pass
    
    def load_voicebank(self, voicebank_path):
        """
        加载UTAU声库
        
        参数:
            voicebank_path: UTAU声库文件夹路径
        
        返回:
            dict: 包含声库信息的字典，如果加载失败返回None
        """
        try:
            # 检查路径是否存在
            if not os.path.exists(voicebank_path) or not os.path.isdir(voicebank_path):
                print(f"错误: 声库路径不存在或不是文件夹: {voicebank_path}")
                return None
            
            # 创建声库信息字典
            voicebank_info = {
                'path': voicebank_path,
                'name': os.path.basename(voicebank_path),
                'sample_files': [],
                'oto_configs': {},
                'character_info': {},
                'valid': False
            }
            
            # 查找character.txt文件
            character_file = os.path.join(voicebank_path, 'character.txt')
            if os.path.exists(character_file):
                voicebank_info['character_info'] = self._parse_character_file(character_file)
            
            # 查找oto.ini文件并解析
            oto_files = self._find_oto_files(voicebank_path)
            for oto_file in oto_files:
                oto_dir = os.path.dirname(oto_file)
                oto_section = os.path.basename(oto_dir) if oto_dir != voicebank_path else 'main'
                voicebank_info['oto_configs'][oto_section] = self._parse_oto_file(oto_file)
            
            # 查找音频文件
            voicebank_info['sample_files'] = self._find_sample_files(voicebank_path)
            
            # 验证声库是否有效
            voicebank_info['valid'] = len(voicebank_info['sample_files']) > 0 or len(voicebank_info['oto_configs']) > 0
            
            if voicebank_info['valid']:
                print(f"成功加载UTAU声库: {voicebank_info['name']}")
            else:
                print(f"警告: 声库 {voicebank_info['name']} 没有找到有效的音频文件或oto配置")
            
            return voicebank_info
            
        except Exception as e:
            print(f"加载UTAU声库时出错: {e}")
            return None
    
    def _parse_character_file(self, file_path):
        """解析character.txt文件"""
        character_info = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        character_info[key] = value
        except UnicodeDecodeError:
            # 尝试用其他编码打开
            try:
                with open(file_path, 'r', encoding='shift_jis') as f:
                    lines = f.readlines()
                    
                    for line in lines:
                        line = line.strip()
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            character_info[key] = value
            except Exception as e:
                print(f"解析character.txt时出错: {e}")
        except Exception as e:
            print(f"解析character.txt时出错: {e}")
        
        return character_info
    
    def _parse_oto_file(self, file_path):
        """解析oto.ini文件"""
        oto_configs = []
        try:
            # UTAU的oto.ini是特殊格式，不是标准的ini文件
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith(';'):
                        continue
                    
                    # 分割oto行，格式: 文件名=别名,偏移,辅音长度,元音长度,预音长,重叠
                    parts = line.split('=')
                    if len(parts) < 2:
                        continue
                    
                    wav_file = parts[0].strip()
                    oto_params = parts[1].split(',')
                    
                    if len(oto_params) >= 5:
                        oto_config = {
                            'wav_file': wav_file,
                            'alias': oto_params[0].strip() if len(oto_params) > 0 else '',
                            'offset': float(oto_params[1]) if len(oto_params) > 1 and oto_params[1] else 0.0,
                            'consonant': float(oto_params[2]) if len(oto_params) > 2 and oto_params[2] else 0.0,
                            'vowel': float(oto_params[3]) if len(oto_params) > 3 and oto_params[3] else 0.0,
                            'preutterance': float(oto_params[4]) if len(oto_params) > 4 and oto_params[4] else 0.0,
                            'overlap': float(oto_params[5]) if len(oto_params) > 5 and oto_params[5] else 0.0
                        }
                        oto_configs.append(oto_config)
        except UnicodeDecodeError:
            # 尝试用其他编码打开
            try:
                with open(file_path, 'r', encoding='shift_jis') as f:
                    lines = f.readlines()
                    
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith(';'):
                            continue
                        
                        parts = line.split('=')
                        if len(parts) < 2:
                            continue
                        
                        wav_file = parts[0].strip()
                        oto_params = parts[1].split(',')
                        
                        if len(oto_params) >= 5:
                            oto_config = {
                                'wav_file': wav_file,
                                'alias': oto_params[0].strip() if len(oto_params) > 0 else '',
                                'offset': float(oto_params[1]) if len(oto_params) > 1 and oto_params[1] else 0.0,
                                'consonant': float(oto_params[2]) if len(oto_params) > 2 and oto_params[2] else 0.0,
                                'vowel': float(oto_params[3]) if len(oto_params) > 3 and oto_params[3] else 0.0,
                                'preutterance': float(oto_params[4]) if len(oto_params) > 4 and oto_params[4] else 0.0,
                                'overlap': float(oto_params[5]) if len(oto_params) > 5 and oto_params[5] else 0.0
                            }
                            oto_configs.append(oto_config)
            except Exception as e:
                print(f"解析oto.ini时出错: {e}")
        except Exception as e:
            print(f"解析oto.ini时出错: {e}")
        
        return oto_configs
    
    def _find_oto_files(self, directory):
        """查找目录下所有的oto.ini文件"""
        oto_files = []
        
        try:
            for root, dirs, files in os.walk(directory):
                if 'oto.ini' in files:
                    oto_files.append(os.path.join(root, 'oto.ini'))
        except Exception as e:
            print(f"查找oto.ini文件时出错: {e}")
        
        return oto_files
    
    def _find_sample_files(self, directory):
        """查找目录下所有的音频文件"""
        sample_files = []
        audio_extensions = ['.wav', '.mp3', '.flac']
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in audio_extensions:
                        sample_files.append(os.path.join(root, file))
        except Exception as e:
            print(f"查找音频文件时出错: {e}")
        
        return sample_files
        
    def find_best_sample_for_pitch(self, voicebank_info, pitch):
        """
        根据音高查找最合适的UTAU采样文件
        
        参数:
            voicebank_info: 声库信息字典
            pitch: MIDI音高值
        
        返回:
            str: 最合适的采样文件路径，如果没有找到返回None
        """
        try:
            # 计算目标频率
            target_freq = 440.0 * (2.0 ** ((pitch - 69) / 12.0))
            
            best_sample = None
            min_freq_diff = float('inf')
            
            # 遍历所有oto配置查找最匹配的采样
            for section, configs in voicebank_info.get('oto_configs', {}).items():
                for config in configs:
                    # 尝试从文件名或别名中提取音高信息
                    sample_freq = self._estimate_frequency_from_sample_name(config['alias'])
                    if sample_freq > 0:
                        # 计算频率差异
                        freq_diff = abs(sample_freq - target_freq)
                        if freq_diff < min_freq_diff:
                            min_freq_diff = freq_diff
                            # 构建完整的文件路径
                            wav_file_path = os.path.join(os.path.dirname(voicebank_info['oto_configs'][section][0]['wav_file']), config['wav_file']) 
                            if not os.path.isabs(wav_file_path):
                                wav_file_path = os.path.join(voicebank_info['path'], section, config['wav_file']) if section != 'main' else os.path.join(voicebank_info['path'], config['wav_file'])
                            best_sample = wav_file_path
            
            # 如果没有找到匹配的采样，返回第一个可用的采样文件
            if best_sample is None and voicebank_info.get('sample_files'):
                best_sample = voicebank_info['sample_files'][0]
            
            return best_sample
        except Exception as e:
            print(f"查找最佳采样文件时出错: {e}")
            return None
            
    def _estimate_frequency_from_sample_name(self, sample_name):
        """
        尝试从采样文件名或别名中估计频率
        
        参数:
            sample_name: 采样文件名或别名
        
        返回:
            float: 估计的频率，如果无法估计返回0
        """
        try:
            # 这是一个简化的实现
            # 在实际应用中，可能需要更复杂的逻辑来解析UTAU采样文件名
            
            # 常见的UTAU采样命名模式：C4, D#4, E5等
            note_pattern = re.compile(r'([A-G]#?)([0-9])')
            match = note_pattern.search(sample_name)
            
            if match:
                note = match.group(1)
                octave = int(match.group(2))
                
                # 将音符名称转换为MIDI音高
                note_to_midi = {
                    'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
                    'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
                }
                
                if note in note_to_midi:
                    midi_pitch = note_to_midi[note] + (octave + 1) * 12
                    # 转换为频率
                    return 440.0 * (2.0 ** ((midi_pitch - 69) / 12.0))
            
            return 0.0
        except Exception as e:
            print(f"从采样名称估计频率时出错: {e}")
            return 0.0