"""
事件总线 - 模块间通信机制
"""

import logging
from typing import Dict, List, Callable, Any

class EventBus:
    """事件总线类"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        """订阅事件
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logging.debug(f"订阅事件: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """取消订阅事件
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
                logging.debug(f"取消订阅事件: {event_type}")
    
    def publish(self, event_type: str, data: Any = None):
        """发布事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logging.error(f"事件处理错误 ({event_type}): {e}")
        
        logging.debug(f"发布事件: {event_type}")
    
    def clear(self):
        """清除所有订阅者"""
        self._subscribers.clear()
        logging.info("事件总线已清空")