"""
项目文件管理器 - 管理歌声合成项目
"""

import logging
import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

class ProjectManager:
    """项目文件管理器"""
    
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.current_project: Optional[Dict[str, Any]] = None
        self.project_file_path: Optional[Path] = None
        
        # 项目文件扩展名
        self.supported_extensions = ['.cvproj', '.json']
        
        logging.info("项目文件管理器初始化完成")
    
    def create_new_project(self, project_name: str, base_path: Optional[str] = None) -> bool:
        """创建新项目
        
        Args:
            project_name: 项目名称
            base_path: 基础路径
            
        Returns:
            是否创建成功
        """
        try:
            if base_path:
                project_dir = Path(base_path) / project_name
            else:
                project_dir = Path("projects") / project_name
            
            # 创建项目目录
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # 初始化项目数据
            self.current_project = {
                'metadata': {
                    'name': project_name,
                    'created_at': datetime.now().isoformat(),
                    'version': '1.0.0',
                    'author': 'ChangVox Editor'
                },
                'settings': {
                    'sample_rate': 44100,
                    'tempo': 120,
                    'time_signature': '4/4'
                },
                'tracks': [],
                'lyrics': '',
                'notes': [],
                'parameters': {},
                'audio_files': []
            }
            
            self.project_file_path = project_dir / f"{project_name}.cvproj"
            
            # 发布项目创建事件
            self.event_bus.publish('project_created', {
                'project_name': project_name,
                'project_path': str(self.project_file_path)
            })
            
            logging.info(f"新项目创建成功: {project_name}")
            return True
            
        except Exception as e:
            logging.error(f"创建新项目失败: {e}")
            return False
    
    def save(self, file_path: Optional[str] = None) -> bool:
        """保存项目
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否保存成功
        """
        if not self.current_project:
            logging.warning("没有当前项目可保存")
            return False
        
        try:
            if file_path:
                self.project_file_path = Path(file_path)
            
            if not self.project_file_path:
                logging.error("未指定项目文件路径")
                return False
            
            # 更新修改时间
            self.current_project['metadata']['modified_at'] = datetime.now().isoformat()
            
            # 保存为JSON格式
            with open(self.project_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_project, f, indent=2, ensure_ascii=False)
            
            # 发布项目保存事件
            self.event_bus.publish('project_saved', {
                'project_path': str(self.project_file_path)
            })
            
            logging.info(f"项目已保存: {self.project_file_path}")
            return True
            
        except Exception as e:
            logging.error(f"保存项目失败: {e}")
            return False
    
    def load(self, file_path: str) -> bool:
        """加载项目
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否加载成功
        """
        try:
            project_path = Path(file_path)
            
            if not project_path.exists():
                logging.error(f"项目文件不存在: {file_path}")
                return False
            
            # 读取项目文件
            with open(project_path, 'r', encoding='utf-8') as f:
                self.current_project = json.load(f)
            
            self.project_file_path = project_path
            
            # 发布项目加载事件
            self.event_bus.publish('project_loaded', {
                'project_name': self.current_project['metadata']['name'],
                'project_path': str(self.project_file_path)
            })
            
            logging.info(f"项目加载成功: {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"加载项目失败: {e}")
            return False
    
    def add_track(self, track_data: Dict[str, Any]) -> bool:
        """添加音轨
        
        Args:
            track_data: 音轨数据
            
        Returns:
            是否添加成功
        """
        if not self.current_project:
            return False
        
        try:
            # 生成音轨ID
            track_id = len(self.current_project['tracks']) + 1
            track_data['id'] = track_id
            
            self.current_project['tracks'].append(track_data)
            
            # 发布音轨添加事件
            self.event_bus.publish('track_added', {'track_data': track_data})
            
            logging.info(f"音轨添加成功: {track_id}")
            return True
            
        except Exception as e:
            logging.error(f"添加音轨失败: {e}")
            return False
    
    def update_lyrics(self, lyrics: str) -> bool:
        """更新歌词
        
        Args:
            lyrics: 歌词文本
            
        Returns:
            是否更新成功
        """
        if not self.current_project:
            return False
        
        try:
            self.current_project['lyrics'] = lyrics
            
            # 发布歌词更新事件
            self.event_bus.publish('lyrics_updated', {'lyrics': lyrics})
            
            logging.info("歌词更新成功")
            return True
            
        except Exception as e:
            logging.error(f"更新歌词失败: {e}")
            return False
    
    def update_notes(self, notes: list) -> bool:
        """更新音符
        
        Args:
            notes: 音符列表
            
        Returns:
            是否更新成功
        """
        if not self.current_project:
            return False
        
        try:
            self.current_project['notes'] = notes
            
            # 发布音符更新事件
            self.event_bus.publish('notes_updated', {'notes': notes})
            
            logging.info("音符更新成功")
            return True
            
        except Exception as e:
            logging.error(f"更新音符失败: {e}")
            return False
    
    def update_parameters(self, parameters: Dict[str, Any]) -> bool:
        """更新合成参数
        
        Args:
            parameters: 参数字典
            
        Returns:
            是否更新成功
        """
        if not self.current_project:
            return False
        
        try:
            self.current_project['parameters'] = parameters
            
            # 发布参数更新事件
            self.event_bus.publish('parameters_updated', {'parameters': parameters})
            
            logging.info("合成参数更新成功")
            return True
            
        except Exception as e:
            logging.error(f"更新合成参数失败: {e}")
            return False
    
    def get_project_info(self) -> Optional[Dict[str, Any]]:
        """获取项目信息"""
        if not self.current_project:
            return None
        
        return {
            'name': self.current_project['metadata']['name'],
            'path': str(self.project_file_path) if self.project_file_path else None,
            'created': self.current_project['metadata']['created_at'],
            'modified': self.current_project['metadata'].get('modified_at'),
            'tracks_count': len(self.current_project['tracks']),
            'lyrics_length': len(self.current_project['lyrics'])
        }
    
    def export_project(self, export_path: str, format: str = 'json') -> bool:
        """导出项目
        
        Args:
            export_path: 导出路径
            format: 导出格式
            
        Returns:
            是否导出成功
        """
        if not self.current_project:
            return False
        
        try:
            export_file = Path(export_path)
            
            if format == 'json':
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(self.current_project, f, indent=2, ensure_ascii=False)
            elif format == 'yaml':
                with open(export_file, 'w', encoding='utf-8') as f:
                    yaml.dump(self.current_project, f, default_flow_style=False, allow_unicode=True)
            else:
                logging.error(f"不支持的导出格式: {format}")
                return False
            
            logging.info(f"项目导出成功: {export_path}")
            return True
            
        except Exception as e:
            logging.error(f"导出项目失败: {e}")
            return False