"""
基础页面对象类
所有页面对象的基类，提供通用的元素操作方法
"""
import os
import time
from typing import Optional, List, Tuple, Union
from datetime import datetime

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementNotInteractableException,
    StaleElementReferenceException
)

from core import driver_manager
from config import config_manager
from utils.logger_manager import get_logger


class BasePage:
    """基础页面对象类"""
    
    def __init__(self, driver=None):
        """
        初始化基础页面
        
        Args:
            driver: WebDriver实例，如果为None则使用全局driver_manager
        """
        self.driver = driver or driver_manager.get_driver()
        self.wait = driver_manager.get_wait()
        self.logger = get_logger(self.__class__.__name__)
        self.config = config_manager
        
        if not self.driver:
            raise RuntimeError("驱动未初始化，请先启动驱动")
    
    # =========================== 元素查找方法 ===========================
    
    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> Optional[WebElement]:
        """
        查找单个元素
        
        Args:
            locator: 定位器元组 (by, value)
            timeout: 超时时间，默认使用配置文件中的值
            
        Returns:
            WebElement或None
        """
        try:
            if timeout is None:
                timeout = self.config.get('test.explicit_wait', 30)
            
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            self.logger.debug(f"找到元素: {locator}")
            return element
            
        except TimeoutException:
            self.logger.warning(f"元素查找超时: {locator}")
            return None
        except Exception as e:
            self.logger.error(f"查找元素失败: {locator}, 错误: {e}")
            return None
    
    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """
        查找多个元素
        
        Args:
            locator: 定位器元组 (by, value)
            timeout: 超时时间
            
        Returns:
            WebElement列表
        """
        try:
            if timeout is None:
                timeout = self.config.get('test.explicit_wait', 30)
            
            wait = WebDriverWait(self.driver, timeout)
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            self.logger.debug(f"找到 {len(elements)} 个元素: {locator}")
            return elements
            
        except TimeoutException:
            self.logger.warning(f"元素查找超时: {locator}")
            return []
        except Exception as e:
            self.logger.error(f"查找元素失败: {locator}, 错误: {e}")
            return []
    
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        等待元素可见
        
        Args:
            locator: 定位器元组
            timeout: 超时时间
            
        Returns:
            是否可见
        """
        try:
            if timeout is None:
                timeout = self.config.get('test.explicit_wait', 30)
            
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            self.logger.debug(f"元素已可见: {locator}")
            return True
            
        except TimeoutException:
            self.logger.warning(f"等待元素可见超时: {locator}")
            return False
    
    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        等待元素可点击
        
        Args:
            locator: 定位器元组
            timeout: 超时时间
            
        Returns:
            是否可点击
        """
        try:
            if timeout is None:
                timeout = self.config.get('test.explicit_wait', 30)
            
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.element_to_be_clickable(locator))
            self.logger.debug(f"元素可点击: {locator}")
            return True
            
        except TimeoutException:
            self.logger.warning(f"等待元素可点击超时: {locator}")
            return False
    
    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """
        检查元素是否存在
        
        Args:
            locator: 定位器元组
            
        Returns:
            是否存在
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """
        检查元素是否可见
        
        Args:
            locator: 定位器元组
            
        Returns:
            是否可见
        """
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    # =========================== 元素操作方法 ===========================
    
    def click(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        点击元素
        
        Args:
            locator: 定位器元组
            timeout: 超时时间
            
        Returns:
            操作是否成功
        """
        try:
            if self.wait_for_element_clickable(locator, timeout):
                element = self.find_element(locator, timeout)
                if element:
                    element.click()
                    self.logger.info(f"点击元素成功: {locator}")
                    return True
            
            self.logger.warning(f"点击元素失败: {locator}")
            return False
            
        except Exception as e:
            self.logger.error(f"点击元素异常: {locator}, 错误: {e}")
            return False
    
    def send_keys(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: int = None) -> bool:
        """
        输入文本
        
        Args:
            locator: 定位器元组
            text: 要输入的文本
            clear_first: 是否先清空
            timeout: 超时时间
            
        Returns:
            操作是否成功
        """
        try:
            element = self.find_element(locator, timeout)
            if element:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                self.logger.info(f"输入文本成功: {locator}, 文本: {text}")
                return True
            
            self.logger.warning(f"输入文本失败: {locator}")
            return False
            
        except Exception as e:
            self.logger.error(f"输入文本异常: {locator}, 错误: {e}")
            return False
    
    def get_text(self, locator: Tuple[str, str], timeout: int = None) -> str:
        """
        获取元素文本
        
        Args:
            locator: 定位器元组
            timeout: 超时时间
            
        Returns:
            元素文本
        """
        try:
            element = self.find_element(locator, timeout)
            if element:
                text = element.text
                self.logger.debug(f"获取文本: {locator}, 文本: {text}")
                return text
            
            return ""
            
        except Exception as e:
            self.logger.error(f"获取文本异常: {locator}, 错误: {e}")
            return ""
    
    def get_attribute(self, locator: Tuple[str, str], attribute: str, timeout: int = None) -> str:
        """
        获取元素属性
        
        Args:
            locator: 定位器元组
            attribute: 属性名
            timeout: 超时时间
            
        Returns:
            属性值
        """
        try:
            element = self.find_element(locator, timeout)
            if element:
                value = element.get_attribute(attribute)
                self.logger.debug(f"获取属性: {locator}, 属性: {attribute}, 值: {value}")
                return value or ""
            
            return ""
            
        except Exception as e:
            self.logger.error(f"获取属性异常: {locator}, 错误: {e}")
            return ""
    
    # =========================== 滑动和手势操作 ===========================
    
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 1000):
        """
        滑动操作
        
        Args:
            start_x: 起始X坐标
            start_y: 起始Y坐标
            end_x: 结束X坐标
            end_y: 结束Y坐标
            duration: 持续时间（毫秒）
        """
        try:
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            self.logger.info(f"滑动操作: ({start_x},{start_y}) -> ({end_x},{end_y})")
        except Exception as e:
            self.logger.error(f"滑动操作失败: {e}")
    
    def scroll_down(self, distance: int = None):
        """
        向下滚动
        
        Args:
            distance: 滚动距离，默认为屏幕高度的1/3
        """
        try:
            size = self.driver.get_window_size()
            width = size['width']
            height = size['height']
            
            if distance is None:
                distance = height // 3
            
            start_x = width // 2
            start_y = height * 2 // 3
            end_x = width // 2
            end_y = start_y - distance
            
            self.swipe(start_x, start_y, end_x, end_y)
            
        except Exception as e:
            self.logger.error(f"向下滚动失败: {e}")
    
    def scroll_up(self, distance: int = None):
        """
        向上滚动
        
        Args:
            distance: 滚动距离，默认为屏幕高度的1/3
        """
        try:
            size = self.driver.get_window_size()
            width = size['width']
            height = size['height']
            
            if distance is None:
                distance = height // 3
            
            start_x = width // 2
            start_y = height // 3
            end_x = width // 2
            end_y = start_y + distance
            
            self.swipe(start_x, start_y, end_x, end_y)
            
        except Exception as e:
            self.logger.error(f"向上滚动失败: {e}")
    
    def scroll_to_element(self, locator: Tuple[str, str], max_scrolls: int = 10) -> bool:
        """
        滚动到指定元素
        
        Args:
            locator: 定位器元组
            max_scrolls: 最大滚动次数
            
        Returns:
            是否找到元素
        """
        for i in range(max_scrolls):
            if self.is_element_present(locator):
                self.logger.info(f"找到元素: {locator}")
                return True
            
            self.scroll_down()
            time.sleep(0.5)
        
        self.logger.warning(f"滚动查找元素失败: {locator}")
        return False
    
    # =========================== 截图和调试方法 ===========================
    
    def take_screenshot(self, filename: str = None) -> str:
        """
        截图
        
        Args:
            filename: 文件名，如果为None则自动生成
            
        Returns:
            截图文件路径
        """
        try:
            # 创建截图目录
            screenshots_dir = self.config.get_project_path(
                self.config.get('report.screenshots_dir', 'reports/screenshots')
            )
            os.makedirs(screenshots_dir, exist_ok=True)
            
            # 生成文件名
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"screenshot_{timestamp}.png"
            
            # 确保文件名有.png扩展名
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(screenshots_dir, filename)
            
            # 截图
            self.driver.save_screenshot(filepath)
            self.logger.info(f"截图保存: {filepath}")
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"截图失败: {e}")
            return ""
    
    def get_page_source(self) -> str:
        """
        获取页面源码
        
        Returns:
            页面源码
        """
        try:
            source = self.driver.page_source
            self.logger.debug("获取页面源码成功")
            return source
        except Exception as e:
            self.logger.error(f"获取页面源码失败: {e}")
            return ""
    
    def wait(self, seconds: float):
        """
        等待指定时间
        
        Args:
            seconds: 等待秒数
        """
        time.sleep(seconds)
        self.logger.debug(f"等待 {seconds} 秒")
    
    # =========================== 应用操作方法 ===========================
    
    def launch_app(self):
        """启动应用"""
        try:
            self.driver.launch_app()
            self.logger.info("启动应用成功")
        except Exception as e:
            self.logger.error(f"启动应用失败: {e}")
    
    def close_app(self):
        """关闭应用"""
        try:
            self.driver.close_app()
            self.logger.info("关闭应用成功")
        except Exception as e:
            self.logger.error(f"关闭应用失败: {e}")
    
    def background_app(self, seconds: int = 3):
        """
        将应用切换到后台
        
        Args:
            seconds: 后台时间（秒）
        """
        try:
            self.driver.background_app(seconds)
            self.logger.info(f"应用切换到后台 {seconds} 秒")
        except Exception as e:
            self.logger.error(f"切换应用到后台失败: {e}")
    
    def reset_app(self):
        """重置应用"""
        try:
            self.driver.reset()
            self.logger.info("重置应用成功")
        except Exception as e:
            self.logger.error(f"重置应用失败: {e}")