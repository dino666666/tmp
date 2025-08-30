"""
配置管理模块
负责读取和管理配置文件
"""
import os
import yaml
from typing import Dict, Any


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = None, env: str = "dev"):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径
            env: 环境名称 (dev, test, prod)
        """
        self.project_root = self._get_project_root()
        self.config_dir = os.path.join(self.project_root, "config")
        self.env = env
        
        # 默认配置文件路径
        if config_path is None:
            config_path = os.path.join(self.config_dir, "config.yaml")
        
        self.config_path = config_path
        self.env_config_path = os.path.join(self.config_dir, "env_config.yaml")
        
        # 加载配置
        self._load_config()
    
    def _get_project_root(self) -> str:
        """获取项目根目录"""
        current_file = os.path.abspath(__file__)
        # 向上查找，直到找到包含config目录的父目录
        current_dir = os.path.dirname(current_file)
        while current_dir != os.path.dirname(current_dir):  # 直到根目录
            if os.path.exists(os.path.join(current_dir, "config")):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        
        # 如果没找到，返回当前文件的父目录的父目录
        return os.path.dirname(os.path.dirname(current_file))
    
    def _load_config(self):
        """加载配置文件"""
        try:
            # 加载主配置文件
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            # 加载环境配置文件
            if os.path.exists(self.env_config_path):
                with open(self.env_config_path, 'r', encoding='utf-8') as f:
                    env_config = yaml.safe_load(f)
                    # 合并环境配置
                    if self.env in env_config:
                        self._merge_config(self.config, env_config[self.env])
            
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            self.config = {}
    
    def _merge_config(self, base_config: Dict, env_config: Dict):
        """合并环境配置到基础配置"""
        for key, value in env_config.items():
            if isinstance(value, dict) and key in base_config:
                self._merge_config(base_config[key], value)
            else:
                base_config[key] = value
    
    def get(self, key_path: str, default=None) -> Any:
        """
        获取配置值
        
        Args:
            key_path: 配置键路径，用'.'分隔，如 'appium.host'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_appium_config(self) -> Dict[str, Any]:
        """获取Appium配置"""
        return self.get('appium', {})
    
    def get_android_config(self) -> Dict[str, Any]:
        """获取Android配置"""
        return self.get('android', {})
    
    def get_ios_config(self) -> Dict[str, Any]:
        """获取iOS配置"""
        return self.get('ios', {})
    
    def get_test_config(self) -> Dict[str, Any]:
        """获取测试配置"""
        return self.get('test', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志配置"""
        return self.get('logging', {})
    
    def get_report_config(self) -> Dict[str, Any]:
        """获取报告配置"""
        return self.get('report', {})
    
    def get_data_config(self) -> Dict[str, Any]:
        """获取数据配置"""
        return self.get('data', {})
    
    def set_env(self, env: str):
        """设置环境"""
        self.env = env
        self._load_config()
    
    def get_project_path(self, relative_path: str = "") -> str:
        """
        获取项目路径
        
        Args:
            relative_path: 相对路径
            
        Returns:
            绝对路径
        """
        return os.path.join(self.project_root, relative_path)


# 全局配置实例
config_manager = ConfigManager()