"""
示例页面对象 - 登录页面
演示如何使用BasePage创建具体的页面对象
"""
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage


class LoginPage(BasePage):
    """登录页面对象"""
    
    # 页面元素定位器
    USERNAME_INPUT = (AppiumBy.ID, "com.example.app:id/username")
    PASSWORD_INPUT = (AppiumBy.ID, "com.example.app:id/password")
    LOGIN_BUTTON = (AppiumBy.ID, "com.example.app:id/login_btn")
    FORGOT_PASSWORD_LINK = (AppiumBy.ID, "com.example.app:id/forgot_password")
    ERROR_MESSAGE = (AppiumBy.ID, "com.example.app:id/error_message")
    
    # 或者使用XPath定位器
    LOGIN_TITLE = (AppiumBy.XPATH, "//android.widget.TextView[@text='登录']")
    
    def __init__(self, driver=None):
        """初始化登录页面"""
        super().__init__(driver)
        self.page_name = "登录页面"
    
    def wait_for_page_load(self, timeout: int = 30) -> bool:
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间
            
        Returns:
            页面是否加载完成
        """
        return self.wait_for_element_visible(self.LOGIN_TITLE, timeout)
    
    def input_username(self, username: str) -> bool:
        """
        输入用户名
        
        Args:
            username: 用户名
            
        Returns:
            操作是否成功
        """
        return self.send_keys(self.USERNAME_INPUT, username)
    
    def input_password(self, password: str) -> bool:
        """
        输入密码
        
        Args:
            password: 密码
            
        Returns:
            操作是否成功
        """
        return self.send_keys(self.PASSWORD_INPUT, password)
    
    def click_login_button(self) -> bool:
        """
        点击登录按钮
        
        Returns:
            操作是否成功
        """
        return self.click(self.LOGIN_BUTTON)
    
    def click_forgot_password(self) -> bool:
        """
        点击忘记密码链接
        
        Returns:
            操作是否成功
        """
        return self.click(self.FORGOT_PASSWORD_LINK)
    
    def get_error_message(self) -> str:
        """
        获取错误信息
        
        Returns:
            错误信息文本
        """
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """
        检查是否显示错误信息
        
        Returns:
            是否显示错误
        """
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def login(self, username: str, password: str) -> bool:
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            登录是否成功
        """
        try:
            # 等待页面加载
            if not self.wait_for_page_load():
                self.logger.error("登录页面加载失败")
                return False
            
            # 输入用户名
            if not self.input_username(username):
                self.logger.error("输入用户名失败")
                return False
            
            # 输入密码
            if not self.input_password(password):
                self.logger.error("输入密码失败")
                return False
            
            # 点击登录按钮
            if not self.click_login_button():
                self.logger.error("点击登录按钮失败")
                return False
            
            self.logger.info(f"执行登录操作成功: {username}")
            return True
            
        except Exception as e:
            self.logger.error(f"登录操作异常: {e}")
            return False
    
    def clear_inputs(self):
        """清空输入框"""
        try:
            username_element = self.find_element(self.USERNAME_INPUT)
            if username_element:
                username_element.clear()
            
            password_element = self.find_element(self.PASSWORD_INPUT)
            if password_element:
                password_element.clear()
                
            self.logger.info("清空输入框成功")
        except Exception as e:
            self.logger.error(f"清空输入框失败: {e}")
    
    def get_username_text(self) -> str:
        """获取用户名输入框的文本"""
        return self.get_attribute(self.USERNAME_INPUT, "text")
    
    def get_password_text(self) -> str:
        """获取密码输入框的文本"""
        return self.get_attribute(self.PASSWORD_INPUT, "text")
    
    def is_login_button_enabled(self) -> bool:
        """检查登录按钮是否可用"""
        try:
            element = self.find_element(self.LOGIN_BUTTON)
            if element:
                return element.is_enabled()
            return False
        except Exception as e:
            self.logger.error(f"检查登录按钮状态失败: {e}")
            return False