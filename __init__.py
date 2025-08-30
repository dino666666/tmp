"""
项目根目录初始化文件
"""

# 版本信息
__version__ = "1.0.0"
__author__ = "Appium Framework Team"

# 导入主要模块
from config import config_manager
from core import driver_manager, device_manager
from utils.logger_manager import get_logger

# 设置默认日志器
logger = get_logger(__name__)

def get_framework_info():
    """获取框架信息"""
    return {
        "name": "Appium Mobile Test Framework",
        "version": __version__,
        "author": __author__,
        "description": "一个完整的Appium移动端自动化测试框架"
    }

# 框架初始化
logger.info(f"Appium测试框架已加载，版本: {__version__}")