"""
驱动管理模块
负责Appium驱动的初始化和管理
"""
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time
from typing import Optional, Dict, Any

from config import config_manager
from utils.logger_manager import get_logger


class DriverManager:
    """驱动管理器"""
    
    def __init__(self):
        self.driver: Optional[webdriver.Remote] = None
        self.wait: Optional[WebDriverWait] = None
        self.logger = get_logger(__name__)
        self.config = config_manager
    
    def start_android_driver(self, capabilities: Dict[str, Any] = None) -> webdriver.Remote:
        """
        启动Android驱动
        
        Args:
            capabilities: 自定义能力配置
            
        Returns:
            WebDriver实例
        """
        try:
            # 获取配置
            appium_config = self.config.get_appium_config()
            android_config = self.config.get_android_config()
            test_config = self.config.get_test_config()
            
            # 构建默认capabilities
            default_caps = {
                'platformName': android_config.get('platform_name', 'Android'),
                'platformVersion': android_config.get('platform_version', '13'),
                'deviceName': android_config.get('device_name', 'Android Device'),
                'automationName': android_config.get('automation_name', 'UiAutomator2'),
                'appPackage': android_config.get('app_package', ''),
                'appActivity': android_config.get('app_activity', ''),
                'noReset': android_config.get('no_reset', True),
                'fullReset': android_config.get('full_reset', False),
                'unicodeKeyboard': android_config.get('unicode_keyboard', True),
                'resetKeyboard': android_config.get('reset_keyboard', True),
                'newCommandTimeout': appium_config.get('new_command_timeout', 300),
            }
            
            # 如果指定了APK路径，添加app能力
            app_path = android_config.get('app_path')
            if app_path and os.path.exists(app_path):
                default_caps['app'] = app_path
            
            # 合并自定义capabilities
            if capabilities:
                default_caps.update(capabilities)
            
            # 构建Appium服务URL
            server_url = f"http://{appium_config.get('host', '127.0.0.1')}:{appium_config.get('port', 4723)}"
            
            self.logger.info(f"启动Android驱动，服务器: {server_url}")
            self.logger.info(f"Capabilities: {default_caps}")
            
            # 创建驱动
            self.driver = webdriver.Remote(server_url, default_caps)
            
            # 设置隐式等待
            implicit_wait = test_config.get('implicit_wait', 10)
            self.driver.implicitly_wait(implicit_wait)
            
            # 创建显式等待对象
            explicit_wait = test_config.get('explicit_wait', 30)
            self.wait = WebDriverWait(self.driver, explicit_wait)
            
            self.logger.info("Android驱动启动成功")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"启动Android驱动失败: {e}")
            raise
    
    def start_ios_driver(self, capabilities: Dict[str, Any] = None) -> webdriver.Remote:
        """
        启动iOS驱动
        
        Args:
            capabilities: 自定义能力配置
            
        Returns:
            WebDriver实例
        """
        try:
            # 获取配置
            appium_config = self.config.get_appium_config()
            ios_config = self.config.get_ios_config()
            test_config = self.config.get_test_config()
            
            # 构建默认capabilities
            default_caps = {
                'platformName': ios_config.get('platform_name', 'iOS'),
                'platformVersion': ios_config.get('platform_version', '16.0'),
                'deviceName': ios_config.get('device_name', 'iPhone'),
                'automationName': ios_config.get('automation_name', 'XCUITest'),
                'bundleId': ios_config.get('bundle_id', ''),
                'noReset': ios_config.get('no_reset', True),
                'fullReset': ios_config.get('full_reset', False),
                'newCommandTimeout': appium_config.get('new_command_timeout', 300),
            }
            
            # 添加UDID（如果配置了）
            udid = ios_config.get('udid')
            if udid:
                default_caps['udid'] = udid
            
            # 如果指定了IPA路径，添加app能力
            app_path = ios_config.get('app_path')
            if app_path and os.path.exists(app_path):
                default_caps['app'] = app_path
            
            # 合并自定义capabilities
            if capabilities:
                default_caps.update(capabilities)
            
            # 构建Appium服务URL
            server_url = f"http://{appium_config.get('host', '127.0.0.1')}:{appium_config.get('port', 4723)}"
            
            self.logger.info(f"启动iOS驱动，服务器: {server_url}")
            self.logger.info(f"Capabilities: {default_caps}")
            
            # 创建驱动
            self.driver = webdriver.Remote(server_url, default_caps)
            
            # 设置隐式等待
            implicit_wait = test_config.get('implicit_wait', 10)
            self.driver.implicitly_wait(implicit_wait)
            
            # 创建显式等待对象
            explicit_wait = test_config.get('explicit_wait', 30)
            self.wait = WebDriverWait(self.driver, explicit_wait)
            
            self.logger.info("iOS驱动启动成功")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"启动iOS驱动失败: {e}")
            raise
    
    def quit_driver(self):
        """退出驱动"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("驱动已退出")
            except Exception as e:
                self.logger.error(f"退出驱动失败: {e}")
            finally:
                self.driver = None
                self.wait = None
    
    def get_driver(self) -> Optional[webdriver.Remote]:
        """获取当前驱动实例"""
        return self.driver
    
    def get_wait(self) -> Optional[WebDriverWait]:
        """获取等待对象"""
        return self.wait
    
    def restart_driver(self, platform: str = "android", capabilities: Dict[str, Any] = None):
        """
        重启驱动
        
        Args:
            platform: 平台名称 (android/ios)
            capabilities: 自定义能力配置
        """
        self.quit_driver()
        time.sleep(2)  # 等待2秒
        
        if platform.lower() == "android":
            return self.start_android_driver(capabilities)
        elif platform.lower() == "ios":
            return self.start_ios_driver(capabilities)
        else:
            raise ValueError(f"不支持的平台: {platform}")
    
    def is_driver_alive(self) -> bool:
        """检查驱动是否存活"""
        if not self.driver:
            return False
        
        try:
            # 尝试获取当前页面源码来检查连接状态
            self.driver.page_source
            return True
        except Exception:
            return False


# 全局驱动管理器实例
driver_manager = DriverManager()