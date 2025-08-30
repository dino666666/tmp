"""
登录功能测试用例
演示如何使用测试框架编写具体的测试用例
"""
import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy

from tests.base_test import BaseTest
from pages.login_page import LoginPage


@allure.feature("用户认证")
@allure.story("登录功能")
class TestLogin(BaseTest):
    """登录功能测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类初始化"""
        super().setup_class()
        # 启动Android驱动
        cls.driver_manager.start_android_driver()
        cls.driver = cls.driver_manager.get_driver()
    
    @classmethod
    def teardown_class(cls):
        """测试类清理"""
        cls.driver_manager.quit_driver()
        super().teardown_class()
    
    def setup_method(self, method):
        """每个测试方法的初始化"""
        super().setup_method(method)
        self.login_page = LoginPage(self.driver)
        
        # 确保在登录页面
        if not self.login_page.wait_for_page_load(timeout=10):
            # 如果不在登录页面，尝试启动应用或导航到登录页面
            self.driver.launch_app()
            assert self.login_page.wait_for_page_load(timeout=30), "无法进入登录页面"
    
    @allure.title("有效用户名密码登录")
    @allure.description("使用有效的用户名和密码进行登录测试")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self):
        """测试有效登录"""
        with allure.step("输入有效的用户名和密码"):
            username = "test_user"
            password = "test_password"
            
            # 输入用户名
            assert self.login_page.input_username(username), "输入用户名失败"
            
            # 输入密码
            assert self.login_page.input_password(password), "输入密码失败"
            
            # 截图记录
            self.take_screenshot("输入用户名密码后")
        
        with allure.step("点击登录按钮"):
            assert self.login_page.click_login_button(), "点击登录按钮失败"
        
        with allure.step("验证登录成功"):
            # 这里应该验证登录后的页面元素
            # 例如检查是否跳转到主页或用户中心
            # 由于这是示例，这里只等待几秒并截图
            import time
            time.sleep(3)
            self.take_screenshot("登录操作后")
            
            # 可以添加具体的验证逻辑
            # 例如：检查是否存在登录后才有的元素
            # assert self.login_page.is_element_present((AppiumBy.ID, "home_page_element"))
    
    @allure.title("无效用户名登录")
    @allure.description("使用无效的用户名进行登录测试，验证错误提示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_username_login(self):
        """测试无效用户名登录"""
        with allure.step("输入无效用户名和有效密码"):
            invalid_username = "invalid_user"
            valid_password = "test_password"
            
            self.login_page.input_username(invalid_username)
            self.login_page.input_password(valid_password)
            
            self.take_screenshot("输入无效用户名")
        
        with allure.step("点击登录按钮"):
            self.login_page.click_login_button()
        
        with allure.step("验证错误提示"):
            # 等待错误信息出现
            import time
            time.sleep(2)
            
            # 检查是否显示错误信息
            if self.login_page.is_error_displayed():
                error_msg = self.login_page.get_error_message()
                self.logger.info(f"错误信息: {error_msg}")
                assert "用户名" in error_msg or "不存在" in error_msg, f"错误信息不正确: {error_msg}"
            
            self.take_screenshot("登录失败后")
    
    @allure.title("空密码登录")
    @allure.description("使用空密码进行登录测试")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_password_login(self):
        """测试空密码登录"""
        with allure.step("输入用户名，密码为空"):
            username = "test_user"
            
            self.login_page.input_username(username)
            # 不输入密码或清空密码
            self.login_page.send_keys(self.login_page.PASSWORD_INPUT, "")
            
            self.take_screenshot("密码为空")
        
        with allure.step("点击登录按钮"):
            self.login_page.click_login_button()
        
        with allure.step("验证错误提示或按钮状态"):
            # 检查登录按钮是否被禁用或显示错误信息
            import time
            time.sleep(2)
            
            # 可能的验证方式：
            # 1. 检查登录按钮是否被禁用
            # 2. 检查是否显示"密码不能为空"的错误信息
            # 3. 检查是否仍在登录页面
            
            # 这里简单验证仍在登录页面
            assert self.login_page.wait_for_page_load(timeout=5), "应该仍在登录页面"
            
            self.take_screenshot("空密码登录后")
    
    @allure.title("登录页面元素验证")
    @allure.description("验证登录页面的所有必要元素是否存在")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_elements(self):
        """测试登录页面元素"""
        with allure.step("验证页面标题"):
            assert self.login_page.is_element_visible(self.login_page.LOGIN_TITLE), "登录标题不可见"
        
        with allure.step("验证用户名输入框"):
            assert self.login_page.is_element_present(self.login_page.USERNAME_INPUT), "用户名输入框不存在"
        
        with allure.step("验证密码输入框"):
            assert self.login_page.is_element_present(self.login_page.PASSWORD_INPUT), "密码输入框不存在"
        
        with allure.step("验证登录按钮"):
            assert self.login_page.is_element_present(self.login_page.LOGIN_BUTTON), "登录按钮不存在"
        
        with allure.step("验证忘记密码链接"):
            assert self.login_page.is_element_present(self.login_page.FORGOT_PASSWORD_LINK), "忘记密码链接不存在"
        
        self.take_screenshot("登录页面元素验证")
    
    @allure.title("用户名密码输入验证")
    @allure.description("验证用户名和密码输入框的功能")
    @allure.severity(allure.severity_level.MINOR)
    def test_input_validation(self):
        """测试输入验证"""
        with allure.step("测试用户名输入"):
            test_username = "test123"
            self.login_page.input_username(test_username)
            
            # 验证输入是否成功
            actual_username = self.login_page.get_username_text()
            assert actual_username == test_username, f"用户名输入不正确: 期望 {test_username}, 实际 {actual_username}"
        
        with allure.step("测试密码输入"):
            test_password = "password123"
            self.login_page.input_password(test_password)
            
            # 验证密码输入（注意：密码可能是隐藏的，这里只验证长度）
            password_text = self.login_page.get_password_text()
            # 密码可能显示为*或者隐藏，这里验证非空即可
            assert len(password_text) > 0, "密码输入失败"
        
        with allure.step("测试清空输入"):
            self.login_page.clear_inputs()
            
            # 验证清空是否成功
            username_after_clear = self.login_page.get_username_text()
            password_after_clear = self.login_page.get_password_text()
            
            assert username_after_clear == "", "用户名未清空"
            assert password_after_clear == "", "密码未清空"
        
        self.take_screenshot("输入验证测试完成")


# 数据驱动测试示例
@allure.feature("用户认证")
@allure.story("登录数据驱动测试")
class TestLoginDataDriven(BaseTest):
    """数据驱动登录测试"""
    
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.driver_manager.start_android_driver()
        cls.driver = cls.driver_manager.get_driver()
    
    @classmethod
    def teardown_class(cls):
        cls.driver_manager.quit_driver()
        super().teardown_class()
    
    def setup_method(self, method):
        super().setup_method(method)
        self.login_page = LoginPage(self.driver)
        
        # 确保在登录页面
        if not self.login_page.wait_for_page_load(timeout=10):
            self.driver.launch_app()
            assert self.login_page.wait_for_page_load(timeout=30), "无法进入登录页面"
    
    # 测试数据
    login_test_data = [
        ("", "", "用户名和密码都为空"),
        ("", "password", "用户名为空"),
        ("username", "", "密码为空"),
        ("invalid", "invalid", "无效用户名密码"),
        ("user123", "short", "密码过短"),
        ("admin", "admin123", "管理员账户"),
    ]
    
    @pytest.mark.parametrize("username,password,description", login_test_data)
    @allure.title("参数化登录测试: {description}")
    def test_login_parametrized(self, username, password, description):
        """参数化登录测试"""
        allure.dynamic.description(f"测试场景: {description}")
        
        with allure.step(f"输入用户名: {username}"):
            self.login_page.input_username(username)
        
        with allure.step(f"输入密码: {'*' * len(password) if password else '(空)'}"):
            self.login_page.input_password(password)
        
        with allure.step("点击登录按钮"):
            self.login_page.click_login_button()
        
        with allure.step("验证结果"):
            # 等待响应
            import time
            time.sleep(2)
            
            # 根据不同的测试数据验证不同的结果
            if not username or not password:
                # 空用户名或密码应该仍在登录页面或显示错误
                assert self.login_page.wait_for_page_load(timeout=5), "空输入应该仍在登录页面"
            
            self.take_screenshot(f"测试结果_{description}")
            
            # 清空输入框以备下次测试
            self.login_page.clear_inputs()