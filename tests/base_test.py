"""
测试基类
所有测试用例的基类，提供通用的测试方法和fixture
"""
import pytest
import allure
import os
from datetime import datetime

from core import driver_manager, device_manager
from config import config_manager
from utils.logger_manager import get_logger


class BaseTest:
    """测试基类"""
    
    @classmethod
    def setup_class(cls):
        """测试类级别的初始化"""
        cls.logger = get_logger(cls.__name__)
        cls.config = config_manager
        cls.device_manager = device_manager
        cls.driver_manager = driver_manager
        cls.logger.info(f"开始测试类: {cls.__name__}")
    
    @classmethod
    def teardown_class(cls):
        """测试类级别的清理"""
        cls.logger.info(f"结束测试类: {cls.__name__}")
    
    def setup_method(self, method):
        """测试方法级别的初始化"""
        self.logger.info(f"开始测试方法: {method.__name__}")
        
        # 检查驱动是否存活，如果不存活则重新启动
        if not self.driver_manager.is_driver_alive():
            self.logger.warning("驱动已断开，正在重新启动...")
            self.start_driver()
    
    def teardown_method(self, method):
        """测试方法级别的清理"""
        # 如果测试失败且配置了失败截图，则进行截图
        if hasattr(self, '_pytest_current_test'):
            test_result = self._pytest_current_test
            if 'FAILED' in str(test_result) and self.config.get('test.screenshot_on_failure', True):
                self.take_failure_screenshot(method.__name__)
        
        self.logger.info(f"结束测试方法: {method.__name__}")
    
    def start_driver(self, platform: str = "android", capabilities: dict = None):
        """
        启动驱动
        
        Args:
            platform: 平台类型 (android/ios)
            capabilities: 自定义能力配置
        """
        try:
            if platform.lower() == "android":
                self.driver = self.driver_manager.start_android_driver(capabilities)
            elif platform.lower() == "ios":
                self.driver = self.driver_manager.start_ios_driver(capabilities)
            else:
                raise ValueError(f"不支持的平台: {platform}")
            
            self.wait = self.driver_manager.get_wait()
            self.logger.info(f"{platform} 驱动启动成功")
            
        except Exception as e:
            self.logger.error(f"启动驱动失败: {e}")
            raise
    
    def stop_driver(self):
        """停止驱动"""
        self.driver_manager.quit_driver()
        self.logger.info("驱动已停止")
    
    def restart_driver(self, platform: str = "android", capabilities: dict = None):
        """
        重启驱动
        
        Args:
            platform: 平台类型
            capabilities: 自定义能力配置
        """
        self.stop_driver()
        self.start_driver(platform, capabilities)
    
    def take_failure_screenshot(self, test_name: str):
        """
        失败截图
        
        Args:
            test_name: 测试名称
        """
        try:
            if hasattr(self, 'driver') and self.driver:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"failure_{test_name}_{timestamp}.png"
                
                # 创建失败截图目录
                failure_dir = self.config.get_project_path("reports/screenshots/failures")
                os.makedirs(failure_dir, exist_ok=True)
                
                filepath = os.path.join(failure_dir, filename)
                self.driver.save_screenshot(filepath)
                
                # 添加到Allure报告
                with open(filepath, 'rb') as f:
                    allure.attach(f.read(), name="失败截图", attachment_type=allure.attachment_type.PNG)
                
                self.logger.info(f"失败截图已保存: {filepath}")
                
        except Exception as e:
            self.logger.error(f"保存失败截图失败: {e}")
    
    def take_screenshot(self, description: str = "测试截图"):
        """
        主动截图并添加到报告
        
        Args:
            description: 截图描述
        """
        try:
            if hasattr(self, 'driver') and self.driver:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"screenshot_{timestamp}.png"
                
                screenshots_dir = self.config.get_project_path("reports/screenshots")
                os.makedirs(screenshots_dir, exist_ok=True)
                
                filepath = os.path.join(screenshots_dir, filename)
                self.driver.save_screenshot(filepath)
                
                # 添加到Allure报告
                with open(filepath, 'rb') as f:
                    allure.attach(f.read(), name=description, attachment_type=allure.attachment_type.PNG)
                
                self.logger.info(f"截图已保存: {filepath}")
                
        except Exception as e:
            self.logger.error(f"截图失败: {e}")
    
    def assert_element_exists(self, locator, timeout: int = 10, message: str = ""):
        """
        断言元素存在
        
        Args:
            locator: 定位器
            timeout: 超时时间
            message: 断言消息
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            self.logger.info(f"断言成功: 元素存在 {locator}")
        except Exception as e:
            error_msg = message or f"元素不存在: {locator}"
            self.logger.error(error_msg)
            self.take_failure_screenshot("assert_element_exists")
            pytest.fail(error_msg)
    
    def assert_element_visible(self, locator, timeout: int = 10, message: str = ""):
        """
        断言元素可见
        
        Args:
            locator: 定位器
            timeout: 超时时间
            message: 断言消息
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            self.logger.info(f"断言成功: 元素可见 {locator}")
        except Exception as e:
            error_msg = message or f"元素不可见: {locator}"
            self.logger.error(error_msg)
            self.take_failure_screenshot("assert_element_visible")
            pytest.fail(error_msg)
    
    def assert_text_present(self, expected_text: str, actual_text: str, message: str = ""):
        """
        断言文本存在
        
        Args:
            expected_text: 期望文本
            actual_text: 实际文本
            message: 断言消息
        """
        if expected_text in actual_text:
            self.logger.info(f"断言成功: 文本存在 '{expected_text}'")
        else:
            error_msg = message or f"期望文本 '{expected_text}' 不在实际文本 '{actual_text}' 中"
            self.logger.error(error_msg)
            self.take_failure_screenshot("assert_text_present")
            pytest.fail(error_msg)
    
    def get_device_info(self):
        """获取当前测试设备信息"""
        try:
            devices = self.device_manager.get_android_devices()
            if devices:
                return devices[0]
            return None
        except Exception as e:
            self.logger.error(f"获取设备信息失败: {e}")
            return None
    
    def wait_for_app_launch(self, timeout: int = 30):
        """
        等待应用启动完成
        
        Args:
            timeout: 超时时间
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # 尝试获取页面源码来判断应用是否已启动
                if self.driver.page_source:
                    self.logger.info("应用启动完成")
                    return True
            except Exception:
                pass
            
            time.sleep(1)
        
        self.logger.error("等待应用启动超时")
        return False