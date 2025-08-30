"""
日志管理模块
"""
import os
import logging
import logging.handlers
from datetime import datetime
from config import config_manager


def setup_logger():
    """设置日志配置"""
    # 获取日志配置
    log_config = config_manager.get_logging_config()
    
    # 创建logs目录
    logs_dir = config_manager.get_project_path("logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # 配置日志级别
    level = getattr(logging, log_config.get('level', 'INFO'))
    
    # 配置日志格式
    log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter(log_format)
    
    # 获取根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # 清除现有的处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 控制台处理器
    if log_config.get('console_handler', True):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # 文件处理器
    if log_config.get('file_handler', True):
        # 按日期创建日志文件
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(logs_dir, f"appium_test_{today}.log")
        
        # 使用RotatingFileHandler，按大小轮转
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger


def get_logger(name: str = None) -> logging.Logger:
    """
    获取日志器
    
    Args:
        name: 日志器名称
        
    Returns:
        Logger实例
    """
    if name is None:
        name = __name__
    
    logger = logging.getLogger(name)
    
    # 如果还没有设置过日志配置，则进行设置
    if not logger.handlers and not logger.parent.handlers:
        setup_logger()
    
    return logger


# 初始化日志配置
setup_logger()