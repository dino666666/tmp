#!/usr/bin/env python3
"""
框架使用示例
演示如何使用Appium自动化测试框架
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import driver_manager, device_manager
from config import config_manager
from pages.login_page import LoginPage
from utils.logger_manager import get_logger


def example_device_operations():
    """示例：设备操作"""
    print("\n🔍 设备操作示例")
    
    # 获取Android设备列表
    devices = device_manager.get_android_devices()
    print(f"发现 {len(devices)} 个Android设备:")
    for device in devices:
        print(f"  - {device['device_id']}: {device['status']}")
    
    # 获取设备详细信息
    if devices:
        device_id = devices[0]['device_id']
        device_info = device_manager.get_device_info(device_id)
        if device_info:
            print(f"\n设备详细信息 ({device_id}):")
            for key, value in device_info.items():
                print(f"  {key}: {value}")


def example_driver_operations():
    """示例：驱动操作"""
    print("\n🚀 驱动操作示例")
    
    try:
        # 注意：这只是演示代码结构，实际需要连接真实设备
        print("启动Android驱动...")
        
        # 自定义capabilities示例
        custom_caps = {
            'appPackage': 'com.android.settings',  # 使用系统设置应用作为示例
            'appActivity': '.Settings'
        }
        
        # 这里只是演示，实际使用时需要确保设备已连接
        # driver = driver_manager.start_android_driver(custom_caps)
        # print("✅ 驱动启动成功")
        
        print("（注意：实际使用需要连接设备并启动Appium服务）")
        
    except Exception as e:
        print(f"❌ 驱动启动失败: {e}")
        print("请确保：")
        print("1. Appium服务已启动")
        print("2. Android设备已连接并启用USB调试")
        print("3. 修改config/config.yaml中的应用配置")


def example_page_operations():
    """示例：页面对象操作"""
    print("\n📱 页面对象示例")
    
    # 演示页面对象的使用方式
    print("登录页面对象使用示例:")
    print("```python")
    print("# 创建页面对象")
    print("login_page = LoginPage(driver)")
    print("")
    print("# 等待页面加载")
    print("login_page.wait_for_page_load()")
    print("")
    print("# 执行登录操作")
    print("login_page.login('username', 'password')")
    print("")
    print("# 验证登录结果")
    print("if login_page.is_error_displayed():")
    print("    error_msg = login_page.get_error_message()")
    print("    print(f'登录失败: {error_msg}')")
    print("```")


def example_config_usage():
    """示例：配置使用"""
    print("\n⚙️ 配置管理示例")
    
    # 获取各种配置
    appium_config = config_manager.get_appium_config()
    android_config = config_manager.get_android_config()
    test_config = config_manager.get_test_config()
    
    print("Appium配置:")
    print(f"  服务地址: {appium_config.get('host')}:{appium_config.get('port')}")
    
    print("\nAndroid配置:")
    print(f"  平台版本: {android_config.get('platform_version')}")
    print(f"  应用包名: {android_config.get('app_package')}")
    print(f"  主Activity: {android_config.get('app_activity')}")
    
    print("\n测试配置:")
    print(f"  隐式等待: {test_config.get('implicit_wait')}秒")
    print(f"  显式等待: {test_config.get('explicit_wait')}秒")
    print(f"  失败截图: {test_config.get('screenshot_on_failure')}")
    
    # 演示环境切换
    print(f"\n当前环境: {config_manager.env}")
    print("可用环境: dev, test, prod")


def example_test_execution():
    """示例：测试执行"""
    print("\n🧪 测试执行示例")
    
    print("运行测试的几种方式:")
    print("\n1. 运行所有测试:")
    print("   python run_tests.py")
    print("   # 或者")
    print("   pytest tests/")
    
    print("\n2. 运行特定测试文件:")
    print("   python run_tests.py tests/test_login.py")
    
    print("\n3. 运行带标记的测试:")
    print("   python run_tests.py -m smoke")
    print("   python run_tests.py -m \"smoke and android\"")
    
    print("\n4. 并行执行测试:")
    print("   python run_tests.py -n 2")
    
    print("\n5. 生成不同类型的报告:")
    print("   python run_tests.py --report allure")
    print("   python run_tests.py --report html")
    print("   python run_tests.py --report both")
    
    print("\n6. 失败重试:")
    print("   python run_tests.py --reruns 2")
    
    print("\n7. 仅收集测试:")
    print("   python run_tests.py --collect-only")


def show_project_structure():
    """显示项目结构"""
    print("\n📁 项目结构")
    print("""
appium-framework/
├── config/                 # 配置文件
│   ├── config.yaml        # 主配置
│   ├── env_config.yaml    # 环境配置
│   └── config_manager.py  # 配置管理器
├── core/                   # 核心模块
│   ├── driver_manager.py  # 驱动管理
│   └── device_manager.py  # 设备管理
├── pages/                  # 页面对象
│   ├── base_page.py       # 基础页面
│   └── login_page.py      # 登录页面示例
├── tests/                  # 测试用例
│   ├── base_test.py       # 测试基类
│   └── test_login.py      # 登录测试示例
├── utils/                  # 工具模块
│   ├── logger_manager.py  # 日志管理
│   ├── data_manager.py    # 数据管理
│   ├── report_manager.py  # 报告管理
│   └── helpers.py         # 通用工具
├── data/                   # 测试数据
├── logs/                   # 日志文件
├── reports/                # 测试报告
├── requirements.txt        # 依赖列表
├── pytest.ini            # pytest配置
├── init_framework.py      # 框架初始化
└── run_tests.py          # 测试运行器
    """)


def main():
    """主函数"""
    print("🎉 Appium自动化测试框架使用示例")
    print("=" * 50)
    
    # 显示项目结构
    show_project_structure()
    
    # 配置使用示例
    example_config_usage()
    
    # 设备操作示例
    example_device_operations()
    
    # 驱动操作示例
    example_driver_operations()
    
    # 页面对象示例
    example_page_operations()
    
    # 测试执行示例
    example_test_execution()
    
    print("\n" + "=" * 50)
    print("📖 更多信息请查看 README.md")
    print("🚀 开始你的自动化测试之旅！")


if __name__ == "__main__":
    main()