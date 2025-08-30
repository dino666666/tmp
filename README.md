# Appium移动端自动化测试框架

一个完整的Appium移动端自动化测试框架，支持Android和iOS平台的自动化测试。

## 🚀 特性

- **跨平台支持**: 支持Android和iOS设备
- **页面对象模式**: 采用POM设计模式，提高代码复用性
- **配置管理**: 灵活的配置文件支持多环境
- **设备管理**: 自动设备发现和管理
- **丰富报告**: 支持Allure和HTML报告
- **数据驱动**: 支持Excel和JSON数据驱动测试
- **失败重试**: 自动重试机制
- **截图功能**: 失败自动截图
- **日志管理**: 完整的日志记录和管理

## 📁 项目结构

```
.
├── config/                 # 配置文件目录
│   ├── config.yaml        # 主配置文件
│   ├── env_config.yaml    # 环境配置文件
│   └── config_manager.py  # 配置管理器
├── core/                   # 核心模块
│   ├── driver_manager.py  # 驱动管理器
│   └── device_manager.py  # 设备管理器
├── pages/                  # 页面对象目录
│   ├── base_page.py       # 基础页面对象
│   └── login_page.py      # 登录页面示例
├── tests/                  # 测试用例目录
│   ├── base_test.py       # 测试基类
│   └── test_login.py      # 登录测试示例
├── utils/                  # 工具模块
│   ├── logger_manager.py  # 日志管理器
│   ├── data_manager.py    # 数据管理器
│   ├── report_manager.py  # 报告管理器
│   └── helpers.py         # 通用工具函数
├── data/                   # 测试数据目录
├── logs/                   # 日志文件目录
├── reports/                # 测试报告目录
└── requirements.txt        # 依赖包列表
```

## 🛠️ 环境准备

### 1. Python环境
```bash
# 确保Python 3.8+已安装
python --version
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. Appium环境

#### 安装Node.js和Appium
```bash
# 安装Node.js (建议使用LTS版本)
# 从 https://nodejs.org/ 下载安装

# 安装Appium
npm install -g appium

# 安装驱动
appium driver install uiautomator2  # Android
appium driver install xcuitest      # iOS
```

#### Android环境
1. 安装Android SDK
2. 配置环境变量 ANDROID_HOME
3. 启用开发者选项和USB调试
4. 安装adb工具

#### iOS环境 (仅macOS)
1. 安装Xcode
2. 安装Command Line Tools
3. 配置iOS开发证书

### 4. Allure报告工具 (可选)
```bash
# macOS
brew install allure

# Windows
# 从 https://github.com/allure-framework/allure2/releases 下载
# 配置环境变量
```

## ⚙️ 配置说明

### 主配置文件 (config/config.yaml)

```yaml
# Appium服务配置
appium:
  host: "127.0.0.1"
  port: 4723

# Android设备配置
android:
  platform_name: "Android"
  platform_version: "13"
  device_name: "Android Device"
  app_package: "com.example.app"    # 修改为目标应用包名
  app_activity: ".MainActivity"      # 修改为主Activity

# 测试配置
test:
  implicit_wait: 10
  explicit_wait: 30
  screenshot_on_failure: true
```

### 环境配置 (config/env_config.yaml)

支持开发、测试、生产环境的不同配置。

## 🚀 快速开始

### 1. 启动Appium服务
```bash
appium
```

### 2. 连接设备
```bash
# 查看Android设备
adb devices

# 查看iOS设备 (macOS)
xcrun simctl list devices
```

### 3. 修改配置
根据你的应用修改 `config/config.yaml` 中的应用包名和Activity。

### 4. 运行测试
```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_login.py

# 运行并生成Allure报告
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results

# 运行并生成HTML报告
pytest tests/ --html=reports/html/report.html --self-contained-html
```

## 📝 编写测试用例

### 1. 创建页面对象

```python
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class YourPage(BasePage):
    # 定义元素定位器
    ELEMENT_LOCATOR = (AppiumBy.ID, "element_id")
    
    def your_action(self):
        return self.click(self.ELEMENT_LOCATOR)
```

### 2. 创建测试用例

```python
import pytest
import allure
from tests.base_test import BaseTest
from pages.your_page import YourPage

@allure.feature("功能模块")
class TestYourFeature(BaseTest):
    
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.driver_manager.start_android_driver()
        cls.driver = cls.driver_manager.get_driver()
    
    def test_your_case(self):
        page = YourPage(self.driver)
        assert page.your_action()
```

## 📊 测试报告

### Allure报告
```bash
# 生成并查看Allure报告
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

### HTML报告
```bash
# 生成HTML报告
pytest tests/ --html=reports/html/report.html --self-contained-html
```

## 📱 支持的定位方式

框架支持所有Appium标准定位方式：

- **ID**: `(AppiumBy.ID, "element_id")`
- **XPATH**: `(AppiumBy.XPATH, "//android.widget.Button")`
- **CLASS_NAME**: `(AppiumBy.CLASS_NAME, "android.widget.Button")`
- **ACCESSIBILITY_ID**: `(AppiumBy.ACCESSIBILITY_ID, "button")`
- **ANDROID_UIAUTOMATOR**: `(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login")')`
- **IOS_PREDICATE**: `(AppiumBy.IOS_PREDICATE, 'name == "Login"')`

## 🔧 高级功能

### 数据驱动测试
```python
@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2")
])
def test_login_data_driven(self, username, password):
    # 测试逻辑
    pass
```

### 设备信息获取
```python
devices = device_manager.get_android_devices()
device_info = device_manager.get_device_info(device_id)
```

### 应用安装/卸载
```python
device_manager.install_app(device_id, "app.apk")
device_manager.uninstall_app(device_id, "com.package.name")
```

## 🛠️ 常见问题

### Q: Appium连接失败
A: 检查Appium服务是否启动，设备是否连接，端口是否被占用。

### Q: 元素定位失败
A: 使用Appium Inspector查看元素属性，确认定位器正确。

### Q: 测试运行缓慢
A: 调整等待时间配置，使用显式等待替代隐式等待。

### Q: 截图失败
A: 检查截图目录权限，确保驱动连接正常。

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证。

## 📞 联系方式

如有问题或建议，请提交Issue或联系维护者。

---

**快速开始你的移动端自动化测试之旅！** 🎉